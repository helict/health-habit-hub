# routers/classify_habit.py
from typing import Optional
import uuid
import json
from fastapi import APIRouter, HTTPException
from enum import Enum
from typing import List
from pydantic import BaseModel, Field, conint, confloat, ValidationError
import re, unicodedata
from uuid import uuid5, NAMESPACE_URL, UUID
from services.llm_habit_service import classify_habit_via_llm_prompt

app02 = APIRouter()


class HabitContext(str, Enum):
    TIME = "TIME"
    PHYSICAL_SETTING = "PHYSICAL SETTING"
    PRIOR_BEHAVIOR = "PRIOR BEHAVIOR"
    OTHER_PEOPLE = "OTHER PEOPLE"
    INTERNAL_STATE = "INTERNAL STATE"
    BEHAVIOR = "BEHAVIOR"


class Context(BaseModel):
    name: HabitContext
    value: Optional[str] = Field(default=None, description="抽取到的具体值；可能为空")
    classification: conint(ge=0, le=1) = Field(
        ge=0, le=1, description="0/1：是否命中该上下文"
    )
    confidence: confloat(ge=0.00, le=1.00) = Field(..., description="置信度 [0,1]")


class ClassifyContextIn(BaseModel):
    uuid: UUID
    habit: str
    language: str = Field(default="en", description="语言代码，如 en/de/zh")


class ClassifyContextOut(BaseModel):
    uuid: UUID
    habit: str
    language: str
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

Now please process the input sentence.
"""
def clean_llm_output(output: str) -> str:
    """
    清理 LLM 输出，去除 JSON 数组之外的额外内容
    
    Args:
        output: LLM 的原始输出字符串
        
    Returns:
        str: 清理后的 JSON 数组字符串
    """
    # 尝试找到 JSON 数组的开始和结束位置
    start_idx = output.find('[')
    end_idx = output.rfind(']')
    
    # 如果找不到有效的开始或结束位置，返回原始输出
    if start_idx == -1 or end_idx == -1 or end_idx <= start_idx:
        return output
    
    # 提取 JSON 数组部分
    json_array = output[start_idx:end_idx + 1]
    
    # 尝试解析以确保它是有效的 JSON
    try:
        parsed = json.loads(json_array)
        return json_array
    except json.JSONDecodeError:
        # 如果提取的部分不是有效的 JSON，尝试进一步清理
        # 移除可能存在的代码块标记
        cleaned = re.sub(r'```(json)?|```', '', json_array)
        cleaned = cleaned.strip()
        
        # 再次尝试解析
        try:
            parsed = json.loads(cleaned)
            return cleaned
        except json.JSONDecodeError:
            # 如果仍然无效，返回原始输出
            return output

def validate_and_parse_context_output(
    output_list: List[dict],
) -> Optional[List[Context]]:
    """
    使用 Pydantic 验证和解析 LLM 输出的上下文列表

    Args:
        output_list: LLM 输出的上下文字典列表

    Returns:
        Optional[List[Context]]: 如果验证成功返回解析后的 Context 列表，否则返回 None
    """
    try:
        # 检查输出是否为列表
        if not isinstance(output_list, list):
            return None

        # 检查列表长度是否为6（对应6个上下文组件）
        if len(output_list) != 6:
            return None

        # 预期的上下文组件名称
        expected_names = [
            "TIME",
            "PHYSICAL SETTING",
            "PRIOR BEHAVIOR",
            "OTHER PEOPLE",
            "INTERNAL STATE",
            "BEHAVIOR",
        ]

        # 检查名称是否符合预期顺序
        for i, item in enumerate(output_list):
            if item.get("name") != expected_names[i]:
                return None

        # 使用列表推导式和 Pydantic 验证每个项目
        validated = [Context(**item) for item in output_list]
        return validated

    except (TypeError, KeyError, IndexError, ValidationError):
        return None


@app02.post("", response_model=ClassifyContextOut, summary="格式化输出习惯的上下文")
def classify_context(payload: ClassifyContextIn):
    max_retries = 3  # 最大重试次数

    for attempt in range(max_retries):
        try:
            if payload.language=="en":
                prompt_str = FEW_SHOT_PROMPT.format(language="English")
            elif payload.language=="de":
                prompt_str = FEW_SHOT_PROMPT.format(language="German")
            else:
                prompt_str = FEW_SHOT_PROMPT.format(language="Chinese")
            # 调用 LLM 服务
            output = classify_habit_via_llm_prompt(
                prompt_str,
                payload.habit,
                provider="scads",
                model="openai/gpt-oss-120b",
                temperature=0.0,
                max_tokens=512,
            )

            # 解析 JSON 输出
            output = clean_llm_output(output)
            parsed_output = json.loads(output)
            print(parsed_output)
            # 使用 Pydantic 验证和解析输出
            validated_output = validate_and_parse_context_output(parsed_output)

            if validated_output is not None:
                # 格式正确，返回结果
                return ClassifyContextOut(
                    uuid=payload.uuid,
                    habit=payload.habit,
                    language=payload.language,
                    result=validated_output,
                )

        except json.JSONDecodeError:
            # JSON 解析失败，继续重试
            if attempt >= max_retries - 1:
                raise HTTPException(status_code=500, detail="无法解析 LLM 输出为 JSON")

        except Exception:
            # 其他异常，继续重试
            if attempt >= max_retries - 1:
                raise HTTPException(status_code=500, detail="处理请求时发生错误")

    # 如果所有尝试都失败
    raise HTTPException(
        status_code=500, detail="LLM 输出格式不正确，已达到最大重试次数"
    )
