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


def _normalize(txt: str) -> str:
    s = unicodedata.normalize("NFC", txt).strip().casefold()
    return re.sub(r"\s+", " ", s)

print(_normalize("Every morning after waking up, i drink a glass of warm water."))