from pathlib import Path
import os
from dotenv import load_dotenv
# 1) 加载 .env（使用绝对路径更稳）
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles  # 若未用到可删
from routers.classify_habit import app01
from routers.classify_context import app02
import uvicorn

app = FastAPI()


@app.get("/health")
def health():
    return {
        "status": "ok",
        "openai_key_loaded": bool(os.getenv("OPENAI_API_KEY")),
        "scads_key_loaded": bool(os.getenv("SCADS_API_KEY")),
    }

app.include_router(app01, prefix="/classify_habit",tags=["判断是否是习惯"])

app.include_router(app02, prefix="/classify_context",tags=["判断习惯的上下文"])

if __name__ == "__main__":
    # "main:app" 里的 main 指的是文件名 main.py
    uvicorn.run("main:app", port=8080, reload=True)
