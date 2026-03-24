"""Initial relational models for persistence foundation."""

from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from uuid import UUID, uuid4

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infra.db.base import Base


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


SOURCE_STATUS_VALUES = tuple(status.value for status in SourceStatus)
REVIEW_STATUS_VALUES = tuple(status.value for status in ReviewStatus)
APPROVAL_STATUS_VALUES = tuple(status.value for status in ApprovalStatus)


class SourceFileORM(Base):
    __tablename__ = "source_files"
    __table_args__ = (
        CheckConstraint(
            f"source_status IN {SOURCE_STATUS_VALUES}",
            name="source_status_allowed_values",
        ),
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    source_type: Mapped[str] = mapped_column(String(16), nullable=False)
    original_filename: Mapped[str | None] = mapped_column(Text, nullable=True)
    source_status: Mapped[str] = mapped_column(
        String(32), nullable=False, default=SourceStatus.UPLOADED.value
    )
    ingested_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=lambda: datetime.now(UTC)
    )
    raw_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    details_json: Mapped[dict[str, object]] = mapped_column(JSONB, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=lambda: datetime.now(UTC)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )

    sessions: Mapped[list[TrainingSessionORM]] = relationship(back_populates="source_file")


class TrainingSessionORM(Base):
    __tablename__ = "training_sessions"
    __table_args__ = (
        CheckConstraint("total_distance_m >= 0", name="total_distance_m_non_negative"),
        CheckConstraint("duration_min >= 0", name="duration_min_non_negative"),
        CheckConstraint(
            f"review_status IN {REVIEW_STATUS_VALUES}",
            name="training_session_review_status_allowed_values",
        ),
        CheckConstraint(
            f"approval_status IN {APPROVAL_STATUS_VALUES}",
            name="training_session_approval_status_allowed_values",
        ),
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    source_file_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("source_files.id", ondelete="RESTRICT"),
        nullable=False,
    )
    title: Mapped[str | None] = mapped_column(Text, nullable=True)
    review_status: Mapped[str] = mapped_column(
        String(24), nullable=False, default=ReviewStatus.NEEDS_REVIEW.value
    )
    approval_status: Mapped[str] = mapped_column(
        String(24), nullable=False, default=ApprovalStatus.PENDING.value
    )
    total_distance_m: Mapped[int | None] = mapped_column(Integer, nullable=True)
    duration_min: Mapped[int | None] = mapped_column(Integer, nullable=True)
    raw_snapshot: Mapped[dict[str, object]] = mapped_column(JSONB, nullable=False, default=dict)
    tags: Mapped[list[str]] = mapped_column(JSONB, nullable=False, default=list)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    details_json: Mapped[dict[str, object]] = mapped_column(JSONB, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=lambda: datetime.now(UTC)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )

    source_file: Mapped[SourceFileORM] = relationship(back_populates="sessions")
    blocks: Mapped[list[SessionBlockORM]] = relationship(
        back_populates="session", cascade="all, delete-orphan"
    )


class SessionBlockORM(Base):
    __tablename__ = "session_blocks"
    __table_args__ = (
        UniqueConstraint(
            "session_id",
            "order_index",
            name="uq_session_blocks_session_id_order_index",
        ),
        CheckConstraint("order_index >= 0", name="order_index_non_negative"),
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    session_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("training_sessions.id", ondelete="CASCADE"),
        nullable=False,
    )
    order_index: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str | None] = mapped_column(Text, nullable=True)
    block_type: Mapped[str | None] = mapped_column(String(64), nullable=True)
    raw_snapshot: Mapped[dict[str, object]] = mapped_column(JSONB, nullable=False, default=dict)
    details_json: Mapped[dict[str, object]] = mapped_column(JSONB, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=lambda: datetime.now(UTC)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )

    session: Mapped[TrainingSessionORM] = relationship(back_populates="blocks")
    sets: Mapped[list[TrainingSetORM]] = relationship(
        back_populates="block", cascade="all, delete-orphan"
    )


class TrainingSetORM(Base):
    __tablename__ = "training_sets"
    __table_args__ = (
        UniqueConstraint("block_id", "order_index", name="uq_training_sets_block_id_order_index"),
        CheckConstraint("order_index >= 0", name="set_order_index_non_negative"),
        CheckConstraint("distance_m >= 0", name="distance_m_non_negative"),
        CheckConstraint("duration_sec >= 0", name="duration_sec_non_negative"),
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    block_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("session_blocks.id", ondelete="CASCADE"),
        nullable=False,
    )
    order_index: Mapped[int] = mapped_column(Integer, nullable=False)
    label: Mapped[str | None] = mapped_column(Text, nullable=True)
    distance_m: Mapped[int | None] = mapped_column(Integer, nullable=True)
    duration_sec: Mapped[int | None] = mapped_column(Integer, nullable=True)
    intensity_note: Mapped[str | None] = mapped_column(Text, nullable=True)
    raw_snapshot: Mapped[dict[str, object]] = mapped_column(JSONB, nullable=False, default=dict)
    normalized_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    tags: Mapped[list[str]] = mapped_column(JSONB, nullable=False, default=list)
    details_json: Mapped[dict[str, object]] = mapped_column(JSONB, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=lambda: datetime.now(UTC)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )

    block: Mapped[SessionBlockORM] = relationship(back_populates="sets")


class GeneratedPlanORM(Base):
    __tablename__ = "generated_plans"
    __table_args__ = (
        CheckConstraint("is_generated = true", name="generated_plan_is_generated_true"),
        CheckConstraint(
            f"review_status IN {REVIEW_STATUS_VALUES}",
            name="generated_plan_review_status_allowed_values",
        ),
        CheckConstraint(
            f"approval_status IN {APPROVAL_STATUS_VALUES}",
            name="generated_plan_approval_status_allowed_values",
        ),
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    plan_type: Mapped[str] = mapped_column(String(32), nullable=False)
    is_generated: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    review_status: Mapped[str] = mapped_column(
        String(24), nullable=False, default=ReviewStatus.NEEDS_REVIEW.value
    )
    approval_status: Mapped[str] = mapped_column(
        String(24), nullable=False, default=ApprovalStatus.PENDING.value
    )
    reference_session_ids: Mapped[list[str]] = mapped_column(JSONB, nullable=False, default=list)
    content_snapshot: Mapped[dict[str, object]] = mapped_column(JSONB, nullable=False, default=dict)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    details_json: Mapped[dict[str, object]] = mapped_column(JSONB, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=lambda: datetime.now(UTC)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )


class ValidationResultORM(Base):
    __tablename__ = "validation_results"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    target_type: Mapped[str] = mapped_column(String(24), nullable=False)
    target_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    severity: Mapped[str] = mapped_column(String(16), nullable=False)
    rule_code: Mapped[str] = mapped_column(String(128), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    field_path: Mapped[str | None] = mapped_column(String(255), nullable=True)
    details_json: Mapped[dict[str, object]] = mapped_column(JSONB, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=lambda: datetime.now(UTC)
    )


Index(
    "ix_validation_results_target",
    ValidationResultORM.target_type,
    ValidationResultORM.target_id,
)
