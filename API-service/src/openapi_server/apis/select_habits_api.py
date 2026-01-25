from __future__ import annotations

import os
import re
import json
import hashlib
import unicodedata
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException
from fastapi.concurrency import run_in_threadpool
from pydantic import BaseModel, Field, ValidationError, confloat

from openapi_server.infra.mongo import HABITS_COLL, CONTEXTS_COLL, CONTEXT_MAPPINGS_COLL
from openapi_server.services.habit_db_state_service import build_habit_db_snapshot
from openapi_server.services.llm_habit_service import classify_habit_via_llm_prompt

router = APIRouter(prefix="", tags=["HabitsDB"])

# ----------------------------
# Models
# ----------------------------
class HabitDBSelectIn(BaseModel):
    request_uuid: str
    text: str

class LLMSelectedHabit(BaseModel):
    habit_key: str
    score: confloat(ge=0.0, le=1.0) = 0.5
    reason: str = ""

class HabitDBSelectLLMOut(BaseModel):
    selected_habits: List[LLMSelectedHabit] = Field(default_factory=list)
    selected_habits_summary: str = ""

class SelectedHabitOut(BaseModel):
    habit: str
    habit_key: str
    score: confloat(ge=0.0, le=1.0)
    reason: str
    contexts: List[Any]  # 7 values

class HabitDBSelectOut(BaseModel):
    request_uuid: str
    text: str
    llm_meta: Dict[str, Any]
    selected_habits: List[SelectedHabitOut] = Field(default_factory=list)
    selected_habits_summary: str = ""
    signatures: Dict[str, str]

# ----------------------------
# Helpers
# ----------------------------
def _normalize_text(s: str) -> str:
    s = unicodedata.normalize("NFC", s).strip()
    return re.sub(r"\s+", " ", s)

def _sha1(s: str) -> str:
    return hashlib.sha1(s.encode("utf-8")).hexdigest()

def _env_signature() -> str:
    keys = [
        "HABIT_DB_SELECT_LLM_PROVIDER",
        "HABIT_DB_SELECT_LLM_MODEL",
        "HABIT_DB_SELECT_LLM_TEMPERATURE",
        "HABIT_DB_SELECT_LLM_MAX_TOKENS",
        "HABIT_DB_SELECT_TOP_K",
        "HABIT_DB_SELECT_CANDIDATE_LIMIT",
    ]
    snap = {k: os.getenv(k, "") for k in keys}
    payload = json.dumps(snap, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return _sha1(payload)


def _extract_json_object(raw: str) -> dict:
    """
    Extract {...} from the LLM output to ensure that only JSON objects are parsed.
    """
    if not raw:
        raise ValueError("empty llm output")
    a = raw.find("{")
    b = raw.rfind("}")
    if a == -1 or b == -1 or b <= a:
        raise ValueError("no json object found")
    return json.loads(raw[a : b + 1])

# ----------------------------
# Prompt (double braces placeholders)
# ----------------------------
PROMPT_TEMPLATE = """
You are a habit-database selection module.

Input description:
- USER_TEXT: the user's goal.
- CANDIDATES: a JSON array showing all habits in the user's habit database. Each item contains:
  - "habit_key" (string)
  - "habit" (string)
  - "contexts" (an array of 7 values in the following order:
    ["TIME","PHYSICAL SETTING","PRIOR BEHAVIOR","OTHER PEOPLE","INTERNAL STATE","BEHAVIOR","REASONING"])

Task:
Select up to {top_k} most relevant habits for USER_TEXT.

OUTPUT CONSTRAINTS:
- Output ONLY valid JSON (no Markdown, no extra text).
- JSON schema:
{{
  "selected_habits":[{{"habit_key":"...","score":0.0-1.0,"reason":"..."}}],
  "selected_habits_summary":"..."
}}
- You MUST ONLY output habit_key values that appear in CANDIDATES.
- Higher score means more relevant to USER_TEXT.
- Keep each "reason" to one short sentence (max 20 words).
- "selected_habits": select at most {top_k} habits from CANDIDATES. If there are no matches, return:
  {{"selected_habits":[], "selected_habits_summary":""}}
- "selected_habits_summary": a concise summary of key points from "selected_habits", to be used as part of a downstream RAG query:
   A) The summary MUST use only information from the selected habits in "selected_habits".
   B) The summary MUST be clear and concise.

USER_TEXT:
{user_text}

CANDIDATES (JSON):
{candidates_json}
""".strip()



# ----------------------------
# Route
# ----------------------------
@router.post(
    "/habit_db/select",
    response_model=HabitDBSelectOut,
    summary="Workflow3 module: select habits from HabitDB snapshot (anti-hallucination enforced)",
)
async def habit_db_select(body: HabitDBSelectIn):
    clean_text = _normalize_text(body.text)

    # signatures
    text_sig = _sha1(clean_text)
    env_sig = _env_signature()

    # snapshot (signature + candidates)
    habit_db_sig, habits_list = await build_habit_db_snapshot(
        HABITS_COLL, CONTEXTS_COLL, CONTEXT_MAPPINGS_COLL, only_habits=True
    )

    cand_limit = int(os.getenv("HABIT_DB_SELECT_CANDIDATE_LIMIT", "200") or 200)
    candidates = habits_list[:cand_limit]
    candidate_map: Dict[str, Dict[str, Any]] = {x["habit_key"]: x for x in candidates if x.get("habit_key")}

    top_k = int(os.getenv("HABIT_DB_SELECT_TOP_K", "5") or 5)

    prompt = PROMPT_TEMPLATE.format(
        top_k=str(top_k),
        user_text=clean_text,
        candidates_json=json.dumps(candidates, ensure_ascii=False, separators=(",", ":")),
    )

    provider = os.getenv("HABIT_DB_SELECT_LLM_PROVIDER", "openai")
    model = os.getenv("HABIT_DB_SELECT_LLM_MODEL", "gpt-4.1")
    temperature = float(os.getenv("HABIT_DB_SELECT_LLM_TEMPERATURE", "0") or 0.0)
    max_tokens = int(os.getenv("HABIT_DB_SELECT_LLM_MAX_TOKENS", "900") or 900)

    # call LLM with small retry (format robustness)
    last_err: Optional[str] = None
    raw = ""
    for attempt in range(3):
        raw = await run_in_threadpool(
            lambda: classify_habit_via_llm_prompt(
                prompt=prompt,
                sentence="",
                provider=provider,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
            )
        )
        try:
            parsed = _extract_json_object(raw)
            llm_out = HabitDBSelectLLMOut(**parsed)
            last_err = None
            break
        except Exception as e:
            last_err = str(e)
            # strengthen prompt on retry
            prompt = prompt + "\n\nREMINDER: Output ONLY valid JSON object. No extra text."
            continue

    if last_err is not None:
        raise HTTPException(status_code=502, detail=f"LLM output invalid after retries: {last_err}")

    # anti-hallucination: accept only habit_key that exists in candidate_map
    selected: List[SelectedHabitOut] = []
    dropped: List[str] = []
    seen: set[str] = set()

    for it in llm_out.selected_habits[:top_k]:
        hk = it.habit_key
        if not hk or hk in seen:
            continue
        if hk not in candidate_map:
            dropped.append(hk)
            continue
        seen.add(hk)
        src = candidate_map[hk]
        selected.append(
            SelectedHabitOut(
                habit=src.get("habit", ""),
                habit_key=hk,
                score=float(it.score),
                reason=it.reason or "",
                contexts=src.get("contexts", []),
            )
        )

    llm_meta = {
        "provider": provider,
        "model": model,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "candidate_limit": cand_limit,
        "candidates_used": len(candidates),
        "top_k": top_k,
        "dropped_hallucinated_keys": dropped,
        "raw_len": len(raw or ""),
    }

    return HabitDBSelectOut(
        request_uuid=body.request_uuid,
        text=body.text,
        llm_meta=llm_meta,
        selected_habits=selected,
        selected_habits_summary=llm_out.selected_habits_summary or "",
        signatures={
            "text_signature": text_sig,
            "habit_db_signature": habit_db_sig,
            "env_signature": env_sig,
        },
    )
