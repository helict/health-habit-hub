import json
import hashlib
from typing import Any, Dict, List, Optional, Tuple

CONTEXT_ORDER = [
    "TIME",
    "PHYSICAL SETTING",
    "PRIOR BEHAVIOR",
    "OTHER PEOPLE",
    "INTERNAL STATE",
    "BEHAVIOR",
    "REASONING",
]

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

    # 1) load habits (unique by habit_key in your current DB design)
    habit_docs: List[Dict[str, Any]] = []
    cursor = habits_coll.find(
        q,
        projection={"_id": 0, "habit_key": 1, "habit": 1, "language": 1, "uuid": 1},
    )
    async for d in cursor:
        if d.get("habit_key"):
            habit_docs.append(d)

    habit_keys = [d["habit_key"] for d in habit_docs if d.get("habit_key")]
    if not habit_keys:
        payload = "[]"
        return hashlib.sha256(payload.encode("utf-8")).hexdigest(), []

    # 2) batch load contexts/mappings by habit_key (stable join key)
    contexts_by_hk: Dict[str, Dict[str, Any]] = {}
    ctx_cursor = contexts_coll.find(
        {"habit_key": {"$in": habit_keys}},
        projection={"_id": 0, "habit_key": 1, "uuid": 1, "result": 1},
    )
    async for d in ctx_cursor:
        hk = d.get("habit_key")
        if hk:
            contexts_by_hk[hk] = d

    mappings_by_hk: Dict[str, Dict[str, Any]] = {}
    map_cursor = mappings_coll.find(
        {"habit_key": {"$in": habit_keys}},
        projection={"_id": 0, "habit_key": 1, "uuid": 1, "result": 1, "mapping_params": 1, "bcio_mapping_error": 1},
    )
    async for d in map_cursor:
        hk = d.get("habit_key")
        if hk:
            mappings_by_hk[hk] = d

    # --- Optional fallback for older data (uuid-join) ---
    # If your old records existed where contexts/mappings didn't store habit_key,
    # this keeps backward compatibility.
    uuids = [d.get("uuid") for d in habit_docs if d.get("uuid")]
    contexts_by_uuid: Dict[str, Dict[str, Any]] = {}
    mappings_by_uuid: Dict[str, Dict[str, Any]] = {}

    if uuids:
        ctx2 = contexts_coll.find({"uuid": {"$in": uuids}}, projection={"_id": 0, "uuid": 1, "result": 1})
        async for d in ctx2:
            u = d.get("uuid")
            if u:
                contexts_by_uuid[u] = d

        mp2 = mappings_coll.find(
            {"uuid": {"$in": uuids}},
            projection={"_id": 0, "uuid": 1, "result": 1, "mapping_params": 1, "bcio_mapping_error": 1},
        )
        async for d in mp2:
            u = d.get("uuid")
            if u:
                mappings_by_uuid[u] = d
    # -----------------------------------------------

    # 3) build habits_list (UNCHANGED structure)
    habits_list: List[Dict[str, Any]] = []
    for h in habit_docs:
        hk = h["habit_key"]
        raw_doc = contexts_by_hk.get(hk)
        mapped_doc = mappings_by_hk.get(hk)

        # fallback if needed
        if (raw_doc is None or mapped_doc is None) and h.get("uuid"):
            u = h["uuid"]
            raw_doc = raw_doc or contexts_by_uuid.get(u)
            mapped_doc = mapped_doc or mappings_by_uuid.get(u)

        habits_list.append(
            {
                "habit": h.get("habit"),
                "habit_key": hk,
                "contexts": _contexts_values(mapped_doc, raw_doc),
            }
        )

    # 4) stable sorting + signature (UNCHANGED)
    habits_list.sort(key=lambda x: x.get("habit_key") or "")
    payload = json.dumps(habits_list, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    signature = hashlib.sha256(payload.encode("utf-8")).hexdigest()

    return signature, habits_list

