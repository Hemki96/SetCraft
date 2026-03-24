from __future__ import annotations

from uuid import UUID

from fastapi import HTTPException
from training_plan_schemas.domain_v1 import (
    GeneratedPlan,
    PlanType,
    SessionApprovalStatus,
    SessionReviewStatus,
    TrainingSession,
)

from app.schemas.generation import (
    GeneratedPlanDetail,
    GeneratedPlanReviewCompleteRequest,
    GenerateSessionPlanRequest,
    GenerateSetPlanRequest,
    GenerateWeekPlanRequest,
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


class GeneratedPlanEntityNotFoundError(LookupError):
    pass


class GeneratedPlanTransitionConflictError(ValueError):
    pass


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


def _transition_error(action: str, plan: GeneratedPlan, reason: str) -> str:
    return (
        f"Invalid transition for {action}: {reason} "
        f"(review_status={plan.review_status.value}, "
        f"approval_status={plan.approval_status.value})"
    )


def _append_review_history(plan: GeneratedPlan, comment: str | None, event: str) -> None:
    existing_history_raw = plan.details_json.get("review_history", [])
    existing_history = (
        list(existing_history_raw) if isinstance(existing_history_raw, list) else []
    )
    existing_history.append(
        {
            "event": event,
            "comment": comment,
            "review_status": plan.review_status.value,
            "approval_status": plan.approval_status.value,
            "timestamp": STORE.now().isoformat(),
        }
    )
    plan.details_json["review_history"] = existing_history


def _target_distance_from_plan(plan: GeneratedPlan) -> int | None:
    target_distance = plan.details_json.get("target_distance_m")
    if not isinstance(target_distance, int):
        target_distance = plan.details_json.get("target_total_distance_m")
    if not isinstance(target_distance, int):
        target_distance = None
    return target_distance


def _approve_with_validation(plan: GeneratedPlan) -> GenerationApprovalResponse:
    target_distance = _target_distance_from_plan(plan)
    validation_results = validate_generated_plan(
        target_id=plan.id,
        content_snapshot=plan.content_snapshot,
        target_distance_m=target_distance,
    )
    STORE.validation_results[plan.id] = validation_results

    has_error = any(result.severity.value == "error" for result in validation_results)
    if has_error:
        plan.approval_status = SessionApprovalStatus.REJECTED
        return GenerationApprovalResponse(
            plan=plan,
            approved=False,
            validation_results=validation_results,
        )

    plan.approval_status = SessionApprovalStatus.APPROVED
    return GenerationApprovalResponse(
        plan=plan,
        approved=True,
        validation_results=validation_results,
    )


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
            review_status=SessionReviewStatus.PENDING_REVIEW,
            approval_status=SessionApprovalStatus.NOT_SUBMITTED,
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
            review_status=SessionReviewStatus.PENDING_REVIEW,
            approval_status=SessionApprovalStatus.NOT_SUBMITTED,
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
            review_status=SessionReviewStatus.PENDING_REVIEW,
            approval_status=SessionApprovalStatus.NOT_SUBMITTED,
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


def start_generated_plan_review(plan_id: UUID) -> GeneratedPlan:
    with STORE.lock:
        plan = STORE.generated_plans.get(plan_id)
        if plan is None:
            raise GeneratedPlanEntityNotFoundError("Generated plan not found")
        if plan.review_status == SessionReviewStatus.IN_REVIEW:
            raise GeneratedPlanTransitionConflictError(
                _transition_error(
                    "generated_plan.review.start",
                    plan,
                    "plan is already in review",
                )
            )
        if plan.approval_status == SessionApprovalStatus.APPROVED:
            raise GeneratedPlanTransitionConflictError(
                _transition_error(
                    "generated_plan.review.start",
                    plan,
                    "approved plans must be changed before review restart",
                )
            )

        plan.review_status = SessionReviewStatus.IN_REVIEW
        _append_review_history(plan, comment=None, event="review_started")
        return plan


def complete_generated_plan_review(
    plan_id: UUID,
    payload: GeneratedPlanReviewCompleteRequest,
) -> GeneratedPlan:
    with STORE.lock:
        plan = STORE.generated_plans.get(plan_id)
        if plan is None:
            raise GeneratedPlanEntityNotFoundError("Generated plan not found")
        if plan.review_status != SessionReviewStatus.IN_REVIEW:
            raise GeneratedPlanTransitionConflictError(
                _transition_error(
                    "generated_plan.review.complete",
                    plan,
                    "plan must be in_review before completion",
                )
            )
        if payload.review_status not in {
            SessionReviewStatus.REVIEWED_WITH_CHANGES,
            SessionReviewStatus.REVIEWED_OK,
        }:
            raise GeneratedPlanTransitionConflictError(
                _transition_error(
                    "generated_plan.review.complete",
                    plan,
                    "review_status must be reviewed_with_changes or reviewed_ok",
                )
            )

        plan.review_status = payload.review_status
        if plan.approval_status == SessionApprovalStatus.REJECTED:
            plan.approval_status = SessionApprovalStatus.NOT_SUBMITTED
        _append_review_history(plan, comment=payload.comment, event="review_completed")
        return plan


def submit_generated_plan_approval(plan_id: UUID) -> GeneratedPlan:
    with STORE.lock:
        plan = STORE.generated_plans.get(plan_id)
        if plan is None:
            raise GeneratedPlanEntityNotFoundError("Generated plan not found")
        if plan.review_status not in {
            SessionReviewStatus.REVIEWED_WITH_CHANGES,
            SessionReviewStatus.REVIEWED_OK,
        }:
            raise GeneratedPlanTransitionConflictError(
                _transition_error(
                    "generated_plan.submit-approval",
                    plan,
                    "plan must be reviewed before submit",
                )
            )
        if plan.approval_status not in {
            SessionApprovalStatus.NOT_SUBMITTED,
            SessionApprovalStatus.REJECTED,
        }:
            raise GeneratedPlanTransitionConflictError(
                _transition_error(
                    "generated_plan.submit-approval",
                    plan,
                    "approval can only be submitted from not_submitted or rejected",
                )
            )

        plan.approval_status = SessionApprovalStatus.SUBMITTED
        _append_review_history(plan, comment=None, event="approval_submitted")
        return plan


def approve_generated_plan_transition(plan_id: UUID) -> GenerationApprovalResponse:
    with STORE.lock:
        plan = STORE.generated_plans.get(plan_id)
        if plan is None:
            raise GeneratedPlanEntityNotFoundError("Generated plan not found")
        if plan.review_status not in {
            SessionReviewStatus.REVIEWED_WITH_CHANGES,
            SessionReviewStatus.REVIEWED_OK,
        }:
            raise GeneratedPlanTransitionConflictError(
                _transition_error(
                    "generated_plan.approve",
                    plan,
                    "plan must be reviewed before approval",
                )
            )
        if plan.approval_status != SessionApprovalStatus.SUBMITTED:
            raise GeneratedPlanTransitionConflictError(
                _transition_error(
                    "generated_plan.approve",
                    plan,
                    "approval_status must be submitted before approval",
                )
            )

        response = _approve_with_validation(plan)
        _append_review_history(plan, comment=None, event="approval_processed")
        return response


def reject_generated_plan_approval(plan_id: UUID, comment: str | None) -> GeneratedPlan:
    with STORE.lock:
        plan = STORE.generated_plans.get(plan_id)
        if plan is None:
            raise GeneratedPlanEntityNotFoundError("Generated plan not found")
        if plan.approval_status != SessionApprovalStatus.SUBMITTED:
            raise GeneratedPlanTransitionConflictError(
                _transition_error(
                    "generated_plan.reject",
                    plan,
                    "approval_status must be submitted before rejection",
                )
            )

        plan.approval_status = SessionApprovalStatus.REJECTED
        _append_review_history(plan, comment=comment, event="approval_rejected")
        return plan


def approve_generated_plan(plan_id: UUID) -> GenerationApprovalResponse | None:
    with STORE.lock:
        plan = STORE.generated_plans.get(plan_id)
        if plan is None:
            return None

        # Compatibility wrapper for existing endpoint/tests.
        if plan.review_status == SessionReviewStatus.PENDING_REVIEW:
            plan.review_status = SessionReviewStatus.REVIEWED_OK
            _append_review_history(plan, comment=None, event="review_auto_completed")
        if plan.approval_status in {
            SessionApprovalStatus.NOT_SUBMITTED,
            SessionApprovalStatus.REJECTED,
        }:
            plan.approval_status = SessionApprovalStatus.SUBMITTED
            _append_review_history(plan, comment=None, event="approval_auto_submitted")

        if plan.approval_status == SessionApprovalStatus.APPROVED:
            validation_results = STORE.validation_results.get(plan.id, [])
            return GenerationApprovalResponse(
                plan=plan,
                approved=True,
                validation_results=validation_results,
            )

        response = _approve_with_validation(plan)
        _append_review_history(plan, comment=None, event="approval_processed")
        return response
