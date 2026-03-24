from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from training_plan_schemas.domain_v1 import GeneratedPlan

from app.schemas.auth import UserRole
from app.schemas.generation import (
    GeneratedPlanDetail,
    GenerateSessionPlanRequest,
    GenerateSetPlanRequest,
    GenerateWeekPlanRequest,
    GenerationApprovalResponse,
)
from app.services.audit_service import record_audit_event
from app.services.auth_service import RequestActor, get_request_actor, require_role
from app.services.generation_service import (
    approve_generated_plan,
    create_session_plan,
    create_set_plan,
    create_week_plan,
    get_generated_plan,
)

router = APIRouter()


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
        require_role(actor=actor, allowed_roles={UserRole.ADMIN}, action="generated-plan-approve")
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

    result = approve_generated_plan(generated_plan_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Generated plan not found")

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
