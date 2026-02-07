from __future__ import annotations

import os
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
_client = AsyncIOMotorClient(MONGO_URI)


USERPROFILES_DB = _client["UserProfiles"]
USERPROFILES_BASIC_COLL = USERPROFILES_DB["basic"]
USERPROFILES_SLIQ_COLL = USERPROFILES_DB["sliq"]
USERPROFILES_RAND36_COLL =  USERPROFILES_DB["rand36"]
