# src/openapi_server/services/clients.py
import os
from functools import lru_cache
from pathlib import Path
from openai import OpenAI, AsyncOpenAI

SCADS_BASE = "https://llm.scads.ai/v1"


@lru_cache(maxsize=1)
def _load_env_once() -> None:
    """
    Lazy load .env only when get_client() is first called.
    Default location (matches your screenshot): src/openapi_server/.env
    """
    try:
        from dotenv import load_dotenv
    except Exception:
        return

    openapi_server_dir = Path(__file__).resolve().parents[1]
    env_path = openapi_server_dir / ".env"
    if env_path.exists():
        load_dotenv(env_path, override=False)


@lru_cache(maxsize=12)
# Singleton pattern, external get_client calls to the same
def get_client(provider: str = "openai", async_: bool = False):
    _load_env_once()

    if provider == "scads":
        api_key = os.getenv("SCADS_API_KEY")
        if not api_key:
            raise RuntimeError("SCADS_API_KEY missing in environment")
        if async_:
            return AsyncOpenAI(base_url=SCADS_BASE, api_key=api_key)
        return OpenAI(base_url=SCADS_BASE, api_key=api_key)

    return AsyncOpenAI() if async_ else OpenAI()
