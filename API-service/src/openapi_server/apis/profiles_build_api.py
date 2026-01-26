# src/openapi_server/apis/profiles_build_api.py
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
    signatures: Dict[str, str] = Field(default_factory=dict)


# ----------------------------
# Helpers
# ----------------------------
def _normalize_text(s: str) -> str:
    s = unicodedata.normalize("NFC", s).strip()
    return re.sub(r"\s+", " ", s)


def _sha1(s: str) -> str:
    return hashlib.sha1(s.encode("utf-8")).hexdigest()


def _get_env_value(key: str) -> str:
    v = os.getenv(key, "")
    if v == "":
        v = os.getenv(key.upper(), "")
    return v


def _env_signature() -> str:
    # Top-K removed
    keys = [
        "Profiles_LLM_PROVIDER",
        "Profiles_LLM_MODEL",
        "Profiles_LLM_TEMPERATURE",
        "Profiles_LLM_MAX_TOKENS",
    ]
    snap = {k: _get_env_value(k) for k in keys}
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

    # Common case: list[dict]
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


async def build_profiles_snapshot() -> Tuple[str, str, Dict[str, Any]]:
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
    profiles_sig = _sha1(combined)

    meta = {
        "basic_present": basic_data is not None,
        "sliq_present": sliq_data is not None,
        "rand36_present": rand36_data is not None,
        "combined": combined,
        "combined_len": len(combined),
    }
    return profiles_sig, combined, meta


# ----------------------------
# Prompt (double braces placeholders)
# ----------------------------
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
   - A short, retrieval-oriented summary for downstream RAG.
   - Must be produced only by compressing/summarizing the content of "profile_detailed".
   - Focus only on high-signal items: constraints (time/physical limitations), major risks, strong preferences, and the most important questionnaire outcomes.
- Do NOT invent any values not supported by USER_TEXT or PROFILES_DATA.
- If PROFILES_DATA contains personal identifiers (names, exact addresses, phone numbers, emails, usernames, org names), replace them with placeholders such as [PERSON], [ADDRESS], [PHONE], [EMAIL], [ORG].
- Do NOT output any unique identifiers, such as IDs, UUIDs, request_uuid, profile_uuid, or timestamps.
- Use neutral, non-judgmental language when describing the user.

USER_TEXT:
{user_text}

PROFILES_DATA:
{profiles_data}
""".strip()



# ----------------------------
# Route
# ----------------------------
@router.post(
    "/profiles/build",
    response_model=ProfilesBuildOut,
    summary="Build a detailed user profile + RAG-oriented summary from UserProfiles (basic/sliq/rand36) and user text",
)
async def profiles_build(body: ProfilesBuildIn):
    clean_text = _normalize_text(body.text)

    # signatures
    text_sig = _sha1(clean_text)
    env_sig = _env_signature()

    # snapshot from mongo
    profiles_sig, profiles_data, snapshot_meta = await build_profiles_snapshot()

    prompt = PROMPT_TEMPLATE.format(
        user_text=clean_text,
        profiles_data=profiles_data,
    )

    provider = _get_env_value("Profiles_LLM_PROVIDER") or "openai"
    model = _get_env_value("Profiles_LLM_MODEL") or "gpt-4.1"
    temperature = float(_get_env_value("Profiles_LLM_TEMPERATURE") or 0.0)
    max_tokens = int(_get_env_value("Profiles_LLM_MAX_TOKENS") or 900)

    # call LLM with small retry (format robustness)
    last_err: Optional[str] = None
    raw = ""
    llm_out = ProfilesBuildLLMOut(profile_detailed="", profile_summary="")

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
            llm_out = ProfilesBuildLLMOut(**parsed)
            last_err = None
            break
        except Exception as e:
            last_err = str(e)
            prompt = prompt + "\n\nREMINDER: Output ONLY a single valid JSON object. No extra text."
            continue

    if last_err is not None:
        raise HTTPException(status_code=502, detail=f"LLM output invalid after retries: {last_err}")

    llm_meta = {
        "provider": provider,
        "model": model,
        "temperature": temperature,
        "max_tokens": max_tokens,
        # "raw_len": len(raw or ""),
    }

    return ProfilesBuildOut(
        request_uuid=body.request_uuid,
        text=body.text,
        llm_meta=llm_meta,
        profile_detailed=llm_out.profile_detailed or "",
        profile_summary=llm_out.profile_summary or "",
        signatures={
            "text_signature": text_sig,
            "profiles_signature": profiles_sig,
            "profiles_env_signature": env_sig,
        },
    )
