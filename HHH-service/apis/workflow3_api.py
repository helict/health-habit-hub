from __future__ import annotations

import os
import re
import uuid
import hashlib
import unicodedata
from datetime import datetime, timezone
from typing import Any, Dict, Optional, List

import requests
from fastapi import APIRouter, HTTPException
from fastapi.concurrency import run_in_threadpool
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, Field, confloat


WORKFLOW3_TAG = "Workflow3: Recommended workflow"
router = APIRouter(prefix="", tags=[WORKFLOW3_TAG])

API_BASE = os.getenv("API_BASE_URL", "http://127.0.0.1:8080").rstrip("/")

# ----------------------------
# Mongo (HHH-service cache DB)
# ----------------------------
# ----------------------------
# Mongo config
# ----------------------------
MONGO_URI = os.getenv(
    "MONGO_URI", os.getenv("MONGODB_URI", "mongodb://127.0.0.1:27017")
)
RECOMMEND_DB_NAME = os.getenv("RECOMMEND_DB_NAME", "RecommendationsDB")

BILDED_PROFILES_COLL_NAME = os.getenv("BILDED_PROFILES_COLL_NAME", "bilded_profiles")
SELECTED_HABITS_COLL_NAME = os.getenv("SELECTED_HABITS_COLL_NAME", "selected_habits")
KB_QUERY_COLL_NAME = os.getenv("KB_QUERY_COLL_NAME", "kb_queries")
RECOMMENDATION_RESULTS_COLL_NAME = os.getenv(
    "RECOMMENDATION_RESULTS_COLL_NAME", "recommendation_results_outputs"
)
RECOMMENDATION_COMMENTS_COLL_NAME = os.getenv(
    "RECOMMENDATION_COMMENTS_COLL_NAME", "recommendation_comments"
)
HISTORY_COLL_NAME = os.getenv("HISTORY_COLL_NAME", "recommendation_history")


# ----------------------------
# Mongo client
# ----------------------------
MONGO = AsyncIOMotorClient(MONGO_URI, serverSelectionTimeoutMS=2000)

RECOMMEND_DB = MONGO.get_database(RECOMMEND_DB_NAME)

BILDED_PROFILES_COLL = RECOMMEND_DB.get_collection(BILDED_PROFILES_COLL_NAME)
SELECTED_HABITS_COLL = RECOMMEND_DB.get_collection(SELECTED_HABITS_COLL_NAME)
KB_QUERY_COLL = RECOMMEND_DB.get_collection(KB_QUERY_COLL_NAME)
RECOMMENDATION_RESULTS_COLL = RECOMMEND_DB.get_collection(
    RECOMMENDATION_RESULTS_COLL_NAME
)
RECOMMENDATION_COMMENTS_COLL = RECOMMEND_DB.get_collection(
    RECOMMENDATION_COMMENTS_COLL_NAME
)
HISTORY_COLL = RECOMMEND_DB.get_collection(HISTORY_COLL_NAME)


# 整个api的输入
class RecommendIn(BaseModel):
    text: str = Field(min_length=1, max_length=5000)


# 习惯选择api的输出
class SelectedHabitOut(BaseModel):
    habit: str
    habit_key: str
    score: confloat(ge=0.0, le=1.0)
    reason: str
    contexts: List[Any]  # 7 values


class HabitDBSelectOut(BaseModel):
    request_uuid: str
    text: str
    llm_meta: Dict[str, Any]
    selected_habits: List[SelectedHabitOut] = Field(default_factory=list)
    selected_habits_summary: str = ""


# profliesapi的输出
class ProfilesBuildOut(BaseModel):
    request_uuid: str
    text: str
    llm_meta: Dict[str, Any] = Field(default_factory=dict)
    profile_detailed: str = ""
    profile_summary: str = ""


# kb查询api的输出
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


# 推荐api的输出


class HabitRecommendation(BaseModel):
    context: str
    behavior: str
    explanation: str


class RecommendApiOut(BaseModel):
    request_uuid: str
    text: str
    habit_recommendations: List[HabitRecommendation] = Field(default_factory=list)
    llm_meta: Dict[str, Any] = Field(default_factory=dict)
    message: str


# 推荐评论api的输出
class RecommendCommentIn(BaseModel):
    request_uuid: str
    text: str
    comment: Optional[str] = None


class RecommendCommentOut(BaseModel):
    request_uuid: str
    text: str
    comment: Optional[str] = None


# 整个workflow3的总输出


class RecommendOut(BaseModel):
    request_uuid: str
    text: str
    text_signature: Optional[str] = None
    created_at: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    selected_habits: Dict[str, Any] = Field(default_factory=dict)
    bilded_profiles: Dict[str, Any] = Field(default_factory=dict)
    kb_queries: Dict[str, Any] = Field(default_factory=dict)
    recommendation_results_outputs: Dict[str, Any] = Field(default_factory=dict)
    user_feedback: Optional[str] = None


# ============================================================
# Helpers (shared)
# ============================================================
def _normalize_text(s: str) -> str:
    s = unicodedata.normalize("NFC", s).strip()
    return re.sub(r"\s+", " ", s)


def _text_key(text: str) -> str:
    base = _normalize_text(text)
    return hashlib.sha256(base.encode("utf-8")).hexdigest()


# 调用api

SESSION = requests.Session()


def call_api_habits_select(request_uuid: str, text: str) -> dict:
    url = f"{API_BASE}/habit_db/select"
    try:
        r = SESSION.post(
            url,
            json={"request_uuid": request_uuid, "text": text},
            timeout=(3, 600),
        )
        r.raise_for_status()
        return r.json()
    except requests.RequestException as e:
        raise HTTPException(
            status_code=502, detail=f"habit_db/select api upstream error: {e}"
        )


def call_api_proflies_build(request_uuid: str, text: str) -> dict:
    url = f"{API_BASE}/profiles/build"
    try:
        r = SESSION.post(
            url,
            json={"request_uuid": request_uuid, "text": text},
            timeout=(3, 600),
        )
        r.raise_for_status()
        return r.json()
    except requests.RequestException as e:
        raise HTTPException(
            status_code=502, detail=f"profiles/build api upstream error: {e}"
        )


def call_api_kb_query(request_uuid: str, text: str) -> dict:
    url = f"{API_BASE}/kb/query"
    try:
        r = SESSION.post(
            url,
            json={"request_uuid": request_uuid, "text": text},
            timeout=(3, 600),
        )
        r.raise_for_status()
        return r.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=502, detail=f"kb/query api upstream error: {e}")


def call_api_recommend(
    request_uuid: str,
    text: str,
    profile_detailed: str,
    selected_habits: list,
    rag_result: list,
    user_feedback: str,
) -> dict:
    url = f"{API_BASE}/recommend"
    try:
        r = SESSION.post(
            url,
            json={
                "request_uuid": request_uuid,
                "text": text,
                "profile_detailed": profile_detailed,
                "selected_habits": selected_habits,
                "rag_result": rag_result,
                "user_feedback": user_feedback,
            },
            timeout=(3, 600),
        )
        r.raise_for_status()
        return r.json()
    except requests.RequestException as e:
        raise HTTPException(
            status_code=502, detail=f"recommend api upstream error: {e}"
        )


# 存储


async def store_selected_habits_data(
    request_uuid: str, text: str, text_signature: str, api_output: dict
) -> None:
    update_doc = {
        "$set": {
            "request_uuid": request_uuid,
            "text": text,
            "llm_meta": api_output.get("llm_meta"),
            "selected_habits": api_output.get("selected_habits"),
            "selected_habits_summary": api_output.get("selected_habits_summary"),
        },
        "$setOnInsert": {"text_signature": text_signature},
    }
    await SELECTED_HABITS_COLL.update_one(
        {"text_signature": text_signature}, update_doc, upsert=True
    )


async def store_bilded_profiles_data(
    request_uuid: str, text: str, text_signature: str, api_output: dict
) -> None:
    update_doc = {
        "$set": {
            "request_uuid": request_uuid,
            "text": text,
            "llm_meta": api_output.get("llm_meta"),
            "profile_detailed": api_output.get("profile_detailed"),
            "profile_summary": api_output.get("profile_summary"),
        },
        "$setOnInsert": {"text_signature": text_signature},
    }
    await BILDED_PROFILES_COLL.update_one(
        {"text_signature": text_signature}, update_doc, upsert=True
    )


async def store_kb_queries_data(
    request_uuid: str, text: str, text_signature: str, api_output: dict
) -> None:
    update_doc = {
        "$set": {
            "request_uuid": request_uuid,
            "text": text,
            "query": api_output.get("query"),
            "llm_meta": api_output.get("llm_meta"),
            "retrieval": api_output.get("retrieval"),
            "hits": api_output.get("hits"),
        },
        "$setOnInsert": {"text_signature": text_signature},
    }
    await KB_QUERY_COLL.update_one(
        {"text_signature": text_signature}, update_doc, upsert=True
    )


async def store_recommendation_results_data(
    request_uuid: str, text: str, text_signature: str, api_output: dict
) -> None:
    update_doc = {
        "$set": {
            "request_uuid": request_uuid,
            "text": text,
            "habit_recommendations": api_output.get("habit_recommendations"),
            "llm_meta": api_output.get("llm_meta"),
            "message": api_output.get("message"),
        },
        "$setOnInsert": {"text_signature": text_signature},
    }
    await RECOMMENDATION_RESULTS_COLL.update_one(
        {"text_signature": text_signature}, update_doc, upsert=True
    )


async def store_recommendation_comment(
    request_uuid: str, text: str, text_signature: str, api_output: dict
) -> None:
    update_doc = {
        "$set": {
            "request_uuid": request_uuid,
            "text": text,
            "comment": api_output.get("comment"),
        },
        "$setOnInsert": {"text_signature": text_signature},
    }
    await RECOMMENDATION_COMMENTS_COLL.update_one(
        {"text_signature": text_signature}, update_doc, upsert=True
    )


async def store_recommendation_history(out: RecommendOut) -> None:
    doc = out.model_dump()
    await HISTORY_COLL.insert_one(doc)


# ============================================================
# /recommend (Workflow3 )
# ============================================================
@router.post(
    "/recommend",
    response_model=RecommendOut,
    summary=(
        "Workflow3: Full recommendation workflow including theory selection, "
        "profile building, habit selection, knowledge base query, and recommendation generation."
    ),
)
async def recommend(payload: RecommendIn) -> RecommendOut:

    request_uuid = str(uuid.uuid4())
    clean_text = _normalize_text(payload.text)
    text_signature = _text_key(clean_text)
    # =========================================================
    # STEP 1) /habit_db/select
    # =========================================================
    habits_select_out = await run_in_threadpool(
        lambda: call_api_habits_select(request_uuid, clean_text)
    )
    # 获取数据
    selected_habits = habits_select_out.get("selected_habits", [])
    selected_habits_summary = habits_select_out.get("selected_habits_summary", "")

    await store_selected_habits_data(
        request_uuid, clean_text, text_signature, habits_select_out
    )

    step1_out = {
        "llm_meta": habits_select_out.get("llm_meta", {}),
        "selected_habits": habits_select_out.get("selected_habits", []),
        "selected_habits_summary": habits_select_out.get("selected_habits_summary", ""),
    }
    # =========================================================
    # STEP 2) /profiles/build
    # =========================================================
    profiles_build_out = await run_in_threadpool(
        lambda: call_api_proflies_build(request_uuid, clean_text)
    )

    # 获取数据
    profile_detailed = profiles_build_out.get("profile_detailed", "")
    profile_summary = profiles_build_out.get("profile_summary", "")

    await store_bilded_profiles_data(
        request_uuid, clean_text, text_signature, profiles_build_out
    )
    step2_out = {
        "llm_meta": profiles_build_out.get("llm_meta", {}),
        "profile_detailed": profiles_build_out.get("profile_detailed", ""),
        "profile_summary": profiles_build_out.get("profile_summary", ""),
    }
    # =========================================================
    # STEP 3) /kb/query
    # =========================================================
    query = f"{clean_text}\n\n{selected_habits_summary}\n\n{profile_summary}"

    kb_query_out = await run_in_threadpool(
        lambda: call_api_kb_query(request_uuid, query)
    )
    await store_kb_queries_data(request_uuid, clean_text, text_signature, kb_query_out)

    hits = kb_query_out.get("hits", [])

    step3_out = {
        "query": kb_query_out.get("query", ""),
        "llm_meta": kb_query_out.get("llm_meta", {}),
        "retrieval": kb_query_out.get("retrieval", {}),
        "hits": kb_query_out.get("hits", []),
    }
    # =========================================================
    # STEP 4) /recommend
    # =========================================================
    comment_doc = await RECOMMENDATION_COMMENTS_COLL.find_one(
        {"text_signature": text_signature}
    )
    latest_user_feedback = (comment_doc or {}).get("comment") or ""
    reco_out_raw = await run_in_threadpool(
        lambda: call_api_recommend(
            request_uuid,
            clean_text,
            profile_detailed,
            selected_habits,
            hits,
            latest_user_feedback,
        )
    )

    step4_out = {
        "habit_recommendations": reco_out_raw.get("habit_recommendations", []),
        "llm_meta": reco_out_raw.get("llm_meta", {}),
        "message": reco_out_raw.get("message", ""),
    }
    await store_recommendation_results_data(
        request_uuid, clean_text, text_signature, reco_out_raw
    )
    out = RecommendOut(
        request_uuid=request_uuid,
        text=clean_text,
        text_signature=text_signature,
        created_at=datetime.now(timezone.utc).isoformat(),
        selected_habits=step1_out,
        bilded_profiles=step2_out,
        kb_queries=step3_out,
        recommendation_results_outputs=step4_out,
        user_feedback=latest_user_feedback,
    )
    await store_recommendation_history(out)
    return out


@router.post(
    "/recommend/comment",
    response_model=RecommendCommentOut,
    summary="Workflow3: Store a user comment for a recommendation request",
)
async def recommend_comment(payload: RecommendCommentIn) -> RecommendCommentOut:
    clean_text = _normalize_text(payload.text)
    text_signature = _text_key(clean_text)

    await store_recommendation_comment(
        payload.request_uuid, clean_text, text_signature, payload.model_dump()
    )

    return RecommendCommentOut(
        request_uuid=payload.request_uuid,
        text=payload.text,
        comment=payload.comment,
    )
