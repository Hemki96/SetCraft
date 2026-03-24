from __future__ import annotations

from fastapi import HTTPException
from training_plan_schemas.domain_v1 import (
    ApprovalStatus,
    GeneratedPlan,
    PlanType,
    ReviewStatus,
    TrainingSession,
    ValidationResult,
)
from uuid import UUID

from app.schemas.generation import (
    GenerateSessionPlanRequest,
    GenerateSetPlanRequest,
    GenerateWeekPlanRequest,
    GeneratedPlanDetail,
    GenerationApprovalResponse,
)
from app.services.store import STORE
from app.services.validation_service import validate_generated_plan
from services.generation.planner import (
    GenerateSessionInput,
    GenerateSetInput,
    GenerateWeekInput,
    build_session_content,
    build_set_content,
    build_week_content,
)


def _resolve_reference_sessions(reference_session_ids: list[UUID]) -> list[TrainingSession]:
    available_sessions = list(STORE.sessions.values())
    if not reference_session_ids:
        return available_sessions

    resolved = [session for session in available_sessions if session.id in reference_session_ids]
    if not resolved:
        raise HTTPException(status_code=404, detail="No reference sessions found")
    return resolved


def _persist_plan_with_validation(
    *,
    plan: GeneratedPlan,
    target_distance_m: int | None,
) -> GeneratedPlan:
    validations = validate_generated_plan(
        target_id=plan.id,
        content_snapshot=plan.content_snapshot,
        target_distance_m=target_distance_m,
    )
    STORE.generated_plans[plan.id] = plan
    STORE.validation_results[plan.id] = validations
    return plan


def create_set_plan(payload: GenerateSetPlanRequest) -> GeneratedPlan:
    with STORE.lock:
        reference_sessions = _resolve_reference_sessions(payload.reference_session_ids)
        content_snapshot = build_set_content(
            GenerateSetInput(
                reference_sessions=reference_sessions,
                target_distance_m=payload.target_distance_m,
                focus_tags=payload.focus_tags,
            )
        )

        plan = GeneratedPlan(
            plan_type=PlanType.SESSION_PLAN,
            review_status=ReviewStatus.NEEDS_REVIEW,
            approval_status=ApprovalStatus.PENDING,
            reference_session_ids=[session.id for session in reference_sessions],
            content_snapshot=content_snapshot,
            notes="Generated set candidate (v1).",
            details_json={"generation_scope": "set", "target_distance_m": payload.target_distance_m},
        )
        return _persist_plan_with_validation(plan=plan, target_distance_m=payload.target_distance_m)


def create_session_plan(payload: GenerateSessionPlanRequest) -> GeneratedPlan:
    with STORE.lock:
        reference_sessions = _resolve_reference_sessions(payload.reference_session_ids)
        content_snapshot = build_session_content(
            GenerateSessionInput(
                reference_sessions=reference_sessions,
                target_distance_m=payload.target_distance_m,
                target_duration_min=payload.target_duration_min,
                focus_tags=payload.focus_tags,
            )
        )

        plan = GeneratedPlan(
            plan_type=PlanType.SESSION_PLAN,
            review_status=ReviewStatus.NEEDS_REVIEW,
            approval_status=ApprovalStatus.PENDING,
            reference_session_ids=[session.id for session in reference_sessions],
            content_snapshot=content_snapshot,
            notes="Generated session candidate (v1).",
            details_json={
                "generation_scope": "session",
                "target_distance_m": payload.target_distance_m,
                "target_duration_min": payload.target_duration_min,
            },
        )
        return _persist_plan_with_validation(plan=plan, target_distance_m=payload.target_distance_m)


def create_week_plan(payload: GenerateWeekPlanRequest) -> GeneratedPlan:
    with STORE.lock:
        reference_sessions = _resolve_reference_sessions(payload.reference_session_ids)
        content_snapshot = build_week_content(
            GenerateWeekInput(
                reference_sessions=reference_sessions,
                sessions_per_week=payload.sessions_per_week,
                target_total_distance_m=payload.target_total_distance_m,
                focus_tags=payload.focus_tags,
            )
        )

        plan = GeneratedPlan(
            plan_type=PlanType.WEEK_PLAN,
            review_status=ReviewStatus.NEEDS_REVIEW,
            approval_status=ApprovalStatus.PENDING,
            reference_session_ids=[session.id for session in reference_sessions],
            content_snapshot=content_snapshot,
            notes="Generated week plan candidate (v1).",
            details_json={
                "generation_scope": "week",
                "target_total_distance_m": payload.target_total_distance_m,
                "sessions_per_week": payload.sessions_per_week,
            },
        )
        return _persist_plan_with_validation(plan=plan, target_distance_m=payload.target_total_distance_m)


def get_generated_plan(plan_id: UUID) -> GeneratedPlanDetail | None:
    with STORE.lock:
        plan = STORE.generated_plans.get(plan_id)
        if plan is None:
            return None

        validation_results = STORE.validation_results.get(plan_id, [])

    return GeneratedPlanDetail(plan=plan, validation_results=validation_results)


def _approve_when_valid(plan: GeneratedPlan, validation_results: list[ValidationResult]) -> bool:
    has_error = any(result.severity.value == "error" for result in validation_results)
    if has_error:
        plan.approval_status = ApprovalStatus.REJECTED
        return False

    plan.review_status = ReviewStatus.REVIEWED
    plan.approval_status = ApprovalStatus.APPROVED
    return True


def approve_generated_plan(plan_id: UUID) -> GenerationApprovalResponse | None:
    with STORE.lock:
        plan = STORE.generated_plans.get(plan_id)
        if plan is None:
            return None

        target_distance = plan.details_json.get("target_distance_m")
        if not isinstance(target_distance, int):
            target_distance = plan.details_json.get("target_total_distance_m")
        if not isinstance(target_distance, int):
            target_distance = None

        validation_results = validate_generated_plan(
            target_id=plan.id,
            content_snapshot=plan.content_snapshot,
            target_distance_m=target_distance,
        )
        STORE.validation_results[plan.id] = validation_results
        approved = _approve_when_valid(plan, validation_results)

        return GenerationApprovalResponse(
            plan=plan,
            approved=approved,
            validation_results=validation_results,
        )
