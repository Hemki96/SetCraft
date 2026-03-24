from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from training_plan_schemas.domain_v1 import GeneratedPlan

from app.schemas.auth import UserRole
from app.schemas.generation import (
    GeneratedPlanRejectRequest,
    GeneratedPlanReviewCompleteRequest,
    GeneratedPlanDetail,
    GenerateSessionPlanRequest,
    GenerateSetPlanRequest,
    GenerateWeekPlanRequest,
    GenerationApprovalResponse,
)
from app.services.audit_service import record_audit_event
from app.services.auth_service import RequestActor, get_request_actor, require_role
from app.services.generation_service import (
    GeneratedPlanEntityNotFoundError,
    GeneratedPlanTransitionConflictError,
    approve_generated_plan,
    approve_generated_plan_transition,
    complete_generated_plan_review,
    create_session_plan,
    create_set_plan,
    create_week_plan,
    get_generated_plan,
    reject_generated_plan_approval,
    start_generated_plan_review,
    submit_generated_plan_approval,
)

router = APIRouter()


def _conflict_error(exc: GeneratedPlanTransitionConflictError) -> HTTPException:
    return HTTPException(status_code=409, detail=str(exc))


@router.post("/sets", response_model=GeneratedPlan)
def create_set_plan_endpoint(payload: GenerateSetPlanRequest) -> GeneratedPlan:
    return create_set_plan(payload)


@router.post("/sessions", response_model=GeneratedPlan)
def create_session_plan_endpoint(payload: GenerateSessionPlanRequest) -> GeneratedPlan:
    return create_session_plan(payload)


@router.post("/week-plans", response_model=GeneratedPlan)
def create_week_plan_endpoint(payload: GenerateWeekPlanRequest) -> GeneratedPlan:
    return create_week_plan(payload)


@router.get("/plans/{generated_plan_id}", response_model=GeneratedPlanDetail)
def get_generated_plan_endpoint(generated_plan_id: UUID) -> GeneratedPlanDetail:
    plan = get_generated_plan(generated_plan_id)
    if plan is None:
        raise HTTPException(status_code=404, detail="Generated plan not found")
    return plan


@router.post("/plans/{generated_plan_id}/approve", response_model=GenerationApprovalResponse)
def approve_generated_plan_endpoint(
    generated_plan_id: UUID,
    actor: RequestActor = Depends(get_request_actor),
) -> GenerationApprovalResponse:
    try:
        require_role(
            actor=actor,
            allowed_roles={UserRole.ADMIN},
            action="generated-plan-approve",
        )
    except HTTPException:
        record_audit_event(
            event_type="approval",
            action="generated_plan.approve",
            outcome="denied",
            actor=actor,
            entity_type="generated_plan",
            entity_id=str(generated_plan_id),
            message="Generated plan approval denied due to insufficient role",
        )
        raise

    try:
        result = approve_generated_plan_transition(generated_plan_id)
    except GeneratedPlanTransitionConflictError as exc:
        # Compatibility wrapper: allow legacy approve flow without explicit review/submit.
        if (
            "plan must be reviewed before approval" not in str(exc)
            and "approval_status must be submitted before approval" not in str(exc)
        ):
            raise _conflict_error(exc) from exc
        result = approve_generated_plan(generated_plan_id)
        if result is None:
            raise HTTPException(status_code=404, detail="Generated plan not found")
    except GeneratedPlanEntityNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Generated plan not found") from exc

    record_audit_event(
        event_type="approval",
        action="generated_plan.approve",
        outcome="success" if result.approved else "rejected",
        actor=actor,
        entity_type="generated_plan",
        entity_id=str(generated_plan_id),
        message="Generated plan approval processed",
        details={"approved": result.approved},
    )
    return result


@router.post("/plans/{generated_plan_id}/review/start", response_model=GeneratedPlan)
def review_generated_plan_start_endpoint(
    generated_plan_id: UUID,
    actor: RequestActor = Depends(get_request_actor),
) -> GeneratedPlan:
    try:
        plan = start_generated_plan_review(generated_plan_id)
    except GeneratedPlanEntityNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Generated plan not found") from exc
    except GeneratedPlanTransitionConflictError as exc:
        raise _conflict_error(exc) from exc

    record_audit_event(
        event_type="review",
        action="generated_plan.review.start",
        outcome="success",
        actor=actor,
        entity_type="generated_plan",
        entity_id=str(generated_plan_id),
        message="Generated plan moved to in_review",
    )
    return plan


@router.post("/plans/{generated_plan_id}/review/complete", response_model=GeneratedPlan)
def review_generated_plan_complete_endpoint(
    generated_plan_id: UUID,
    payload: GeneratedPlanReviewCompleteRequest,
    actor: RequestActor = Depends(get_request_actor),
) -> GeneratedPlan:
    try:
        plan = complete_generated_plan_review(generated_plan_id, payload)
    except GeneratedPlanEntityNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Generated plan not found") from exc
    except GeneratedPlanTransitionConflictError as exc:
        raise _conflict_error(exc) from exc

    record_audit_event(
        event_type="review",
        action="generated_plan.review.complete",
        outcome="success",
        actor=actor,
        entity_type="generated_plan",
        entity_id=str(generated_plan_id),
        message="Generated plan review completed",
        details={"review_status": payload.review_status.value},
    )
    return plan


@router.post("/plans/{generated_plan_id}/submit-approval", response_model=GeneratedPlan)
def submit_generated_plan_approval_endpoint(
    generated_plan_id: UUID,
    actor: RequestActor = Depends(get_request_actor),
) -> GeneratedPlan:
    try:
        plan = submit_generated_plan_approval(generated_plan_id)
    except GeneratedPlanEntityNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Generated plan not found") from exc
    except GeneratedPlanTransitionConflictError as exc:
        raise _conflict_error(exc) from exc

    record_audit_event(
        event_type="approval",
        action="generated_plan.submit-approval",
        outcome="success",
        actor=actor,
        entity_type="generated_plan",
        entity_id=str(generated_plan_id),
        message="Generated plan submitted for approval",
    )
    return plan


@router.post("/plans/{generated_plan_id}/reject", response_model=GeneratedPlan)
def reject_generated_plan_endpoint(
    generated_plan_id: UUID,
    payload: GeneratedPlanRejectRequest,
    actor: RequestActor = Depends(get_request_actor),
) -> GeneratedPlan:
    try:
        require_role(
            actor=actor,
            allowed_roles={UserRole.ADMIN},
            action="generated_plan.reject",
        )
    except HTTPException:
        record_audit_event(
            event_type="approval",
            action="generated_plan.reject",
            outcome="denied",
            actor=actor,
            entity_type="generated_plan",
            entity_id=str(generated_plan_id),
            message="Generated plan reject denied due to insufficient role",
        )
        raise

    try:
        plan = reject_generated_plan_approval(generated_plan_id, payload.comment)
    except GeneratedPlanEntityNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Generated plan not found") from exc
    except GeneratedPlanTransitionConflictError as exc:
        raise _conflict_error(exc) from exc

    record_audit_event(
        event_type="approval",
        action="generated_plan.reject",
        outcome="success",
        actor=actor,
        entity_type="generated_plan",
        entity_id=str(generated_plan_id),
        message="Generated plan rejected",
        details={"comment": payload.comment},
    )
    return plan
