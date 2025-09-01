# llm_habit_service.py
from __future__ import annotations
import os
from typing import Tuple, Optional, Literal
from openai import OpenAI

Provider = Literal["openai", "scads"]


def classify_habit_via_llm_prompt(
    prompt: str,
    sentence: str,
    provider: Optional[Provider] ="openai",
    model: Optional[str] = "gpt-4.1",
    temperature: float = 0.0,
    max_tokens: int = 512,
) -> Tuple[int, float, str, str]:
    """
    传入已拼好的 prompt，调用 LLM 并解析为 (label, confidence, sentence, raw_text)。
    main 只需加载 .env 提供密钥；模型与 provider 在此决定（也可外部覆盖）。
    """
    pv: Provider = provider
    use_model = model
    base_url = "https://llm.scads.ai/v1" if pv == "scads" else None
    full_prompt = prompt + "\n\n" + sentence

    if pv == "scads":
        api_key = os.getenv("SCADS_API_KEY")
        if not api_key:
            raise RuntimeError("SCADS_API_KEY missing in environment")
        client = OpenAI(base_url=base_url, api_key=api_key)
        resp = client.chat.completions.create(
            model=use_model,
            messages=[{"role": "user", "content": full_prompt}],
            temperature=temperature,
            max_tokens=max_tokens,
        )
        raw_text = resp.choices[0].message.content
        return raw_text

    else:  # openai
        # OPENAI_API_KEY 由环境变量读取；base_url 如设置则走自定义代理
        client = OpenAI()
        # 使用 Responses API（更通用）
        resp = client.responses.create(
            model=use_model,
            input=full_prompt,
            temperature=temperature,
            max_output_tokens=max_tokens,
        )
        raw_text = resp.output_text
        return raw_text

