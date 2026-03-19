"""Minimal domain model v1 for the MVP foundation."""

from __future__ import annotations

from datetime import UTC, datetime
from enum import Enum
from typing import Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field, model_validator


class StrictSchema(BaseModel):
    """Shared strict defaults for all schema models."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


class SourceType(str, Enum):
    DOCX = "docx"
    PDF = "pdf"
    TEXT = "text"


class SourceStatus(str, Enum):
    UPLOADED = "uploaded"
    QUEUED = "queued"
    EXTRACTING = "extracting"
    EXTRACTED = "extracted"
    NORMALIZING = "normalizing"
    NEEDS_REVIEW = "needs_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    FAILED = "failed"


class ReviewStatus(str, Enum):
    NEEDS_REVIEW = "needs_review"
    REVIEWED = "reviewed"
    CORRECTED = "corrected"


class ApprovalStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class PlanType(str, Enum):
    SESSION_PLAN = "session_plan"
    WEEK_PLAN = "week_plan"


class ReviewTargetType(str, Enum):
    SESSION = "session"
    GENERATED_PLAN = "generated_plan"


class ReviewDecisionType(str, Enum):
    REVIEWED = "reviewed"
    CORRECTED = "corrected"
    REJECTED = "rejected"


class ValidationSeverity(str, Enum):
    WARNING = "warning"
    ERROR = "error"


class SourceFile(StrictSchema):
    id: UUID = Field(default_factory=uuid4)
    source_type: SourceType
    original_filename: str | None = None
    source_status: SourceStatus = SourceStatus.UPLOADED
    ingested_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    raw_text: str | None = None
    details_json: dict[str, object] = Field(default_factory=dict)


class TrainingSet(StrictSchema):
    id: UUID = Field(default_factory=uuid4)
    order_index: int = Field(ge=0)
    label: str | None = None
    distance_m: int | None = Field(default=None, ge=0)
    duration_sec: int | None = Field(default=None, ge=0)
    intensity_note: str | None = None
    raw_snapshot: dict[str, object] = Field(default_factory=dict)
    normalized_notes: str | None = None
    tags: list[str] = Field(default_factory=list)
    details_json: dict[str, object] = Field(default_factory=dict)


class SessionBlock(StrictSchema):
    id: UUID = Field(default_factory=uuid4)
    order_index: int = Field(ge=0)
    title: str | None = None
    block_type: str | None = None
    sets: list[TrainingSet] = Field(default_factory=list)
    raw_snapshot: dict[str, object] = Field(default_factory=dict)
    details_json: dict[str, object] = Field(default_factory=dict)


class TrainingSession(StrictSchema):
    id: UUID = Field(default_factory=uuid4)
    source_file_id: UUID
    title: str | None = None
    review_status: ReviewStatus = ReviewStatus.NEEDS_REVIEW
    approval_status: ApprovalStatus = ApprovalStatus.PENDING
    total_distance_m: int | None = Field(default=None, ge=0)
    duration_min: int | None = Field(default=None, ge=0)
    blocks: list[SessionBlock] = Field(default_factory=list)
    raw_snapshot: dict[str, object] = Field(default_factory=dict)
    tags: list[str] = Field(default_factory=list)
    notes: str | None = None
    details_json: dict[str, object] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    @model_validator(mode="after")
    def _ensure_approval_after_review(self) -> TrainingSession:
        if (
            self.approval_status == ApprovalStatus.APPROVED
            and self.review_status == ReviewStatus.NEEDS_REVIEW
        ):
            raise ValueError(
                "training session cannot be approved before review is completed"
            )
        return self


class ValidationResult(StrictSchema):
    id: UUID = Field(default_factory=uuid4)
    target_type: ReviewTargetType
    target_id: UUID
    severity: ValidationSeverity
    rule_code: str
    message: str
    field_path: str | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    details_json: dict[str, object] = Field(default_factory=dict)


class ReviewDecision(StrictSchema):
    id: UUID = Field(default_factory=uuid4)
    target_type: ReviewTargetType
    target_id: UUID
    decision: ReviewDecisionType
    comment: str | None = None
    decided_by_user_id: UUID | None = None
    decided_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class GeneratedPlan(StrictSchema):
    id: UUID = Field(default_factory=uuid4)
    plan_type: PlanType
    is_generated: Literal[True] = True
    review_status: ReviewStatus = ReviewStatus.NEEDS_REVIEW
    approval_status: ApprovalStatus = ApprovalStatus.PENDING
    reference_session_ids: list[UUID] = Field(default_factory=list)
    content_snapshot: dict[str, object] = Field(default_factory=dict)
    validation_results: list[ValidationResult] = Field(default_factory=list)
    notes: str | None = None
    details_json: dict[str, object] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    @model_validator(mode="after")
    def _ensure_approval_after_review(self) -> GeneratedPlan:
        if (
            self.approval_status == ApprovalStatus.APPROVED
            and self.review_status == ReviewStatus.NEEDS_REVIEW
        ):
            raise ValueError("generated plan cannot be approved before review")
        return self

