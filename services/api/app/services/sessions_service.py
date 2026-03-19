from __future__ import annotations

from uuid import UUID

from training_plan_schemas.domain_v1 import (
    ApprovalStatus,
    ReviewStatus,
    SessionBlock,
    TrainingSession,
    TrainingSet,
)

from app.schemas.sessions import SessionListResponse

_PLACEHOLDER_SESSION = TrainingSession(
    id=UUID("11111111-1111-1111-1111-111111111111"),
    source_file_id=UUID("22222222-2222-2222-2222-222222222222"),
    title="Scaffold Session Placeholder",
    review_status=ReviewStatus.NEEDS_REVIEW,
    approval_status=ApprovalStatus.PENDING,
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


def list_sessions_placeholder() -> SessionListResponse:
    return SessionListResponse(items=[_PLACEHOLDER_SESSION])


def list_session_items_placeholder() -> list[TrainingSession]:
    return [_PLACEHOLDER_SESSION]


def get_session_placeholder(session_id: UUID) -> TrainingSession | None:
    if session_id == _PLACEHOLDER_SESSION.id:
        return _PLACEHOLDER_SESSION
    return None
