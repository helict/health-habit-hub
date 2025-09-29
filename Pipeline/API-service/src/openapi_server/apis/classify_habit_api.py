# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from openapi_server.apis.classify_habit_api_base import BaseClassifyHabitApi
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
from openapi_server.models.http_validation_error import HTTPValidationError
from openapi_server.models.habit_in import HabitIn
from openapi_server.models.habit_out import HabitOut


router = APIRouter()

ns_pkg = openapi_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.post(
    "/classify_habit",
    responses={
        200: {"model": HabitOut, "description": "Successful Response"},
        422: {"model": HTTPValidationError, "description": "Validation Error"},
    },
    tags=["Classify Habit"],
    summary="Determine whether the sentence entered by the user is a habit",
    response_model_by_alias=True,
)
async def classify_habit_classify_habit_post(
    habit_in: HabitIn = Body(None, description=""),
) -> HabitOut:
    if not BaseClassifyHabitApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseClassifyHabitApi.subclasses[0]().classify_habit_classify_habit_post(habit_in)
