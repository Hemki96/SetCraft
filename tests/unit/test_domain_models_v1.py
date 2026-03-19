from __future__ import annotations

from uuid import uuid4

import pytest
from pydantic import ValidationError
from training_plan_schemas.domain_v1 import (
    ApprovalStatus,
    GeneratedPlan,
    PlanType,
    ReviewStatus,
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
                "review_status": ReviewStatus.NEEDS_REVIEW,
                "approval_status": ApprovalStatus.APPROVED,
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
