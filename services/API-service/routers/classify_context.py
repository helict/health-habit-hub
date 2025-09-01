# routers/classify_habit.py
from typing import Optional
import uuid
import json
from fastapi import APIRouter
from enum import Enum
from typing import List
from pydantic import BaseModel, Field, conint, confloat
import re, unicodedata
from uuid import uuid5, NAMESPACE_URL, UUID
from services.llm_habit_service import classify_habit_via_llm_prompt

app02 = APIRouter()



class HabitContext(str, Enum):
    TIME = "TIME"
    PHYSICAL_SETTING = "PHYSICAL SETTING"
    PRIOR_BEHAVIOR = "PRIOR_BEHAVIOR"
    OTHER_PEOPLE = "OTHER PEOPLE"
    INTERNAL_STATE = "INTERNAL_STATE"
    BEHAVIOR = "BEHAVIOR"

class Context(BaseModel):
    name: HabitContext
    value: Optional[str] = Field(default=None, description="抽取到的具体值；可能为空")
    classification: conint(ge=0, le=1) = Field(ge=0, le=1, description="0/1：是否命中该上下文")
    confidence: confloat(ge=0.0, le=1.0) = Field(..., description="置信度 [0,1]")


class ClassifyContextIn(BaseModel):
    uuid: UUID
    habit: str
    language: str = Field(default="en", description="语言代码，如 en/de/zh")

class ClassifyContextOut(BaseModel):
    uuid: UUID
    habit: str
    result: List[Context]


# 添加我的few shot prompt
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
  3. PRIOR_BEHAVIOR
  4. OTHER PEOPLE
  5. INTERNAL_STATE
  6. BEHAVIOR
- Each object must follow this pattern:
  `{{"name": "<one of the six contextual components>", "value": "<exact snippet from sentence>" | null, "classification": 0 | 1, "confidence": 0.00-1.00}}`

Below is a correct example:

Input:
`"After dinner I always read on the couch with my wife."`

Output:
'[
{{"name":"TIME","value":"After dinner","classification":1,"confidence":0.96}},
{{"name":"PHYSICAL SETTING","value":"on the couch","classification":1,"confidence":0.90}},
{{"name":"PRIOR_BEHAVIOR","value":null,"classification":0,"confidence":0.90}},
{{"name":"OTHER PEOPLE","value":"my wife","classification":1,"confidence":0.93}},
{{"name":"INTERNAL_STATE","value":null,"classification":0,"confidence":0.98}},
{{"name":"BEHAVIOR","value":"read","classification":1,"confidence":0.96}}
]'

Now please process the input sentence.
"""

@app02.post("", response_model=ClassifyContextOut, summary="格式化输出习惯的上下文")
def classify_context(payload: ClassifyContextIn):
    prompt_str=FEW_SHOT_PROMPT.format(language=payload.language)
    # 3) 分类（把 simple_habit_classifier 换成你的 LLM 实现即可）
    # output = classify_habit_via_llm_prompt(prompt_str,payload.habit,provider="openai",model="gpt-4.1-mini",temperature=0.0,max_tokens=512)
    output = classify_habit_via_llm_prompt(prompt_str,payload.habit,provider="scads",model="openai/gpt-oss-120b",temperature=0.0,max_tokens=512)
    # 添加到cache数据库
    output=json.loads(output)
    # 4) 返回（按你的 HabitOut 契约）
    return ClassifyContextOut(
        uuid=payload.uuid,
        habit=payload.habit,
        language=payload.language,
        result=output
    )