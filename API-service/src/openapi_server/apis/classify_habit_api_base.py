# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from openapi_server.models.http_validation_error import HTTPValidationError
from openapi_server.models.habit_in import HabitIn
from openapi_server.models.habit_out import HabitOut


class BaseClassifyHabitApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseClassifyHabitApi.subclasses = BaseClassifyHabitApi.subclasses + (cls,)
    async def classify_habit_classify_habit_post(
        self,
        habit_in: HabitIn,
    ) -> HabitOut:
        ...
