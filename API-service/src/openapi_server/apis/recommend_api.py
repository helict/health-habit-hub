from __future__ import annotations

import json
import os, re, unicodedata
from typing import Any, Dict, List, Optional, Tuple

from fastapi import APIRouter, HTTPException
from fastapi.concurrency import run_in_threadpool
from pydantic import BaseModel, Field

from openapi_server.services.llm_habit_service import classify_habit_via_llm_prompt
from openapi_server.services.redis_service import (
    RedisCache,
    recommendation_cache_key_from_habit,
)

router = APIRouter(tags=["Recommendation"])


class RecommendIn(BaseModel):
    request_uuid: str
    text: str
    profile_detailed: str

    selected_habits: List[Dict[str, Any]] = Field(default_factory=list)
    rag_result: List[Dict[str, Any]] = Field(default_factory=list)

    user_feedback: Optional[str] = None


class HabitRecommendation(BaseModel):
    context: str
    behavior: str
    explanation: str


class EvidenceItem(BaseModel):
    title: str = ""
    text: str = ""


class RecommendLLMOut(BaseModel):
    habit_recommendations: List[HabitRecommendation] = Field(default_factory=list)
    habit_recommendations_evidence: List[EvidenceItem] = Field(default_factory=list)


class RecommendOut(BaseModel):
    request_uuid: str
    text: str
    habit_recommendations: List[HabitRecommendation] = Field(default_factory=list)
    llm_meta: Dict[str, Any] = Field(default_factory=dict)
    message: str


def _is_blank(s: Optional[str]) -> bool:
    return s is None or (isinstance(s, str) and s.strip() == "")


def strip_selected_habits_fields(
    selected_habits: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    drop = {"habit_key", "score", "reason"}
    out: List[Dict[str, Any]] = []
    for item in selected_habits or []:
        if not isinstance(item, dict):
            continue
        out.append({k: v for k, v in item.items() if k not in drop})
    return out


def merge_rag_by_book(
    rag_result: List[Dict[str, Any]],
    *,
    sep: str = "\n\n",
    dedupe: bool = True,
) -> List[Dict[str, str]]:
    groups: Dict[Tuple[str, str], Dict[str, Any]] = {}

    for hit in rag_result or []:
        if not isinstance(hit, dict):
            continue

        domain = (hit.get("domain") or "").strip()
        doc_title = (hit.get("doc_title") or "").strip()
        text = hit.get("text")

        if not isinstance(text, str):
            continue
        text = text.strip()
        if not text:
            continue

        key = (domain, doc_title)
        if key not in groups:
            groups[key] = {
                "domain": domain,
                "doc_title": doc_title,
                "texts": [],
                "seen": set(),
            }

        if dedupe:
            if text in groups[key]["seen"]:
                continue
            groups[key]["seen"].add(text)

        groups[key]["texts"].append(text)

    out: List[Dict[str, str]] = []
    for g in groups.values():
        out.append(
            {
                "domain": g["domain"],
                "doc_title": g["doc_title"],
                "text": sep.join(g["texts"]),
            }
        )
    return out


def _extract_json_object(raw: str) -> Dict[str, Any]:
    if not raw or not isinstance(raw, str):
        raise ValueError("LLM output is empty or not a string.")
    s = raw.strip()
    if s.startswith("```"):
        s = re.sub(r"^```[a-zA-Z]*\s*", "", s)
        s = re.sub(r"\s*```$", "", s).strip()

    start = s.find("{")
    end = s.rfind("}")
    if start == -1 or end == -1 or end <= start:
        raise ValueError("No JSON object found in LLM output.")

    js = s[start : end + 1]
    obj = json.loads(js)
    if not isinstance(obj, dict):
        raise ValueError("Top-level JSON is not an object.")
    return obj


def _normalize(txt: str) -> str:
    s = unicodedata.normalize("NFC", txt).strip()
    return re.sub(r"\s+", " ", s)


PROMPT_TEMPLATE = """
You are a recommendation generator.

Your task is to recommend a behavior for the user in a specific context.

Inputs:
- [TEXT] is the user’s desired goal.
- [PROFILE_DETAILED] is the detailed user profile generated from the forms filled out by the user, filtered based on the user’s goal.
- [SELECTED_HABITS] is the list of relevant habits retrieved from the habit database based on the user’s goal.
 - It includes the context of each habit in the following order: [TIME,PHYSICAL SETTING,PRIOR BEHAVIOR,OTHER PEOPLE,INTERNAL STATE,BEHAVIOR,REASONING]
- [RAG_RESULT] is the content retrieved from the local knowledge base via RAG based on the user’s goal, the user profile summary, and the selected habits summary. It includes specific recommended behaviors, behavior change theories, and so on.
- [USER_FEEDBACK] is the user’s feedback on the recommendation results for the same [TEXT].

Output:
- Return ONLY valid JSON (no markdown, no extra text).
- Schema:
{{
  "habit_recommendations": [
    {{
      "context": "string",
      "behavior": "string",
      "explanation": "string"
    }}
  ]
}}
- The context should primarily come from contexts explicitly mentioned in [PROFILE_DETAILED], [SELECTED_HABITS], or [USER_FEEDBACK] (TIME,PHYSICAL SETTING,PRIOR BEHAVIOR,OTHER PEOPLE,INTERNAL STATE,BEHAVIOR,REASONING). You may infer a context only when the behavior generated in [RAG_RESULT] is very specific and appropriate, and this context can also be inferred from [PROFILE_DETAILED], [SELECTED_HABITS], or [USER_FEEDBACK] as an environment that frequently occurs around the user, and this context does not appear in [PROFILE_DETAILED], [SELECTED_HABITS], or [USER_FEEDBACK]; only when all three conditions are met may you appropriately infer the context. The context should remain diverse. Try to cover different (TIME,PHYSICAL SETTING,PRIOR BEHAVIOR,OTHER PEOPLE,INTERNAL STATE,BEHAVIOR,REASONING). If you must repeat the same type of scenario, explain the reason in the explanation.
- The behavior must come only from [RAG_RESULT]; you must read all of [RAG_RESULT] before making a decision. Prefer to summarize or directly extract (if the behavior is specific enough and appropriate) the best “actionable instruction” for that context after considering all factors. You may appropriately infer the behavior based on [RAG_RESULT] only when [RAG_RESULT] contains no concrete executable behavior and can only serve as a general normative evidence source. Whether inferred or not, the explanation must clearly point out all specific sources of the behavior (book title and original sentence). If the final behavior is not specific enough or does not fit the user’s situation (not appropriate), the recommendation can be empty.
- Return only the single best recommendation. If the input content is insufficient to support a reliable recommendation, return an empty list.
- The explanation must be detailed in bullet points: 1. Why this context is chosen (specific (where it comes from) / if inferred (what it is inferred from)). 2. Why this behavior is recommended (from which specific book titles and original sentences in [RAG_RESULT]); if inferred, explain specifically how it is inferred. When quoting original sentences, please provide a short English quote (≤25 English words) and enclose it in quotation marks. Do not copy large passages. 3. How this recommendation can help you achieve the goal in [TEXT].
- For the input [USER_FEEDBACK]: you need to first judge whether it has adoptable value. Adoptable value means an update to the user’s own state (behavior habits) or a specific, reasonable viewpoint/attitude toward a concrete recommendation. If it has adoptable value, it can be incorporated as evidence for generating recommendations; otherwise, ignore it directly.
- Recommendations should balance credibility and reasonableness. Credibility means the recommendation has clear evidence (existing inputs), and reasonableness means the recommendation can effectively help the user achieve the goal. Overall, the recommendations should be somewhat innovative but must not deviate from the actual situation. The goal is to make the user feel the recommendations are well-grounded, valuable for reference, and well-explained.
- If the generated behavior is different from the user’s existing habits [SELECTED_HABITS], you must additionally state this in the explanation so the user pays attention and follows the new behavior recommendation. It is strictly forbidden to generate behaviors that are highly similar to or even the same as the user’s current habits; if this happens, please regenerate the behavior to strengthen the user’s existing habits.
- Avoid recommending specific numbers (frequency, quantities) and specific times unless the numbers have a specific source ([RAG_RESULT] or [SELECTED_HABITS] or [PROFILE_DETAILED]). When outputting specific numbers, you must emphasize the source in the explanation.
- Address the user in the second person in the output.
- Also avoid showing labels such as [PROFILE_DETAILED], [SELECTED_HABITS], [RAG_RESULT], [USER_FEEDBACK] in the output; instead, use more natural, semantic expressions.

[TEXT]
{text}

[PROFILE_DETAILED]
{profile_detailed}

[SELECTED_HABITS]
{selected_habits_json}

[RAG_RESULT]
{rag_result_json}

[USER_FEEDBACK]
{user_feedback}
""".strip()


@router.post(
    "/recommend",
    response_model=RecommendOut,
    summary="Call a large language model to generate appropriate behavior/habit recommendations based on all provided inputs. Redis caching is implemented.",
)
async def recommend(payload: RecommendIn) -> RecommendOut:
    message: str = ""
    if _is_blank(payload.profile_detailed):
        message += (
            "The user profile generated based on your goal is empty. Please check whether the required profile information has been filled in correctly. "
            "Also confirm that the goal you entered is correct, or whether the LLM generated the profile properly in the previous steps. "
            "Alternatively, check whether the relevant configuration parameters are reasonable.\n"
        )

    if not payload.selected_habits:
        message += (
            "No habits were retrieved based on your goal. Please check whether you have donated a sufficiently diverse set of habits. "
            "Also confirm that the goal you entered is correct, or whether the LLM generated the habit summary properly in the previous steps. "
            "Alternatively, check whether the relevant configuration parameters are reasonable.\n"
        )

    if not payload.rag_result:
        message += (
            "The RAG result from the local knowledge base, based on the retrieved habits and user profile, is empty. Please check whether the goal you entered is correct. "
            "Also check whether the local knowledge base is sufficiently rich and relevant to your goal, and whether the previous workflow steps ran successfully. "
            "Alternatively, check whether the relevant configuration parameters are reasonable.\n"
        )

    selected_habits = strip_selected_habits_fields(payload.selected_habits)
    rag_result = merge_rag_by_book(payload.rag_result)

    clean_text = _normalize(payload.text)
    clean_profile = _normalize(payload.profile_detailed)
    clean_feedback = (
        _normalize(payload.user_feedback)
        if isinstance(payload.user_feedback, str)
        else ""
    )

    prompt = PROMPT_TEMPLATE.format(
        text=clean_text,
        profile_detailed=clean_profile,
        selected_habits_json=json.dumps(
            selected_habits, ensure_ascii=False, sort_keys=True, separators=(",", ":")
        ),
        rag_result_json=json.dumps(
            rag_result, ensure_ascii=False, sort_keys=True, separators=(",", ":")
        ),
        user_feedback=clean_feedback,
    )

    provider = os.getenv("RECO_LLM_PROVIDER", "openai")
    model = os.getenv("RECO_LLM_MODEL", "gpt-4.1")
    temperature = float(os.getenv("RECO_LLM_TEMPERATURE", "0") or 0.0)
    max_tokens = int(os.getenv("RECO_LLM_MAX_TOKENS", "900") or 900)

    llm_meta = {
        "provider": provider,
        "model": model,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }

    cache = RedisCache.default()

    cache_payload = {
        "text": clean_text,
        "profile_detailed": clean_profile,
        "selected_habits": selected_habits,
        "rag_result": rag_result,
        "user_feedback": clean_feedback,
    }
    cache_key_text = json.dumps(
        cache_payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    )
    key = recommendation_cache_key_from_habit(cache_key_text)

    cached = await cache.get_json(key)
    if cached:
        cached["request_uuid"] = payload.request_uuid
        return RecommendOut(**cached)

    last_err: Optional[str] = None
    for _ in range(3):
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
            llm_out = RecommendLLMOut(**parsed)

            if message:
                message = (
                    message
                    + "The recommendations were generated successfully. However, please refer to the guidance messages and review your inputs."
                )
            else:
                message = "The recommendations were generated successfully. However, if the results are empty or do not meet your expectations, please consider whether you entered the correct goal, whether all forms have been completed correctly, whether the documents stored in the local knowledge base can support your goal, and whether you have provided a sufficient number of high-quality habits. Higher quality inputs usually lead to better recommendation results."
            out = RecommendOut(
                request_uuid=payload.request_uuid,
                text=clean_text,
                habit_recommendations=llm_out.habit_recommendations,
                llm_meta=llm_meta,
                message=message.strip(),
            )
            await cache.set_json(key, out.model_dump(mode="json"))
            return out
        except Exception as e:
            last_err = str(e)
            prompt += (
                "\n\nREMINDER: Output ONLY a single valid JSON object. No extra text."
            )

    raise HTTPException(
        status_code=502, detail=f"LLM output invalid after retries: {last_err}"
    )
