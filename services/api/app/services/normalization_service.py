from __future__ import annotations

import re
from typing import Iterable
from uuid import UUID

from training_plan_schemas.domain_v1 import (
    SessionApprovalStatus,
    SessionBlock,
    SessionReviewStatus,
    TrainingSession,
    TrainingSet,
)

_DISTANCE_PATTERN = re.compile(r"(?P<reps>\d+)\s*x\s*(?P<distance>\d+)", re.IGNORECASE)


def _parse_set_line(line: str, order_index: int) -> TrainingSet:
    match = _DISTANCE_PATTERN.search(line)
    if match:
        reps = int(match.group("reps"))
        distance = int(match.group("distance"))
        distance_m = reps * distance
    else:
        distance_m = None

    return TrainingSet(
        order_index=order_index,
        label=line,
        distance_m=distance_m,
        raw_snapshot={"line": line},
    )


def normalize_to_session(*, source_file_id: UUID, segments: Iterable[str]) -> TrainingSession:
    segment_list = [segment for segment in segments if segment.strip()]
    sets = [_parse_set_line(line, idx) for idx, line in enumerate(segment_list)]
    if not sets:
        sets = [
            TrainingSet(
                order_index=0,
                label="Unstructured segment",
                raw_snapshot={"line": ""},
            )
        ]

    total_distance_m = sum(training_set.distance_m or 0 for training_set in sets)
    duration_min = max(20, len(sets) * 5)

    block = SessionBlock(
        order_index=0,
        title="Imported Block",
        block_type="mixed",
        sets=sets,
        raw_snapshot={"segments": segment_list},
    )

    return TrainingSession(
        source_file_id=source_file_id,
        title="Imported Session",
        review_status=SessionReviewStatus.PENDING_REVIEW,
        approval_status=SessionApprovalStatus.NOT_SUBMITTED,
        total_distance_m=total_distance_m,
        duration_min=duration_min,
        blocks=[block],
        raw_snapshot={"segments": segment_list},
        tags=["historical"],
        notes="Auto-normalized from source import.",
    )
