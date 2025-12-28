# coding: utf-8
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, APIRouter

# Load .env
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

# --- Import generated routers ---
from openapi_server.apis.classify_habit_api import router as ClassifyHabitApiRouter
from openapi_server.apis.classify_context_api import router as ClassifyContextApiRouter
from openapi_server.apis.bcio_mapping_api import router as BcioMappingApiRouter
from openapi_server.apis.system_api import router as SystemApiRouter

# --- Import KB query router (your Workflow3 module) ---
from openapi_server.apis.kb_query_api import router as KbQueryRouter

WORKFLOW1_TAG = "Workflow1: Habitual structured collection workflow"
WORKFLOW2_TAG = "Workflow2: User Profile/Form Workflow"
WORKFLOW3_TAG = "Workflow3: Recommended workflow"
SYSTEM_TAG = "System: API Key / Health Check"


def force_single_tag(router: APIRouter, tag: str) -> None:
    """Overwrite tags on every route so Swagger groups exactly as we want."""
    for r in router.routes:
        if hasattr(r, "tags"):
            r.tags = [tag]  # overwrite (not append)


app = FastAPI(
    title="Habit Recommendation System API",
    description=(
        "A modular API for a Habit Recommendation System. "
        "Workflow1: habit detection, context extraction, BCIO mapping. "
        "Workflow2: user profiling and form handling. "
        "Workflow3: Based on user profiles, a knowledge-based knowledge base, and a framework for changing user choices, a multi-LLMs recommendation workflow enhanced by RAG is presented."
    ),
    version="1.0.2",
    openapi_tags=[
        {"name": WORKFLOW1_TAG, "description": "Habitual structured collection, context extraction, BCIO mapping"},
        {"name": WORKFLOW2_TAG, "description": "User profiling/form-related workflow"},
        {"name": WORKFLOW3_TAG, "description": "Workflow for habit recommendation based on knowledge base"},
        {"name": SYSTEM_TAG, "description": "Perform API key/runtime status checks only"},
    ],
)

# --- Top-level routers (grouping) ---
workflow1_router = APIRouter(tags=[WORKFLOW1_TAG])
workflow2_router = APIRouter(tags=[WORKFLOW2_TAG])
workflow3_router = APIRouter(tags=[WORKFLOW3_TAG])
system_router = APIRouter(tags=[SYSTEM_TAG])

# --- Force tag override (important if OpenAPI Generator hard-coded tags per endpoint) ---
force_single_tag(ClassifyHabitApiRouter, WORKFLOW1_TAG)
force_single_tag(ClassifyContextApiRouter, WORKFLOW1_TAG)
force_single_tag(BcioMappingApiRouter, WORKFLOW1_TAG)

force_single_tag(KbQueryRouter, WORKFLOW3_TAG)

force_single_tag(SystemApiRouter, SYSTEM_TAG)

# --- Mount subrouters in desired groups ---
workflow1_router.include_router(ClassifyHabitApiRouter)
workflow1_router.include_router(ClassifyContextApiRouter)
workflow1_router.include_router(BcioMappingApiRouter)

workflow3_router.include_router(KbQueryRouter)

system_router.include_router(SystemApiRouter)

# --- Finally mount only these routers to the app ---
app.include_router(workflow1_router)
app.include_router(workflow2_router)
app.include_router(workflow3_router)
app.include_router(system_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)
