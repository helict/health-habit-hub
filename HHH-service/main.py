# main.py (HHH-service)
from __future__ import annotations

import os
import re
import uuid
import unicodedata
import requests
import hashlib
from typing import Any, Optional

import uvicorn
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi.concurrency import run_in_threadpool
from fastapi import FastAPI, HTTPException, APIRouter, Query
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# bson is available via pymongo (motor dependency)
from bson import ObjectId

# ----------------------------
# OpenAPI / Docs (3 Workflows + System)
# ----------------------------
WORKFLOW1_TAG = "Workflow1: Habitual structured collection workflow"
WORKFLOW2_TAG = "Workflow2: User Profile/Form Workflow "
WORKFLOW3_TAG = "Workflow3: Recommended workflow"
SYSTEM_TAG = "System"

OPENAPI_TAGS = [
    {
        "name": WORKFLOW1_TAG,
        "description": (
            "Collect user-inputted habitual phrases in a structured manner and complete the entire pipeline:"
            " habit detection → context extraction → BCIO mapping, and persist raw and enriched results;"
            " also provide habit management (list/detail query) interfaces."
        ),
    },
    {"name": WORKFLOW2_TAG, "description": "Form filling and user profile structuring module (reserved)."},
    {"name": WORKFLOW3_TAG, "description": "RAG-based recommendation system (reserved)."},
    {
        "name": SYSTEM_TAG,
        "description": "Perform API key/runtime status checks only",
    },
]

app = FastAPI(
    title="Workflow Orchestrator for Habit Recommendation System",
    description=(
        "This service is a workflow coordination (orchestration) layer of the Habit Recommendation System.\n\n"
        "Workflows:\n"
        f"1) {WORKFLOW1_TAG}: habit ingestion + structuring (habit detection → context extraction → BCIO mapping)\n"
        f"2) {WORKFLOW2_TAG}: form-based user profiling (reserved)\n"
        f"3) {WORKFLOW3_TAG}: RAG-based recommendation generation (reserved)\n\n"
        "This service orchestrates upstream API-service calls and persists business data in MongoDB.\n"
    ),
    version="0.1.0",
    openapi_tags=OPENAPI_TAGS,
)

# ----------------------------
# Middleware
# ----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=False,
)

# ----------------------------
# Routers
# ----------------------------
workflow1_router = APIRouter(tags=[WORKFLOW1_TAG])
system_router = APIRouter(tags=[SYSTEM_TAG])

# ----------------------------
# Config
# ----------------------------
API_BASE = os.getenv("API_BASE_URL", "http://127.0.0.1:8080")

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://127.0.0.1:27017/HabitDB")
MONGO = AsyncIOMotorClient(MONGODB_URI, serverSelectionTimeoutMS=2000)
DB = MONGO.get_default_database()

HABITS_COLL = DB.get_collection("habits")
CONTEXTS_COLL = DB.get_collection("contexts")  # raw classify_context output (no mapping)
CONTEXT_MAPPINGS_COLL = DB.get_collection("context_mappings")  # enriched mapping results

SESSION = requests.Session()

# ----------------------------
# Env helpers (type-safe)
# ----------------------------
def _env_float(name: str, default: float) -> float:
    v = os.getenv(name)
    if v is None or str(v).strip() == "":
        return float(default)
    try:
        return float(v)
    except ValueError:
        return float(default)

def _env_int(name: str, default: int) -> int:
    v = os.getenv(name)
    if v is None or str(v).strip() == "":
        return int(default)
    try:
        return int(v)
    except ValueError:
        return int(default)

# ----------------------------
# Mongo helpers
# ----------------------------
def _oid_str(oid: Any) -> Optional[str]:
    return str(oid) if oid is not None else None

def _created_at_from_oid(oid: Any) -> Optional[str]:
    if oid is None:
        return None
    try:
        return oid.generation_time.isoformat()  # UTC
    except Exception:
        return None

# ----------------------------
# Models
# ----------------------------
class IngestIn(BaseModel):
    habit: str
    language: str = "en"

class IngestOut(BaseModel):
    ok: bool
    message: str
    data: dict

# ----------------------------
# Helpers
# ----------------------------
def _normalize_text(s: str) -> str:
    s = unicodedata.normalize("NFC", s).strip()
    return re.sub(r"\s+", " ", s)

def _habit_key(habit: str, language: str) -> str:
    """
    Stable key based on normalized input text.
    NOTE: includes language to avoid cross-language collision.
    """
    base = f"{language.strip()}|{_normalize_text(habit)}"
    return hashlib.sha256(base.encode("utf-8")).hexdigest()

def call_api_classify_habit(habit: str, language: str, uuid_str: str) -> dict:
    url = f"{API_BASE}/classify_habit"
    try:
        r = SESSION.post(
            url,
            json={"uuid": uuid_str, "habit": habit, "language": language},
            timeout=(3, 600),
        )
        r.raise_for_status()
        return r.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=502, detail=f"classify_habit upstream error: {e}")

def call_api_classify_context(habit: str, language: str, uuid_str: str) -> dict:
    url = f"{API_BASE}/classify_context"
    try:
        r = SESSION.post(
            url,
            json={"uuid": uuid_str, "habit": habit, "language": language},
            timeout=(3, 600),
        )
        r.raise_for_status()
        return r.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=502, detail=f"classify_context upstream error: {e}")

def call_api_bcio_map(
    context_payload: dict,
    threshold: float = 0.6,
    top_n: int = 2,
    expr: str | None = 'etype in ["Class","ObjectProperty"]',
    debug: bool = False,
) -> dict:
    """
    Call upstream API-service POST /map
    body: ClassifyContextOut (dict)
    query: threshold, top_n, expr, debug
    """
    url = f"{API_BASE}/map"
    try:
        r = SESSION.post(
            url,
            params={
                "threshold": threshold,
                "top_n": top_n,
                "expr": expr,
                "debug": str(debug).lower(),
            },
            json=context_payload,
            timeout=(3, 600),
        )
        r.raise_for_status()
        return r.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=502, detail=f"bcio_map upstream error: {e}")

async def store_habit_data(habit_data: dict, habit_key: str) -> None:
    update_doc = {
        "$setOnInsert": {"uuid": habit_data.get("uuid")},
        "$set": {
            "habit": habit_data.get("habit"),
            "language": habit_data.get("language"),
            "habit_class": habit_data.get("habit_class", 0),
            "confidence": habit_data.get("confidence", None),
            "habit_key": habit_key,
        },
    }
    await HABITS_COLL.update_one({"uuid": habit_data.get("uuid")}, update_doc, upsert=True)

async def store_context_raw(context_data: dict) -> None:
    """
    contexts：只存原始 classify_context 输出（不含 mapping）
    """
    update_doc = {
        "$setOnInsert": {"uuid": context_data.get("uuid")},
        "$set": {
            "habit": context_data.get("habit"),
            "language": context_data.get("language"),
            "result": context_data.get("result", []),
        },
    }
    await CONTEXTS_COLL.update_one({"uuid": context_data.get("uuid")}, update_doc, upsert=True)

async def store_context_mapping(mapped_data: dict) -> None:
    """
    context_mappings: Stores enriched data (including bcio_mappings / mapping error)
    + mapping_params (threshold used in this call / top_n)
    """
    update_doc = {
        "$setOnInsert": {"uuid": mapped_data.get("uuid")},
        "$set": {
            "habit": mapped_data.get("habit"),
            "language": mapped_data.get("language"),
            "result": mapped_data.get("result", []),
            "bcio_mapping_error": mapped_data.get("bcio_mapping_error"),
            "mapping_params": mapped_data.get("mapping_params"),
        },
    }
    await CONTEXT_MAPPINGS_COLL.update_one({"uuid": mapped_data.get("uuid")}, update_doc, upsert=True)

async def _merge_habit(uuid_str: str) -> dict:
    """
    Merge habits + contexts + context_mappings into one record for frontend.
    """
    habit_doc = await HABITS_COLL.find_one({"uuid": uuid_str})
    if not habit_doc:
        raise HTTPException(status_code=404, detail="habit not found")

    raw_doc = await CONTEXTS_COLL.find_one({"uuid": uuid_str})
    mapped_doc = await CONTEXT_MAPPINGS_COLL.find_one({"uuid": uuid_str})

    return {
        "_id": _oid_str(habit_doc.get("_id")),
        "created_at": _created_at_from_oid(habit_doc.get("_id")),
        "uuid": habit_doc.get("uuid"),
        "habit": habit_doc.get("habit"),
        "language": habit_doc.get("language"),
        "habit_class": habit_doc.get("habit_class", 0),
        "confidence": habit_doc.get("confidence"),
        "contexts_raw": (raw_doc or {}).get("result", []),
        "contexts_mapped": (mapped_doc or {}).get("result", []),
        "bcio_mapping_error": (mapped_doc or {}).get("bcio_mapping_error"),
        "mapping_params": (mapped_doc or {}).get("mapping_params"),
    }

def _ingest_response_from_merged(merged: dict) -> IngestOut:
    """
    Build the same response shape as /ingest would return,
    but using stored results (deduplicated).
    """
    is_habit = int(merged.get("habit_class", 0)) == 1

    if is_habit:
        data = {
            "uuid": merged.get("uuid"),
            "habit": merged.get("habit"),
            "language": merged.get("language"),
            "result": merged.get("contexts_mapped") or merged.get("contexts_raw") or [],
            "mapping_params": merged.get("mapping_params"),
            "_meta": {
                "mongo_id": merged.get("_id"),
                "created_at": merged.get("created_at"),
                "mapping_params": merged.get("mapping_params"),
            },
        }
        if merged.get("bcio_mapping_error") is not None:
            data["bcio_mapping_error"] = merged.get("bcio_mapping_error")

        return IngestOut(
            ok=True,
            message=(
                "This sentence has already been processed. Returning the stored result (deduplicated)."
            ),
            data=data,
        )

    data = {
        "uuid": merged.get("uuid"),
        "habit": merged.get("habit"),
        "language": merged.get("language"),
        "habit_class": merged.get("habit_class", 0),
        "confidence": merged.get("confidence"),
        "_meta": {"mongo_id": merged.get("_id"), "created_at": merged.get("created_at")},
    }
    return IngestOut(
        ok=False,
        message="This sentence already exists and was classified as not a habit. Returning the stored result (deduplicated).",
        data=data,
    )

# ----------------------------
# System routes
# ----------------------------
@system_router.get(
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

@system_router.get(
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
        "mapping_params": {
            "threshold": threshold,
            "top_n": top_n,
        },
    }

# ----------------------------
# Workflow 1 routes
# ----------------------------
@workflow1_router.post(
    "/ingest",
    response_model=IngestOut,
    summary="Workflow 1: classify habit -> classify context -> BCIO map -> store raw+mapped into HabitDB",
)
async def ingest(body: IngestIn):
    clean_habit = _normalize_text(body.habit)
    hk = _habit_key(clean_habit, body.language)

    # dedup: if habit_key exists, return stored results directly (no upstream calls, no writes)
    existing = await HABITS_COLL.find_one({"habit_key": hk})
    if existing and existing.get("uuid"):
        merged = await _merge_habit(existing["uuid"])
        return _ingest_response_from_merged(merged)

    uuid_str = str(uuid.uuid4())

    # 1) classify_habit
    habit_out = await run_in_threadpool(
        lambda: call_api_classify_habit(clean_habit, body.language, uuid_str)
    )
    is_habit = int(habit_out.get("habit_class", 0)) == 1

    # 2) store habit result (with habit_key)
    await store_habit_data(habit_out, habit_key=hk)

    # 3) if habit -> classify_context
    if is_habit:
        context_out = await run_in_threadpool(
            lambda: call_api_classify_context(clean_habit, body.language, uuid_str)
        )

        # 3.1 store raw contexts (no mapping)
        await store_context_raw(context_out)

        # 3.2 BCIO mapping (failure does not block the workflow)
        threshold = _env_float("THRESHOLD_BCIO_MAP", 0.6)
        top_n = _env_int("TOP_N_BCIO_MAP", 2)

        try:
            mapped_out = await run_in_threadpool(
                lambda: call_api_bcio_map(context_out, threshold=threshold, top_n=top_n)
            )
        except HTTPException as e:
            mapped_out = dict(context_out)  # copy to avoid accidental shared reference
            mapped_out["bcio_mapping_error"] = str(e.detail)

        # attach mapping params for storage + UI
        mapped_out["mapping_params"] = {"threshold": threshold, "top_n": top_n}

        # 3.3 store mapping result in new collection
        await store_context_mapping(mapped_out)

        # Optional meta for UI: mongo _id + time (derived from ObjectId)
        merged = await _merge_habit(uuid_str)
        mapped_out["_meta"] = {
            "mongo_id": merged.get("_id"),
            "created_at": merged.get("created_at"),
            "mapping_params": merged.get("mapping_params"),
        }

        return IngestOut(
            ok=True,
            message=(
                "Excellent! Your habit sentence has been processed using the seven predefined context labels "
                '["TIME", "PHYSICAL SETTING", "PRIOR BEHAVIOR", "OTHER PEOPLE", "INTERNAL STATE", "BEHAVIOR", "REASONING"]. '
                "Extracted phrases were mapped to BCIO and stored successfully."
            ),
            data=mapped_out,
        )

    # still return habit_out with meta
    merged = await _merge_habit(uuid_str)
    habit_out["_meta"] = {"mongo_id": merged.get("_id"), "created_at": merged.get("created_at")}
    return IngestOut(ok=False, message="The input provided is not a habit. Please retry.", data=habit_out)

@workflow1_router.get(
    "/habits",
    summary="List habits (for management UI)",
    description="Returns habits sorted by Mongo _id desc (newest first).",
)
async def list_habits(
    limit: int = Query(30, ge=1, le=200),
    skip: int = Query(0, ge=0),
    only_habits: bool = Query(True, description="If true, only habit_class==1 are returned."),
):
    q: dict[str, Any] = {}
    if only_habits:
        q["habit_class"] = 1

    cursor = HABITS_COLL.find(q).sort([("_id", -1)]).skip(skip).limit(limit)
    items = []
    async for doc in cursor:
        u = doc.get("uuid")
        if not u:
            continue
        items.append(await _merge_habit(u))

    total = await HABITS_COLL.count_documents(q)
    return {"ok": True, "total": total, "limit": limit, "skip": skip, "items": items}

@workflow1_router.get(
    "/habits/{uuid_str}",
    summary="Get habit detail (for management UI)",
)
async def get_habit(uuid_str: str):
    merged = await _merge_habit(uuid_str)
    return {"ok": True, "item": merged}

# ----------------------------
# Mount routers
# ----------------------------
app.include_router(workflow1_router)
app.include_router(system_router)

# ----------------------------
# Entrypoint
# ----------------------------
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8081, reload=True)
