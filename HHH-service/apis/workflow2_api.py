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
# Time helpers
# ----------------------------
def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _created_at_from_oid(oid: Any) -> Optional[str]:
    if oid is None:
        return None
    try:
        return oid.generation_time.isoformat()  # UTC
    except Exception:
        return None


# ----------------------------
# Ensure indexes (lazy, once)
# ----------------------------
_INDEX_READY = False


async def _ensure_indexes():
    global _INDEX_READY
    if _INDEX_READY:
        return

    for _, coll in COLL_BY_FORM.items():
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
    success: bool
    message: str
    data: Optional[Any] = None


class ProfileLatestMetaOut(BaseModel):
    form: ProfileFormKey
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class ProfileLatestItemOut(BaseModel):
    form: ProfileFormKey
    data: Dict[str, Any] = Field(default_factory=dict)
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


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
        raise HTTPException(status_code=400, detail=f"Invalid form: {body.form}")

    now = _now_iso()

    # NOTE:
    # - profile_uuid 仍然用于 DB 的唯一键（只是“响应里”不再返回它）
    # - created_at 用 $setOnInsert 只在首次插入时写入
    try:
        await coll.update_one(
            {"profile_uuid": profile_uuid},
            {
                "$set": {
                    "profile_uuid": profile_uuid,
                    "data": body.data,
                    "updated_at": now,
                },
                "$setOnInsert": {
                    "created_at": now,
                },
            },
            upsert=True,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB error while saving form '{body.form}': {e}")

    saved = await coll.find_one({"profile_uuid": profile_uuid}) or {}

    created_at = saved.get("created_at") or _created_at_from_oid(saved.get("_id"))
    updated_at = saved.get("updated_at", now)

    return ApiOut(
        success=True,
        message=f"Saved latest '{body.form}' form successfully. created_at={created_at}, updated_at={updated_at}.",
        data=ProfileLatestMetaOut(
            form=body.form,
            created_at=created_at,
            updated_at=updated_at,
        ).model_dump(),
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

    # ---- single form ----
    if form:
        coll = COLL_BY_FORM.get(form)
        doc = await coll.find_one({"profile_uuid": profile_uuid})

        if not doc:
            return ApiOut(
                success=True,
                message=f"No saved data found for form '{form}' yet.",
                data=None,
            )

        created_at = doc.get("created_at") or _created_at_from_oid(doc.get("_id"))
        updated_at = doc.get("updated_at")

        return ApiOut(
            success=True,
            message=f"Retrieved latest '{form}' form successfully. updated_at={updated_at}.",
            data=ProfileLatestItemOut(
                form=form,
                data=doc.get("data", {}) or {},
                created_at=created_at,
                updated_at=updated_at,
            ).model_dump(),
        )

    # ---- all forms ----
    out: Dict[str, Any] = {}
    found_keys: list[str] = []

    for k, coll in COLL_BY_FORM.items():
        doc = await coll.find_one({"profile_uuid": profile_uuid})
        if not doc:
            continue

        created_at = doc.get("created_at") or _created_at_from_oid(doc.get("_id"))
        updated_at = doc.get("updated_at")

        out[k] = ProfileLatestItemOut(
            form=k,  # 冗余但好用：即使 map key 丢了也能知道是哪张表
            data=doc.get("data", {}) or {},
            created_at=created_at,
            updated_at=updated_at,
        ).model_dump()

        found_keys.append(k)

    if not out:
        return ApiOut(
            success=True,
            message="No saved profile forms found yet (basic/sliq/rand36 are all empty).",
            data={},
        )

    return ApiOut(
        success=True,
        message=f"Retrieved latest profile forms successfully: {', '.join(found_keys)}.",
        data=out,
    )
