from __future__ import annotations

from uuid import uuid4

import pytest
from pydantic import ValidationError
from training_plan_schemas.domain_v1 import (
    ApprovalStatus,
    GeneratedPlan,
    PlanType,
    ReviewStatus,
    SessionApprovalStatus,
    SessionReviewStatus,
    SourceFile,
    TrainingSession,
)


def test_source_file_forbids_unknown_fields() -> None:
    with pytest.raises(ValidationError):
        SourceFile.model_validate({"source_type": "text", "unexpected_field": "x"})


def test_training_session_requires_source_reference() -> None:
    with pytest.raises(ValidationError):
        TrainingSession.model_validate({})


def test_training_session_approval_requires_review() -> None:
    with pytest.raises(ValidationError):
        TrainingSession.model_validate(
            {
                "source_file_id": str(uuid4()),
                "review_status": SessionReviewStatus.PENDING_REVIEW,
                "approval_status": SessionApprovalStatus.APPROVED,
            }
        )


def test_generated_plan_generation_marker_is_fixed() -> None:
    with pytest.raises(ValidationError):
        GeneratedPlan.model_validate({"plan_type": PlanType.WEEK_PLAN, "is_generated": False})


def test_generated_plan_approval_requires_review() -> None:
    with pytest.raises(ValidationError):
        GeneratedPlan.model_validate(
            {
                "plan_type": PlanType.SESSION_PLAN,
                "review_status": ReviewStatus.NEEDS_REVIEW,
                "approval_status": ApprovalStatus.APPROVED,
            }
        )


def test_training_session_legacy_status_values_are_normalized() -> None:
    session = TrainingSession.model_validate(
        {
            "source_file_id": str(uuid4()),
            "review_status": "corrected",
            "approval_status": "pending",
        }
    )
    assert session.review_status == SessionReviewStatus.REVIEWED_WITH_CHANGES
    assert session.approval_status == SessionApprovalStatus.NOT_SUBMITTED


def test_generated_plan_legacy_status_values_are_normalized() -> None:
    plan = GeneratedPlan.model_validate(
        {
            "plan_type": PlanType.SESSION_PLAN,
            "review_status": "reviewed",
            "approval_status": "pending",
        }
    )
    assert plan.review_status == SessionReviewStatus.REVIEWED_OK
    assert plan.approval_status == SessionApprovalStatus.NOT_SUBMITTED


def test_training_session_extraction_confidence_must_be_between_zero_and_one() -> None:
    with pytest.raises(ValidationError):
        TrainingSession.model_validate(
            {
                "source_file_id": str(uuid4()),
                "extraction_confidence": 1.2,
            }
        )


def test_source_file_accepts_valid_extraction_confidence() -> None:
    source = SourceFile.model_validate(
        {
            "source_type": "text",
            "extraction_confidence": 0.67,
        }
    )
    assert source.extraction_confidence == pytest.approx(0.67)
