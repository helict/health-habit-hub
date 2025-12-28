# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from openapi_server.models.classify_context_in import ClassifyContextIn
from openapi_server.models.classify_context_out import ClassifyContextOut
from openapi_server.models.http_validation_error import HTTPValidationError


class BaseClassifyContextApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseClassifyContextApi.subclasses = BaseClassifyContextApi.subclasses + (cls,)
    async def classify_context_classify_context_post(
        self,
        classify_context_in: ClassifyContextIn,
    ) -> ClassifyContextOut:
        ...
