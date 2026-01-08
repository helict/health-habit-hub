from __future__ import annotations

import os
import re
import json
import uuid
import hashlib
import unicodedata
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, Optional, Tuple, List

import requests
import redis.asyncio as redis
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
MONGO_URI = os.getenv("MONGO_URI", os.getenv("MONGODB_URI", "mongodb://127.0.0.1:27017"))
RECOMMEND_DB_NAME = os.getenv("RECOMMEND_DB_NAME", "recommendations")

SELECTED_USER_INFO_COLL_NAME = os.getenv("SELECTED_USER_INFO_COLL_NAME", "selected_user_info")
SELECTED_HABITS_COLL_NAME = os.getenv("SELECTED_HABITS_COLL_NAME", "selected_habits")

# store every request_uuid's theory choice (no cache)
THEORY_SELECTIONS_COLL_NAME = os.getenv("THEORY_SELECTIONS_COLL_NAME", "theory_selections")

# store every request_uuid's kb query output (no cache)
KB_QUERY_COLL_NAME = os.getenv("KB_QUERY_COLL_NAME", "kb_queries")

# NEW: store every request_uuid's API /recommend output (no cache)
RECO_API_OUTPUT_COLL_NAME = os.getenv("RECO_API_OUTPUT_COLL_NAME", "reco_api_outputs")

# NEW: store user comments for each request_uuid (no cache)
RECO_COMMENTS_COLL_NAME = os.getenv("RECO_COMMENTS_COLL_NAME", "recommendation_comments")

# Used to compute profiles_signature (same algorithm as profiles_build_api.py)
USERPROFILES_DB_NAME = os.getenv("USERPROFILES_DB_NAME", "UserProfiles")
USERPROFILES_BASIC_COLL_NAME = os.getenv("USERPROFILES_BASIC_COLL_NAME", "basic")
USERPROFILES_SLIQ_COLL_NAME = os.getenv("USERPROFILES_SLIQ_COLL_NAME", "sliq")
USERPROFILES_WHOQOL_COLL_NAME = os.getenv("USERPROFILES_WHOQOL_COLL_NAME", "whoqol")

# ----------------------------
# Redis (5 seconds cache for Step4 only, keyed by text_sig)
# ----------------------------
REDIS_URL = os.getenv("REDIS_URL", "redis://127.0.0.1:6379/0").strip()
RECO_REDIS_TTL_SECONDS = int(os.getenv("RECO_REDIS_TTL_SECONDS", "300"))
RECO_REDIS_KEY_PREFIX = os.getenv("RECO_REDIS_KEY_PREFIX", "w3:reco:").strip() or "w3:reco:"

_redis_client: Optional[redis.Redis] = None


def _get_redis_client() -> Optional[redis.Redis]:
    global _redis_client
    if not REDIS_URL:
        return None
    if _redis_client is None:
        _redis_client = redis.from_url(REDIS_URL, decode_responses=True)
    return _redis_client


# ----------------------------
# Theory enum (matches /theories/prompt)
# ----------------------------
class TheoryName(str, Enum):
    COMB = "COM-B"
    TTM = "TTM"
    SCT = "SCT"


# ----------------------------
# Request model (leave positions)
# ----------------------------



class RecommendIn(BaseModel):
    text: str = Field(min_length=1, max_length=5000)

    # behavior change theory chosen by user
    theory_name: Optional[TheoryName] = None



class RecommendCommentIn(BaseModel):
    request_uuid: str = Field(min_length=8, max_length=80)
    text: str = Field(min_length=1, max_length=5000)
    text_signature: str = Field(min_length=40, max_length=40)  # sha1 hex
    comment: str = Field(min_length=1, max_length=4000)


class RecommendCommentOut(BaseModel):
    ok: bool = True
    data: Dict[str, Any] = Field(default_factory=dict)

# ----------------------------
# Step1 output model (matches /profiles/build)
# ----------------------------
class ProfilesBuildOut(BaseModel):
    request_uuid: str
    text: str
    llm_meta: Dict[str, Any] = Field(default_factory=dict)
    profile_detailed: str = ""
    profile_summary: str = ""
    profiles_snapshot_meta: Dict[str, Any] = Field(default_factory=dict)
    signatures: Dict[str, str] = Field(default_factory=dict)


# ----------------------------
# Step2 output model (matches /habit_db/select)
# ----------------------------
class SelectedHabitOut(BaseModel):
    habit: str
    habit_key: str
    score: confloat(ge=0.0, le=1.0)
    reason: str = ""
    contexts: list[Any] = Field(default_factory=list)


class HabitDBSelectOut(BaseModel):
    request_uuid: str
    text: str
    llm_meta: Dict[str, Any] = Field(default_factory=dict)
    selected_habits: list[SelectedHabitOut] = Field(default_factory=list)
    selected_habits_summary: str = ""
    signatures: Dict[str, str] = Field(default_factory=dict)


# ----------------------------
# Step0 theory prompt models (same as your /theories/prompt output)
# ----------------------------
class TheoryPromptOut(BaseModel):
    request_uuid: str
    theory_name: str
    display_name: str
    prompt: str
    allowed_theories: list[str] = Field(default_factory=list)


# ----------------------------
# Step3 KB query models (matches /kb/query output)
# ----------------------------
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

    top_n: int
    score_threshold: float

    collection: str
    embed_provider: str
    embed_model: str
    embed_dim: int

    kb_root: str
    kb_changed: bool
    kb_signature: str
    last_sync_at: str

    hits: list[KbHit] = Field(default_factory=list)


# ============================================================
# Helpers (shared)
# ============================================================
def _normalize_text(s: str) -> str:
    s = unicodedata.normalize("NFC", s).strip()
    return re.sub(r"\s+", " ", s)


def _sha1(s: str) -> str:
    return hashlib.sha1(s.encode("utf-8")).hexdigest()


def _iso_utc_now() -> str:
    return datetime.utcnow().isoformat() + "Z"


def _build_kb_query_text(user_text: str, profile_summary: str) -> str:
    clean = _normalize_text(user_text)
    ps = (profile_summary or "").strip()
    return f"USER_TEXT:\n{clean}\n\nPROFILE_SUMMARY:\n{ps}\n"


# ----------------------------
# Step1 env signature (profiles)
# ----------------------------
def _get_env_value(key: str) -> str:
    v = os.getenv(key, "")
    if v == "":
        v = os.getenv(key.upper(), "")
    return v


def _profiles_env_signature() -> str:
    keys = [
        "Profiles_LLM_PROVIDER",
        "Profiles_LLM_MODEL",
        "Profiles_LLM_TEMPERATURE",
        "Profiles_LLM_MAX_TOKENS",
        "Profiles_TOP_K",
    ]
    snap = {k: _get_env_value(k) for k in keys}
    payload = json.dumps(snap, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return _sha1(payload)


# ----------------------------
# Step2 env signature (habit_db/select) - MUST match API-service exactly
# IMPORTANT: API-service uses os.getenv(k,"") WITHOUT upper fallback.
# So we must ensure these exact keys are present in os.environ.
# ----------------------------
def _habit_db_select_env_signature() -> str:
    keys = [
        "HABIT_DB_SELECT_LLM_PROVIDER",
        "HABIT_DB_SELECT_LLM_MODEL",
        "HABIT_DB_SELECT_LLM_TEMPERATURE",
        "HABIT_DB_SELECT_LLM_MAX_TOKENS",
        "HABIT_DB_SELECT_TOP_K",
        "HABIT_DB_SELECT_CANDIDATE_LIMIT",
    ]
    snap = {k: os.getenv(k, "") for k in keys}
    payload = json.dumps(snap, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return _sha1(payload)


# ============================================================
# Load API-service .env (so changing .env affects next /recommend)
# We load BOTH Step1 + Step2 required keys into os.environ, overriding.
# ============================================================
def _infer_api_service_env_path() -> str:
    override = os.getenv("API_SERVICE_ENV_PATH", "").strip()
    if override:
        return override

    here = Path(__file__).resolve()
    root = here.parent.parent.parent  # .../HHH-service/apis -> .../Dip_Code_Jingting_Hua
    guessed = root / "API-service" / "src" / "openapi_server" / ".env"
    return str(guessed)


def _load_required_env_keys_from_file(env_path: str, required_keys: set[str]) -> None:
    """
    Parse .env file and override ONLY required_keys in os.environ.
    Case-insensitive matching, but write using canonical key names from required_keys.
    """
    p = Path(env_path)
    if not p.exists():
        return

    upper_to_canonical = {k.upper(): k for k in required_keys}

    for raw in p.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        k, v = line.split("=", 1)
        k = k.strip()
        v = v.strip()

        if len(v) >= 2 and ((v[0] == v[-1] == '"') or (v[0] == v[-1] == "'")):
            v = v[1:-1]

        ku = k.upper()
        if ku not in upper_to_canonical:
            continue

        canonical = upper_to_canonical[ku]
        os.environ[canonical] = v


def _load_api_service_env_for_workflow3() -> None:
    env_path = _infer_api_service_env_path()

    step1_keys = {
        "Profiles_LLM_PROVIDER",
        "Profiles_LLM_MODEL",
        "Profiles_LLM_TEMPERATURE",
        "Profiles_LLM_MAX_TOKENS",
        "Profiles_TOP_K",
    }
    step2_keys = {
        "HABIT_DB_SELECT_LLM_PROVIDER",
        "HABIT_DB_SELECT_LLM_MODEL",
        "HABIT_DB_SELECT_LLM_TEMPERATURE",
        "HABIT_DB_SELECT_LLM_MAX_TOKENS",
        "HABIT_DB_SELECT_TOP_K",
        "HABIT_DB_SELECT_CANDIDATE_LIMIT",
    }
    _load_required_env_keys_from_file(env_path, step1_keys | step2_keys)


# ============================================================
# Profiles snapshot/signature (SAME algorithm as profiles_build_api.py)
# ============================================================
async def _fetch_latest_doc(coll) -> Optional[Dict[str, Any]]:
    return await coll.find_one(
        {},
        sort=[("updated_at", -1), ("created_at", -1), ("_id", -1)],
    )


def _stable_data_string(name: str, data: Any) -> str:
    payload = json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return f"{name}={payload}"


async def build_profiles_snapshot(client: AsyncIOMotorClient) -> Tuple[str, str, Dict[str, Any]]:
    db = client[USERPROFILES_DB_NAME]
    basic_coll = db[USERPROFILES_BASIC_COLL_NAME]
    sliq_coll = db[USERPROFILES_SLIQ_COLL_NAME]
    whoqol_coll = db[USERPROFILES_WHOQOL_COLL_NAME]

    basic_doc = await _fetch_latest_doc(basic_coll)
    sliq_doc = await _fetch_latest_doc(sliq_coll)
    whoqol_doc = await _fetch_latest_doc(whoqol_coll)

    def pick_data(doc: Optional[Dict[str, Any]]) -> Any:
        if not doc:
            return None
        return doc.get("data", doc)

    basic_data = pick_data(basic_doc)
    sliq_data = pick_data(sliq_doc)
    whoqol_data = pick_data(whoqol_doc)

    parts = []
    if basic_data is not None:
        parts.append(_stable_data_string("basic", basic_data))
    if sliq_data is not None:
        parts.append(_stable_data_string("sliq", sliq_data))
    if whoqol_data is not None:
        parts.append(_stable_data_string("whoqol", whoqol_data))

    combined = "\n".join(parts)
    profiles_sig = _sha1(combined)

    meta = {
        "basic_present": basic_data is not None,
        "sliq_present": sliq_data is not None,
        "whoqol_present": whoqol_data is not None,
        "combined": combined,
        "combined_len": len(combined),
    }
    return profiles_sig, combined, meta


# ============================================================
# Mongo singleton (HHH-service cache DB)
# ============================================================
_mongo_client: Optional[AsyncIOMotorClient] = None


def _get_mongo_client() -> AsyncIOMotorClient:
    global _mongo_client
    if _mongo_client is None:
        _mongo_client = AsyncIOMotorClient(MONGO_URI)
    return _mongo_client


def _selected_user_info_coll():
    client = _get_mongo_client()
    return client[RECOMMEND_DB_NAME][SELECTED_USER_INFO_COLL_NAME]


def _selected_habits_coll():
    client = _get_mongo_client()
    return client[RECOMMEND_DB_NAME][SELECTED_HABITS_COLL_NAME]


def _theory_selections_coll():
    client = _get_mongo_client()
    return client[RECOMMEND_DB_NAME][THEORY_SELECTIONS_COLL_NAME]


def _kb_query_coll():
    client = _get_mongo_client()
    return client[RECOMMEND_DB_NAME][KB_QUERY_COLL_NAME]


def _reco_api_output_coll():
    client = _get_mongo_client()
    return client[RECOMMEND_DB_NAME][RECO_API_OUTPUT_COLL_NAME]


def _reco_comments_coll():
    client = _get_mongo_client()
    return client[RECOMMEND_DB_NAME][RECO_COMMENTS_COLL_NAME]

# ============================================================
# Step2: import API-service "same algorithm" for habit_db_signature
# (so signature matches /habit_db/select output exactly)
# ============================================================
_api_service_imported = False
_build_habit_db_snapshot = None
_HABITS_COLL = None
_CONTEXTS_COLL = None
_CONTEXT_MAPPINGS_COLL = None


def _ensure_api_service_imports():
    global _api_service_imported, _build_habit_db_snapshot, _HABITS_COLL, _CONTEXTS_COLL, _CONTEXT_MAPPINGS_COLL

    if _api_service_imported:
        return

    here = Path(__file__).resolve()
    root = here.parent.parent.parent
    api_src = root / "API-service" / "src"
    if not api_src.exists():
        raise RuntimeError(f"API-service src not found at: {api_src}")

    import sys

    if str(api_src) not in sys.path:
        sys.path.insert(0, str(api_src))

    from openapi_server.services.habit_db_state_service import build_habit_db_snapshot  # type: ignore
    from openapi_server.infra.mongo import (  # type: ignore
        HABITS_COLL,
        CONTEXTS_COLL,
        CONTEXT_MAPPINGS_COLL,
    )

    _build_habit_db_snapshot = build_habit_db_snapshot
    _HABITS_COLL = HABITS_COLL
    _CONTEXTS_COLL = CONTEXTS_COLL
    _CONTEXT_MAPPINGS_COLL = CONTEXT_MAPPINGS_COLL
    _api_service_imported = True


async def _compute_habit_db_signature_same_as_api() -> str:
    _ensure_api_service_imports()
    habit_db_sig, _habits_list = await _build_habit_db_snapshot(  # type: ignore
        _HABITS_COLL, _CONTEXTS_COLL, _CONTEXT_MAPPINGS_COLL, only_habits=True  # type: ignore
    )
    return habit_db_sig


# ============================================================
# HTTP callers
# ============================================================
def _post_json(url: str, payload: Dict[str, Any], timeout: int = 120) -> Dict[str, Any]:
    resp = requests.post(url, json=payload, timeout=timeout)
    if resp.status_code != 200:
        raise RuntimeError(f"POST failed: {resp.status_code} {resp.text}")
    return resp.json()


# ============================================================
# Step4 adapter: build API-service /recommend input
# (A) profile_detailed -> profile_summary field (name unchanged)
# ============================================================
CONTEXT_LABELS_STEP4: Tuple[str, ...] = (
    "TIME",
    "PHYSICAL SETTING",
    "PRIOR BEHAVIOR",
    "OTHER PEOPLE",
    "INTERNAL STATE",
    "BEHAVIOR",
    "REASONING",
)


def _norm_opt_str(v: Any) -> Optional[str]:
    if v is None:
        return None
    if isinstance(v, str):
        s = v.strip()
        return s if s else None
    s = str(v).strip()
    return s if s else None


def _coerce_contexts_to_list7(contexts: Any) -> List[Optional[str]]:
    """
    API-service expects: List[Optional[str]] in fixed 7-label order.
    We accept common shapes from HabitDBSelectOut and coerce safely.
    """
    # dict: {"TIME": "...", ...}
    if isinstance(contexts, dict):
        m = {str(k).strip().upper(): contexts[k] for k in contexts.keys()}
        out = [_norm_opt_str(m.get(lab.upper())) for lab in CONTEXT_LABELS_STEP4]
        return out

    # list: either ["...", None, ...] or [{"name":"TIME","value":"..."}, ...]
    if isinstance(contexts, list):
        # already list[str|None]
        if all((x is None or isinstance(x, str)) for x in contexts):
            out0 = [(_norm_opt_str(x) if x is not None else None) for x in contexts]
            out = (out0 + [None] * 7)[:7]
            return out

        # list[dict]
        if all(isinstance(x, dict) for x in contexts):
            m: Dict[str, Any] = {}
            for it in contexts:
                name = it.get("name") or it.get("label") or it.get("type")
                val = it.get("value") or it.get("text") or it.get("phrase")
                if isinstance(name, str) and name.strip():
                    m[name.strip().upper()] = val
            out = [_norm_opt_str(m.get(lab.upper())) for lab in CONTEXT_LABELS_STEP4]
            return out

        # fallback: stringify items
        out0 = [_norm_opt_str(x) for x in contexts]
        out = (out0 + [None] * 7)[:7]
        return out

    # unknown
    return [None] * 7


def _coerce_selected_habits_for_step4(selected_habits: Any) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    if not isinstance(selected_habits, list):
        return out
    for h in selected_habits:
        if not isinstance(h, dict):
            continue
        out.append(
            {
                "habit": h.get("habit"),
                "habit_key": h.get("habit_key"),
                "score": h.get("score"),
                "reason": h.get("reason"),
                "contexts": _coerce_contexts_to_list7(h.get("contexts")),
            }
        )
    return out


def _coerce_rag_hits_for_step4(kb_hits: Any) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    if not isinstance(kb_hits, list):
        return out
    for h in kb_hits:
        if not isinstance(h, dict):
            continue
        out.append(
            {
                "score": h.get("score"),
                "doc_id": h.get("doc_id"),
                "domain": h.get("domain"),
                "chunk_id": h.get("chunk_id"),
                "page_number": h.get("page_number"),
                "doc_title": h.get("doc_title"),
                "text": h.get("text"),
            }
        )
    return out


def _patch_step4_output_for_current_request(api_out: Dict[str, Any], request_uuid: str) -> Dict[str, Any]:
    """
    Redis cache is keyed by text_sig, but workflow ALWAYS uses a new request_uuid.
    So we patch request_uuid + created_at to current values before returning/storing.
    """
    out = dict(api_out)
    out["request_uuid"] = request_uuid
    out["created_at"] = _iso_utc_now()
    return out


# ============================================================
# /recommend (Workflow3 = Step0 + Step1 + Step2 + Step3 + Step4)
# Return dict: { api_name: api_output }
# ============================================================
@router.post(
    "/recommend",
    response_model=Dict[str, Any],
    summary=(
        "Workflow3: Step0 theories/prompt (no cache) + "
        "Step1 profiles/build cached + Step2 habit_db/select cached + "
        "Step3 kb/query (no cache, store output) + "
        "Step4 recommend (API-service /recommend, Redis 5s by text_sig, store output)"
    ),
)
async def recommend(payload: RecommendIn) -> Dict[str, Any]:
    # ALWAYS new request_uuid
    request_uuid = str(uuid.uuid4())

    # shared signatures
    clean_text = _normalize_text(payload.text)
    text_sig = _sha1(clean_text)

    def _strip_id(d: Dict[str, Any]) -> Dict[str, Any]:
        out = dict(d)
        out.pop("_id", None)
        return out

    # Load API-service .env keys every request (so edits invalidate cache)
    _load_api_service_env_for_workflow3()

    # =========================================================
    # STEP 0) /theories/prompt (NO cache) + store selection per request_uuid
    # =========================================================
    def _call_theory_prompt() -> Dict[str, Any]:
        body = {
            "request_uuid": request_uuid,
            "theory_name": payload.theory_name.value if payload.theory_name is not None else None,
        }
        return _post_json(f"{API_BASE}/theories/prompt", body, timeout=30)

    try:
        theory_out_raw = await run_in_threadpool(_call_theory_prompt)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"theories/prompt failed: {e}")

    try:
        theory_out = TheoryPromptOut(**theory_out_raw).model_dump()
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"theories/prompt output invalid: {e}")

    # store every request_uuid selection (NO cache)
    try:
        await _theory_selections_coll().insert_one(
            {
                "_id": request_uuid,
                "created_at": _iso_utc_now(),
                "request_uuid": request_uuid,
                "text_signature": text_sig,
                "input_theory_name": payload.theory_name.value if payload.theory_name is not None else None,
                "resolved_theory_name": theory_out.get("theory_name"),
                "prompt": theory_out.get("prompt"),
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to store theory selection: {e}")

    # =========================================================
    # STEP 1) /profiles/build (cached)
    # =========================================================
    profiles_env_sig = _profiles_env_signature()

    client = _get_mongo_client()
    try:
        profiles_sig, _, _ = await build_profiles_snapshot(client)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=(
                "Failed to compute profiles_signature from MongoDB. "
                "Check USERPROFILES_DB_NAME / *_COLL_NAME. "
                f"Error: {e}"
            ),
        )

    profiles_coll = _selected_user_info_coll()
    doc1 = await profiles_coll.find_one({"_id": text_sig})

    step1_out: Dict[str, Any]
    if doc1:
        sigs = doc1.get("signatures") or {}
        if (
            sigs.get("text_signature") == text_sig
            and sigs.get("profiles_signature") == profiles_sig
            and sigs.get("profiles_env_signature") == profiles_env_sig
        ):
            await profiles_coll.update_one({"_id": text_sig}, {"$set": {"request_uuid": request_uuid}})
            doc1["request_uuid"] = request_uuid
            step1_out = _strip_id(doc1)
        else:
            doc1 = None

    if not doc1:

        def _call_profiles_build() -> Dict[str, Any]:
            return _post_json(
                f"{API_BASE}/profiles/build",
                {"request_uuid": request_uuid, "text": payload.text},
                timeout=120,
            )

        try:
            api_out = await run_in_threadpool(_call_profiles_build)
        except Exception as e:
            raise HTTPException(status_code=502, detail=str(e))

        _ = ProfilesBuildOut(**api_out)
        await profiles_coll.replace_one({"_id": text_sig}, {"_id": text_sig, **api_out}, upsert=True)
        step1_out = api_out

    # =========================================================
    # STEP 2) /habit_db/select (cached) + signatures computed in HHH-service
    # =========================================================
    habit_env_sig = _habit_db_select_env_signature()
    try:
        habit_db_sig = await _compute_habit_db_signature_same_as_api()
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to compute habit_db_signature in HHH-service (import/call API-service code). Error: {e}",
        )

    habits_coll = _selected_habits_coll()
    doc2 = await habits_coll.find_one({"_id": text_sig})

    step2_out: Dict[str, Any]
    if doc2:
        sigs = doc2.get("signatures") or {}
        if (
            sigs.get("text_signature") == text_sig
            and sigs.get("habit_db_signature") == habit_db_sig
            and sigs.get("env_signature") == habit_env_sig
        ):
            await habits_coll.update_one({"_id": text_sig}, {"$set": {"request_uuid": request_uuid}})
            doc2["request_uuid"] = request_uuid
            step2_out = _strip_id(doc2)
        else:
            doc2 = None

    if not doc2:

        def _call_habit_db_select() -> Dict[str, Any]:
            return _post_json(
                f"{API_BASE}/habit_db/select",
                {"request_uuid": request_uuid, "text": payload.text},
                timeout=120,
            )

        try:
            api_out = await run_in_threadpool(_call_habit_db_select)
        except Exception as e:
            raise HTTPException(status_code=502, detail=str(e))

        _ = HabitDBSelectOut(**api_out)
        await habits_coll.replace_one({"_id": text_sig}, {"_id": text_sig, **api_out}, upsert=True)
        step2_out = api_out

    # =========================================================
    # STEP 3) /kb/query (NO cache) + store KbQueryOut per request_uuid
    # text := USER_TEXT + PROFILE_SUMMARY
    # =========================================================
    kb_query_text = _build_kb_query_text(payload.text, step1_out.get("profile_summary", ""))

    def _call_kb_query() -> Dict[str, Any]:
        return _post_json(
            f"{API_BASE}/kb/query",
            {"request_uuid": request_uuid, "text": kb_query_text},
            timeout=120,
        )

    try:
        kb_out_raw = await run_in_threadpool(_call_kb_query)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"kb/query failed: {e}")

    try:
        kb_out = KbQueryOut(**kb_out_raw).model_dump()
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"kb/query output invalid: {e}")

    # store ONLY api output (no extra fields), with Mongo _id=request_uuid
    try:
        await _kb_query_coll().insert_one({"_id": request_uuid, **kb_out_raw})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to store kb_query: {e}")

    # =========================================================
    # STEP 4) API-service /recommend (Redis 5s by text_sig)
    # Inputs:
    #   - theory_prompt.prompt
    #   - profiles_build.profile_detailed  -> profile_summary field (as you requested)
    #   - habit_db_select.selected_habits
    #   - kb_query.hits -> rag_hits
    # Store output into new coll; workflow return includes new key.
    # =========================================================
    redis_client = _get_redis_client()
    redis_key = f"{RECO_REDIS_KEY_PREFIX}{text_sig}"

    cached_raw: Optional[str] = None
    if redis_client is not None:
        try:
            cached_raw = await redis_client.get(redis_key)
        except Exception:
            cached_raw = None  # redis is optional in runtime; do not break workflow

    reco_out_raw: Dict[str, Any]

    if cached_raw:
        try:
            cached_obj = json.loads(cached_raw)
            if isinstance(cached_obj, dict):
                reco_out_raw = _patch_step4_output_for_current_request(cached_obj, request_uuid)
            else:
                cached_raw = None
        except Exception:
            cached_raw = None

    if not cached_raw:
        # Build Step4 input payload
        step4_payload: Dict[str, Any] = {
            "request_uuid": request_uuid,
            "text": payload.text,
            # (A) profile_detailed -> profile_summary field
            "profile_summary": step1_out.get("profile_detailed", "") or "",
            "theory": {
                "theory_name": theory_out.get("theory_name"),
                "prompt": theory_out.get("prompt"),
            },
            "selected_habits": _coerce_selected_habits_for_step4(step2_out.get("selected_habits", [])),
            "rag_hits": _coerce_rag_hits_for_step4(kb_out.get("hits", [])),
            # keep default max_prompt_chars in API-service unless you want to override:
            # "max_prompt_chars": 45000,
        }

        def _call_reco_api() -> Dict[str, Any]:
            # API-service endpoint is /recommend (NOT the workflow endpoint; different service host/port)
            return _post_json(f"{API_BASE}/recommend", step4_payload, timeout=180)

        try:
            api_out = await run_in_threadpool(_call_reco_api)
        except Exception as e:
            raise HTTPException(status_code=502, detail=f"API /recommend failed: {e}")

        if not isinstance(api_out, dict):
            raise HTTPException(status_code=502, detail="API /recommend returned non-object JSON.")

        reco_out_raw = api_out

        # Write to redis (5s)
        if redis_client is not None:
            try:
                await redis_client.set(
                    redis_key,
                    json.dumps(reco_out_raw, ensure_ascii=False, separators=(",", ":")),
                    ex=RECO_REDIS_TTL_SECONDS,
                )
            except Exception:
                pass

    # Store ONLY api output (no extra fields), with Mongo _id=request_uuid
    try:
        await _reco_api_output_coll().insert_one({"_id": request_uuid, **reco_out_raw})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to store reco_api_output: {e}")

    # =========================================================
    # FINAL: dict keyed by each module/API
    # =========================================================
    return {
        "theory_prompt": theory_out,
        "profiles_build": step1_out,
        "habit_db_select": step2_out,
        "kb_query": kb_out,
        "recommendation": reco_out_raw,  # NEW
    }

from pymongo.errors import DuplicateKeyError

@router.post(
    "/recommend/comment",
    response_model=RecommendCommentOut,
    summary="Workflow3: Store a user comment for a recommendation request (strict, one-time only)",
)
async def recommend_comment(payload: RecommendCommentIn) -> RecommendCommentOut:
    # 0) validate request_uuid
    req_id = (payload.request_uuid or "").strip()
    if not req_id:
        raise HTTPException(
            status_code=422,
            detail={"error": "INVALID_REQUEST_UUID", "message": "request_uuid is empty."},
        )

    # 1) validate comment (non-empty)
    comment_clean = _normalize_text(payload.comment)
    if not comment_clean:
        raise HTTPException(
            status_code=422,
            detail={"error": "EMPTY_COMMENT", "message": "comment is empty after normalization."},
        )

    # 2) verify signature
    clean_text = _normalize_text(payload.text)
    expected_sig = _sha1(clean_text)
    if expected_sig != payload.text_signature:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "TEXT_SIGNATURE_MISMATCH",
                "message": "text_signature does not match sha1(normalized text).",
                "hint": [
                    "Use signatures.text_signature returned by /recommend (Step1/Step2).",
                    "Or compute sha1(_normalize_text(text)) consistently.",
                ],
            },
        )

    created_at = _iso_utc_now()

    # 3) build doc (stable comment id == request_uuid)
    doc = {
        "_id": req_id,                 # <- stable ID; makes it one-time only
        "created_at": created_at,
        "request_uuid": req_id,
        "text": payload.text,
        "text_signature": payload.text_signature,
        "comment": comment_clean,
    }

    # 4) insert (strict one-time)
    try:
        await _reco_comments_coll().insert_one(doc)
    except DuplicateKeyError:
        raise HTTPException(
            status_code=409,
            detail={
                "error": "COMMENT_ALREADY_EXISTS",
                "message": "A comment for this request_uuid already exists (one-time only).",
                "hint": [
                    "Do not submit twice for the same request_uuid.",
                    "If you want editing, change backend to upsert/replace_one().",
                ],
            },
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to store recommendation comment: {e}")

    # 5) return itself
    return RecommendCommentOut(
        ok=True,
        data={
            "created_at": created_at,
            "request_uuid": req_id,
            "text": payload.text,
            "text_signature": payload.text_signature,
            "comment": comment_clean,
        },
    )



from fastapi import Query
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

class RecommendationLatestItem(BaseModel):
    text_signature: str
    request_uuid: str
    updated_at: Optional[str] = None

    text: str = ""
    profile_summary: str = ""
    selected_habits: List[Dict[str, Any]] = Field(default_factory=list)

    recommendation_text: str = ""
    llm_meta: Dict[str, Any] = Field(default_factory=dict)
    rag_assessment: Dict[str, Any] = Field(default_factory=dict)
    used_evidence_rag: List[Dict[str, Any]] = Field(default_factory=list)

    comment: Optional[str] = None
    theory_name: Optional[str] = None


class RecommendationLatestOut(BaseModel):
    ok: bool = True
    total: int = 0
    items: List[RecommendationLatestItem] = Field(default_factory=list)


@router.get(
    "/recommend/history/latest",
    response_model=RecommendationLatestOut,
    summary="History (dedup by text_signature): latest recommendation per text",
)
async def recommend_history_latest(
    limit: int = Query(50, ge=1, le=200),
    skip: int = Query(0, ge=0),
) -> RecommendationLatestOut:
    habits_coll = _selected_habits_coll()          # _id=text_sig, request_uuid=latest
    profile_coll = _selected_user_info_coll()      # _id=text_sig
    reco_coll = _reco_api_output_coll()            # _id=request_uuid
    comments_coll = _reco_comments_coll()          # _id=request_uuid
    theory_coll = _theory_selections_coll()        # _id=request_uuid

    total = await habits_coll.count_documents({})

    cursor = (
        habits_coll.find({}, projection={"_id": 1, "request_uuid": 1, "text": 1, "updated_at": 1, "selected_habits": 1})
        .sort("updated_at", -1)
        .skip(skip)
        .limit(limit)
    )
    habit_docs = await cursor.to_list(length=limit)

    items: List[RecommendationLatestItem] = []
    for hdoc in habit_docs:
        text_sig = hdoc.get("_id")
        req_id = (hdoc.get("request_uuid") or "").strip()
        if not text_sig or not req_id:
            continue

        prof = await profile_coll.find_one({"_id": text_sig}) or {}
        reco = await reco_coll.find_one({"_id": req_id}) or {}
        comm = await comments_coll.find_one({"_id": req_id}) or {}
        theo = await theory_coll.find_one({"_id": req_id}) or {}

        reco_reco = reco.get("recommendation") or {}
        used = (reco_reco.get("used_evidence") or {}) if isinstance(reco_reco, dict) else {}

        items.append(
            RecommendationLatestItem(
                text_signature=text_sig,
                request_uuid=req_id,
                updated_at=hdoc.get("updated_at"),
                text=hdoc.get("text", "") or prof.get("text", "") or "",
                profile_summary=prof.get("profile_summary", "") or "",
                selected_habits=hdoc.get("selected_habits", []) or [],
                recommendation_text=(reco_reco.get("recommendation_text", "") if isinstance(reco_reco, dict) else "") or "",
                llm_meta=reco.get("llm_meta") or {},
                rag_assessment=(reco_reco.get("rag_assessment") if isinstance(reco_reco, dict) else {}) or {},
                used_evidence_rag=(used.get("rag", []) if isinstance(used, dict) else []) or [],
                comment=comm.get("comment") if isinstance(comm, dict) else None,
                theory_name=(theo.get("resolved_theory_name") or theo.get("input_theory_name")),
            )
        )

    return RecommendationLatestOut(ok=True, total=total, items=items)
