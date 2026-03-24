from __future__ import annotations

from uuid import UUID

from training_plan_schemas.domain_v1 import (
    ReviewDecision,
    ReviewDecisionType,
    ReviewTargetType,
    SessionApprovalStatus,
    SessionReviewStatus,
    TrainingSession,
)

from app.schemas.sessions import (
    BlockUpdateRequest,
    SessionListResponse,
    SessionReviewRequest,
    SessionReviewCompleteRequest,
    SessionUpdateRequest,
    SetUpdateRequest,
)
from app.services.store import STORE, seed_placeholder_data


class SessionEntityNotFoundError(LookupError):
    pass


class SessionTransitionConflictError(ValueError):
    pass


def normalize_session_review_status(
    value: str | SessionReviewStatus | None,
) -> SessionReviewStatus | None:
    if value is None:
        return None
    if isinstance(value, SessionReviewStatus):
        return value

    normalized = value.strip().lower()
    if not normalized:
        return None

    legacy_map = {
        "needs_review": SessionReviewStatus.PENDING_REVIEW,
        "reviewed": SessionReviewStatus.REVIEWED_OK,
        "corrected": SessionReviewStatus.REVIEWED_WITH_CHANGES,
    }
    return SessionReviewStatus(legacy_map.get(normalized, normalized))


def _build_transition_error_message(action: str, session: TrainingSession, reason: str) -> str:
    return (
        f"Invalid transition for {action}: {reason} "
        f"(review_status={session.review_status.value}, "
        f"approval_status={session.approval_status.value})"
    )


def _append_review_history(
    session: TrainingSession,
    review_decision: ReviewDecision,
) -> None:
    existing_history_raw = session.details_json.get("review_history", [])
    existing_history = (
        list(existing_history_raw) if isinstance(existing_history_raw, list) else []
    )
    existing_history.append(review_decision.model_dump(mode="json"))
    session.details_json["review_history"] = existing_history


def list_session_items_placeholder() -> list[TrainingSession]:
    seed_placeholder_data()
    with STORE.lock:
        return list(STORE.sessions.values())


def list_sessions_placeholder() -> SessionListResponse:
    return SessionListResponse(items=list_session_items_placeholder())


def get_session_placeholder(session_id: UUID) -> TrainingSession | None:
    seed_placeholder_data()
    with STORE.lock:
        return STORE.sessions.get(session_id)


def start_session_review_placeholder(session_id: UUID) -> TrainingSession | None:
    seed_placeholder_data()
    with STORE.lock:
        session = STORE.sessions.get(session_id)
        if session is None:
            return None

        if session.review_status == SessionReviewStatus.IN_REVIEW:
            raise SessionTransitionConflictError(
                _build_transition_error_message(
                    "session.review.start",
                    session,
                    "session is already in review",
                )
            )

        if session.approval_status == SessionApprovalStatus.APPROVED:
            raise SessionTransitionConflictError(
                _build_transition_error_message(
                    "session.review.start",
                    session,
                    "approved sessions must be edited before review restart",
                )
            )

        session.review_status = SessionReviewStatus.IN_REVIEW
        session.updated_at = STORE.now()
        return session


def complete_session_review_placeholder(
    session_id: UUID,
    payload: SessionReviewCompleteRequest,
) -> TrainingSession | None:
    seed_placeholder_data()
    with STORE.lock:
        session = STORE.sessions.get(session_id)
        if session is None:
            return None

        if session.review_status != SessionReviewStatus.IN_REVIEW:
            raise SessionTransitionConflictError(
                _build_transition_error_message(
                    "session.review.complete",
                    session,
                    "session must be in_review before completion",
                )
            )

        if payload.review_status not in {
            SessionReviewStatus.REVIEWED_WITH_CHANGES,
            SessionReviewStatus.REVIEWED_OK,
        }:
            raise SessionTransitionConflictError(
                _build_transition_error_message(
                    "session.review.complete",
                    session,
                    "review_status must be reviewed_with_changes or reviewed_ok",
                )
            )

        decision = (
            ReviewDecisionType.CORRECTED
            if payload.review_status == SessionReviewStatus.REVIEWED_WITH_CHANGES
            else ReviewDecisionType.REVIEWED
        )
        review_decision = ReviewDecision(
            target_type=ReviewTargetType.SESSION,
            target_id=session.id,
            decision=decision,
            comment=payload.comment,
        )
        _append_review_history(session, review_decision)

        session.review_status = payload.review_status
        if session.approval_status == SessionApprovalStatus.REJECTED:
            session.approval_status = SessionApprovalStatus.NOT_SUBMITTED
        session.updated_at = STORE.now()
        return session


def submit_session_approval_placeholder(session_id: UUID) -> TrainingSession | None:
    seed_placeholder_data()
    with STORE.lock:
        session = STORE.sessions.get(session_id)
        if session is None:
            return None

        if session.review_status not in {
            SessionReviewStatus.REVIEWED_WITH_CHANGES,
            SessionReviewStatus.REVIEWED_OK,
        }:
            raise SessionTransitionConflictError(
                _build_transition_error_message(
                    "session.submit-approval",
                    session,
                    "session must be reviewed before submit",
                )
            )

        if session.approval_status not in {
            SessionApprovalStatus.NOT_SUBMITTED,
            SessionApprovalStatus.REJECTED,
        }:
            raise SessionTransitionConflictError(
                _build_transition_error_message(
                    "session.submit-approval",
                    session,
                    "approval can only be submitted from not_submitted or rejected",
                )
            )

        session.approval_status = SessionApprovalStatus.SUBMITTED
        session.updated_at = STORE.now()
        return session


def approve_session_placeholder(session_id: UUID) -> TrainingSession | None:
    seed_placeholder_data()
    with STORE.lock:
        session = STORE.sessions.get(session_id)
        if session is None:
            return None

        if session.review_status not in {
            SessionReviewStatus.REVIEWED_WITH_CHANGES,
            SessionReviewStatus.REVIEWED_OK,
        }:
            raise SessionTransitionConflictError(
                _build_transition_error_message(
                    "session.approve",
                    session,
                    "session must be reviewed before approval",
                )
            )

        if session.approval_status != SessionApprovalStatus.SUBMITTED:
            raise SessionTransitionConflictError(
                _build_transition_error_message(
                    "session.approve",
                    session,
                    "approval_status must be submitted before approval",
                )
            )

        session.approval_status = SessionApprovalStatus.APPROVED
        session.updated_at = STORE.now()
        return session


def reject_session_approval_placeholder(
    session_id: UUID, comment: str | None
) -> TrainingSession | None:
    seed_placeholder_data()
    with STORE.lock:
        session = STORE.sessions.get(session_id)
        if session is None:
            return None

        if session.approval_status != SessionApprovalStatus.SUBMITTED:
            raise SessionTransitionConflictError(
                _build_transition_error_message(
                    "session.reject",
                    session,
                    "approval_status must be submitted before rejection",
                )
            )

        review_decision = ReviewDecision(
            target_type=ReviewTargetType.SESSION,
            target_id=session.id,
            decision=ReviewDecisionType.REJECTED,
            comment=comment,
        )
        _append_review_history(session, review_decision)

        session.approval_status = SessionApprovalStatus.REJECTED
        session.updated_at = STORE.now()
        return session


def _apply_legacy_review_decision(
    session: TrainingSession,
    payload: SessionReviewRequest,
) -> TrainingSession:
    if session.review_status != SessionReviewStatus.IN_REVIEW:
        # Compatibility wrapper: old endpoint allowed direct completion without explicit start.
        if session.approval_status == SessionApprovalStatus.APPROVED:
            raise SessionTransitionConflictError(
                _build_transition_error_message(
                    "session.review",
                    session,
                    "approved sessions must be edited before review restart",
                )
            )
        session.review_status = SessionReviewStatus.IN_REVIEW

    review_status = (
        SessionReviewStatus.REVIEWED_WITH_CHANGES
        if payload.decision == ReviewDecisionType.CORRECTED
        else SessionReviewStatus.REVIEWED_OK
    )
    decision = (
        ReviewDecisionType.CORRECTED
        if review_status == SessionReviewStatus.REVIEWED_WITH_CHANGES
        else ReviewDecisionType.REVIEWED
    )
    review_decision = ReviewDecision(
        target_type=ReviewTargetType.SESSION,
        target_id=session.id,
        decision=decision,
        comment=payload.comment,
    )
    _append_review_history(session, review_decision)
    session.review_status = review_status
    if session.approval_status == SessionApprovalStatus.REJECTED:
        session.approval_status = SessionApprovalStatus.NOT_SUBMITTED
    session.updated_at = STORE.now()
    return session


def patch_session_placeholder(
    session_id: UUID,
    payload: SessionUpdateRequest,
) -> TrainingSession | None:
    seed_placeholder_data()
    with STORE.lock:
        session = STORE.sessions.get(session_id)
        if session is None:
            return None

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

        session.review_status = SessionReviewStatus.PENDING_REVIEW
        session.approval_status = SessionApprovalStatus.NOT_SUBMITTED
        session.updated_at = STORE.now()
        return session


def patch_block_placeholder(
    session_id: UUID,
    block_id: UUID,
    payload: BlockUpdateRequest,
) -> TrainingSession | None:
    seed_placeholder_data()
    with STORE.lock:
        session = STORE.sessions.get(session_id)
        if session is None:
            return None

        block = next((item for item in session.blocks if item.id == block_id), None)
        if block is None:
            return None

        if payload.title is not None:
            block.title = payload.title
        if payload.block_type is not None:
            block.block_type = payload.block_type

        session.review_status = SessionReviewStatus.PENDING_REVIEW
        session.approval_status = SessionApprovalStatus.NOT_SUBMITTED
        session.updated_at = STORE.now()
        return session


def patch_set_placeholder(
    session_id: UUID,
    block_id: UUID,
    set_id: UUID,
    payload: SetUpdateRequest,
) -> TrainingSession | None:
    seed_placeholder_data()
    with STORE.lock:
        session = STORE.sessions.get(session_id)
        if session is None:
            return None

        block = next((item for item in session.blocks if item.id == block_id), None)
        if block is None:
            return None

        set_item = next((item for item in block.sets if item.id == set_id), None)
        if set_item is None:
            return None

        if payload.label is not None:
            set_item.label = payload.label
        if payload.distance_m is not None:
            set_item.distance_m = payload.distance_m
        if payload.duration_sec is not None:
            set_item.duration_sec = payload.duration_sec
        if payload.intensity_note is not None:
            set_item.intensity_note = payload.intensity_note
        if payload.normalized_notes is not None:
            set_item.normalized_notes = payload.normalized_notes
        if payload.tags is not None:
            set_item.tags = payload.tags

        session.review_status = SessionReviewStatus.PENDING_REVIEW
        session.approval_status = SessionApprovalStatus.NOT_SUBMITTED
        session.updated_at = STORE.now()
        return session


def list_sessions() -> SessionListResponse:
    return list_sessions_placeholder()


def get_session(session_id: UUID) -> TrainingSession | None:
    return get_session_placeholder(session_id)


def start_session_review(session_id: UUID) -> TrainingSession:
    session = start_session_review_placeholder(session_id)
    if session is None:
        raise SessionEntityNotFoundError("Session not found")
    return session


def complete_session_review(
    session_id: UUID,
    payload: SessionReviewCompleteRequest,
) -> TrainingSession:
    session = complete_session_review_placeholder(session_id, payload)
    if session is None:
        raise SessionEntityNotFoundError("Session not found")
    return session


def submit_session_review(
    session_id: UUID,
    payload: SessionReviewRequest,
) -> TrainingSession:
    with STORE.lock:
        session = STORE.sessions.get(session_id)
        if session is None:
            raise SessionEntityNotFoundError("Session not found")

        if payload.decision == ReviewDecisionType.REJECTED:
            review_decision = ReviewDecision(
                target_type=ReviewTargetType.SESSION,
                target_id=session.id,
                decision=payload.decision,
                comment=payload.comment,
            )
            _append_review_history(session, review_decision)
            session.review_status = SessionReviewStatus.PENDING_REVIEW
            session.approval_status = SessionApprovalStatus.REJECTED
            session.updated_at = STORE.now()
            return session

        return _apply_legacy_review_decision(session, payload)


def submit_approval(session_id: UUID) -> TrainingSession:
    session = submit_session_approval_placeholder(session_id)
    if session is None:
        raise SessionEntityNotFoundError("Session not found")
    return session


def approve_session(session_id: UUID) -> TrainingSession | None:
    session = approve_session_placeholder(session_id)
    if session is None:
        return None
    return session


def reject_approval(session_id: UUID, comment: str | None = None) -> TrainingSession:
    session = reject_session_approval_placeholder(session_id, comment)
    if session is None:
        raise SessionEntityNotFoundError("Session not found")
    return session


def update_session(session_id: UUID, payload: SessionUpdateRequest) -> TrainingSession:
    session = patch_session_placeholder(session_id, payload)
    if session is None:
        raise SessionEntityNotFoundError("Session not found")
    return session


def update_block(
    session_id: UUID,
    block_id: UUID,
    payload: BlockUpdateRequest,
) -> TrainingSession:
    session = patch_block_placeholder(session_id, block_id, payload)
    if session is None:
        raise SessionEntityNotFoundError("Session or block not found")
    return session


def update_set(
    session_id: UUID,
    block_id: UUID,
    set_id: UUID,
    payload: SetUpdateRequest,
) -> TrainingSession:
    session = patch_set_placeholder(session_id, block_id, set_id, payload)
    if session is None:
        raise SessionEntityNotFoundError("Session, block or set not found")
    return session
