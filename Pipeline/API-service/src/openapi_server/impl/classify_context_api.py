# coding: utf-8
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import List, Optional
import os,re,unicodedata

from dotenv import load_dotenv
from pydantic import ValidationError

from openapi_server.apis.classify_context_api_base import BaseClassifyContextApi
from openapi_server.models.classify_context_in import ClassifyContextIn
from openapi_server.models.classify_context_out import ClassifyContextOut
from openapi_server.models.context import Context

from openapi_server.services.llm_habit_service import classify_habit_via_llm_prompt

from openapi_server.services.redis_service import RedisCache, context_cache_key_from_habit


FEW_SHOT_PROMPT = """You are a behavioral scientist LLM specializing in habit context recognition.

Your task is to analyze a sentence written in {language}. For each of the six contextual components, you must:

1. Extract the exact text snippet from the sentence that represents the component.
2. Assign a probabilistic confidence value (0.00-1.00, two decimals) for that extraction.
3. Determine whether the contextual component is present (classification = 1) or not present (classification = 0).
4. Assign a probabilistic confidence value between [0,1] to the extraction result, keeping two decimal places.

Contextual components:
1. TIME
2. PHYSICAL SETTING
3. PRIOR BEHAVIOR
4. OTHER PEOPLE
5. INTERNAL STATE
6. BEHAVIOR

Output Format:
- Return only the list, without any additional text or code block markers.
- The top-level output is a JSON list.
- Each element in this list is an object (one for each component), in the fixed order:
  1. TIME
  2. PHYSICAL SETTING
  3. PRIOR BEHAVIOR
  4. OTHER PEOPLE
  5. INTERNAL STATE
  6. BEHAVIOR
- Each object must follow this pattern:
  {{"name": "<one of the six contextual components>", "value": "<exact snippet from sentence>" | null, "classification": 0 | 1, "confidence": 0.00-1.00}}

Below is a correct example:

Input:
"After dinner I always read on the couch with my wife."

Output:
[
{{"name":"TIME","value":"After dinner","classification":1,"confidence":0.96}},
{{"name":"PHYSICAL SETTING","value":"on the couch","classification":1,"confidence":0.90}},
{{"name":"PRIOR BEHAVIOR","value":null,"classification":0,"confidence":0.90}},
{{"name":"OTHER PEOPLE","value":"my wife","classification":1,"confidence":0.93}},
{{"name":"INTERNAL STATE","value":null,"classification":0,"confidence":0.98}},
{{"name":"BEHAVIOR","value":"read","classification":1,"confidence":0.96}}
]

Now please process the input sentence:
"""



_THINK_RE = re.compile(r"<think>.*?</think>", re.I | re.S)
_CODE_FENCE_RE = re.compile(r"```(?:json)?(.*?)```", re.I | re.S)
_CTX_KEY_RE = re.compile(r'"contexts"\s*:\s*\[', re.I)

def _find_balanced_square(text: str, start_idx: int) -> int:
    depth = 0
    for i in range(start_idx, len(text)):
        ch = text[i]
        if ch == "[":
            depth += 1
        elif ch == "]":
            depth -= 1
            if depth == 0:
                return i
    return -1

def _clean_llm_output(raw: str) -> str:
    if not raw:
        return ""

    s = _THINK_RE.sub("", raw).strip()

    m = _CODE_FENCE_RE.search(s)
    if m:
        s = m.group(1).strip()

    m2 = _CTX_KEY_RE.search(s)
    if m2:
        start = m2.end() - 1
        end = _find_balanced_square(s, start)
        if end != -1:
            arr = s[start:end + 1]
            return arr.strip()

    start = s.find("[")
    if start != -1:
        end = _find_balanced_square(s, start)
        if end != -1:
            arr = s[start:end + 1]
            arr = re.sub(r"```(?:json)?|```", "", arr).strip()
            return arr

    return s


def _validate_and_parse(output_list: List[dict]) -> Optional[List[Context]]:
    try:
        if not isinstance(output_list, list):
            return None
        if len(output_list) != 6:
            return None

        expected_names = [
            "TIME",
            "PHYSICAL SETTING",
            "PRIOR BEHAVIOR",
            "OTHER PEOPLE",
            "INTERNAL STATE",
            "BEHAVIOR",
        ]

        for i, item in enumerate(output_list):
            if item.get("name") != expected_names[i]:
                return None

        validated = [Context(**item) for item in output_list]
        return validated

    except (TypeError, KeyError, IndexError, ValidationError):
        return None


def _lang_name(lang_code: str) -> str:
    code = (lang_code or "").lower()
    if code.startswith("en"):
        return "English"
    if code.startswith("de"):
        return "German"
    if code.startswith("zh"):
        return "Chinese"
    return "English"


def _normalize(txt: str) -> str:
    s = unicodedata.normalize("NFC", txt).strip()
    return re.sub(r"\s+", " ", s)

class ClassifyContextApi(BaseClassifyContextApi):
    async def classify_context_classify_context_post(
        self, classify_context_in: ClassifyContextIn
    ) -> ClassifyContextOut:
        max_retries = 3

        cache = RedisCache.default()
        clean_habit=_normalize(classify_context_in.habit)
        key = context_cache_key_from_habit(clean_habit)
        cached = await cache.get_json(key)
        if cached:
            return ClassifyContextOut(**cached)

        for _ in range(max_retries):
            try:
                prompt = FEW_SHOT_PROMPT.format(language=_lang_name(classify_context_in.language))
                raw_output = classify_habit_via_llm_prompt(
                    prompt,
                    clean_habit,
                    provider=os.getenv("PROVIDER_CLASSIFY_CONTEXT"),
                    model=os.getenv("CLASSIFY_HABIT_CONTEXT_MODEL"),
                    temperature=os.getenv("TEMPERATURE"),
                    max_tokens=os.getenv("MAX_TOKENS"),
                )

                cleaned = _clean_llm_output(raw_output)
                parsed = json.loads(cleaned)
                validated = _validate_and_parse(parsed)
                if validated is None:
                    continue

                out = ClassifyContextOut(
                    uuid=classify_context_in.uuid,
                    habit=clean_habit,
                    language=classify_context_in.language,
                    result=validated,
                )
                await cache.set_json(key, out.model_dump(mode="json"))
                return out

            except Exception:
                pass

        raise RuntimeError(
            "LLM output format is incorrect or could not be parsed after retries(The reason may be that the sentence entered is not a common one, or the language is not selected correctly)."
        )