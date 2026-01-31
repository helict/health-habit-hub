# src/openapi_server/apis/kb_query_api.py
from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime
from functools import lru_cache
from pathlib import Path
from typing import Any, List, Optional

from fastapi import APIRouter, HTTPException
from fastapi.concurrency import run_in_threadpool
from pydantic import BaseModel, Field, constr

from openapi_server.services.kb_milvus_service import (
    load_config,
    KbMilvusStore,
    sync_kb,
    search as kb_search,
)

router = APIRouter(prefix="/kb", tags=["KB"])


# -----------------------
# Minimal IO models
# -----------------------
class KbQueryIn(BaseModel):
    request_uuid: constr(min_length=6)
    text: constr(min_length=1)


class KbHit(BaseModel):
    score: float
    doc_id: str
    domain: str
    chunk_id: int
    page_number: int
    text: str

    doc_title: Optional[str] = None
    doc_summary: Optional[str] = None


class RetrievalInfo(BaseModel):
    top_n: int
    score_threshold: float


class StoreInfo(BaseModel):
    collection: str
    embed_provider: str
    embed_model: str
    embed_dim: int


class KbStateInfo(BaseModel):
    kb_root: str
    kb_changed: bool
    last_sync_at: str

class LlmMeta(BaseModel):
    provider: str
    model: str

class KbQueryOut(BaseModel):
    request_uuid: str
    query: str
    llm_meta: LlmMeta

    retrieval: RetrievalInfo
    # store: StoreInfo
    # kb_state: KbStateInfo

    hits: List[KbHit] = Field(default_factory=list)


# -----------------------
# Helpers: json / state
# -----------------------
def _json_dump(obj: Any) -> str:
    def default(o):
        if isinstance(o, (datetime,)):
            return o.isoformat()
        return str(o)

    return json.dumps(obj, ensure_ascii=False, indent=2, default=default)


def _read_json(p: Path) -> Optional[dict]:
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return None


def _write_json(p: Path, data: dict) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(_json_dump(data), encoding="utf-8")


def _kb_state_path(meta_dir: Path) -> Path:
    return meta_dir / "_kb_state.json"


# -----------------------
# Signature: files + watched env (so env change triggers sync -> reindex)
# Only these env changes should trigger reindex (your requirement)
# -----------------------
_WATCHED_ENV_KEYS = [
    "KB_PDF_STRATEGY",
    "KB_INFER_TABLE_STRUCTURE",
    "KB_CHUNK_MAX_CHARACTERS",
    "KB_CHUNK_NEW_AFTER_N_CHARS",
    "KB_CHUNK_COMBINE_UNDER_N_CHARS",
    "KB_EXTRACT_IMAGES",
]


def _env_bool_1(key: str, default: str) -> bool:
    # Keep consistent with your kb_milvus_service.py logic: == "1"
    return (os.getenv(key, default) or default) == "1"


def _env_int(key: str, default: str) -> int:
    try:
        return int(os.getenv(key, default) or default)
    except Exception:
        return int(default)


def _env_snapshot_for_signature() -> dict:
    """
    Canonicalized env snapshot included in kb_signature.
    Only includes watched keys.
    """
    return {
        "KB_PDF_STRATEGY": (os.getenv("KB_PDF_STRATEGY", "fast") or "fast").strip(),
        "KB_INFER_TABLE_STRUCTURE": _env_bool_1("KB_INFER_TABLE_STRUCTURE", "1"),
        "KB_CHUNK_MAX_CHARACTERS": _env_int("KB_CHUNK_MAX_CHARACTERS", "2800"),
        "KB_CHUNK_NEW_AFTER_N_CHARS": _env_int("KB_CHUNK_NEW_AFTER_N_CHARS", "2400"),
        "KB_CHUNK_COMBINE_UNDER_N_CHARS": _env_int("KB_CHUNK_COMBINE_UNDER_N_CHARS", "900"),
        "KB_EXTRACT_IMAGES": _env_bool_1("KB_EXTRACT_IMAGES", "0"),
    }


def _compute_kb_signature(kb_root: Path, exclude_dirs: set[str]) -> str:
    """
    Signature calculation:
    - File stat information (mtime/size/path) for PDFs
    - PLUS watched env snapshot (chunking-related keys only)

    This makes env changes trigger:
      kb_signature change -> sync_kb() -> per-doc ingest_one_pdf() checks cache/env mismatch -> reindex.
    """
    # 1) env part (stable order)
    env = _env_snapshot_for_signature()
    env_lines = [f"{k}={env[k]}" for k in _WATCHED_ENV_KEYS]

    if not kb_root.exists():
        payload = "missing\n" + "\n".join(env_lines)
        return hashlib.sha1(payload.encode("utf-8")).hexdigest()

    # 2) files part
    file_items: List[str] = []
    for p in kb_root.rglob("*.pdf"):
        parts_lower = {x.lower() for x in p.parts}
        if any(ex in parts_lower for ex in exclude_dirs):
            continue
        try:
            st = p.stat()
        except Exception:
            continue

        rel = str(p.relative_to(kb_root)).replace("\\", "/").lower()
        file_items.append(f"{rel}|{int(st.st_mtime)}|{int(st.st_size)}")

    file_items.sort()

    payload_lines = ["ENV"] + env_lines + ["FILES"] + file_items
    payload = "\n".join(payload_lines).encode("utf-8")
    return hashlib.sha1(payload).hexdigest()


def _load_thresholds() -> tuple[int, float, int]:
    """
    top_n / threshold are calculated using:
    - KB_TOP_N: Default 5
    - KB_SCORE_THRESHOLD: Default 0.25 (normalized embedding + IP)
    - KB_CANDIDATES: Default 20 (select candidates, then filter and truncate to top_n)
    """
    top_n = int(os.getenv("KB_TOP_N") or "5")
    thr = float(os.getenv("KB_SCORE_THRESHOLD") or "0.25")
    cand = int(os.getenv("KB_CANDIDATES") or str(max(20, top_n * 4)))
    top_n = max(1, top_n)
    cand = max(top_n, cand)
    return top_n, thr, cand


# -----------------------
# Store singleton
# -----------------------
@lru_cache(maxsize=1)
def get_store() -> KbMilvusStore:
    # Load .env once on boot (typical for FastAPI).
    try:
        from dotenv import load_dotenv  # type: ignore

        openapi_server_dir = Path(__file__).resolve().parents[1]  # .../src/openapi_server
        env_path = openapi_server_dir / ".env"
        if env_path.exists():
            load_dotenv(env_path)
    except Exception:
        pass

    cfg = load_config()
    return KbMilvusStore(cfg)


def _ensure_kb_synced(store: KbMilvusStore, verbose: bool = True) -> tuple[bool, str]:
    """
    Auto-sync trigger:
      - kb_signature changed (file stats OR watched env snapshot)

    sync_kb() handles:
      - ingest new PDFs
      - delete stale docs
      - update per-doc cache
    """
    cfg = store.cfg
    meta_dir = cfg.meta_dir
    state_file = _kb_state_path(meta_dir)

    sig_now = _compute_kb_signature(cfg.kb_root, cfg.exclude_dirs)

    state = _read_json(state_file) if state_file.exists() else None
    sig_prev = (state or {}).get("kb_signature")

    changed = sig_prev != sig_now
    last_sync_at = (state or {}).get("last_sync_at") or ""

    if not changed:
        return False, last_sync_at

    out = sync_kb(store, force_rebuild=False, verbose=verbose)

    last_sync_at = datetime.now().astimezone().isoformat()
    _write_json(
        state_file,
        {
            "kb_signature": sig_now,
            "last_sync_at": last_sync_at,
            "sync_ok": bool(out.get("ok")),
            "sync_summary": out,
            "watched_env": _env_snapshot_for_signature(),
            "watched_env_keys": list(_WATCHED_ENV_KEYS),
        },
    )
    return True, last_sync_at


# -----------------------
# The ONLY API you want
# -----------------------
@router.post("/query", response_model=KbQueryOut)
async def kb_query_api(body: KbQueryIn):
    """
    input: string + request_uuid
    behaviour:
      1) auto-detect kb changes (files OR watched env) -> sync (cache+milvus)
      2) search with threshold + top_n
      3) return structured output (kb_signature not returned)
    """
    store = get_store()

    # 1) auto sync if kb changed
    try:
        kb_changed, last_sync_at = await run_in_threadpool(_ensure_kb_synced, store, True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"KB sync failed: {repr(e)}")

    # 2) retrieval controls
    top_n, thr, candidates = _load_thresholds()

    # 3) search (get candidates then filter by threshold, cut to top_n)
    try:
        hits_raw = await run_in_threadpool(
            kb_search,
            store,
            body.text,
            candidates,  # top_k candidates
            None,        # domain=None
            True,        # include_doc_meta=True
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {repr(e)}")

    hits: List[KbHit] = []
    for h in hits_raw:
        try:
            score = float(h.get("score") or 0.0)
        except Exception:
            score = 0.0
        if score < thr:
            continue
        hits.append(KbHit(**h))
        if len(hits) >= top_n:
            break

    cfg = store.cfg
    return KbQueryOut(
        request_uuid=body.request_uuid,
        query=body.text,
        llm_meta=LlmMeta(
            provider=(os.getenv("KB_PROVIDER", "scads") or "").strip(),
            model=(os.getenv("KB_MODEL", "") or "openai/gpt-oss-120b").strip(),
        ),
        retrieval=RetrievalInfo(top_n=top_n, score_threshold=thr),
        # store=StoreInfo(
        #     collection=cfg.collection_name,
        #     embed_provider=cfg.embed_provider,
        #     embed_model=cfg.embed_model,
        #     embed_dim=int(cfg.embed_dim),
        # ),
        # kb_state=KbStateInfo(
        #     kb_root=str(cfg.kb_root),
        #     kb_changed=kb_changed,
        #     last_sync_at=last_sync_at or "",
        # ),
        hits=hits,
    )
