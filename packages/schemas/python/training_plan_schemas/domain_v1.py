"""Minimal domain model v1 for the MVP foundation."""

from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from typing import Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class StrictSchema(BaseModel):
    """Shared strict defaults for all schema models."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


class SourceType(StrEnum):
    DOCX = "docx"
    PDF = "pdf"
    TEXT = "text"


class SourceStatus(StrEnum):
    UPLOADED = "uploaded"
    QUEUED = "queued"
    EXTRACTING = "extracting"
    EXTRACTED = "extracted"
    NORMALIZING = "normalizing"
    NEEDS_REVIEW = "needs_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    FAILED = "failed"


class ReviewStatus(StrEnum):
    NEEDS_REVIEW = "needs_review"
    REVIEWED = "reviewed"
    CORRECTED = "corrected"


class ApprovalStatus(StrEnum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class SessionReviewStatus(StrEnum):
    PENDING_REVIEW = "pending_review"
    IN_REVIEW = "in_review"
    REVIEWED_WITH_CHANGES = "reviewed_with_changes"
    REVIEWED_OK = "reviewed_ok"


class SessionApprovalStatus(StrEnum):
    NOT_SUBMITTED = "not_submitted"
    SUBMITTED = "submitted"
    APPROVED = "approved"
    REJECTED = "rejected"


class PlanType(StrEnum):
    SESSION_PLAN = "session_plan"
    WEEK_PLAN = "week_plan"


class ReviewTargetType(StrEnum):
    SESSION = "session"
    GENERATED_PLAN = "generated_plan"


class ReviewDecisionType(StrEnum):
    REVIEWED = "reviewed"
    CORRECTED = "corrected"
    REJECTED = "rejected"


class ValidationSeverity(StrEnum):
    WARNING = "warning"
    ERROR = "error"


class SourceFile(StrictSchema):
    id: UUID = Field(default_factory=uuid4)
    source_type: SourceType
    original_filename: str | None = None
    source_status: SourceStatus = SourceStatus.UPLOADED
    ingested_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    raw_text: str | None = None
    extraction_confidence: float | None = Field(default=None, ge=0.0, le=1.0)
    details_json: dict[str, object] = Field(default_factory=dict)


class TrainingSet(StrictSchema):
    id: UUID = Field(default_factory=uuid4)
    order_index: int = Field(ge=0)
    label: str | None = None
    distance_m: int | None = Field(default=None, ge=0)
    duration_sec: int | None = Field(default=None, ge=0)
    intensity_note: str | None = None
    raw_snapshot: dict[str, object] = Field(default_factory=dict)
    extraction_confidence: float | None = Field(default=None, ge=0.0, le=1.0)
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
    extraction_confidence: float | None = Field(default=None, ge=0.0, le=1.0)
    details_json: dict[str, object] = Field(default_factory=dict)


class TrainingSession(StrictSchema):
    id: UUID = Field(default_factory=uuid4)
    source_file_id: UUID
    title: str | None = None
    review_status: SessionReviewStatus = SessionReviewStatus.PENDING_REVIEW
    approval_status: SessionApprovalStatus = SessionApprovalStatus.NOT_SUBMITTED
    total_distance_m: int | None = Field(default=None, ge=0)
    duration_min: int | None = Field(default=None, ge=0)
    blocks: list[SessionBlock] = Field(default_factory=list)
    raw_snapshot: dict[str, object] = Field(default_factory=dict)
    extraction_confidence: float | None = Field(default=None, ge=0.0, le=1.0)
    tags: list[str] = Field(default_factory=list)
    notes: str | None = None
    details_json: dict[str, object] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    @field_validator("review_status", mode="before")
    @classmethod
    def _normalize_legacy_review_status(
        cls, value: SessionReviewStatus | str
    ) -> SessionReviewStatus | str:
        legacy_map = {
            "needs_review": SessionReviewStatus.PENDING_REVIEW,
            "reviewed": SessionReviewStatus.REVIEWED_OK,
            "corrected": SessionReviewStatus.REVIEWED_WITH_CHANGES,
        }
        if isinstance(value, str):
            return legacy_map.get(value, value)
        return value

    @field_validator("approval_status", mode="before")
    @classmethod
    def _normalize_legacy_approval_status(
        cls, value: SessionApprovalStatus | str
    ) -> SessionApprovalStatus | str:
        legacy_map = {"pending": SessionApprovalStatus.NOT_SUBMITTED}
        if isinstance(value, str):
            return legacy_map.get(value, value)
        return value

    @model_validator(mode="after")
    def _ensure_approval_after_review(self) -> TrainingSession:
        if (
            self.approval_status == SessionApprovalStatus.APPROVED
            and self.review_status
            not in {
                SessionReviewStatus.REVIEWED_WITH_CHANGES,
                SessionReviewStatus.REVIEWED_OK,
            }
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
    confidence: float | None = Field(default=None, ge=0.0, le=1.0)
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
    review_status: SessionReviewStatus = SessionReviewStatus.PENDING_REVIEW
    approval_status: SessionApprovalStatus = SessionApprovalStatus.NOT_SUBMITTED
    reference_session_ids: list[UUID] = Field(default_factory=list)
    content_snapshot: dict[str, object] = Field(default_factory=dict)
    validation_results: list[ValidationResult] = Field(default_factory=list)
    notes: str | None = None
    details_json: dict[str, object] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    @field_validator("review_status", mode="before")
    @classmethod
    def _normalize_legacy_generated_review_status(
        cls, value: SessionReviewStatus | str
    ) -> SessionReviewStatus | str:
        legacy_map = {
            "needs_review": SessionReviewStatus.PENDING_REVIEW,
            "reviewed": SessionReviewStatus.REVIEWED_OK,
            "corrected": SessionReviewStatus.REVIEWED_WITH_CHANGES,
        }
        if isinstance(value, str):
            return legacy_map.get(value, value)
        return value

    @field_validator("approval_status", mode="before")
    @classmethod
    def _normalize_legacy_generated_approval_status(
        cls, value: SessionApprovalStatus | str
    ) -> SessionApprovalStatus | str:
        legacy_map = {"pending": SessionApprovalStatus.NOT_SUBMITTED}
        if isinstance(value, str):
            return legacy_map.get(value, value)
        return value

    @model_validator(mode="after")
    def _ensure_approval_after_review(self) -> GeneratedPlan:
        if (
            self.approval_status == SessionApprovalStatus.APPROVED
            and self.review_status
            not in {
                SessionReviewStatus.REVIEWED_WITH_CHANGES,
                SessionReviewStatus.REVIEWED_OK,
            }
        ):
            raise ValueError("generated plan cannot be approved before review")
        return self
