from __future__ import annotations

import os
from motor.motor_asyncio import AsyncIOMotorClient

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://127.0.0.1:27017/HabitDB")

MONGO = AsyncIOMotorClient(MONGODB_URI, serverSelectionTimeoutMS=2000)
DB = MONGO.get_default_database()

HABITS_COLL = DB.get_collection("habits")
CONTEXTS_COLL = DB.get_collection("contexts")
CONTEXT_MAPPINGS_COLL = DB.get_collection("context_mappings")
