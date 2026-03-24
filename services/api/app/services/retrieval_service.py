from __future__ import annotations

from fastapi import HTTPException
from training_plan_schemas.domain_v1 import SessionReviewStatus, TrainingSession

from app.schemas.retrieval import RetrievalSearchMatch, RetrievalSearchResponse
from app.services.sessions_service import (
    list_session_items_placeholder,
    normalize_session_review_status,
)
from services.retrieval.hybrid import hybrid_search_sessions


def search_sessions(
    query: str | None,
    min_distance_m: int | None,
    max_distance_m: int | None,
    distance_m: int | None,
    intensity: str | None,
    set_type: str | None,
    review_status: str | SessionReviewStatus | None,
) -> RetrievalSearchResponse:
    normalized_query = _normalize(query)
    normalized_intensity = _normalize(intensity)
    normalized_type = _normalize(set_type)

    try:
        normalized_review_status = normalize_session_review_status(review_status)
    except ValueError as exc:
        raise HTTPException(
            status_code=422,
            detail=f"Invalid review_status: {review_status}",
        ) from exc

    filtered_items = [
        item
        for item in list_session_items_placeholder()
        if _matches_distance_range(item, min_distance_m, max_distance_m)
        and _matches_distance(item, distance_m)
        and _matches_intensity(item, normalized_intensity)
        and _matches_type(item, normalized_type)
        and _matches_review_status(item, normalized_review_status)
    ]

    matches = hybrid_search_sessions(query=normalized_query, sessions=filtered_items)
    return RetrievalSearchResponse(
        items=[match.session for match in matches],
        matches=[
            RetrievalSearchMatch(
                session=match.session,
                structured_score=match.structured_score,
                semantic_score=match.semantic_score,
                combined_score=match.combined_score,
                matched_fields=match.matched_fields,
            )
            for match in matches
        ],
        semantic_enabled=True,
    )


def _normalize(value: str | None) -> str | None:
    if value is None:
        return None
    stripped = value.strip().lower()
    return stripped or None


def _matches_distance_range(
    session: TrainingSession,
    min_distance_m: int | None,
    max_distance_m: int | None,
) -> bool:
    total = session.total_distance_m
    if total is None:
        return min_distance_m is None and max_distance_m is None

    if min_distance_m is not None and total < min_distance_m:
        return False
    if max_distance_m is not None and total > max_distance_m:
        return False
    return True


def _matches_distance(session: TrainingSession, distance_m: int | None) -> bool:
    if distance_m is None:
        return True

    if session.total_distance_m == distance_m:
        return True

    for block in session.blocks:
        for training_set in block.sets:
            if training_set.distance_m == distance_m:
                return True

    return False


def _matches_intensity(session: TrainingSession, intensity: str | None) -> bool:
    if intensity is None:
        return True

    for block in session.blocks:
        for training_set in block.sets:
            intensity_note = (training_set.intensity_note or "").lower()
            if intensity in intensity_note:
                return True

    return False


def _matches_type(session: TrainingSession, set_type: str | None) -> bool:
    if set_type is None:
        return True

    for block in session.blocks:
        block_type = (block.block_type or "").lower()
        if set_type in block_type:
            return True

        for training_set in block.sets:
            if any(set_type in tag.lower() for tag in training_set.tags):
                return True

    return False


def _matches_review_status(
    session: TrainingSession,
    review_status: SessionReviewStatus | None,
) -> bool:
    if review_status is None:
        return True
    return session.review_status == review_status
