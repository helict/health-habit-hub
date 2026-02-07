# coding: utf-8
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, APIRouter

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env", override=False)

from openapi_server.apis.classify_habit_api import router as ClassifyHabitApiRouter
from openapi_server.apis.classify_context_api import router as ClassifyContextApiRouter
from openapi_server.apis.bcio_mapping_api import router as BcioMappingApiRouter
from openapi_server.apis.system_api import router as SystemApiRouter

from openapi_server.apis.profiles_build_api import router as ProfilesBuildApiRouter
from openapi_server.apis.kb_query_api import router as KbQueryRouter
from openapi_server.apis.select_habits_api import router as HabitDbSelectRouter
# from openapi_server.apis.theory_prompt_api import router as TheoryPromptApiRouter
from openapi_server.apis.recommend_api import router as RecommendApiRouter

WORKFLOW1_TAG = "Required APIs for Workflow 1: Habitual structured collection"
WORKFLOW2_TAG = "Required APIs for Workflow 2: User form completion"
WORKFLOW3_TAG = "Required APIs for Workflow 3: Habit Recommendation"
SYSTEM_TAG    = "System: API key check"


def force_single_tag(router: APIRouter, tag: str) -> None:
    for r in router.routes:
        if hasattr(r, "tags"):
            r.tags = [tag]


app = FastAPI(
    title="Habit Recommendation System APIs",
    description=(
        "Provide modular and reusable APIs for the three workflows of the Habit Recommendation System."
    ),
    version="1.0.0",
    openapi_tags=[
        {"name": WORKFLOW1_TAG, "description": "Provide these three APIs: Habitual structured collection, context extraction, and BCIO mapping."},
        {"name": WORKFLOW2_TAG, "description": "User form data collection is relatively simple, so no additional APIs are provided here."},
        {"name": WORKFLOW3_TAG, "description": "Provide the following four APIs: habit selection, user profile selection/summarization, RAG knowledge base retrieval, and recommendation generation."},
        {"name": SYSTEM_TAG, "description": "Perform API key status checks only"},
    ],
)

workflow1_router = APIRouter(tags=[WORKFLOW1_TAG])
workflow2_router = APIRouter(tags=[WORKFLOW2_TAG])
workflow3_router = APIRouter(tags=[WORKFLOW3_TAG])
system_router = APIRouter(tags=[SYSTEM_TAG])

force_single_tag(ClassifyHabitApiRouter, WORKFLOW1_TAG)
force_single_tag(ClassifyContextApiRouter, WORKFLOW1_TAG)
force_single_tag(BcioMappingApiRouter, WORKFLOW1_TAG)

force_single_tag(HabitDbSelectRouter, WORKFLOW3_TAG)
force_single_tag(ProfilesBuildApiRouter, WORKFLOW3_TAG)
force_single_tag(KbQueryRouter, WORKFLOW3_TAG)
# force_single_tag(TheoryPromptApiRouter, WORKFLOW3_TAG)
force_single_tag(RecommendApiRouter, WORKFLOW3_TAG)

force_single_tag(SystemApiRouter, SYSTEM_TAG)

workflow1_router.include_router(ClassifyHabitApiRouter)
workflow1_router.include_router(ClassifyContextApiRouter)
workflow1_router.include_router(BcioMappingApiRouter)

workflow3_router.include_router(HabitDbSelectRouter)
workflow3_router.include_router(ProfilesBuildApiRouter)

workflow3_router.include_router(KbQueryRouter)
# workflow3_router.include_router(TheoryPromptApiRouter)
workflow3_router.include_router(RecommendApiRouter)

system_router.include_router(SystemApiRouter)

app.include_router(workflow1_router)
app.include_router(workflow2_router)
app.include_router(workflow3_router)
app.include_router(system_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)
