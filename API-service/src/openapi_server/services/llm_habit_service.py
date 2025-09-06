from __future__ import annotations
import os
from typing import Tuple, Optional, Literal
from openai import OpenAI, AsyncOpenAI

Provider = Literal["openai", "scads"]


from .clients import get_client

def classify_habit_via_llm_prompt(
    prompt: str,
    sentence: str,
    provider: str = "openai",
    model: str = "gpt-4.1",
    temperature: float = 0.0,
    max_tokens: int = 512,
) -> str:
    full_prompt = f"{prompt}\n\n{sentence}"
    client = get_client(provider, async_=False)

    if provider == "scads":
        resp = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": full_prompt},
            ],
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return resp.choices[0].message.content

    resp = client.responses.create(
        model=model,
        input=full_prompt,
    )
    return resp.output_text
