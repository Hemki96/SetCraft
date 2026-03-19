from __future__ import annotations

import sys
from pathlib import Path
from uuid import uuid4

import pytest
from pydantic import ValidationError

SCHEMA_ROOT = Path(__file__).resolve().parents[2] / "packages" / "schemas" / "python"
sys.path.insert(0, str(SCHEMA_ROOT))

from training_plan_schemas.domain_v1 import (  # noqa: E402
    ApprovalStatus,
    GeneratedPlan,
    PlanType,
    ReviewStatus,
    SourceFile,
    SourceType,
    TrainingSession,
)


def test_source_file_forbids_unknown_fields() -> None:
    with pytest.raises(ValidationError):
        SourceFile(source_type=SourceType.TEXT, unexpected_field="x")


def test_training_session_requires_source_reference() -> None:
    with pytest.raises(ValidationError):
        TrainingSession()


def test_training_session_approval_requires_review() -> None:
    with pytest.raises(ValidationError):
        TrainingSession(
            source_file_id=uuid4(),
            review_status=ReviewStatus.NEEDS_REVIEW,
            approval_status=ApprovalStatus.APPROVED,
        )


def test_generated_plan_generation_marker_is_fixed() -> None:
    with pytest.raises(ValidationError):
        GeneratedPlan(plan_type=PlanType.WEEK_PLAN, is_generated=False)


def test_generated_plan_approval_requires_review() -> None:
    with pytest.raises(ValidationError):
        GeneratedPlan(
            plan_type=PlanType.SESSION_PLAN,
            review_status=ReviewStatus.NEEDS_REVIEW,
            approval_status=ApprovalStatus.APPROVED,
        )

