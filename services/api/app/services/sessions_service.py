from __future__ import annotations

from uuid import UUID

from training_plan_schemas.domain_v1 import (
    ApprovalStatus,
    ReviewDecisionType,
    ReviewStatus,
    SessionBlock,
    TrainingSession,
    TrainingSet,
)

from app.schemas.sessions import (
    BlockUpdateRequest,
    SessionListResponse,
    SessionReviewRequest,
    SessionUpdateRequest,
    SetUpdateRequest,
)
from app.services.store import STORE, reset_store, seed_placeholder_data


class SessionEntityNotFoundError(LookupError):
    pass


def reset_session_store() -> None:
    reset_store()


def list_session_items() -> list[TrainingSession]:
    seed_placeholder_data()
    with STORE.lock:
        return list(STORE.sessions.values())


def list_sessions() -> SessionListResponse:
    return SessionListResponse(items=list_session_items())


def get_session(session_id: UUID) -> TrainingSession | None:
    seed_placeholder_data()
    with STORE.lock:
        return STORE.sessions.get(session_id)


def approve_session(session_id: UUID) -> TrainingSession | None:
    seed_placeholder_data()
    with STORE.lock:
        session = STORE.sessions.get(session_id)
        if session is None:
            return None

        session.approval_status = ApprovalStatus.APPROVED
        session.updated_at = STORE.now()
        return session


def submit_session_review(
    session_id: UUID,
    payload: SessionReviewRequest,
) -> TrainingSession:
    with STORE.lock:
        session = STORE.sessions.get(session_id)
        if session is None:
            raise SessionEntityNotFoundError(f"Session '{session_id}' not found")

        if payload.decision == ReviewDecisionType.CORRECTED:
            session.review_status = ReviewStatus.CORRECTED
        elif payload.decision == ReviewDecisionType.REJECTED:
            session.review_status = ReviewStatus.REVIEWED
            session.approval_status = ApprovalStatus.REJECTED
        else:
            session.review_status = ReviewStatus.REVIEWED

        session.updated_at = STORE.now()
        return session


def _get_session_or_raise(session_id: UUID) -> TrainingSession:
    session = STORE.sessions.get(session_id)
    if session is None:
        raise SessionEntityNotFoundError(f"Session '{session_id}' not found")
    return session


def update_session(session_id: UUID, payload: SessionUpdateRequest) -> TrainingSession:
    with STORE.lock:
        session = _get_session_or_raise(session_id)
        if payload.title is not None:
            session.title = payload.title
        if payload.total_distance_m is not None:
            session.total_distance_m = payload.total_distance_m
        if payload.duration_min is not None:
            session.duration_min = payload.duration_min
        if payload.notes is not None:
            session.notes = payload.notes
        if payload.tags is not None:
            session.tags = payload.tags
        session.updated_at = STORE.now()
        return session


def _get_block_or_raise(session: TrainingSession, block_id: UUID) -> SessionBlock:
    for block in session.blocks:
        if block.id == block_id:
            return block
    raise SessionEntityNotFoundError(f"Block '{block_id}' not found")


def update_block(
    session_id: UUID,
    block_id: UUID,
    payload: BlockUpdateRequest,
) -> TrainingSession:
    with STORE.lock:
        session = _get_session_or_raise(session_id)
        block = _get_block_or_raise(session, block_id)
        if payload.title is not None:
            block.title = payload.title
        if payload.block_type is not None:
            block.block_type = payload.block_type
        session.updated_at = STORE.now()
        return session


def _get_set_or_raise(block: SessionBlock, set_id: UUID) -> TrainingSet:
    for training_set in block.sets:
        if training_set.id == set_id:
            return training_set
    raise SessionEntityNotFoundError(f"Set '{set_id}' not found")


def update_set(
    session_id: UUID,
    block_id: UUID,
    set_id: UUID,
    payload: SetUpdateRequest,
) -> TrainingSession:
    with STORE.lock:
        session = _get_session_or_raise(session_id)
        block = _get_block_or_raise(session, block_id)
        training_set = _get_set_or_raise(block, set_id)
        if payload.label is not None:
            training_set.label = payload.label
        if payload.distance_m is not None:
            training_set.distance_m = payload.distance_m
        if payload.duration_sec is not None:
            training_set.duration_sec = payload.duration_sec
        if payload.intensity_note is not None:
            training_set.intensity_note = payload.intensity_note
        if payload.normalized_notes is not None:
            training_set.normalized_notes = payload.normalized_notes
        if payload.tags is not None:
            training_set.tags = payload.tags
        session.updated_at = STORE.now()
        return session


# Backward-compatible aliases for existing endpoints/imports.
list_session_items_placeholder = list_session_items
list_sessions_placeholder = list_sessions
get_session_placeholder = get_session
approve_session_placeholder = approve_session


def review_session_placeholder(
    session_id: UUID,
    *,
    decision: ReviewDecisionType,
) -> TrainingSession | None:
    try:
        return submit_session_review(
            session_id,
            SessionReviewRequest(decision=decision),
        )
    except SessionEntityNotFoundError:
        return None

