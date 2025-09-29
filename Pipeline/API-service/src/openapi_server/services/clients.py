# clients.py
import os
from functools import lru_cache
from openai import OpenAI, AsyncOpenAI

SCADS_BASE = "https://llm.scads.ai/v1"

@lru_cache(maxsize=8)
def get_client(provider: str = "openai", async_: bool = False):
    if provider == "scads":
        api_key = os.getenv("SCADS_API_KEY")
        if not api_key:
            raise RuntimeError("SCADS_API_KEY missing in environment")
        if async_:
            return AsyncOpenAI(base_url=SCADS_BASE, api_key=api_key)
        return OpenAI(base_url=SCADS_BASE, api_key=api_key)
    return AsyncOpenAI() if async_ else OpenAI()
