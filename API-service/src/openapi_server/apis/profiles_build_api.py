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
    USERPROFILES_WHOQOL_COLL,
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
    profiles_snapshot_meta: Dict[str, Any] = Field(default_factory=dict)
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
    keys = [
        "Profiles_LLM_PROVIDER",
        "Profiles_LLM_MODEL",
        "Profiles_LLM_TEMPERATURE",
        "Profiles_LLM_MAX_TOKENS",
        "Profiles_TOP_K",
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


def _stable_data_string(name: str, data: Any) -> str:
    payload = json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return f"{name}={payload}"


async def build_profiles_snapshot() -> Tuple[str, str, Dict[str, Any]]:
    basic_doc = await _fetch_latest_doc(USERPROFILES_BASIC_COLL)
    sliq_doc = await _fetch_latest_doc(USERPROFILES_SLIQ_COLL)
    whoqol_doc = await _fetch_latest_doc(USERPROFILES_WHOQOL_COLL)

    def pick_data(doc: Optional[Dict[str, Any]]) -> Any:
        if not doc:
            return None
        return doc.get("data", doc)

    basic_data = pick_data(basic_doc)
    sliq_data = pick_data(sliq_doc)
    whoqol_data = pick_data(whoqol_doc)

    parts = []
    if basic_data is not None:
        parts.append(_stable_data_string("basic", basic_data))
    if sliq_data is not None:
        parts.append(_stable_data_string("sliq", sliq_data))
    if whoqol_data is not None:
        parts.append(_stable_data_string("whoqol", whoqol_data))

    combined = "\n".join(parts)
    profiles_sig = _sha1(combined)

    meta = {
        "basic_present": basic_data is not None,
        "sliq_present": sliq_data is not None,
        "whoqol_present": whoqol_data is not None,
        "combined": combined,
        "combined_len": len(combined),
    }
    return profiles_sig, combined, meta


# ----------------------------
# Prompt (double braces placeholders)
# ----------------------------
PROMPT_TEMPLATE = """
You are a user-profile synthesis module for a Habit Recommendation System.

You will receive:
- USER_TEXT: the user's current request/goal (free text).
- PROFILES_DATA: a merged string containing the latest saved form submissions from:
  - Basic
  - SLIQ
  - WHOQOL-BREF

Task:
Generate:
1) "profile_detailed": a detailed, structured narrative user profile grounded ONLY in USER_TEXT + PROFILES_DATA.
2) "profile_summary": a short summary (max {top_k} key points) suitable as downstream input for habit recommendation.

Hard Rules:
1) Output ONLY valid JSON (no markdown, no extra text).
2) Do NOT invent values not supported by USER_TEXT or PROFILES_DATA. If unknown, say "unknown" or omit.
3) Privacy:
   - If PROFILES_DATA contains personal identifiers (names, exact addresses, phone numbers, emails, usernames, org names),
     replace them with placeholders like [PERSON], [ADDRESS], [PHONE], [EMAIL], [ORG].
   - Do NOT output any unique identifiers, IDs, UUIDs, request_uuid, profile_uuid, timestamps.
4) Use neutral, non-judgmental language.
5) If PROFILES_DATA is empty/missing, base the result mainly on USER_TEXT and explicitly state uncertainty.

JSON schema:
{{
  "profile_detailed": "...",
  "profile_summary": "..."
}}

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
    summary="Build a detailed user profile + summary from UserProfiles (basic/sliq/whoqol) and user text",
)
async def profiles_build(body: ProfilesBuildIn):
    clean_text = _normalize_text(body.text)

    # signatures
    text_sig = _sha1(clean_text)
    env_sig = _env_signature()

    # snapshot from mongo
    profiles_sig, profiles_data, snapshot_meta = await build_profiles_snapshot()

    top_k = int(_get_env_value("Profiles_TOP_K") or 6)

    prompt = PROMPT_TEMPLATE.format(
        top_k=str(top_k),
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
        "top_k": top_k,
        "raw_len": len(raw or ""),
    }

    return ProfilesBuildOut(
        request_uuid=body.request_uuid,
        text=body.text,
        llm_meta=llm_meta,
        profile_detailed=llm_out.profile_detailed or "",
        profile_summary=llm_out.profile_summary or "",
        profiles_snapshot_meta=snapshot_meta,
        signatures={
            "text_signature": text_sig,
            "profiles_signature": profiles_sig,
            "profiles_env_signature": env_sig,
        },
    )
