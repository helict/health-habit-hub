from typing import Dict, List
import importlib
import pkgutil

from openapi_server.apis.classify_context_api_base import BaseClassifyContextApi
import openapi_server.impl

from fastapi import (
    APIRouter,
    Body,
    Cookie,
    Depends,
    Form,
    Header,
    HTTPException,
    Path,
    Query,
    Response,
    Security,
    status,
)

from openapi_server.models.extra_models import TokenModel
from openapi_server.models.classify_context_in import ClassifyContextIn
from openapi_server.models.classify_context_out import ClassifyContextOut
from openapi_server.models.http_validation_error import HTTPValidationError


router = APIRouter()

ns_pkg = openapi_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.post(
    "/classify_context",
    responses={
        200: {"model": ClassifyContextOut, "description": "Successful Response"},
        422: {"model": HTTPValidationError, "description": "Validation Error"},
    },
    tags=["Classify Context"],
    summary="Call a large language model to determine the context of the user-entered habit sentence: TIME, PHYSICAL SETTING, PRIOR BEHAVIOR, OTHER PEOPLE, INTERNAL STATE, BEHAVIOR, and REASONING. Redis is used as a cache.",
    response_model_by_alias=True,
)
async def classify_context_classify_context_post(
    classify_context_in: ClassifyContextIn = Body(None, description=""),
) -> ClassifyContextOut:
    if not BaseClassifyContextApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseClassifyContextApi.subclasses[0]().classify_context_classify_context_post(classify_context_in)
