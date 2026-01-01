from __future__ import annotations

from typing import Literal
from .clients import get_client

Provider = Literal["openai", "scads"]


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
            messages=[{"role": "user", "content": full_prompt}],
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return resp.choices[0].message.content or ""

    resp = client.responses.create(
        model=model,
        input=full_prompt,
    )
    return resp.output_text or ""


async def classify_habit_via_llm_prompt_async(
    prompt: str,
    sentence: str,
    provider: str = "openai",
    model: str = "gpt-4.1",
    temperature: float = 0.0,
    max_tokens: int = 512,
) -> str:
    """
    True async version: uses AsyncOpenAI from get_client(async_=True) and awaits network calls.
    """
    full_prompt = f"{prompt}\n\n{sentence}"
    client = get_client(provider, async_=True)

    if provider == "scads":
        resp = await client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": full_prompt}],
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return resp.choices[0].message.content or ""

    resp = await client.responses.create(
        model=model,
        input=full_prompt,
    )
    return resp.output_text or ""
