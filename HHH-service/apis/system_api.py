# apis/system_api.py
from __future__ import annotations

from fastapi import APIRouter

from apis.workflow1_api import (
    API_BASE,
    MONGO,
    DB,
    HABITS_COLL,
    CONTEXTS_COLL,
    CONTEXT_MAPPINGS_COLL,
    _env_float,
    _env_int,
)

SYSTEM_TAG = "System"

router = APIRouter(tags=[SYSTEM_TAG])

@router.get(
    "/health",
    summary="Service health check (Mongo + configuration)",
)
async def health():
    try:
        await MONGO.admin.command("ping")
        mongo_ok = True
    except Exception:
        mongo_ok = False

    return {
        "ok": True,
        "api_base": API_BASE,
        "mongo_ok": mongo_ok,
        "mongo_db": DB.name,
        "collections": {
            "habits": HABITS_COLL.name,
            "contexts": CONTEXTS_COLL.name,
            "context_mappings": CONTEXT_MAPPINGS_COLL.name,
        },
    }

@router.get(
    "/system/config",
    summary="Workflow configuration (mapping params)",
    description="Expose env-driven mapping parameters for frontend display.",
)
async def system_config():
    threshold = _env_float("THRESHOLD_BCIO_MAP", 0.6)
    top_n = _env_int("TOP_N_BCIO_MAP", 2)
    return {
        "ok": True,
        "api_base": API_BASE,
        "mapping_params": {"threshold": threshold, "top_n": top_n},
    }
