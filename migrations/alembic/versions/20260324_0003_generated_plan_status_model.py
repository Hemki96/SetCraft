"""migrate generated plan status model to explicit review/approval states

Revision ID: 20260324_0003
Revises: 20260324_0002
Create Date: 2026-03-24 12:05:00
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "20260324_0003"
down_revision = "20260324_0002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        UPDATE generated_plans
        SET review_status = CASE review_status
            WHEN 'needs_review' THEN 'pending_review'
            WHEN 'reviewed' THEN 'reviewed_ok'
            WHEN 'corrected' THEN 'reviewed_with_changes'
            ELSE review_status
        END
        """
    )
    op.execute(
        """
        UPDATE generated_plans
        SET approval_status = CASE approval_status
            WHEN 'pending' THEN 'not_submitted'
            ELSE approval_status
        END
        """
    )

    op.drop_constraint(
        "ck_generated_plans_generated_plan_review_status_allowed_values",
        "generated_plans",
        type_="check",
    )
    op.drop_constraint(
        "ck_generated_plans_generated_plan_approval_status_allowed_values",
        "generated_plans",
        type_="check",
    )
    op.create_check_constraint(
        "ck_generated_plans_generated_plan_review_status_allowed_values",
        "generated_plans",
        "review_status IN ('pending_review', 'in_review', 'reviewed_with_changes', 'reviewed_ok')",
    )
    op.create_check_constraint(
        "ck_generated_plans_generated_plan_approval_status_allowed_values",
        "generated_plans",
        "approval_status IN ('not_submitted', 'submitted', 'approved', 'rejected')",
    )
    op.alter_column("generated_plans", "review_status", type_=sa.String(length=32))


def downgrade() -> None:
    op.execute(
        """
        UPDATE generated_plans
        SET review_status = CASE review_status
            WHEN 'pending_review' THEN 'needs_review'
            WHEN 'in_review' THEN 'needs_review'
            WHEN 'reviewed_with_changes' THEN 'corrected'
            WHEN 'reviewed_ok' THEN 'reviewed'
            ELSE review_status
        END
        """
    )
    op.execute(
        """
        UPDATE generated_plans
        SET approval_status = CASE approval_status
            WHEN 'not_submitted' THEN 'pending'
            WHEN 'submitted' THEN 'pending'
            ELSE approval_status
        END
        """
    )

    op.drop_constraint(
        "ck_generated_plans_generated_plan_review_status_allowed_values",
        "generated_plans",
        type_="check",
    )
    op.drop_constraint(
        "ck_generated_plans_generated_plan_approval_status_allowed_values",
        "generated_plans",
        type_="check",
    )
    op.create_check_constraint(
        "ck_generated_plans_generated_plan_review_status_allowed_values",
        "generated_plans",
        "review_status IN ('needs_review', 'reviewed', 'corrected')",
    )
    op.create_check_constraint(
        "ck_generated_plans_generated_plan_approval_status_allowed_values",
        "generated_plans",
        "approval_status IN ('pending', 'approved', 'rejected')",
    )
    op.alter_column("generated_plans", "review_status", type_=sa.String(length=24))
