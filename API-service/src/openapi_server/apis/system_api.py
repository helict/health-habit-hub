# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil
import os
from openapi_server.apis.system_api_base import BaseSystemApi
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
from openapi_server.models.health_status import HealthStatus


router = APIRouter()

ns_pkg = openapi_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.get(
    "/health",
    responses={
        200: {"model": HealthStatus, "description": "Successful Response"},
    },
    tags=["System"],
    summary="Health Check",
    response_model_by_alias=True,
)
async def health_health_get(
) -> HealthStatus:
    """Checks if the API is running properly and returns whether the OpenAI/SCADS key has been loaded"""
    if not BaseSystemApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseSystemApi.subclasses[0]().health_health_get()
