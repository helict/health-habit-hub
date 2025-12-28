# src/openapi_server/apis/bcio_mapping_api.py
from __future__ import annotations

from typing import Any, Dict, Optional

from fastapi import APIRouter, Body, HTTPException, Query
from fastapi.encoders import jsonable_encoder

from openapi_server.models.classify_context_out import ClassifyContextOut
from openapi_server.services.bcio_mapper_service import map_bcio_for_contexts

router = APIRouter(prefix="", tags=["BCIO Mapping"])


@router.post(
    "/map",
    summary="Map extracted context phrases to BCIO concepts (hybrid dense+sparse)",
)
def bcio_map(
    payload: ClassifyContextOut = Body(...),
    threshold: float = Query(0.75, ge=0.0, le=1.0),
    top_n: int = Query(3, ge=1, le=50),
    expr: Optional[str] = Query('etype in ["Class","ObjectProperty"]'),
    debug: bool = Query(False),
) -> Dict[str, Any]:
    """
    Input: ClassifyContextOut
    Output: dict (same payload + each hit context gets bcio_mappings)
    """
    try:
        enriched = map_bcio_for_contexts(
            payload=payload,
            threshold=threshold,
            top_n=top_n,
            expr=expr,
            debug=debug,
        )
        return jsonable_encoder(enriched)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
