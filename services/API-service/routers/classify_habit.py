# routers/classify_habit.py
from typing import Optional
import uuid
import json
from fastapi import APIRouter
from pydantic import BaseModel, Field, conint, confloat
import re, unicodedata
from uuid import uuid5, NAMESPACE_URL, UUID
from services.llm_habit_service import classify_habit_via_llm_prompt

app01 = APIRouter()

class HabitIn(BaseModel):
    uuid:str
    habit: str = Field(..., description="原始习惯句子")
    language: str = Field(..., description="语言代码，如 en/de/zh")

class HabitOut(BaseModel):
    uuid:str
    habit: str = Field(..., description="原始习惯句子")
    language: str = Field(..., description="语言代码，如 en/de/zh")
    habit_class: conint(ge=0, le=1) = Field(..., description="是否为习惯：0/1")
    confidence: confloat(ge=0.0, le=1.0) = Field(..., description="置信度[0,1]")


# 添加我的few shot prompt
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

@app01.post("", response_model=HabitOut, summary="判断是否是习惯句")
def classify_habit(payload: HabitIn):
    prompt_str=FEW_SHOT_PROMPT.format(language=payload.language)
    # 3) 分类（把 simple_habit_classifier 换成你的 LLM 实现即可）
    # output = classify_habit_via_llm_prompt(prompt_str,payload.habit,provider="openai",model="gpt-4.1-mini",temperature=0.0,max_tokens=512)
    output = classify_habit_via_llm_prompt(prompt_str,payload.habit,provider="scads",model="openai/gpt-oss-120b",temperature=0.0,max_tokens=512)
    # 添加到cache数据库
    output=json.loads(output)
    # 4) 返回（按你的 HabitOut 契约）
    return HabitOut(
        uuid=payload.uuid,
        habit=payload.habit,
        language=payload.language,
        habit_class=output["label"],
        confidence=output["confidence"],
    )