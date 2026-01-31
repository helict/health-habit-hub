from __future__ import annotations

import os
import re
import uuid
import unicodedata
import requests
import hashlib
from typing import Any, Optional, Dict
from datetime import datetime, timezone
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi.concurrency import run_in_threadpool
from fastapi import HTTPException, APIRouter, Query
from pydantic import BaseModel

WORKFLOW1_TAG = "Workflow1: Habitual structured collection workflow"
router = APIRouter(tags=[WORKFLOW1_TAG])

API_BASE = os.getenv("API_BASE_URL", "http://127.0.0.1:8080")

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://127.0.0.1:27017/HabitDB")
MONGO = AsyncIOMotorClient(MONGODB_URI, serverSelectionTimeoutMS=2000)
DB = MONGO.get_default_database()

HABITS_COLL = DB.get_collection("habits")
CONTEXTS_COLL = DB.get_collection("contexts")  # raw classify_context output (no mapping)
CONTEXT_MAPPINGS_COLL = DB.get_collection("context_mappings")  # enriched mapping results
HABIT_HISTORY_COLL = DB.get_collection("habit_history")  # historical versions of habits


SESSION = requests.Session()


# ----------------------------
# Models
# ----------------------------
class IngestIn(BaseModel):
    habit: str
    language: str = "en"


class IngestOut(BaseModel):
    uuid: Optional[str] = None
    stored_at: Optional[datetime]
    ok: bool
    message: str
    data: dict
    mapping_params: Optional[Dict[str, Any]] = None
    llm_meta: Optional[Dict[str, Any]] = None


# ----------------------------
# Helpers
# ----------------------------
def _normalize_text(s: str) -> str:
    s = unicodedata.normalize("NFC", s).strip()
    return re.sub(r"\s+", " ", s)


def _habit_key(habit: str) -> str:
    """
    Stable key based on normalized input text.
    NOTE: language does NOT participate (per your requirement).
    """
    base = _normalize_text(habit)
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
    expr: str | None = 'etype in ["Class","ObjectProperty"]',
    debug: bool = False,
) -> dict:
    url = f"{API_BASE}/map"
    try:
        r = SESSION.post(
            url,
            params={
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


# ----------------------------
# Mongo store (latest overwrite by habit_key)
# ----------------------------
async def store_habit_data(habit_data: dict, habit_key: str, habit_text: str, language: str, uuid: str) -> None:
    """
    habits: only business fields + llm_meta, keyed by habit_key
    """
    update_doc = {
        "$set": {
            "uuid": uuid,
            "habit": habit_text,
            "language": language,
            "habit_class": habit_data.get("habit_class", 0),
            "confidence": habit_data.get("confidence", None),
            "llm_meta": habit_data.get("llm_meta"),
        },"$setOnInsert": {
            "habit_key": habit_key
        },
    }
    await HABITS_COLL.update_one({"habit_key": habit_key}, update_doc, upsert=True)


async def store_context_raw(context_data: dict, habit_key: str, habit_text: str, language: str, uuid: str) -> None:
    """
    contexts: only raw classify_context output + llm_meta, keyed by habit_key
    """
    update_doc = {
        "$set": {
            "uuid": uuid,
            "habit": habit_text,
            "language": language,
            "result": context_data.get("result", []),
            "llm_meta": context_data.get("llm_meta"),
        },"$setOnInsert": {
            "habit_key": habit_key
        },
    }
    await CONTEXTS_COLL.update_one({"habit_key": habit_key}, update_doc, upsert=True)


async def store_context_mapping(mapped_data: dict, habit_key: str, habit_text: str, language: str, uuid: str) -> None:
    """
    context_mappings: only mapped result + mapping_params + mapping_error, keyed by habit_key
    NOTE: DO NOT store llm_meta here (your requirement)
    """
    update_doc = {
        "$set": {
            "uuid": uuid,
            "habit": habit_text,
            "language": language,
            "result": mapped_data.get("result", []),
            "bcio_mapping_error": mapped_data.get("bcio_mapping_error"),
            "mapping_params": mapped_data.get("mapping_params"),
        },"$setOnInsert": {
            "habit_key": habit_key
        },
    }
    await CONTEXT_MAPPINGS_COLL.update_one({"habit_key": habit_key}, update_doc, upsert=True)

async def write_habit_history(out: IngestOut) -> None:
    doc = out.model_dump()
    await HABIT_HISTORY_COLL.insert_one(doc)


# ----------------------------
# Routes
# ----------------------------
@router.post(
    "/ingest",
    response_model=IngestOut,
    response_model_exclude_none=True,
    summary="Workflow 1: classify habit -> classify context -> BCIO map -> store raw+mapped into HabitDB (latest overwrite)",
)
async def ingest(body: IngestIn):
    clean_habit = _normalize_text(body.habit)
    hk = _habit_key(clean_habit)

    # one request uuid for this ingest call
    req_uuid = str(uuid.uuid4())

    # 1) classify habit
    habit_out = await run_in_threadpool(
        lambda: call_api_classify_habit(clean_habit, body.language, req_uuid)
    )
    is_habit = int(habit_out.get("habit_class", 0)) == 1

    # 2) store habit (always)
    await store_habit_data(
        habit_out,
        habit_key=hk,
        habit_text=clean_habit,
        language=body.language,
        uuid=req_uuid,
    )

    # 3) if NOT habit -> return
    if not is_habit:
        out=IngestOut(
            uuid=req_uuid,
            stored_at=datetime.now(timezone.utc),
            ok=False,
            message=(
                "The input you provided is not a habitual behavior. Please enter a habit instead. "
                "This data will be stored locally in the MongoDB habits collection, but it will not be used "
                "for subsequent context classification or Behaviour Change Intervention Ontology Mapping."
            ),
            data={
                "habit_key": hk,
                "habit": clean_habit,
                "language": body.language,
                "habit_class": habit_out.get("habit_class", 0),
                "confidence": habit_out.get("confidence", None),
            },
            llm_meta={"habit": habit_out.get("llm_meta"), "context": {}},
        )
        await write_habit_history(out)
        return out

    # 4) habit -> classify context
    context_out = await run_in_threadpool(
        lambda: call_api_classify_context(clean_habit, body.language, req_uuid)
    )

    await store_context_raw(
        context_out,
        habit_key=hk,
        habit_text=clean_habit,
        language=body.language,
        uuid=req_uuid,
    )

    # 5) mapping (drop llm_meta before sending to mapper, per your requirement)

    context_payload = {k: v for k, v in context_out.items() if k != "llm_meta"}

    try:
        mapped_out = await run_in_threadpool(
            lambda: call_api_bcio_map(context_payload)
        )
    except HTTPException as e:
        mapped_out = {
            "result": context_out.get("result", []),
            "bcio_mapping_error": str(e.detail),
        }

    mapped_out["mapping_params"] = {
    "threshold": mapped_out.get("threshold"),
    "top_n": mapped_out.get("top_n"),
}

    await store_context_mapping(
        mapped_out,
        habit_key=hk,
        habit_text=clean_habit,
        language=body.language,
        uuid=req_uuid,
    )

    # 6) response
    resp_data = {
        "habit_key": hk,
        "habit": clean_habit,
        "language": body.language,
        "result": mapped_out.get("result", []),
    }
    if mapped_out.get("bcio_mapping_error") is not None:
        resp_data["bcio_mapping_error"] = mapped_out.get("bcio_mapping_error")

    out = IngestOut(
        uuid=req_uuid,
        stored_at=datetime.now(timezone.utc),
        ok=True,
        message="This input describes a habit, and it has been successfully processed: habit classification, context classification (TIME, PHYSICAL SETTING, PRIOR BEHAVIOR, OTHER PEOPLE, INTERNAL STATE, BEHAVIOR, and REASONING), and BCIO mapping have been completed and stored in the local database.",
        data=resp_data,
        mapping_params=mapped_out["mapping_params"],
        llm_meta={
            "habit": habit_out.get("llm_meta"),
            "context": context_out.get("llm_meta"),
        },
    )
    await write_habit_history(out)
    return out


async def _get_latest_item(habit_key: str) -> dict:
    habit_doc = await HABITS_COLL.find_one({"habit_key": habit_key}) or {}
    raw_doc = await CONTEXTS_COLL.find_one({"habit_key": habit_key}) or {}
    mapped_doc = await CONTEXT_MAPPINGS_COLL.find_one({"habit_key": habit_key}) or {}

    return {
        "habit_key": habit_key,
        "habit": habit_doc.get("habit"),
        "language": habit_doc.get("language"),
        "habit_class": habit_doc.get("habit_class", 0),
        "confidence": habit_doc.get("confidence"),
        "contexts_raw": raw_doc.get("result", []),
        "contexts_mapped": mapped_doc.get("result", []),
        "bcio_mapping_error": mapped_doc.get("bcio_mapping_error"),
        "mapping_params": mapped_doc.get("mapping_params"),
        "llm_meta_habit": habit_doc.get("llm_meta"),
        "llm_meta_context": raw_doc.get("llm_meta"),
    }


def _public_habit_item(latest: dict) -> dict:
    return {
        "habit_key": latest.get("habit_key"),
        "habit": latest.get("habit"),
        "language": latest.get("language"),
        "habit_class": latest.get("habit_class", 0),
        "confidence": latest.get("confidence"),
        "mapping_params": latest.get("mapping_params"),
        "contexts_raw": latest.get("contexts_raw") or [],
        "contexts_mapped": latest.get("contexts_mapped") or [],
        "bcio_mapping_error": latest.get("bcio_mapping_error"),
        "llm_meta":{"habit": latest.get("llm_meta_habit")or {}, "context": latest.get("llm_meta_context") or {}},
    }


@router.get(
    "/habits",
    summary="List habits (for management UI)",
    description="Returns habits sorted by Mongo _id desc (newest first). Items joined by habit_key.",
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
        hk = doc.get("habit_key")
        if not hk:
            continue
        latest = await _get_latest_item(hk)
        items.append(_public_habit_item(latest))

    total = await HABITS_COLL.count_documents(q)
    return {"ok": True, "total": total, "limit": limit, "skip": skip, "items": items}


@router.get(
    "/habits/{habit_key}",
    summary="Get habit detail (for management UI)",
    description="Joined by habit_key.",
)
async def get_habit(habit_key: str):
    latest = await _get_latest_item(habit_key)
    if not latest.get("habit"):
        raise HTTPException(status_code=404, detail="habit not found")
    return {"ok": True, "item": _public_habit_item(latest)}
