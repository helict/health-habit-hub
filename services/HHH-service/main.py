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

app = FastAPI(title="HHH Seed Service", version="1.0.0")

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

# ---- Motor（异步 MongoDB；最小改动，仅全局创建一次）----
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://127.0.0.1:27017/HabitDB")
MONGO = AsyncIOMotorClient(MONGODB_URI, serverSelectionTimeoutMS=2000)
DB = MONGO.get_default_database()
HABITS_COLL = DB.get_collection("habits")  # 只存 HabitOut（habit_class、confidence 等）
CONTEXTS_COLL = DB.get_collection("contexts")  # 只存 ClassifyContextOut（result 列表）

# ---- 复用连接池（同步 HTTP）----
SESSION = requests.Session()


# -------- Pydantic I/O 模型（与你现有一致）--------
class SeedIn(BaseModel):
    habit: str
    language: str = "en"


class SeedOut(BaseModel):
    ok: bool
    message: str
    data: dict


# ------- 上游 API（保持同步 requests，用线程池避免阻塞）-------
def call_api_classify_habit(habit: str, language: str, uuid_str: str) -> dict:
    url = f"{API_BASE}/classify_habit"
    try:
        r = SESSION.post(
            url,
            json={"uuid": uuid_str, "habit": habit, "language": language},
            timeout=(3, 20),
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
            timeout=(3, 20),
        )
        r.raise_for_status()
        return r.json()
    except requests.RequestException as e:
        raise HTTPException(
            status_code=502, detail=f"classify_context upstream error: {e}"
        )


# ------- 生成稳定 UUID（基于句子+语言）-------
def _normalize(txt: str) -> str:
    s = unicodedata.normalize("NFC", txt).strip()
    return re.sub(r"\s+", " ", s)


def make_sentence_uuid(sentence: str, language: str) -> str:
    name = f"{language}:{_normalize(sentence)}"
    return str(uuid.uuid5(uuid.NAMESPACE_URL, name))


# ------- 存储方法 -------
async def store_habit_data(habit_data: dict) -> bool:
    """
    将习惯数据存储到habits集合中
    """
    try:
        # 构建更新文档
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
        
        # 执行更新操作
        await HABITS_COLL.update_one(
            {"uuid": habit_data.get("uuid")},
            update_doc,
            upsert=True
        )
        return True
    except Exception as e:
        print(f"存储习惯数据失败 (UUID: {habit_data.get('uuid')}): {e}")
        return False


async def store_context_data(context_data: dict) -> bool:
    """
    将上下文数据存储到contexts集合中
    """
    try:
        # 构建更新文档
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
        
        # 执行更新操作
        await CONTEXTS_COLL.update_one(
            {"uuid": context_data.get("uuid")},
            update_doc,
            upsert=True
        )
        return True
    except Exception as e:
        print(f"存储上下文数据失败 (UUID: {context_data.get('uuid')}): {e}")
        return False


# ------- seed：调用上游并分别写两个集合 -------
@app.post("/seed", response_model=SeedOut, summary="最小 seed：不是习惯则提示重试")
async def seed(body: SeedIn):
    # 1) 若前端没给 uuid，则基于内容生成稳定 uuid（想要随机则改成 str(uuid.uuid4())）
    uuid_str = make_sentence_uuid(body.habit, body.language)
    clean_habit=_normalize(body.habit)
    # 2) 调用 API-service（habit 分类）
    habit_out = await run_in_threadpool(
        lambda: call_api_classify_habit(clean_habit, body.language, uuid_str)
    )


    is_habit = int(habit_out.get("habit_class", 0)) == 1

    # ---- 始终把 HabitOut 存到 habits 集合（无论 0/1）----
    success = await store_habit_data(habit_out)
    if not success:
        print(f"警告: 习惯数据存储失败 (UUID: {uuid_str})")

    if is_habit:
        # 3) 是习惯 → 调用 API-service（context 分类）
        context_out = await run_in_threadpool(
            lambda: call_api_classify_context(clean_habit, body.language, uuid_str)
        )
        # print(f"上游API响应: {context_out}")  # 添加这行来调试
        # 4) ClassifyContextOut 写入 contexts 集合
        success = await store_context_data(context_out)
        if not success:
            print(f"警告: 上下文数据存储失败 (UUID: {uuid_str})")

        # 返回 context 结果
        return SeedOut(ok=True, message="ok", data=context_out)

    # 5) 非习惯：只返回 HabitOut（已写入 habits）
    return SeedOut(
        ok=False,
        message="Not a habit. Please try again.",
        data=habit_out,
    )


if __name__ == "__main__":
    # "main:app" 里的 main 指的是文件名 main.py
    uvicorn.run("main:app", port=8081, reload=True)