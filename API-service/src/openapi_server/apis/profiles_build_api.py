from __future__ import annotations

import os
import re
import json
import hashlib
import unicodedata
from typing import Any, Dict, Optional, Tuple

from fastapi import APIRouter, HTTPException
from fastapi.concurrency import run_in_threadpool
from pydantic import BaseModel, Field

from openapi_server.infra.mongo_UserProfiles import (
    USERPROFILES_BASIC_COLL,
    USERPROFILES_SLIQ_COLL,
    USERPROFILES_RAND36_COLL,
)

from openapi_server.services.llm_habit_service import classify_habit_via_llm_prompt
from openapi_server.services.redis_service import (
    RedisCache,
    profiles_cache_key_from_habit,
)

router = APIRouter(prefix="", tags=["UserProfiles"])


# ----------------------------
# Models
# ----------------------------
class ProfilesBuildIn(BaseModel):
    request_uuid: str
    text: str


class ProfilesBuildLLMOut(BaseModel):
    profile_detailed: str = ""
    profile_summary: str = ""


class ProfilesBuildOut(BaseModel):
    request_uuid: str
    text: str
    llm_meta: Dict[str, Any] = Field(default_factory=dict)
    profile_detailed: str = ""
    profile_summary: str = ""



# ----------------------------
# Helpers
# ----------------------------
def _normalize_text(s: str) -> str:
    s = unicodedata.normalize("NFC", s).strip()
    return re.sub(r"\s+", " ", s)


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


async def _fetch_latest_doc(coll) -> Optional[Dict[str, Any]]:
    doc = await coll.find_one(
        {},
        sort=[
            ("updated_at", -1),
            ("created_at", -1),
            ("_id", -1),
        ],
    )
    return doc


def _project_question_label(data: Any) -> Any:
    """
    Keep ONLY (question, label) pairs for LLM input (token-efficient, less ambiguity).
    - If label is missing, fall back to string(value) so we still keep the answer meaning.
    - Never output id/value keys.
    """
    if data is None:
        return None

    if isinstance(data, list):
        out = []
        for item in data:
            if not isinstance(item, dict):
                continue
            q = item.get("question")
            lbl = item.get("label")
            if (lbl is None or str(lbl).strip() == "") and "value" in item:
                lbl = str(item.get("value"))
            if q is None and lbl is None:
                continue
            out.append({"question": q, "label": lbl})
        return out

    # Sometimes stored as a dict
    if isinstance(data, dict):
        q = data.get("question")
        lbl = data.get("label")
        if (lbl is None or str(lbl).strip() == "") and "value" in data:
            lbl = str(data.get("value"))
        if q is None and lbl is None:
            return None
        return [{"question": q, "label": lbl}]

    return None


def _stable_data_string(name: str, data: Any) -> str:
    payload = json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return f"{name}={payload}"


async def build_profiles_snapshot() -> str:
    basic_doc = await _fetch_latest_doc(USERPROFILES_BASIC_COLL)
    sliq_doc = await _fetch_latest_doc(USERPROFILES_SLIQ_COLL)
    rand36_doc = await _fetch_latest_doc(USERPROFILES_RAND36_COLL)

    def pick_data(doc: Optional[Dict[str, Any]]) -> Any:
        if not doc:
            return None
        return doc.get("data", doc)

    # Only (question, label) pairs go to LLM
    basic_data = _project_question_label(pick_data(basic_doc))
    sliq_data = _project_question_label(pick_data(sliq_doc))
    rand36_data = _project_question_label(pick_data(rand36_doc))

    parts = []
    if basic_data is not None:
        parts.append(_stable_data_string("basic", basic_data))
    if sliq_data is not None:
        parts.append(_stable_data_string("sliq", sliq_data))
    if rand36_data is not None:
        parts.append(_stable_data_string("rand36", rand36_data))

    combined = "\n".join(parts)
    return combined


PROMPT_TEMPLATE = """
You are a user-profile synthesis module for a Habit Recommendation System.

Input
- USER_TEXT: the user's current request/goal (free text).
- PROFILES_DATA: a merged string from the latest saved form submissions, containing ONLY (question, label) pairs. Sources include:
  - Basic: a custom form.
  - SLIQ: focuses on health behaviors and lifestyle risk factors, used to characterize the user's behavioral patterns in diet, physical activity, smoking, alcohol use, and stress.
  - RAND-36: focuses on cognitive and affective states as well as social and functional status, measuring the individual's overall health experience via quality of life.

Task
Generate the following two fields: "profile_detailed" and "profile_summary".

Output
- Output ONLY valid JSON (no markdown, no extra text):
{{
  "profile_detailed": "...",
  "profile_summary": "..."
}}
- "profile_detailed":
   - Derived from PROFILES_DATA only, USER_TEXT may be used only to prioritize what to include.
   - "profile_detailed" should describe only the user profile itself and must not include the user's stated goal/purpose from USER_TEXT.
- "profile_summary":
   - It contains two parts: GOAL and PROFILE_CONSTRAINTS.
   - GOAL
    - Rewrite / paraphrase the "user_text" and expand it with synonyms and retrieval keywords ONLY.
    - Do NOT introduce any facts from the user profile.
    - Purpose: improve downstream RAG recall for actionable, step-by-step behaviors/instructions.
   - PROFILE_CONSTRAINTS
    - A short, retrieval-friendly summary for downstream RAG retrieval, intended to help retrieve actionable, step-by-step behaviors/instructions.
    - Include only high-signal, decision-relevant content. Prioritize: constraints (time budget, physical limitations/pain impact, resource/environment constraints if any), major risks/contraindications/verify items (safety flags), strong preferences/aversions (that significantly affect adherence), and the most important questionnaire outcomes (avoid listing fine-grained items or the question text).
    - Output must be category-level abstractions only (low/medium/high, mild/moderate/severe, adequate/inadequate, stable/unstable, yes/no).Forbidden: any explicit frequencies, counts, durations, distances, schedules, or time patterns, including but not limited to: “per day/week”, “X times”, “minutes/hours”, “km”, “steps”, “usually at 23:00”, “often/rarely” when used as a quasi-frequency.
    - It must be generated only by compressing/summarizing the existing information in “profile_detailed”, without adding new facts, making inferences, or introducing external knowledge.
    - Focus only on the current goal; by default, omit any information that is not relevant to the current goal.
    - Example:
     - "GOAL: Weight loss | Weight management | Reduce body fat | Control energy intake | Increase daily physical activity; PROFILE: sex: male; age: 25; BMI: overweight (≈25.7); time_budget: ≥30 min/day; baseline_activity: low; mobility_limit: mild (slight limitation for higher-intensity activity); pain: very mild; stress: moderate; diet_quality: moderate; substances: no alcohol/no smoking; self_rated_health: fair."
- Do NOT invent any values not supported by USER_TEXT or PROFILES_DATA.
- If PROFILES_DATA contains personal identifiers (names, exact addresses, phone numbers, emails, usernames, org names), replace them with placeholders such as [PERSON], [ADDRESS], [PHONE], [EMAIL], [ORG].
- Do NOT output any unique identifiers, such as IDs, UUIDs, request_uuid, profile_uuid, or timestamps.
- Use neutral, non-judgmental language when describing the user.
- If PROFILES_DATA is empty, missing, or contains no usable (question, label) pairs,
  return:
  {{
    "profile_detailed": "",
    "profile_summary": ""
  }}

USER_TEXT:
{user_text}

PROFILES_DATA:
{profiles_data}
""".strip()



@router.post(
    "/profiles/build",
    response_model=ProfilesBuildOut,
    summary="Use a large language model to extract profile_detailed and profile_summary from the user’s local form database based on the user’s goal statement. The profile_summary is passed to /recommend, while profile_detailed, including a rewrite of the user’s goal statement optimized for use as a RAG query, is used as part of the RAG query for /kb/query. Redis caching is implemented.",
)
async def profiles_build(body: ProfilesBuildIn):
    clean_text = _normalize_text(body.text)

    profiles_combined= await build_profiles_snapshot()

    prompt = PROMPT_TEMPLATE.format(
        user_text=clean_text,
        profiles_data=profiles_combined,
    )

    provider = os.getenv("Profiles_LLM_PROVIDER") or "openai"
    model = os.getenv("Profiles_LLM_MODEL") or "gpt-4.1"
    temperature = float(os.getenv("Profiles_LLM_TEMPERATURE") or 0.0)
    max_tokens = int(os.getenv("Profiles_LLM_MAX_TOKENS") or 900)

    llm_meta = {
        "provider": provider,
        "model": model,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    cache = RedisCache.default()
    cache_payload = {
        "text": clean_text,
        "profiles_data": profiles_combined,
    }
    cache_key_text = json.dumps(
        cache_payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    )
    key = profiles_cache_key_from_habit(cache_key_text)

    cached = await cache.get_json(key)
    if cached:
        cached["request_uuid"] = body.request_uuid
        return ProfilesBuildOut(**cached)

    last_err: Optional[str] = None
    raw = ""
    llm_out = ProfilesBuildLLMOut(profile_detailed="", profile_summary="")

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
            llm_out = ProfilesBuildLLMOut(**parsed)
            last_err = None
            break
        except Exception as e:
            last_err = str(e)
            prompt += "\n\nREMINDER: Output ONLY a single valid JSON object. No extra text."

    if last_err is not None:
        raise HTTPException(status_code=502, detail=f"LLM output invalid after retries: {last_err}")

    out = ProfilesBuildOut(
        request_uuid=body.request_uuid,
        text=clean_text,
        llm_meta=llm_meta,
        profile_detailed=llm_out.profile_detailed or "",
        profile_summary=llm_out.profile_summary or "",
    )
    await cache.set_json(key, out.model_dump(mode="json"))
    return out
