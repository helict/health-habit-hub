from __future__ import annotations

# coding: utf-8
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, APIRouter

# BASE_DIR = Path(__file__).resolve().parent
# load_dotenv(BASE_DIR / ".env", override=False)

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from apis.workflow1_api import router as workflow1_router
from apis.workflow2_api import router as workflow2_router
from apis.workflow3_api import router as workflow3_router

WORKFLOW1_TAG = "Workflow 1: Habitual structured collection"
WORKFLOW2_TAG = "Workflow 2: User form completion"
WORKFLOW3_TAG = "Workflow 3: Habit Recommendation"


OPENAPI_TAGS = [
    {
        "name": WORKFLOW1_TAG,
        "description": (
            "Workflow 1 completed: habit donation is implemented, and two additional APIs for displaying habits in the front end have been added."
        ),
    },
    {"name": WORKFLOW2_TAG, "description": "Workflow 2 completed: users can fill in and update form data at any time."},
    {"name": WORKFLOW3_TAG, "description": "Workflow 3 completed: users can obtain recommendations at any time, provide explicit feedback, and regenerate recommendations based on that feedback, forming a feedback loop."},
]

app = FastAPI(
    title="Workflow Orchestrator for Habit Recommendation System",
    description=(
        "This service is a workflow coordination (orchestration) layer of the Habit Recommendation System.\n\n"
        "Directly call the various APIs provided by the API service; the APIs in this layer interact directly with the front end.\n\n"
    ),
    version="1.0.0",
    openapi_tags=OPENAPI_TAGS,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=False,
)

app.include_router(workflow1_router)
app.include_router(workflow2_router)
app.include_router(workflow3_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8081, reload=True)
