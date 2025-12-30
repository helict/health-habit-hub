import json
import hashlib
from typing import Any, Dict, List, Optional, Tuple

# Fixed context order
CONTEXT_ORDER = [
    "TIME",
    "PHYSICAL SETTING",
    "PRIOR BEHAVIOR",
    "OTHER PEOPLE",
    "INTERNAL STATE",
    "BEHAVIOR",
    "REASONING",
]

# Transform the result list into a dictionary of name and value.
def _result_list_to_value_map(result_list: Optional[List[Dict[str, Any]]]) -> Dict[str, Any]:
    if not result_list:
        return {}
    out: Dict[str, Any] = {}
    for item in result_list:
        name = item.get("name")
        if name:
            out[name] = item.get("value", None)
    return out

def _contexts_values(mapped_doc: Optional[Dict[str, Any]], raw_doc: Optional[Dict[str, Any]]) -> List[Any]:
    # Extract 7 value arrays from the mapped/raw document.
    m = _result_list_to_value_map((mapped_doc or {}).get("result"))
    if not m:
        m = _result_list_to_value_map((raw_doc or {}).get("result"))
    return [m.get(k, None) for k in CONTEXT_ORDER]

async def build_habit_db_snapshot(
    habits_coll,
    contexts_coll,
    mappings_coll,
    only_habits: bool = True,
) -> Tuple[str, List[Dict[str, Any]]]:
    """
    return:
      signature: str
      habits_list: [{habit, habit_key, contexts:[...]}]
    """
    q: Dict[str, Any] = {}
    if only_habits:
        q["habit_class"] = 1

    # 1) Main table: habits (each entry is a unique habit_key, and the process is only performed once)
    habit_docs: List[Dict[str, Any]] = []
    cursor = habits_coll.find(
        q,
        projection={"_id": 0, "uuid": 1, "habit": 1, "language": 1, "habit_key": 1},
    )
    async for d in cursor:
        if d.get("uuid") and d.get("habit_key"):
            habit_docs.append(d)

    uuids = [d["uuid"] for d in habit_docs]
    if not uuids:
        payload = "[]"
        return hashlib.sha256(payload.encode("utf-8")).hexdigest(), []

    # 2) Batch retrieve contexts
    contexts_by_uuid: Dict[str, Dict[str, Any]] = {}
    ctx_cursor = contexts_coll.find(
        {"uuid": {"$in": uuids}},
        projection={"_id": 0, "uuid": 1, "result": 1},
    )
    async for d in ctx_cursor:
        u = d.get("uuid")
        if u:
            contexts_by_uuid[u] = d

    mappings_by_uuid: Dict[str, Dict[str, Any]] = {}
    map_cursor = mappings_coll.find(
        {"uuid": {"$in": uuids}},
        projection={"_id": 0, "uuid": 1, "result": 1, "mapping_params": 1, "bcio_mapping_error": 1},
    )
    async for d in map_cursor:
        u = d.get("uuid")
        if u:
            mappings_by_uuid[u] = d

    # 3) habits_list
    habits_list: List[Dict[str, Any]] = []
    for h in habit_docs:
        u = h["uuid"]
        raw_doc = contexts_by_uuid.get(u)
        mapped_doc = mappings_by_uuid.get(u)
        habits_list.append(
            {
                "habit": h.get("habit"),
                "habit_key": h.get("habit_key"),
                "contexts": _contexts_values(mapped_doc, raw_doc),
            }
        )

    # 4) Stable sorting + signature
    habits_list.sort(key=lambda x: x.get("habit_key") or "")
    payload = json.dumps(habits_list, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    # payload = "the canonical JSON representation of the current habits_list". The signature is determined based on the payload.
    signature = hashlib.sha256(payload.encode("utf-8")).hexdigest()

    return signature, habits_list


if __name__ == "__main__":
    import os
    import asyncio
    from motor.motor_asyncio import AsyncIOMotorClient

    MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://127.0.0.1:27017/HabitDB")
    MONGO = AsyncIOMotorClient(MONGODB_URI, serverSelectionTimeoutMS=2000)
    DB = MONGO.get_default_database()

    HABITS_COLL = DB.get_collection("habits")
    CONTEXTS_COLL = DB.get_collection("contexts")
    CONTEXT_MAPPINGS_COLL = DB.get_collection("context_mappings")

    async def _main():
        await MONGO.admin.command("ping")
        print("DB:", DB.name)
        names = await DB.list_collection_names()
        print("Collections:", names)
        print("habits.count:", await HABITS_COLL.count_documents({}))
        print("contexts.count:", await CONTEXTS_COLL.count_documents({}))
        print("context_mappings.count:", await CONTEXT_MAPPINGS_COLL.count_documents({}))

        sig, habits_list = await build_habit_db_snapshot(
            HABITS_COLL, CONTEXTS_COLL, CONTEXT_MAPPINGS_COLL, only_habits=True
        )

        print("\nsignature:", sig)
        print("habits_list.count:", len(habits_list))
        print("all_items:", habits_list if habits_list else None)

        MONGO.close()
    asyncio.run(_main())
