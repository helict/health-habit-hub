# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from openapi_server.models.health_status import HealthStatus


class BaseSystemApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseSystemApi.subclasses = BaseSystemApi.subclasses + (cls,)
    async def health_health_get(
        self,
    ) -> HealthStatus:
        """Checks if the API is running properly and returns whether the OpenAI/SCADS key has been loaded"""
        ...
