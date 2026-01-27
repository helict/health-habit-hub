# reco_api.py
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
    feasibility: float = Field(ge=0.0, le=1.0)


class RecommendLLMOut(BaseModel):
    habit_recommendations: List[HabitRecommendation] = Field(default_factory=list)


class RecommendOut(BaseModel):
    request_uuid: str
    text: str
    habit_recommendations: List[HabitRecommendation] = Field(default_factory=list)
    llm_meta: Dict[str, Any] = Field(default_factory=dict)


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

Return ONLY valid JSON (no markdown, no extra text).
Schema:
{{
  "habit_recommendations": [
    {{
      "context": "string",
      "behavior": "string",
      "explanation": "string",
      "feasibility": 0.0
    }}
  ]
}}

INPUTS:
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


@router.post("/recommend", response_model=RecommendOut)
async def recommend(payload: RecommendIn) -> RecommendOut:
    errors: List[str] = []

    if _is_blank(payload.profile_detailed):
        errors.append(
            "按照你的目的生成的用户画像为空。请你检查是否已经正确填写了必填的用户画像信息。"
            "或者再次确认输入的目的是否正确。或者是大模型在之前的步骤有没有正确生成用户画像信息。"
            "或者相关设置的参数是否合理。"
        )

    if not payload.selected_habits:
        errors.append(
            "按照你的目的检索到的习惯为空。请你检查是否已经捐赠了足够丰富的习惯。"
            "或者再次确认输入的目的是否正确。或者是大模型在之前的步骤有没有正确生成用户的习惯总结。"
            "或者相关设置的参数是否合理。"
        )

    if not payload.rag_result:
        errors.append(
            "按照你检索到的习惯和用户画像在本地知识库通过rag之后得到的结果为空。请你检查输入的目的是否正确。"
            "或者是本地知识库的内容是否足够丰富。或者之前的流程有没有运行成功。"
            "或者相关设置的参数是否合理。"
        )

    if errors:
        raise HTTPException(status_code=422, detail=errors)


    selected_habits = strip_selected_habits_fields(payload.selected_habits)
    rag_result = merge_rag_by_book(payload.rag_result)

    clean_text = _normalize(payload.text)
    clean_profile = _normalize(payload.profile_detailed)
    clean_feedback = (
        _normalize(payload.user_feedback) if isinstance(payload.user_feedback, str) else ""
    )

    prompt = PROMPT_TEMPLATE.format(
        text=clean_text,
        profile_detailed=clean_profile,
        selected_habits_json=json.dumps(selected_habits, ensure_ascii=False, sort_keys=True, separators=(",", ":")),
        rag_result_json=json.dumps(rag_result, ensure_ascii=False, sort_keys=True, separators=(",", ":")),
        user_feedback=clean_feedback,
    )

    provider = os.getenv("RECO_LLM_PROVIDER", "openai")
    model = os.getenv("RECO_LLM_MODEL", "gpt-4.1")
    temperature = float(os.getenv("RECO_LLM_TEMPERATURE", "0") or 0.0)
    max_tokens = int(os.getenv("RECO_LLM_MAX_TOKENS", "900") or 900)

    llm_meta = {"provider": provider, "model": model, "temperature": temperature, "max_tokens": max_tokens}

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

            out = RecommendOut(
                request_uuid=payload.request_uuid,
                text=clean_text,
                habit_recommendations=llm_out.habit_recommendations,
                llm_meta=llm_meta,
            )
            await cache.set_json(key, out.model_dump(mode="json"))
            return out
        except Exception as e:
            last_err = str(e)
            prompt += "\n\nREMINDER: Output ONLY a single valid JSON object. No extra text."

    raise HTTPException(status_code=502, detail=f"LLM output invalid after retries: {last_err}")