# coding: utf-8
from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from pydantic import BaseModel, ValidationError, conint, confloat

from openapi_server.apis.classify_habit_api_base import BaseClassifyHabitApi
from openapi_server.models.habit_in import HabitIn
from openapi_server.models.habit_out import HabitOut

from openapi_server.services.llm_habit_service import classify_habit_via_llm_prompt

from openapi_server.services.redis_service import RedisCache, habit_cache_key


FEW_SHOT_PROMPT = """
You are a habit recognition expert.

The input sentence is written in {language}.

Your task is to determine whether the given sentence describes a habit.

Output: a JSON dictionary with the following keys only:
- "sentence": the original input sentence
- "label": 0 or 1, where 1 = habit, 0 = not a habit
- "confidence": a decimal between 0 and 1 indicating classification confidence

Do not output explanations or extra text.

Here are our examples (two habits, two non-habits):

Example 1:
Input: "He checks his phone before going to bed every night."
Output: {{"sentence": "He checks his phone before going to bed every night.", "label": 1, "confidence": 0.95}}

Example 2:
Input: "I always read a book before going to sleep."
Output: {{"sentence": "I always read a book before going to sleep.", "label": 1, "confidence": 0.99}}

Example 3:
Input: "She visited Paris last summer."
Output: {{"sentence": "She visited Paris last summer.", "label": 0, "confidence": 0.95}}

Example 4:
Input: "I jog."
Output: {{"sentence": "I jog.", "label": 0, "confidence": 0.87}}

Now process the input sentence:
"""


class LLMHabitOutput(BaseModel):
    sentence: str
    label: conint(ge=0, le=1)
    confidence: confloat(ge=0.00, le=1.00)


def _clean_llm_output(output: str) -> Optional[dict]:
    start_index = output.find("{")
    end_index = output.rfind("}")
    if start_index == -1 or end_index == -1 or end_index <= start_index:
        return None
    json_str = output[start_index : end_index + 1]
    try:
        return json.loads(json_str)
    except json.JSONDecodeError:
        return None


def _validate_habit_output(output_dict: dict) -> Optional[LLMHabitOutput]:
    try:
        return LLMHabitOutput(**output_dict)
    except ValidationError:
        return None



class ClassifyHabitApi(BaseClassifyHabitApi):
    async def classify_habit_classify_habit_post(self, habit_in: HabitIn) -> HabitOut:
        max_retries = 6
        cache = RedisCache.default()
        key = habit_cache_key(habit_in.uuid)
        cached = await cache.get_json(key)
        if cached:
            return HabitOut(**cached)

        for attempt in range(max_retries):
            try:
                prompt_str = FEW_SHOT_PROMPT.format(language=habit_in.language)

                raw_output = classify_habit_via_llm_prompt(
                    prompt_str,
                    habit_in.habit,
                    # provider="openai",
                    provider="scads",
                    model="meta-llama/Llama-3.3-70B-Instruct",
                    # model="gpt-4.1",
                    temperature=0.0,
                    max_tokens=1024,
                )

                parsed = _clean_llm_output(raw_output)
                if not parsed:
                    continue

                validated = _validate_habit_output(parsed)
                if validated is None:
                    continue

                out = HabitOut(
                    uuid=habit_in.uuid,
                    habit=habit_in.habit,
                    language=habit_in.language,
                    habit_class=validated.label,
                    confidence=validated.confidence,
                )

                data = out.model_dump(mode="json")
                await cache.set_json(key, data)
                return out

            except Exception:
                if attempt >= max_retries - 1:
                    raise

        raise RuntimeError(
            "LLM output format is incorrect or could not be parsed after retries(The reason may be that the sentence entered is not a common one, or the language is not selected correctly)."
        )