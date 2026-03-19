from __future__ import annotations

from app.schemas.retrieval import RetrievalSearchResponse
from app.services.sessions_service import list_session_items_placeholder


def search_sessions_placeholder(query: str | None) -> RetrievalSearchResponse:
    items = list_session_items_placeholder()
    if not query:
        return RetrievalSearchResponse(items=items)

    normalized_query = query.strip().lower()
    if not normalized_query:
        return RetrievalSearchResponse(items=items)

    filtered_items = [
        item
        for item in items
        if normalized_query in (item.title or "").lower()
        or normalized_query in (item.notes or "").lower()
    ]
    return RetrievalSearchResponse(items=filtered_items)
