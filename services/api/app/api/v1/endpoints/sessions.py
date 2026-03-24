from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from training_plan_schemas.domain_v1 import TrainingSession

from app.schemas.auth import UserRole
from app.schemas.sessions import (
    BlockUpdateRequest,
    SessionListResponse,
    SessionRejectRequest,
    SessionReviewCompleteRequest,
    SessionReviewRequest,
    SessionUpdateRequest,
    SetUpdateRequest,
)
from app.services.audit_service import record_audit_event
from app.services.auth_service import RequestActor, get_request_actor, require_role
from app.services.sessions_service import (
    SessionEntityNotFoundError,
    SessionTransitionConflictError,
    approve_session,
    complete_session_review,
    get_session,
    list_sessions,
    reject_approval,
    start_session_review,
    submit_approval,
    submit_session_review,
    update_block,
    update_session,
    update_set,
)

router = APIRouter()


def _get_session_or_404(session_id: UUID) -> TrainingSession:
    session = get_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    return session


def _conflict_error(exc: SessionTransitionConflictError) -> HTTPException:
    return HTTPException(status_code=409, detail=str(exc))


def _require_admin_or_audit_denied(
    *,
    actor: RequestActor,
    session_id: UUID,
    action: str,
) -> None:
    try:
        require_role(
            actor=actor,
            allowed_roles={UserRole.ADMIN},
            action=action,
        )
    except HTTPException as exc:
        record_audit_event(
            event_type="approval",
            action=action,
            outcome="denied",
            actor=actor,
            entity_type="session",
            entity_id=str(session_id),
            message=str(exc.detail),
            details={"status_code": exc.status_code},
        )
        raise


@router.get("", response_model=SessionListResponse)
def list_sessions_endpoint() -> SessionListResponse:
    return list_sessions()


@router.get("/{session_id}", response_model=TrainingSession)
def get_session_endpoint(session_id: UUID) -> TrainingSession:
    return _get_session_or_404(session_id)


@router.patch("/{session_id}", response_model=TrainingSession)
def update_session_endpoint(
    session_id: UUID,
    payload: SessionUpdateRequest,
) -> TrainingSession:
    try:
        return update_session(session_id, payload)
    except SessionEntityNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Session not found") from exc


@router.patch("/{session_id}/blocks/{block_id}", response_model=TrainingSession)
def update_block_endpoint(
    session_id: UUID,
    block_id: UUID,
    payload: BlockUpdateRequest,
) -> TrainingSession:
    try:
        return update_block(session_id, block_id, payload)
    except SessionEntityNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.patch(
    "/{session_id}/blocks/{block_id}/sets/{set_id}",
    response_model=TrainingSession,
)
def update_set_endpoint(
    session_id: UUID,
    block_id: UUID,
    set_id: UUID,
    payload: SetUpdateRequest,
) -> TrainingSession:
    try:
        return update_set(session_id, block_id, set_id, payload)
    except SessionEntityNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/{session_id}/review/start", response_model=TrainingSession)
def review_start_session_endpoint(
    session_id: UUID,
    actor: RequestActor = Depends(get_request_actor),
) -> TrainingSession:
    try:
        session = start_session_review(session_id)
    except SessionEntityNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Session not found") from exc
    except SessionTransitionConflictError as exc:
        raise _conflict_error(exc) from exc

    record_audit_event(
        event_type="review",
        action="session.review.start",
        outcome="success",
        actor=actor,
        entity_type="session",
        entity_id=str(session_id),
        message="Session moved to in_review",
    )
    return session


@router.post("/{session_id}/review/complete", response_model=TrainingSession)
def review_complete_session_endpoint(
    session_id: UUID,
    payload: SessionReviewCompleteRequest,
    actor: RequestActor = Depends(get_request_actor),
) -> TrainingSession:
    try:
        session = complete_session_review(session_id, payload)
    except SessionEntityNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Session not found") from exc
    except SessionTransitionConflictError as exc:
        raise _conflict_error(exc) from exc

    record_audit_event(
        event_type="review",
        action="session.review.complete",
        outcome="success",
        actor=actor,
        entity_type="session",
        entity_id=str(session_id),
        message="Session review completed",
        details={"review_status": payload.review_status.value},
    )
    return session


@router.post("/{session_id}/submit-approval", response_model=TrainingSession)
def submit_approval_session_endpoint(
    session_id: UUID,
    actor: RequestActor = Depends(get_request_actor),
) -> TrainingSession:
    try:
        session = submit_approval(session_id)
    except SessionEntityNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Session not found") from exc
    except SessionTransitionConflictError as exc:
        raise _conflict_error(exc) from exc

    record_audit_event(
        event_type="approval",
        action="session.submit-approval",
        outcome="success",
        actor=actor,
        entity_type="session",
        entity_id=str(session_id),
        message="Session submitted for approval",
    )
    return session


@router.post("/{session_id}/approve", response_model=TrainingSession)
def approve_session_endpoint(
    session_id: UUID,
    actor: RequestActor = Depends(get_request_actor),
) -> TrainingSession:
    _require_admin_or_audit_denied(
        actor=actor,
        session_id=session_id,
        action="session.approve",
    )

    try:
        approved_session = approve_session(session_id)
    except SessionTransitionConflictError as exc:
        # Compatibility wrapper: old endpoint skipped explicit submit-approval.
        if "approval_status must be submitted" not in str(exc):
            raise _conflict_error(exc) from exc
        try:
            submit_approval(session_id)
            approved_session = approve_session(session_id)
        except SessionTransitionConflictError as submit_exc:
            raise _conflict_error(submit_exc) from submit_exc

    if approved_session is None:
        raise HTTPException(status_code=404, detail="Session not found")

    record_audit_event(
        event_type="approval",
        action="session.approve",
        outcome="success",
        actor=actor,
        entity_type="session",
        entity_id=str(session_id),
        message="Session approved",
    )
    return approved_session


@router.post("/{session_id}/reject", response_model=TrainingSession)
def reject_session_endpoint(
    session_id: UUID,
    payload: SessionRejectRequest,
    actor: RequestActor = Depends(get_request_actor),
) -> TrainingSession:
    _require_admin_or_audit_denied(
        actor=actor,
        session_id=session_id,
        action="session.reject",
    )

    try:
        session = reject_approval(session_id, comment=payload.comment)
    except SessionEntityNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Session not found") from exc
    except SessionTransitionConflictError as exc:
        raise _conflict_error(exc) from exc

    record_audit_event(
        event_type="approval",
        action="session.reject",
        outcome="success",
        actor=actor,
        entity_type="session",
        entity_id=str(session_id),
        message="Session rejected",
        details={"comment": payload.comment},
    )
    return session


@router.post("/{session_id}/review", response_model=TrainingSession)
def review_session_endpoint(
    session_id: UUID,
    payload: SessionReviewRequest,
    actor: RequestActor = Depends(get_request_actor),
) -> TrainingSession:
    try:
        session = submit_session_review(session_id, payload)
    except SessionEntityNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Session not found") from exc
    except SessionTransitionConflictError as exc:
        raise _conflict_error(exc) from exc

    record_audit_event(
        event_type="review",
        action="session.review",
        outcome="success",
        actor=actor,
        entity_type="session",
        entity_id=str(session_id),
        message="Session review decision stored",
        details={"decision": payload.decision.value},
    )
    return session
