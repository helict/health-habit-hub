from __future__ import annotations
import os, json, logging
from typing import Optional, Any, Dict

import hashlib, re, unicodedata

_LOG = logging.getLogger(__name__)

try:
    import redis.asyncio as redis
except Exception as e:
    redis = None
    _IMPORT_ERR = e


def _normalize_text(s: str) -> str:
    s = unicodedata.normalize("NFC", s).strip()
    return re.sub(r"\s+", " ", s)

def _hash_habit(habit: str, language: Optional[str] = None) -> str:
    include_lang = os.getenv("HASH_INCLUDE_LANGUAGE", "false").lower() in {"1", "true", "yes"}
    base = _normalize_text(habit)
    if include_lang and language:
        base = f"{base}||{language.strip().lower()}"
    return hashlib.md5(base.encode("utf-8")).hexdigest()

def _env_fingerprint(meta: Dict[str, Any]) -> str:
    payload = json.dumps(meta, ensure_ascii=False, sort_keys=True)
    return hashlib.sha1(payload.encode("utf-8")).hexdigest()

def _habit_env_sig() -> str:
    return _env_fingerprint({
        "provider": os.getenv("PROVIDER") or "",
        "model": os.getenv("CLASSIFY_HABIT_MODEL") or "",
        "temperature": str(os.getenv("TEMPERATURE") or ""),
        "max_tokens": str(os.getenv("MAX_TOKENS") or ""),
    })

def _context_env_sig() -> str:
    return _env_fingerprint({
        "provider": os.getenv("PROVIDER") or "",
        "model": os.getenv("CLASSIFY_HABIT_CONTEXT_MODEL") or "",
        "temperature": str(os.getenv("TEMPERATURE") or ""),
        "max_tokens": str(os.getenv("MAX_TOKENS") or ""),
    })



def _profiles_env_sig() -> str:
    return _env_fingerprint({
        "provider": os.getenv("Profiles_LLM_PROVIDER") or "",
        "model": os.getenv("Profiles_LLM_MODEL") or "",
        "temperature": str(os.getenv("Profiles_LLM_TEMPERATURE") or ""),
        "max_tokens": str(os.getenv("Profiles_LLM_MAX_TOKENS") or ""),
    })

def _habitdbselect_env_sig() -> str:
    return _env_fingerprint({
        "provider": os.getenv("HABIT_DB_SELECT_LLM_PROVIDER") or "",
        "model": os.getenv("HABIT_DB_SELECT_LLM_MODEL") or "",
        "temperature": str(os.getenv("HABIT_DB_SELECT_LLM_TEMPERATURE") or ""),
        "max_tokens": str(os.getenv("HABIT_DB_SELECT_LLM_MAX_TOKENS") or ""),
        "top_k": str(os.getenv("HABIT_DB_SELECT_TOP_K") or ""),
        "candidate_limit": str(os.getenv("HABIT_DB_CANDIDATE_LIMIT") or ""),
    })

def _recommendation_env_sig() -> str:
    return _env_fingerprint({
        "provider": os.getenv("RECO_LLM_PROVIDER") or "",
        "model": os.getenv("RECO_LLM_MODEL") or "",
        "temperature": str(os.getenv("RECO_LLM_TEMPERATURE") or ""),
        "max_tokens": str(os.getenv("RECO_LLM_MAX_TOKENS") or ""),
    })

def habit_cache_key_from_habit(habit: str, language: Optional[str] = None) -> str:
    return f"habit:{_hash_habit(habit, language)}:{_habit_env_sig()}"

def context_cache_key_from_habit(habit: str, language: Optional[str] = None) -> str:
    return f"context:{_hash_habit(habit, language)}:{_context_env_sig()}"

def profiles_cache_key_from_habit(text: str, language: Optional[str] = None) -> str:
    return f"profiles:{_hash_habit(text, language)}:{_profiles_env_sig()}"

def habitdbselect_cache_key_from_habit(text: str, language: Optional[str] = None) -> str:
    return f"habitdbselect:{_hash_habit(text, language)}:{_habitdbselect_env_sig()}"

def recommendation_cache_key_from_habit(text: str, language: Optional[str] = None) -> str:
    return f"recommendation:{_hash_habit(text, language)}:{_recommendation_env_sig()}"

class RedisCache:
    _instance: Optional["RedisCache"] = None
    def __init__(self, url: Optional[str] = None) -> None:
        if redis is None:
            raise RuntimeError(
                f"redis-py (asyncio) not available. Install with: pip install 'redis>=5,<6'\n{_IMPORT_ERR}"
            )
        self.url = url or os.getenv("REDIS_URL") or self._build_url_from_parts()
        self.ttl = int(os.getenv("CACHE_TTL_SECONDS", "300"))
        self.client = redis.from_url(
            self.url,
            encoding="utf-8",
            decode_responses=True,
        )
    @staticmethod
    def _build_url_from_parts() -> str:
        host = os.getenv("REDIS_HOST", "redis")
        port = int(os.getenv("REDIS_PORT", "6379"))
        db = int(os.getenv("REDIS_DB", "0"))
        pwd = os.getenv("REDIS_PASSWORD")
        if pwd:
            return f"redis://:{pwd}@{host}:{port}/{db}"
        return f"redis://{host}:{port}/{db}"
    @classmethod
    def default(cls) -> "RedisCache":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    async def ping(self) -> bool:
        pong = await self.client.ping()
        return bool(pong)
    async def get_json(self, key: str) -> Optional[Dict[str, Any]]:
        val = await self.client.get(key)
        if val is None:
            return None
        return json.loads(val)
    async def set_json(self, key: str, value: Dict[str, Any], ttl: Optional[int] = None) -> None:
        payload = json.dumps(value, ensure_ascii=False)
        ex = ttl or self.ttl
        await self.client.set(key, payload, ex=ex)
    async def delete(self, key: str) -> int:
        return int(await self.client.delete(key))
    async def close(self) -> None:
        try:
            await self.client.aclose()
        except Exception:
            pass
