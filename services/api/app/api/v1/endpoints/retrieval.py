from __future__ import annotations

from fastapi import APIRouter, Query
from training_plan_schemas.domain_v1 import ReviewStatus

from app.schemas.retrieval import RetrievalSearchResponse
from app.services.retrieval_service import search_sessions

router = APIRouter()


@router.get(
    "/search",
    response_model=RetrievalSearchResponse,
    response_model_exclude_defaults=True,
)
def search_sessions_route(
    q: str | None = Query(default=None, min_length=1, max_length=200),
    distance_m: int | None = Query(default=None, ge=0),
    min_distance_m: int | None = Query(default=None, ge=0),
    max_distance_m: int | None = Query(default=None, ge=0),
    intensity: str | None = Query(default=None, min_length=1, max_length=50),
    type: str | None = Query(default=None, min_length=1, max_length=50),
    review_status: ReviewStatus | None = Query(default=None),
) -> RetrievalSearchResponse:
    return search_sessions(
        query=q,
        distance_m=distance_m,
        min_distance_m=min_distance_m,
        max_distance_m=max_distance_m,
        intensity=intensity,
        set_type=type,
        review_status=review_status,
    )
