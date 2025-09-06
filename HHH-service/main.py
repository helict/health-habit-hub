from inspect import cleandoc
import os
import uuid, re, unicodedata
import requests
import uvicorn
from datetime import datetime, timezone
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi.concurrency import run_in_threadpool

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="HHH Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=False,
)

API_BASE = os.getenv("API_BASE_URL", "http://127.0.0.1:8080")

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://127.0.0.1:27017/HabitDB")
MONGO = AsyncIOMotorClient(MONGODB_URI, serverSelectionTimeoutMS=2000)
DB = MONGO.get_default_database()
HABITS_COLL = DB.get_collection("habits")
CONTEXTS_COLL = DB.get_collection("contexts")

SESSION = requests.Session()


class SeedIn(BaseModel):
    habit: str
    language: str = "en"


class SeedOut(BaseModel):
    ok: bool
    message: str
    data: dict


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
        raise HTTPException(
            status_code=502, detail=f"classify_habit upstream error: {e}"
        )


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
        raise HTTPException(
            status_code=502, detail=f"classify_context upstream error: {e}"
        )


def _normalize(txt: str) -> str:
    s = unicodedata.normalize("NFC", txt).strip()
    return re.sub(r"\s+", " ", s)


def make_sentence_uuid(sentence: str, language: str) -> str:
    name = f"{language}:{_normalize(sentence)}"
    return str(uuid.uuid5(uuid.NAMESPACE_URL, name))


async def store_habit_data(habit_data: dict) -> bool:
    try:
        update_doc = {
            "$setOnInsert": {
                "uuid": habit_data.get("uuid"),
            },
            "$set": {
                "habit": habit_data.get("habit"),
                "language": habit_data.get("language"),
                "habit_class": habit_data.get("habit_class", 0),
                "confidence": habit_data.get("confidence", None),
            }
        }
        
        await HABITS_COLL.update_one(
            {"uuid": habit_data.get("uuid")},
            update_doc,
            upsert=True
        )
        return True
    except Exception as e:
        print(f"Failed to store habit data (UUID: {habit_data.get('uuid')}): {e}")
        return False


async def store_context_data(context_data: dict) -> bool:
    try:
        update_doc = {
            "$setOnInsert": {
                "uuid": context_data.get("uuid"),
            },
            "$set": {
                "habit": context_data.get("habit"),
                "language": context_data.get("language"),
                "result": context_data.get("result", []),
            }
        }
        await CONTEXTS_COLL.update_one(
            {"uuid": context_data.get("uuid")},
            update_doc,
            upsert=True
        )
        return True
    except Exception as e:
        print(f"Failed to store context data (UUID: {context_data.get('uuid')}): {e}")
        return False


@app.post("/seed", response_model=SeedOut, summary="Minimum seed: If it is not a habit, prompt to try again")
async def seed(body: SeedIn):
    uuid_str = make_sentence_uuid(body.habit, body.language)
    clean_habit=_normalize(body.habit)
    habit_out = await run_in_threadpool(
        lambda: call_api_classify_habit(clean_habit, body.language, uuid_str)
    )


    is_habit = int(habit_out.get("habit_class", 0)) == 1

    success = await store_habit_data(habit_out)
    if not success:
        print(f"Warning: Custom data storage failed (UUID: {uuid_str})")

    if is_habit:
        context_out = await run_in_threadpool(
            lambda: call_api_classify_context(clean_habit, body.language, uuid_str)
        )
        success = await store_context_data(context_out)
        if not success:
            print(f"Warning: Context data storage failed (UUID: {uuid_str})")
        return SeedOut(ok=True, message="ok", data=context_out)

    return SeedOut(
        ok=False,
        message="Not a habit. Please try again.",
        data=habit_out,
    )


if __name__ == "__main__":
    uvicorn.run("main:app", port=8081, reload=True)