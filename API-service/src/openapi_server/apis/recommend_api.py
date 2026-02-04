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

你的任务是为用户在具体的context出推荐某种behavior。

输入:
- [TEXT] 是用户的希望目标
- [PROFILE_DETAILED] 是根据用户的目标筛选出的用户填写的表单生成的详细用户画像。
- [SELECTED_HABITS] 是根据用户的目标从习惯库中检索到的相关习惯列表。
 - 其中包含每个习惯的上下文，顺序如下：[TIME,PHYSICAL SETTING,PRIOR BEHAVIOR,OTHER PEOPLE,INTERNAL STATE,BEHAVIOR,REASONING]
- [RAG_RESULT] 是根据用户的目标和用户画像总结和相关习惯列表总结在本地知识库中通过RAG检索到的内容。包括具体的推荐行为，行为改变理论等等。
- [USER_FEEDBACK] 是用户对相同[TEXT]的推荐结果的反馈意见。

输出：
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
- context应该优先来自于[PROFILE_DETAILED]，[SELECTED_HABITS]或者[USER_FEEDBACK]中明确提到的上下文(TIME,PHYSICAL SETTING,PRIOR BEHAVIOR,OTHER PEOPLE,INTERNAL STATE,BEHAVIOR,REASONING)。只有当[RAG_RESULT]中生成的behavior非常具体并且恰当时，并且这个上下文也应该由[PROFILE_DETAILED]，[SELECTED_HABITS]或者[USER_FEEDBACK]可以推断出是用户身边经常性出现的环境，而且这个上下文没有出现在[PROFILE_DETAILED]，[SELECTED_HABITS]或者[USER_FEEDBACK]，当且仅当满足这三个条件的时候才能适当推理上下文。context应该保持多样性。尽量覆盖不同的(TIME,PHYSICAL SETTING,PRIOR BEHAVIOR,OTHER PEOPLE,INTERNAL STATE,BEHAVIOR,REASONING)。若不得不重复同一类场景，在explanation中解释原因。
- behavior只能是来源于[RAG_RESULT]，你要读完所有的[RAG_RESULT]再做出判断。优先从[RAG_RESULT]总结或者直接提取出(如果behavior足够具体和合适)综合考虑最优推荐在该情境下“能做的动作指令”。完全禁止推测behavior。在explanation中则需要明确指出behavior的所有具体来源(书名和原句)。如果behavior不够具体或者和用户情况不符合，推荐可以为空。
- 推荐条目的数量要控制在3到7条之间。如果输入的内容非常有限，甚至无法支撑3条推荐，可以适当减少推荐条目的数量，如果实在没有推荐才能返回空列表。
- explanation需要详细说明:1. 为什么选取这个context(具体(从哪里来的)/如果是推测(依据什么推测的)). 2. 为什么推荐这个behavior(从[RAG_RESULT]的具体哪些书名和原句)，引用原句时请提供英文短引（≤25 English words），并用引号包住。不要大段复制。3. 以及这个推荐如何能够帮助用户实现[TEXT]中的目标。
- 对于输入的[USER_FEEDBACK]：你需要先判断是否具有采纳价值。采纳价值意味着对自身状态(行为习惯)的更新或者对具体推荐有具体的合理的观点/态度。如果有采纳价值就可以纳入生成推荐的依据。反之，直接忽略。
- 推荐要在可信和合理之间平衡。可信指的是推荐有明确的依据(现有的输入)，合理指的是推荐能够有效帮助用户实现目标。总体上要有一定的创新性，但不能脱离实际情况。目标是让让用户觉得推荐很有依据并且有参考价值并且有很好的解释性。
- 如果生成的behavior和用户现有的习惯不一样[SELECTED_HABITS]，要在 explanation 里额外说明这一点，让用户注意，遵循新的行为推荐。完全禁止生成的behavior和现在用户的习惯高度相似甚至一样，如果出现这样的情况，请重新生成behavior来增强现有的习惯。
- 避免推荐具体的数值(次数，计量)，具体的时间，除非数值有具体的来源([RAG_RESULT]或者[SELECTED_HABITS]或者[PROFILE_DETAILED])。输出具体数值的时候一定要在explanation强调来源。
- 输出是以第二人称称呼用户。
- 且避免在输出中出现[PROFILE_DETAILED]，[SELECTED_HABITS]，[RAG_RESULT]，[USER_FEEDBACK]等标签。而是使用更加自然的语义化表达。

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
    message: str = ""
    if _is_blank(payload.profile_detailed):
        message += (
            "按照你的目的生成的用户画像为空。请你检查是否已经正确填写了必填的用户画像信息。"
            "或者再次确认输入的目的是否正确。或者是大模型在之前的步骤有没有正确生成用户画像信息。"
            "或者检查相关设置的参数是否合理。\n"
        )

    if not payload.selected_habits:
        message += (
            "按照你的目的检索到的习惯为空。请你检查是否已经捐赠了足够丰富的习惯。"
            "或者再次确认输入的目的是否正确。或者是大模型在之前的步骤有没有正确生成用户的习惯总结。"
            "或者检查相关设置的参数是否合理。\n"
        )

    if not payload.rag_result:
        message += (
            "按照你检索到的习惯和用户画像在本地知识库通过rag之后得到的结果为空。请你检查输入的目的是否正确。"
            "或者是本地知识库的内容是否足够丰富和你的目的是否足够相关。或者之前的流程有没有运行成功。"
            "或者检查相关设置的参数是否合理。\n"
        )

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
            
            if message:
                message = message + "推荐生成成功。但是请参考提示的信息检查输入的信息的质量和完整性。高质量的输入通常会带来更好的推荐结果。"
            else:
                message="推荐生成成功。但是如果推荐结果为空或者不符合预期，请考虑是否输入正确的目的，是否已经正确填写所有的表单，本地知识仓库存储的文献是否能支持回答用户的目的，是否提供了足够数量和质量的习惯。高质量的输入通常会带来更好的推荐结果。"
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
            prompt += "\n\nREMINDER: Output ONLY a single valid JSON object. No extra text."

    raise HTTPException(status_code=502, detail=f"LLM output invalid after retries: {last_err}")