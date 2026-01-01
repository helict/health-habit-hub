from __future__ import annotations

import hashlib
import json
import os
import re
import unicodedata
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, constr

from openapi_server.services.llm_habit_service import classify_habit_via_llm_prompt_async


# ----------------------------
# Helpers
# ----------------------------
def _normalize_text(s: str) -> str:
    s = unicodedata.normalize("NFC", (s or "")).strip()
    return re.sub(r"\s+", " ", s)


def _sha1(s: str) -> str:
    return hashlib.sha1(s.encode("utf-8")).hexdigest()


def _env_signature(prefix: str = "RECO") -> str:
    keys = [
        f"{prefix}_LLM_PROVIDER",
        f"{prefix}_LLM_MODEL",
        f"{prefix}_LLM_TEMPERATURE",
        f"{prefix}_LLM_MAX_TOKENS",
    ]
    snap = {k: os.getenv(k, "") for k in keys}
    payload = json.dumps(snap, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return _sha1(payload)


def _extract_first_json_object(raw: str) -> Optional[str]:
    if not raw:
        return None
    s = raw.strip()

    if s.startswith("```"):
        s = re.sub(r"^```[a-zA-Z]*\s*", "", s)
        s = re.sub(r"\s*```$", "", s).strip()

    start = s.find("{")
    end = s.rfind("}")
    if start == -1 or end == -1 or end <= start:
        return None
    return s[start : end + 1]


def _k_to_index(k: str) -> Optional[int]:
    if k is None:
        return None
    s = str(k).strip()
    m = re.match(r"^[Kk]\s*(\d+)$", s)
    if m:
        return int(m.group(1))
    if re.match(r"^\d+$", s):
        return int(s)
    return None


def _dedupe_keep_order(items: List[str]) -> List[str]:
    seen = set()
    out: List[str] = []
    for x in items:
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out


# ----------------------------
# Context labels
# ----------------------------
CONTEXT_LABELS: Tuple[str, ...] = (
    "TIME",
    "PHYSICAL SETTING",
    "PRIOR BEHAVIOR",
    "OTHER PEOPLE",
    "INTERNAL STATE",
    "BEHAVIOR",
    "REASONING",
)


def _contexts_to_dict(contexts: List[Optional[str]]) -> Dict[str, Optional[str]]:
    out: Dict[str, Optional[str]] = {}
    for i, lab in enumerate(CONTEXT_LABELS):
        out[lab] = contexts[i] if i < len(contexts) else None
    return out


# ----------------------------
# Pydantic models
# ----------------------------
class LLMMeta(BaseModel):
    provider: Optional[str] = None
    model: Optional[str] = None
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None


class SelectedHabit(BaseModel):
    habit: Optional[str] = None
    habit_key: Optional[str] = None
    score: Optional[float] = None
    reason: Optional[str] = None
    contexts: List[Optional[str]] = Field(default_factory=list)


class RAGHit(BaseModel):
    score: Optional[float] = None
    doc_id: Optional[str] = None
    domain: Optional[str] = None
    chunk_id: Optional[int] = None
    page_number: Optional[int] = None
    doc_title: Optional[str] = None
    text: Optional[str] = None


class TheoryInput(BaseModel):
    theory_name: Optional[str] = None
    prompt: Optional[str] = None


class RecommendIn(BaseModel):
    request_uuid: constr(strip_whitespace=True, min_length=8)
    text: constr(strip_whitespace=False)
    selected_habits: Optional[List[SelectedHabit]] = None
    rag_hits: Optional[List[RAGHit]] = None
    profile_summary: Optional[str] = None
    theory: Optional[TheoryInput] = None
    llm_meta: Optional[LLMMeta] = None

    # prompt max chars (request-level). If prompt exceeds -> 413 error.
    max_prompt_chars: int = 45000


# ---- Used Evidence output models ----
class UsedRAGEvidence(BaseModel):
    k: str  # e.g. "K3"
    quote: str


class UsedHabitEvidence(BaseModel):
    habit_key: str
    why: Optional[str] = None


class UsedEvidenceOut(BaseModel):
    rag: List[UsedRAGEvidence] = Field(default_factory=list)
    habits: List[UsedHabitEvidence] = Field(default_factory=list)
    context_phrases: List[str] = Field(default_factory=list)


# ---- NEW: RAG assessment (expose the problem) ----
class RAGAssessmentOut(BaseModel):
    rag_available: bool = False         # any usable rag text exists?
    rag_actionable: bool = False        # can RAG support a concrete behavior recommendation?
    reason: Optional[str] = None        # short explanation, must not add facts


class RecommendationOut(BaseModel):
    recommendation_text: Optional[str] = None
    rag_assessment: RAGAssessmentOut = Field(default_factory=RAGAssessmentOut)
    used_evidence: UsedEvidenceOut = Field(default_factory=UsedEvidenceOut)

    # debug / storage
    raw: Optional[str] = None
    parse_ok: bool = True
    parse_error: Optional[str] = None


class RecommendOut(BaseModel):
    ok: bool
    request_uuid: str
    prompt: str
    prompt_signature: str
    env_signature: str
    created_at: str
    llm_meta: Dict[str, Any]
    recommendation: RecommendationOut


# ----------------------------
# Prompt building
# ----------------------------
def _build_prompt(req: RecommendIn) -> Tuple[str, List[RAGHit], List[SelectedHabit], List[str], bool]:
    """
    Returns:
      - prompt
      - usable_rag (K indexing)
      - habits
      - allowed_context_phrases (deduped)
      - rag_available (bool)
    """
    user_text = _normalize_text(req.text or "")

    profile_summary = _normalize_text(req.profile_summary or "")
    if not profile_summary:
        profile_summary = "(empty) profile_summary was not provided."

    habits = req.selected_habits or []
    rag_hits = req.rag_hits or []
    theory = req.theory or TheoryInput()

    # Theory gate
    theory_prompt = _normalize_text(theory.prompt or "")
    theory_name = _normalize_text(theory.theory_name or "")
    if not theory_prompt:
        theory_mode_line = "No specific behavior change theory was provided/used."
        required_theory_token = "no specific theory"
    else:
        theory_mode_line = f"Theory will be used. theory_name={theory_name if theory_name else '(unspecified)'}"
        required_theory_token = theory_name if theory_name else "unspecified theory"

    # selected_habits
    habit_lines: List[str] = []
    context_pool: List[str] = []

    def score_val(h: SelectedHabit) -> float:
        try:
            return float(h.score) if h.score is not None else 0.0
        except Exception:
            return 0.0

    if habits:
        habits_sorted = sorted(habits, key=score_val, reverse=True)
        for idx, h in enumerate(habits_sorted, start=1):
            cdict = _contexts_to_dict(h.contexts or [])
            for v in cdict.values():
                if isinstance(v, str) and v.strip():
                    context_pool.append(_normalize_text(v))

            habit_lines.append(
                f"[H{idx}] habit_key={_normalize_text(h.habit_key or '')}\n"
                f"habit={_normalize_text(h.habit or '')}\n"
                f"score={h.score if h.score is not None else ''}\n"
                f"reason={_normalize_text(h.reason or '')}\n"
                f"contexts={json.dumps(cdict, ensure_ascii=False)}"
            )
    else:
        habit_lines.append("(empty) No selected_habits were provided.")

    allowed_context_phrases = _dedupe_keep_order(context_pool)
    allowed_context_block = "; ".join(allowed_context_phrases) if allowed_context_phrases else "(empty) no contexts available"

    # rag_hits
    rag_lines: List[str] = []
    usable_rag = [h for h in rag_hits if (h.text or "").strip()]
    rag_available = bool(usable_rag)

    if usable_rag:
        for idx, h in enumerate(usable_rag, start=1):
            meta = {
                "doc_title": h.doc_title or "",
                "domain": h.domain or "",
                "score": h.score if h.score is not None else "",
            }
            rag_lines.append(
                f"[K{idx}] meta={json.dumps(meta, ensure_ascii=False)}\n"
                f"text={_normalize_text(h.text or '')}"
            )
    else:
        rag_lines.append("(empty) No usable rag_hits.text were provided.")

    prompt = f"""
You are a grounded recommendation generator.

{theory_mode_line}

INPUTS:
[TEXT]
{user_text}

[PROFILE_SUMMARY]
{profile_summary}

[THEORY_NAME]
{required_theory_token}

[THEORY_PROMPT]
{theory_prompt if theory_prompt else "(empty) no theory prompt"}

[SELECTED_HABITS]
{chr(10).join(habit_lines)}

[RAG_HITS]
{chr(10).join(rag_lines)}

[RAG_STATUS]
rag_available={str(rag_available).lower()}

[ALLOWED_CONTEXT_PHRASES]
{allowed_context_block}

DEFINITION: "RAG actionable"
- actionable=true ONLY if at least one [RAG_HITS] block contains concrete, directly usable behavior advice (e.g., do/avoid X) that can be recommended WITHOUT inventing new objects/tools/numbers.
- actionable=false if RAG_HITS are missing OR are only concepts/definitions/mechanisms/principles that do not directly specify a safe behavior to recommend.

CRITICAL ANTI-HALLUCINATION RULES (mandatory):
1) Grounded recommendation only:
   - You MUST base your output ONLY on the inputs above.
2) Controlled summarization:
   - recommendation_text MAY lightly paraphrase [TEXT]/[PROFILE_SUMMARY], but do NOT add new facts or new goals.
3) No new concrete claims:
   - Do NOT introduce new objects, tools, apps, equipment, medications, or exact numbers/timelines not explicitly present in the inputs.
4) Context is constrained:
   - used_evidence.context_phrases MUST be composed ONLY of phrases from [ALLOWED_CONTEXT_PHRASES].
   - Each phrase must match exactly (case/spacing as given), no invented phrases.
5) RAG usability & evidence:
   - You MUST set rag_assessment.rag_available to match [RAG_STATUS].
   - You MUST decide rag_assessment.rag_actionable per the definition above and explain briefly in rag_assessment.reason.
   - If rag_assessment.rag_actionable=true:
       * used_evidence.rag MUST contain 1-3 items.
       * used_evidence.rag[i].k MUST refer to an existing [K#] block.
       * used_evidence.rag[i].quote MUST be a short verbatim quote copied from THAT [K#] text (substring).
       * recommendation_text should align closely with the RAG wording.
   - If rag_assessment.rag_actionable=false:
       * used_evidence.rag MUST be [].
       * recommendation_text MUST explicitly disclose that no actionable retrieved evidence was available (missing or too abstract).
       * recommendation_text MUST use ONLY selected_habits + profile_summary + allowed context phrases to propose a generic, harmless behavior (no new tools/numbers).
6) Habit references must be grounded:
   - used_evidence.habits[].habit_key MUST be one of the habit_key values shown in [SELECTED_HABITS].
   - why (if provided) must be short and must not add new facts.

OUTPUT FORMAT (JSON ONLY, no markdown, no extra keys, no extra text):
{{
  "recommendation_text": "one short paragraph (1-3 sentences max)",
  "rag_assessment": {{
    "rag_available": true,
    "rag_actionable": false,
    "reason": "short reason, e.g. no RAG hits or too conceptual"
  }},
  "used_evidence": {{
    "rag": [{{"k":"K3","quote":"..."}}, {{"k":"K5","quote":"..."}}],
    "habits": [{{"habit_key":"...","why":"(optional, short)"}}, {{"habit_key":"...","why":null}}],
    "context_phrases": ["...", "..."]
  }}
}}

Hard limits:
- used_evidence.rag: at most 3 items; each quote <= 220 characters.
- used_evidence.habits: at most 5 items.
- used_evidence.context_phrases: at most 10 items.
- rag_assessment.reason: <= 200 characters.
""".strip()

    return prompt, usable_rag, habits, allowed_context_phrases, rag_available


def _parse_and_validate_llm_output(
    raw: str,
    usable_rag: List[RAGHit],
    habits: List[SelectedHabit],
    allowed_context_phrases: List[str],
    rag_available: bool,
) -> RecommendationOut:
    out = RecommendationOut(raw=raw, recommendation_text=_normalize_text(raw), parse_ok=False)

    json_str = _extract_first_json_object(raw)
    if not json_str:
        out.parse_error = "No JSON object found in LLM output."
        out.rag_assessment = RAGAssessmentOut(rag_available=rag_available, rag_actionable=False, reason="No JSON output; cannot assess RAG usability.")
        return out

    try:
        obj = json.loads(json_str)
    except Exception as e:
        out.parse_error = f"JSON parse failed: {type(e).__name__}: {e}"
        out.rag_assessment = RAGAssessmentOut(rag_available=rag_available, rag_actionable=False, reason="JSON parse failed; cannot assess RAG usability.")
        return out

    if not isinstance(obj, dict):
        out.parse_error = "Top-level JSON is not an object."
        out.rag_assessment = RAGAssessmentOut(rag_available=rag_available, rag_actionable=False, reason="Invalid JSON shape; cannot assess RAG usability.")
        return out

    rec_text = _normalize_text(str(obj.get("recommendation_text", "") or ""))

    # ---- rag_assessment (LLM-reported, but we enforce consistency) ----
    ra = obj.get("rag_assessment", {}) if isinstance(obj.get("rag_assessment", {}), dict) else {}
    llm_actionable = bool(ra.get("rag_actionable", False))
    llm_reason = _normalize_text(str(ra.get("reason", "") or ""))[:200] if ra.get("reason") else None

    # enforce rag_available (source of truth = actual usable_rag)
    rag_text_by_k: Dict[int, str] = {i: _normalize_text(h.text or "") for i, h in enumerate(usable_rag, start=1)}
    actual_available = bool(rag_text_by_k)

    rag_assessment = RAGAssessmentOut(
        rag_available=actual_available,
        rag_actionable=False,  # set after validation
        reason=llm_reason or ("No usable RAG hits." if not actual_available else None),
    )

    used = obj.get("used_evidence", {})
    if not isinstance(used, dict):
        used = {}

    # validation sets
    habit_keys_set = {(_normalize_text(h.habit_key or "")) for h in habits if (h.habit_key or "").strip()}
    allowed_set = set(allowed_context_phrases)

    used_out = UsedEvidenceOut()

    # ---- validate habits evidence (always allowed) ----
    habit_items = used.get("habits", [])
    if isinstance(habit_items, list):
        for it in habit_items[:5]:
            if isinstance(it, dict):
                hk = _normalize_text(str(it.get("habit_key", "") or ""))
                if not hk or hk not in habit_keys_set:
                    continue
                why = it.get("why", None)
                why_norm = _normalize_text(str(why)) if isinstance(why, str) and why.strip() else None
                used_out.habits.append(UsedHabitEvidence(habit_key=hk, why=why_norm))
            elif isinstance(it, str):
                hk = _normalize_text(it)
                if hk and hk in habit_keys_set:
                    used_out.habits.append(UsedHabitEvidence(habit_key=hk, why=None))

    # ---- validate context phrases (always allowed) ----
    ctx_items = used.get("context_phrases", [])
    if isinstance(ctx_items, list):
        for ph in ctx_items[:10]:
            if not isinstance(ph, str):
                continue
            phr = ph.strip()
            if phr in allowed_set:
                used_out.context_phrases.append(phr)

    # ---- validate rag evidence (only if actionable and available) ----
    validated_rag: List[UsedRAGEvidence] = []
    rag_items = used.get("rag", [])
    if actual_available and isinstance(rag_items, list):
        for it in rag_items[:3]:
            if not isinstance(it, dict):
                continue
            k_idx = _k_to_index(it.get("k", ""))
            if not k_idx or k_idx not in rag_text_by_k:
                continue
            quote = str(it.get("quote", "") or "").strip()
            if not quote:
                continue
            if len(quote) > 220:
                quote = quote[:220]
            if quote not in rag_text_by_k[k_idx]:
                continue
            validated_rag.append(UsedRAGEvidence(k=f"K{k_idx}", quote=quote))

    # Decide final actionable flag (server-enforced):
    # - If LLM says actionable BUT we cannot validate at least 1 quote => force fallback (actionable=false)
    if llm_actionable and actual_available and len(validated_rag) >= 1:
        rag_assessment.rag_actionable = True
        used_out.rag = validated_rag
        if not rag_assessment.reason:
            rag_assessment.reason = "Actionable RAG evidence was found and cited."
    else:
        rag_assessment.rag_actionable = False
        used_out.rag = []
        # If available but not actionable, explain why (prefer LLM reason, else server reason)
        if actual_available:
            rag_assessment.reason = rag_assessment.reason or "RAG hits were too abstract/conceptual to recommend a concrete behavior safely."
            if llm_actionable and len(validated_rag) == 0:
                rag_assessment.reason = "LLM claimed actionable RAG, but no verifiable quote could be validated; falling back."

    out.recommendation_text = rec_text or _normalize_text(raw)
    out.rag_assessment = rag_assessment
    out.used_evidence = used_out
    out.parse_ok = True
    out.parse_error = None
    return out


# ----------------------------
# Router
# ----------------------------
router = APIRouter()


@router.post("/recommend", response_model=RecommendOut, tags=["Recommendation"])
async def recommend(payload: RecommendIn) -> RecommendOut:
    prompt, usable_rag, habits, allowed_context_phrases, rag_available = _build_prompt(payload)

    # Hard oversize error (no silent truncation)
    max_prompt_chars = int(payload.max_prompt_chars or 45000)
    if len(prompt) > max_prompt_chars:
        raise HTTPException(
            status_code=413,
            detail={
                "error": "PROMPT_TOO_LARGE",
                "prompt_chars": len(prompt),
                "max_prompt_chars": max_prompt_chars,
                "hint": "Reduce rag_hits/selected_habits size, or increase payload.max_prompt_chars.",
            },
        )

    prompt_signature = _sha1(_normalize_text(prompt))
    env_sig = _env_signature(prefix="RECO")

    provider = os.getenv("RECO_LLM_PROVIDER") or (payload.llm_meta.provider if payload.llm_meta else None) or "openai"
    model = os.getenv("RECO_LLM_MODEL") or (payload.llm_meta.model if payload.llm_meta else None) or "gpt-4.1"

    temperature = float(
        os.getenv(
            "RECO_LLM_TEMPERATURE",
            str(payload.llm_meta.temperature if payload.llm_meta and payload.llm_meta.temperature is not None else 0.0),
        )
    )

    # You only need to define RECO_LLM_MAX_TOKENS in env
    max_tokens = int(
        os.getenv(
            "RECO_LLM_MAX_TOKENS",
            str(payload.llm_meta.max_tokens if payload.llm_meta and payload.llm_meta.max_tokens else 2048),
        )
    )

    try:
        raw = await classify_habit_via_llm_prompt_async(
            prompt=prompt,
            sentence="",
            provider=provider,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
        )
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"LLM call failed: {type(e).__name__}: {e}")

    parsed = _parse_and_validate_llm_output(
        raw=raw,
        usable_rag=usable_rag,
        habits=habits,
        allowed_context_phrases=allowed_context_phrases,
        rag_available=rag_available,
    )

    return RecommendOut(
        ok=True,
        request_uuid=payload.request_uuid,
        prompt=prompt,
        prompt_signature=prompt_signature,
        env_signature=env_sig,
        created_at=datetime.utcnow().isoformat() + "Z",
        llm_meta={"provider": provider, "model": model, "temperature": temperature, "max_tokens": max_tokens},
        recommendation=parsed,
    )
