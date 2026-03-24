"""initial core tables

Revision ID: 20260319_0001
Revises: None
Create Date: 2026-03-19 22:00:00
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "20260319_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        DO $$
        BEGIN
            IF EXISTS (SELECT 1 FROM pg_available_extensions WHERE name = 'vector') THEN
                CREATE EXTENSION IF NOT EXISTS vector;
            END IF;
        END $$;
        """
    )

    op.create_table(
        "source_files",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("source_type", sa.String(length=16), nullable=False),
        sa.Column("original_filename", sa.Text(), nullable=True),
        sa.Column("source_status", sa.String(length=32), nullable=False),
        sa.Column("ingested_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("raw_text", sa.Text(), nullable=True),
        sa.Column("details_json", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "source_status IN ('uploaded', 'queued', 'extracting', 'extracted', "
            "'normalizing', 'needs_review', 'approved', 'rejected', 'failed')",
            name="ck_source_files_source_status_allowed_values",
        ),
    )

    op.create_table(
        "training_sessions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("source_file_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("title", sa.Text(), nullable=True),
        sa.Column("review_status", sa.String(length=24), nullable=False),
        sa.Column("approval_status", sa.String(length=24), nullable=False),
        sa.Column("total_distance_m", sa.Integer(), nullable=True),
        sa.Column("duration_min", sa.Integer(), nullable=True),
        sa.Column("raw_snapshot", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("tags", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("details_json", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["source_file_id"], ["source_files.id"], ondelete="RESTRICT"),
        sa.CheckConstraint(
            "total_distance_m >= 0",
            name="ck_training_sessions_total_distance_m_non_negative",
        ),
        sa.CheckConstraint(
            "duration_min >= 0",
            name="ck_training_sessions_duration_min_non_negative",
        ),
        sa.CheckConstraint(
            "review_status IN ('needs_review', 'reviewed', 'corrected')",
            name="ck_training_sessions_training_session_review_status_allowed_values",
        ),
        sa.CheckConstraint(
            "approval_status IN ('pending', 'approved', 'rejected')",
            name="ck_training_sessions_training_session_approval_status_allowed_values",
        ),
    )

    op.create_table(
        "session_blocks",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("session_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("order_index", sa.Integer(), nullable=False),
        sa.Column("title", sa.Text(), nullable=True),
        sa.Column("block_type", sa.String(length=64), nullable=True),
        sa.Column("raw_snapshot", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("details_json", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["session_id"], ["training_sessions.id"], ondelete="CASCADE"),
        sa.UniqueConstraint(
            "session_id",
            "order_index",
            name="uq_session_blocks_session_id_order_index",
        ),
        sa.CheckConstraint("order_index >= 0", name="ck_session_blocks_order_index_non_negative"),
    )

    op.create_table(
        "training_sets",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("block_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("order_index", sa.Integer(), nullable=False),
        sa.Column("label", sa.Text(), nullable=True),
        sa.Column("distance_m", sa.Integer(), nullable=True),
        sa.Column("duration_sec", sa.Integer(), nullable=True),
        sa.Column("intensity_note", sa.Text(), nullable=True),
        sa.Column("raw_snapshot", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("normalized_notes", sa.Text(), nullable=True),
        sa.Column("tags", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("details_json", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["block_id"], ["session_blocks.id"], ondelete="CASCADE"),
        sa.UniqueConstraint(
            "block_id",
            "order_index",
            name="uq_training_sets_block_id_order_index",
        ),
        sa.CheckConstraint(
            "order_index >= 0",
            name="ck_training_sets_set_order_index_non_negative",
        ),
        sa.CheckConstraint("distance_m >= 0", name="ck_training_sets_distance_m_non_negative"),
        sa.CheckConstraint("duration_sec >= 0", name="ck_training_sets_duration_sec_non_negative"),
    )

    op.create_table(
        "generated_plans",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("plan_type", sa.String(length=32), nullable=False),
        sa.Column("is_generated", sa.Boolean(), nullable=False),
        sa.Column("review_status", sa.String(length=24), nullable=False),
        sa.Column("approval_status", sa.String(length=24), nullable=False),
        sa.Column("reference_session_ids", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("content_snapshot", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("details_json", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "is_generated = true",
            name="ck_generated_plans_generated_plan_is_generated_true",
        ),
        sa.CheckConstraint(
            "review_status IN ('needs_review', 'reviewed', 'corrected')",
            name="ck_generated_plans_generated_plan_review_status_allowed_values",
        ),
        sa.CheckConstraint(
            "approval_status IN ('pending', 'approved', 'rejected')",
            name="ck_generated_plans_generated_plan_approval_status_allowed_values",
        ),
    )

    op.create_table(
        "validation_results",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("target_type", sa.String(length=24), nullable=False),
        sa.Column("target_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("severity", sa.String(length=16), nullable=False),
        sa.Column("rule_code", sa.String(length=128), nullable=False),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("field_path", sa.String(length=255), nullable=True),
        sa.Column("details_json", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(
        "ix_validation_results_target",
        "validation_results",
        ["target_type", "target_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_validation_results_target", table_name="validation_results")
    op.drop_table("validation_results")
    op.drop_table("generated_plans")
    op.drop_table("training_sets")
    op.drop_table("session_blocks")
    op.drop_table("training_sessions")
    op.drop_table("source_files")
