from typing import Optional
import uuid
import json
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, conint, confloat, ValidationError
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

# 定义 LLM 输出模型
class LLMHabitOutput(BaseModel):
    sentence: str
    label: conint(ge=0, le=1)
    confidence: confloat(ge=0.0, le=1.0)

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

def validate_habit_output(output_dict: dict) -> Optional[LLMHabitOutput]:
    """
    验证 LLM 输出是否符合预期的 Habit 格式
    
    Args:
        output_dict: LLM 输出的字典
        
    Returns:
        Optional[LLMHabitOutput]: 如果验证成功返回解析后的 LLMHabitOutput，否则返回 None
    """
    try:
        # 使用 Pydantic 验证输出
        validated = LLMHabitOutput(**output_dict)
        return validated
    except ValidationError:
        return None

@app01.post("", response_model=HabitOut, summary="判断是否是习惯句")
def classify_habit(payload: HabitIn):
    max_retries = 3  # 最大重试次数
    
    for attempt in range(max_retries):
        try:
            prompt_str = FEW_SHOT_PROMPT.format(language=payload.language)
            
            # 调用 LLM 服务
            output = classify_habit_via_llm_prompt(
                prompt_str, 
                payload.habit, 
                provider="scads", 
                model="openai/gpt-oss-120b", 
                temperature=0.0, 
                max_tokens=512
            )
            
            # 解析 JSON 输出
            parsed_output = json.loads(output)
            
            # 使用 Pydantic 验证输出
            validated_output = validate_habit_output(parsed_output)
            
            if validated_output is not None:
                # 格式正确，返回结果
                return HabitOut(
                    uuid=payload.uuid,
                    habit=payload.habit,
                    language=payload.language,
                    habit_class=validated_output.label,
                    confidence=validated_output.confidence,
                )
                    
        except json.JSONDecodeError:
            # JSON 解析失败，继续重试
            if attempt >= max_retries - 1:
                raise HTTPException(
                    status_code=500, 
                    detail="无法解析 LLM 输出为 JSON"
                )
                    
        except Exception:
            # 其他异常，继续重试
            if attempt >= max_retries - 1:
                raise HTTPException(
                    status_code=500, 
                    detail="处理请求时发生错误"
                )
    
    # 如果所有尝试都失败
    raise HTTPException(
        status_code=500, 
        detail="LLM 输出格式不正确，已达到最大重试次数"
    )