# coding: utf-8
from __future__ import annotations

import os
from pathlib import Path
from dotenv import load_dotenv

from openapi_server.apis.system_api_base import BaseSystemApi
from openapi_server.models.health_status import HealthStatus


class SystemApi(BaseSystemApi):
    async def health_health_get(self) -> HealthStatus:
        """
        Checks if the API is running properly and returns whether the OpenAI/SCADS key has been loaded
        """
        return HealthStatus(
            status="ok",
            openai_key_loaded=bool(os.getenv("OPENAI_API_KEY")),
            scads_key_loaded=bool(os.getenv("SCADS_API_KEY")),
        )
