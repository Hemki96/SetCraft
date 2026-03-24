from __future__ import annotations

from training_plan_schemas.domain_v1 import ReviewStatus, TrainingSession

from app.schemas.retrieval import RetrievalSearchMatch, RetrievalSearchResponse
from app.services.sessions_service import list_session_items_placeholder
from services.retrieval.hybrid import hybrid_search_sessions


def search_sessions(
    query: str | None,
    distance_m: int | None,
    min_distance_m: int | None,
    max_distance_m: int | None,
    intensity: str | None,
    set_type: str | None,
    review_status: ReviewStatus | None,
) -> RetrievalSearchResponse:
    normalized_query = _normalize(query)
    normalized_intensity = _normalize(intensity)
    normalized_type = _normalize(set_type)

    filtered_items = [
        item
        for item in list_session_items_placeholder()
        if _matches_distance(item, distance_m, min_distance_m, max_distance_m)
        and _matches_intensity(item, normalized_intensity)
        and _matches_type(item, normalized_type)
        and _matches_review_status(item, review_status)
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


def _resolve_session_distance_m(session: TrainingSession) -> int | None:
    if session.total_distance_m is not None:
        return session.total_distance_m

    total = 0
    for block in session.blocks:
        for training_set in block.sets:
            if training_set.distance_m is not None:
                total += training_set.distance_m
    return total or None


def _matches_distance(
    session: TrainingSession,
    distance_m: int | None,
    min_distance_m: int | None,
    max_distance_m: int | None,
) -> bool:
    session_distance = _resolve_session_distance_m(session)

    if distance_m is not None:
        if session_distance == distance_m:
            return True
        for block in session.blocks:
            for training_set in block.sets:
                if training_set.distance_m == distance_m:
                    return True
        return False

    if min_distance_m is not None:
        if session_distance is None or session_distance < min_distance_m:
            return False
    if max_distance_m is not None:
        if session_distance is None or session_distance > max_distance_m:
            return False
    return True


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
    review_status: ReviewStatus | None,
) -> bool:
    if review_status is None:
        return True
    return session.review_status == review_status
