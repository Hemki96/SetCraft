from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from threading import Lock
from uuid import UUID, uuid4

from training_plan_schemas.domain_v1 import (
    GeneratedPlan,
    PlanType,
    SessionApprovalStatus,
    SessionBlock,
    SessionReviewStatus,
    SourceFile,
    TrainingSession,
    TrainingSet,
    ValidationResult,
)

from app.schemas.auth import UserRole
from app.schemas.exports import ExportFormat, ExportStatus


@dataclass
class SourceRecord:
    source: SourceFile
    content: str
    extraction_confidence: float | None = None
    session_ids: list[UUID] = field(default_factory=list)


@dataclass
class ExportJob:
    id: UUID
    generated_plan_id: UUID
    export_format: ExportFormat
    status: ExportStatus
    file_name: str | None
    created_at: datetime
    completed_at: datetime | None = None
    error_message: str | None = None


@dataclass
class AuditEvent:
    id: UUID
    occurred_at: datetime
    event_type: str
    action: str
    outcome: str
    actor_user_id: str
    actor_role: UserRole
    entity_type: str
    entity_id: str
    message: str
    details: dict[str, object] = field(default_factory=dict)


class AppStore:
    def __init__(self) -> None:
        self._lock = Lock()
        self.sources: dict[UUID, SourceRecord] = {}
        self.sessions: dict[UUID, TrainingSession] = {}
        self.generated_plans: dict[UUID, GeneratedPlan] = {}
        self.validation_results: dict[UUID, list[ValidationResult]] = {}
        self.export_jobs: dict[UUID, ExportJob] = {}
        self.export_paths: dict[UUID, str] = {}
        self.audit_events: list[AuditEvent] = []

    def next_uuid(self) -> UUID:
        return uuid4()

    def now(self) -> datetime:
        return datetime.now(UTC)

    @property
    def lock(self) -> Lock:
        return self._lock


STORE = AppStore()


def seed_placeholder_data() -> None:
    with STORE.lock:
        if STORE.sessions or STORE.generated_plans:
            return

        session = TrainingSession(
            id=UUID("11111111-1111-1111-1111-111111111111"),
            source_file_id=UUID("22222222-2222-2222-2222-222222222222"),
            title="Scaffold Session Placeholder",
            review_status=SessionReviewStatus.PENDING_REVIEW,
            approval_status=SessionApprovalStatus.NOT_SUBMITTED,
            total_distance_m=1600,
            duration_min=45,
            blocks=[
                SessionBlock(
                    order_index=0,
                    title="Warmup",
                    block_type="warmup",
                    raw_snapshot={"line": "400 easy swim"},
                    sets=[
                        TrainingSet(
                            order_index=0,
                            label="4x100 easy",
                            distance_m=400,
                            raw_snapshot={"line": "4x100 easy"},
                        )
                    ],
                )
            ],
            raw_snapshot={"source_excerpt": "Warmup 400m"},
            tags=["scaffold", "historical-placeholder"],
            notes="Placeholder only, no business logic.",
        )
        STORE.sessions[session.id] = session

        approved_plan = GeneratedPlan(
            id=UUID("44444444-4444-4444-4444-444444444444"),
            plan_type=PlanType.SESSION_PLAN,
            review_status=SessionReviewStatus.REVIEWED_OK,
            approval_status=SessionApprovalStatus.APPROVED,
            content_snapshot={
                "title": "Approved Sprint Session",
                "blocks": ["Warmup", "Main", "Cooldown"],
            },
        )
        pending_plan = GeneratedPlan(
            id=UUID("55555555-5555-5555-5555-555555555555"),
            plan_type=PlanType.WEEK_PLAN,
            review_status=SessionReviewStatus.REVIEWED_OK,
            approval_status=SessionApprovalStatus.NOT_SUBMITTED,
            content_snapshot={"title": "Pending Week Plan"},
        )

        STORE.generated_plans[approved_plan.id] = approved_plan
        STORE.generated_plans[pending_plan.id] = pending_plan


def reset_store() -> None:
    with STORE.lock:
        STORE.sources.clear()
        STORE.sessions.clear()
        STORE.generated_plans.clear()
        STORE.validation_results.clear()
        STORE.export_jobs.clear()
        STORE.export_paths.clear()
        STORE.audit_events.clear()


seed_placeholder_data()
