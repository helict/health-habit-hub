# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from openapi_server.apis.classify_context_api_base import BaseClassifyContextApi
import openapi_server.impl

from fastapi import (  # noqa: F401
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

from openapi_server.models.extra_models import TokenModel  # noqa: F401
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
    summary="Determine the context of the sentence describing the habit entered by the user",
    response_model_by_alias=True,
)
async def classify_context_classify_context_post(
    classify_context_in: ClassifyContextIn = Body(None, description=""),
) -> ClassifyContextOut:
    if not BaseClassifyContextApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseClassifyContextApi.subclasses[0]().classify_context_classify_context_post(classify_context_in)
