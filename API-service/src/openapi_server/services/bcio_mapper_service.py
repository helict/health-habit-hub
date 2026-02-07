from __future__ import annotations

import os
import threading
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

SRC_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(SRC_DIR))

from openapi_server.models.classify_context_out import ClassifyContextOut
from openapi_server.services.bcio_hybrid_mapper import BCIOHybridMapper
OPENAPI_SERVER_DIR = Path(__file__).resolve().parents[1]


def _resolve_under_openapi_server(p: str) -> Path:
    pp = Path(p)
    if pp.is_absolute():
        return pp
    return (OPENAPI_SERVER_DIR / pp).resolve()


def _ensure_concept_cards_jsonl(jsonl_path: Path) -> Path:
    """
    Ensure JSONL concept cards exist.
    If missing, export from OWL once.
    """
    if jsonl_path.exists():
        return jsonl_path

    # Lazy import: owlready2 is heavy; only load when needed
    from openapi_server.services.owl2conceptcards_service import export_concept_cards

    owl_path = _resolve_under_openapi_server(os.getenv("BCIO_OWL_PATH", "Ontologies/bcio.owl"))
    mode = os.getenv("EXTRACTION_MODEL", "ALL_MERGED")

    stats = export_concept_cards(
        owl_path=owl_path,
        mode=mode,
    )

    # Prefer the produced path (source of truth)
    out_path = Path(stats.out_path).resolve()
    return out_path


# -----------------------
# Global Singleton: Initialized only once
# -----------------------
_MAPPER: Optional[BCIOHybridMapper] = None
_LOCK = threading.Lock()
_CACHE: Dict[Tuple[str, float, int, Optional[str], bool], List[Dict[str, Any]]] = {}
_CACHE_LOCK = threading.Lock()
_CACHE_MAX = int(os.getenv("BCIO_MAP_CACHE_MAX", "2000"))


def _get_mapper() -> BCIOHybridMapper:
    """Lazy singleton: Initialized only on the first call, and the same instance is reused thereafter."""
    global _MAPPER
    if _MAPPER is not None:
        return _MAPPER

    with _LOCK:
        if _MAPPER is not None:
            return _MAPPER

        milvus_uri = os.getenv("MILVUS_URI", "http://localhost:19530")

        # The default file used is openapi_server/Ontologies/concepts_all_merged.json.
        raw_jsonl = os.getenv("BCIO_JSONL_PATH", "Ontologies/concepts_all_merged.jsonl")
        jsonl_path = _resolve_under_openapi_server(raw_jsonl)

        # If jsonl does not exist: automatically export it from OWL once.
        jsonl_path = _ensure_concept_cards_jsonl(jsonl_path)
        collection_name = os.getenv("BCIO_COLLECTION_NAME") or None

        device = os.getenv("BCIO_DEVICE", "cuda")
        use_fp16 = os.getenv("BCIO_USE_FP16", "0") == "1"
        dense_weight = float(os.getenv("BCIO_DENSE_WEIGHT", "0.65"))

        et_raw = os.getenv("BCIO_ENTITY_TYPES", "Class,ObjectProperty")
        entity_types = tuple(x.strip() for x in et_raw.split(",") if x.strip())

        mapper = BCIOHybridMapper(
            milvus_uri=milvus_uri,
            collection_name=collection_name,
            jsonl_path=str(jsonl_path),
            device=device,
            use_fp16=use_fp16,
            entity_types=entity_types,
            dense_weight=dense_weight,
        )

        # Only during initial initialization: database creation/index creation/loading
        rebuild = os.getenv("BCIO_REBUILD_INDEX", "0") == "1"
        mapper.index_if_needed(batch_size=256, rebuild=rebuild)
        mapper.collection.load()

        _MAPPER = mapper
        return _MAPPER


def map_bcio_for_contexts(
    payload: ClassifyContextOut,
    threshold: float = 0.75,
    top_n: int = 3,
    expr: Optional[str] = 'etype in ["Class","ObjectProperty"]',
    debug: bool = False,
) -> Dict[str, Any]:
    """
    Input: `ClassifyContextOut(result: List[Context])`
    Output: `dict` (add `bcio_mappings` to each `Context` with a value and `classification==1`, based on the payload)
    Note: Your generated `Context` model currently does not have a `bcio_mappings` field.
    If you force a `ClassifyContextOut` object to be returned, Pydantic may lose the `extra` field.
    Therefore, this returns a `dict` (FastAPI can also directly return a `dict`).
    """
    mapper = _get_mapper()

    out = payload.to_dict()
    results: List[Dict[str, Any]] = out.get("result") or []

    for ctx in results:
        if int(ctx.get("classification") or 0) != 1:
            continue

        value = (ctx.get("value") or "").strip()
        if not value:
            continue

        cache_key = (value, float(threshold), int(top_n), expr, bool(debug))

        with _CACHE_LOCK:
            cached = _CACHE.get(cache_key)

        if cached is not None:
            ctx["bcio_mappings"] = cached
            continue

        mappings = mapper.map_sentence(
            sentence=value,
            threshold=float(threshold),
            top_n=int(top_n),
            expr=expr,
            debug=bool(debug),
        )
        ctx["bcio_mappings"] = mappings

        with _CACHE_LOCK:
            if len(_CACHE) >= _CACHE_MAX:
                for k in list(_CACHE.keys())[: _CACHE_MAX // 2]:
                    _CACHE.pop(k, None)
            _CACHE[cache_key] = mappings

    out["result"] = results
    return out


# -----------------------
# Example test
# -----------------------
if __name__ == "__main__":
    import uuid
    import json

    os.environ["BCIO_COLLECTION_NAME"] = f"tmp_bcio_{uuid.uuid4().hex[:8]}"
    os.environ["BCIO_REBUILD_INDEX"] = "1"

    from openapi_server.models.context import Context
    try:
        from openapi_server.models.habit_context import HabitContext
    except ModuleNotFoundError as e:
        raise RuntimeError(
            "HabitContext(enum) not found. Please check the actual filename under src/openapi_server/models/ and modify the import accordingly."
        ) from e

    def run_case(title: str, payload: ClassifyContextOut) -> None:
        print("\n" + "=" * 80)
        print(title)
        print("=" * 80)

        # First, use threshold=0 + debug=True to view the candidates (verification links).
        out_debug = map_bcio_for_contexts(payload, threshold=0.0, top_n=5, expr=None, debug=True)
        print("\n[DEBUG] threshold=0.0, debug=True")
        print(json.dumps(out_debug, ensure_ascii=False, indent=2, default=str))

        # Then use your desired filtering conditions.
        out_filtered = map_bcio_for_contexts(
            payload,
            threshold=0.70,
            top_n=5,
            expr='etype in ["Class","ObjectProperty"]',
            debug=False,
        )
        print("\n[FILTERED] threshold=0.70, debug=False")
        print(json.dumps(out_filtered, ensure_ascii=False, indent=2, default=str))

    # Case A: Everyday habit phrases (it's normal that they might not match BCIO).
    payload_habit = ClassifyContextOut(
        uuid=uuid.uuid4(),
        habit="After dinner I always read on the couch with my wife because it helps me relax.",
        language="en",
        result=[
            Context(name=HabitContext.TIME, value="After dinner", classification=1, confidence=0.96),
            Context(name=HabitContext.PHYSICAL_SETTING, value="on the couch", classification=1, confidence=0.90),
            Context(name=HabitContext.OTHER_PEOPLE, value="my wife", classification=1, confidence=0.93),
            Context(name=HabitContext.BEHAVIOR, value="read", classification=1, confidence=0.94),
            Context(name=HabitContext.REASONING, value="it helps me relax", classification=1, confidence=0.88),
        ],
    )

    # Case B: BCIO-like (used to prove that the retrieval can produce results)
    payload_bcio_like = ClassifyContextOut(
        uuid=uuid.uuid4(),
        habit="(BCIO test) behaviour change intervention delivery example",
        language="en",
        result=[
            Context(
                name=HabitContext.BEHAVIOR,
                value="behaviour change intervention delivery",
                classification=1,
                confidence=0.99,
            ),
            Context(
                name=HabitContext.REASONING,
                value="behaviour change intervention",
                classification=1,
                confidence=0.99,
            ),
        ],
    )

    run_case("CASE A: Habit-context phrases (Empty is not necessarily a bug)", payload_habit)
    run_case("CASE B: BCIO-like phrases (You should be able to see non-empty bcio_mappings)", payload_bcio_like)
