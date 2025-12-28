# src/openapi_server/apis/kb_query_api.py
from __future__ import annotations

import hashlib
import json
import os
from dataclasses import asdict
from datetime import datetime
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List, Optional

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


class KbQueryOut(BaseModel):
    ok: bool
    request_uuid: str
    query: str

    # retrieval controls (from env)
    top_n: int
    score_threshold: float

    # store info
    collection: str
    embed_provider: str
    embed_model: str
    embed_dim: int

    # sync info
    kb_root: str
    kb_changed: bool
    kb_signature: str
    last_sync_at: str

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


def _compute_kb_signature(kb_root: Path, exclude_dirs: set[str]) -> str:
    """
    Signature calculation using only stat information (mtime/size/path):
    - Fast, does not read file content
    - Can detect: additions/deletions/modifications (mtime/size changes)
    """
    items: List[str] = []
    if not kb_root.exists():
        return "missing"

    for p in kb_root.rglob("*.pdf"):
        parts_lower = {x.lower() for x in p.parts}
        if any(ex in parts_lower for ex in exclude_dirs):
            continue
        try:
            st = p.stat()
        except Exception:
            continue

        rel = str(p.relative_to(kb_root)).replace("\\", "/").lower()
        items.append(f"{rel}|{int(st.st_mtime)}|{int(st.st_size)}")

    items.sort()
    payload = "\n".join(items).encode("utf-8")
    return hashlib.sha1(payload).hexdigest()


def _load_thresholds() -> tuple[int, float, int]:
    """
    Since only string + request_uuid is input, top_n / threshold are calculated using the following parameters:
    - KB_TOP_N: Default 5
    - KB_SCORE_THRESHOLD: Default 0.25 (normalized embedding + IP)
    - KB_CANDIDATES: Default 20 (first select candidates, then filter and truncate top_n according to the threshold)
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
    try:
        from dotenv import load_dotenv  # type: ignore

        # .../src/openapi_server
        openapi_server_dir = Path(__file__).resolve().parents[1]
        env_path = openapi_server_dir / ".env"
        if env_path.exists():
            load_dotenv(env_path)
    except Exception:
        pass

    cfg = load_config()
    return KbMilvusStore(cfg)


def _ensure_kb_synced(
    store: KbMilvusStore, verbose: bool = True
) -> tuple[bool, str, str]:
    """
    Key: Make "KB changes" automatically reflected in:
    - kb/_meta cache
    - Milvus collection
    Strategy: Calculate the signature for each query; run sync_kb() if it changes.
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
        return False, sig_now, last_sync_at

    # KB changed -> Automatic synchronization (sync_kb internally performs: adding to the database/deleting stale/updating the cache)
    out = sync_kb(store, force_rebuild=False, verbose=verbose)

    # After syncing, write back the state (even if there are errors in the output, record the time and sig).
    last_sync_at = datetime.now().astimezone().isoformat()
    _write_json(
        state_file,
        {
            "kb_signature": sig_now,
            "last_sync_at": last_sync_at,
            "sync_ok": bool(out.get("ok")),
            "sync_summary": out,
        },
    )
    return True, sig_now, last_sync_at


# -----------------------
# The ONLY API you want
# -----------------------
@router.post("/query", response_model=KbQueryOut)
async def kb_query_api(body: KbQueryIn):
    """
    ONLY ONE API:
    input: string + request_uuid
    behaviour:
      1) auto-detect kb changes -> sync (cache+milvus)
      2) search with threshold + top_n
      3) return minimal structured output
    """
    store = get_store()

    # 1) auto sync if kb changed
    try:
        kb_changed, kb_sig, last_sync_at = await run_in_threadpool(
            _ensure_kb_synced, store, True
        )
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
            None,  # domain=None
            True,  # include_doc_meta=True
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {repr(e)}")

    # filter + top_n
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
        ok=True,
        request_uuid=body.request_uuid,
        query=body.text,
        top_n=top_n,
        score_threshold=thr,
        collection=cfg.collection_name,
        embed_provider=cfg.embed_provider,
        embed_model=cfg.embed_model,
        embed_dim=int(cfg.embed_dim),
        kb_root=str(cfg.kb_root),
        kb_changed=kb_changed,
        kb_signature=kb_sig,
        last_sync_at=last_sync_at or "",
        hits=hits,
    )
