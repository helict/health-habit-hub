# apis/workflow2_api.py
from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Any, Dict, Optional, Literal

from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

WORKFLOW2_TAG = "Workflow2: User Profile/Form Workflow "

router = APIRouter(tags=[WORKFLOW2_TAG])

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://127.0.0.1:27017/UserProfiles")
MONGO = AsyncIOMotorClient(MONGODB_URI, serverSelectionTimeoutMS=2000)
DB = MONGO.get_default_database()
ProfileFormKey = Literal["basic", "sliq", "rand36"]
FORM_KEYS: tuple[str, ...] = ("basic", "sliq", "rand36")
COLL_BY_FORM = {k: DB.get_collection(k) for k in FORM_KEYS}


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


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


# ----------------------------
# Ensure indexes (lazy, once)
# ----------------------------
_INDEX_READY = False


async def _ensure_indexes():
    global _INDEX_READY
    if _INDEX_READY:
        return

    for k, coll in COLL_BY_FORM.items():
        await coll.create_index([("profile_uuid", 1)], unique=True)
        await coll.create_index([("profile_uuid", 1), ("updated_at", -1)])

    _INDEX_READY = True


# ----------------------------
# Models
# ----------------------------
class ProfileLatestIn(BaseModel):
    form: ProfileFormKey
    data: Dict[str, Any] = Field(default_factory=dict)


class ApiOut(BaseModel):
    ok: bool
    message: str
    data: Optional[Any] = None


# ----------------------------
# Routes
# ----------------------------
@router.put(
    "/profile/{profile_uuid}/latest",
    response_model=ApiOut,
    summary="Workflow 2: Save latest profile form (one collection per form, upsert by profile_uuid)",
)
async def put_profile_latest(profile_uuid: str, body: ProfileLatestIn):
    await _ensure_indexes()

    coll = COLL_BY_FORM.get(body.form)
    if coll is None:
        raise HTTPException(status_code=400, detail="Invalid form")

    updated_at = _now_iso()
    doc = {
        "profile_uuid": profile_uuid,
        "data": body.data,
        "updated_at": updated_at,
    }

    try:
        await coll.update_one(
            {"profile_uuid": profile_uuid},
            {"$set": doc},
            upsert=True,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB error: {e}")

    saved = await coll.find_one({"profile_uuid": profile_uuid})
    meta = {
        "mongo_id": _oid_str((saved or {}).get("_id")),
        "created_at": _created_at_from_oid((saved or {}).get("_id")),
        "updated_at": (saved or {}).get("updated_at", updated_at),
        "collection": body.form,
    }

    return ApiOut(
        ok=True,
        message="Saved",
        data={
            "profile_uuid": profile_uuid,
            "form": body.form,
            "_meta": meta,
        },
    )


@router.get(
    "/profile/{profile_uuid}/latest",
    response_model=ApiOut,
    summary="Workflow 2: Get latest profile form (one form or all forms)",
)
async def get_profile_latest(
    profile_uuid: str,
    form: Optional[ProfileFormKey] = Query(default=None, description="If provided, return only that form."),
):
    await _ensure_indexes()

    if form:
        coll = COLL_BY_FORM.get(form)
        doc = await coll.find_one({"profile_uuid": profile_uuid})
        if not doc:
            return ApiOut(ok=True, message="No data yet", data=None)

        return ApiOut(
            ok=True,
            message="OK",
            data={
                "profile_uuid": doc.get("profile_uuid"),
                "form": form,
                "data": doc.get("data", {}),
                "updated_at": doc.get("updated_at"),
                "_meta": {
                    "mongo_id": _oid_str(doc.get("_id")),
                    "created_at": _created_at_from_oid(doc.get("_id")),
                    "collection": form,
                },
            },
        )

    out: Dict[str, Any] = {}
    for k, coll in COLL_BY_FORM.items():
        doc = await coll.find_one({"profile_uuid": profile_uuid})
        if not doc:
            continue
        out[k] = {
            "profile_uuid": doc.get("profile_uuid"),
            "form": k,
            "data": doc.get("data", {}),
            "updated_at": doc.get("updated_at"),
            "_meta": {
                "mongo_id": _oid_str(doc.get("_id")),
                "created_at": _created_at_from_oid(doc.get("_id")),
                "collection": k,
            },
        }

    return ApiOut(ok=True, message="OK", data=out)
