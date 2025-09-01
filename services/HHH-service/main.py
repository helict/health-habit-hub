# services/HHH-service/main.py
import os
import uuid, re, unicodedata
import requests
import uvicorn
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
    allow_methods=["*"],  # 至少包含 POST, OPTIONS
    allow_headers=["*"],  # 至少包含 Content-Type
    allow_credentials=False,  # 若 True，就不能用 "*"，必须精确 Origin
)

API_BASE = os.getenv(
    "API_BASE_URL", "http://127.0.0.1:8080"
)  # 不加载 .env，只读系统环境变量

# ---- 复用连接池 ----
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
            timeout=(3, 20),
        )  # (连接超时, 总超时)
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
    # 统一全角、空格、大小写；压缩多余空白
    s = unicodedata.normalize("NFKC", txt).strip().lower()
    return re.sub(r"\s+", " ", s)


def make_sentence_uuid(sentence: str, language: str) -> str:
    name = f"{language}:{_normalize(sentence)}"
    return str(uuid.uuid5(uuid.NAMESPACE_URL, name))


# ------- seed：先生成 uuid，再转发到 API -------
@app.post("/seed", response_model=SeedOut, summary="最小 seed：不是习惯则提示重试")
def seed(body: SeedIn):
    # 1) 若前端没给 uuid，则基于内容生成稳定 uuid（想要随机则改成 str(uuid.uuid4())）
    uuid = make_sentence_uuid(body.habit, body.language)

    # 2) 调用 API-service 分类
    classify_habit_result = call_api_classify_habit(body.habit, body.language, uuid)

    # 3) 简单规则：不是习惯 → try again
    is_habit = int(classify_habit_result.get("habit_class", 0)) == 1
    if is_habit:
        
        classify_context_result = call_api_classify_context(
            body.habit, body.language, uuid
        )
        # 数据库存储相关习惯分类信息
        return SeedOut(ok=True, message="ok", data=classify_context_result)
    else:
        # 数据库存储相关上下文信息
        return SeedOut(
            ok=False,
            message="Not a habit. Please try again.",
            data=classify_habit_result,
        )


if __name__ == "__main__":
    # "main:app" 里的 main 指的是文件名 main.py
    uvicorn.run("main:app", port=8081, reload=True)
