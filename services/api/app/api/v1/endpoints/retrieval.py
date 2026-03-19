from __future__ import annotations

from fastapi import APIRouter, Query

from app.schemas.retrieval import RetrievalSearchResponse
from app.services.retrieval_service import search_sessions_placeholder

router = APIRouter()


@router.get("/search", response_model=RetrievalSearchResponse)
def search_sessions(q: str | None = Query(default=None, min_length=1, max_length=200)) -> RetrievalSearchResponse:
    return search_sessions_placeholder(q)
