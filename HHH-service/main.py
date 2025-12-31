# main.py
from __future__ import annotations

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from apis.workflow1_api import router as workflow1_router
from apis.workflow2_api import router as workflow2_router
from apis.system_api import router as system_router

WORKFLOW1_TAG = "Workflow1: Habitual structured collection workflow"
WORKFLOW2_TAG = "Workflow2: User Profile/Form Workflow "
WORKFLOW3_TAG = "Workflow3: Recommended workflow"
SYSTEM_TAG = "System"

OPENAPI_TAGS = [
    {
        "name": WORKFLOW1_TAG,
        "description": (
            "Collect user-inputted habitual phrases in a structured manner and complete the entire pipeline:"
            " habit detection → context extraction → BCIO mapping, and persist raw and enriched results;"
            " also provide habit management (list/detail query) interfaces."
        ),
    },
    {"name": WORKFLOW2_TAG, "description": "Form filling and user profile structuring module (reserved)."},
    {"name": WORKFLOW3_TAG, "description": "RAG-based recommendation system (reserved)."},
    {"name": SYSTEM_TAG, "description": "Perform API key/runtime status checks only"},
]

app = FastAPI(
    title="Workflow Orchestrator for Habit Recommendation System",
    description=(
        "This service is a workflow coordination (orchestration) layer of the Habit Recommendation System.\n\n"
        "Workflows:\n"
        f"1) {WORKFLOW1_TAG}: habit ingestion + structuring (habit detection → context extraction → BCIO mapping)\n"
        f"2) {WORKFLOW2_TAG}: form-based user profiling (reserved)\n"
        f"3) {WORKFLOW3_TAG}: RAG-based recommendation generation (reserved)\n\n"
        "This service orchestrates upstream API-service calls and persists business data in MongoDB.\n"
    ),
    version="0.1.0",
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
app.include_router(system_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8081, reload=True)
