from __future__ import annotations

from fastapi import APIRouter, Query

from app.schemas.retrieval import RetrievalSearchResponse
from app.services.retrieval_service import search_sessions

router = APIRouter()


@router.get("/search", response_model=RetrievalSearchResponse)
def search_sessions_route(
    q: str | None = Query(default=None, min_length=1, max_length=200),
    min_distance_m: int | None = Query(default=None, ge=0),
    max_distance_m: int | None = Query(default=None, ge=0),
    distance_m: int | None = Query(default=None, ge=0),
    intensity: str | None = Query(default=None, min_length=1, max_length=50),
    type: str | None = Query(default=None, min_length=1, max_length=50),
    review_status: str | None = Query(default=None, min_length=1, max_length=50),
) -> RetrievalSearchResponse:
    return search_sessions(
        query=q,
        min_distance_m=min_distance_m,
        max_distance_m=max_distance_m,
        distance_m=distance_m,
        intensity=intensity,
        set_type=type,
        review_status=review_status,
    )
