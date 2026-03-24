from __future__ import annotations

import re
from typing import Iterable
from uuid import UUID

from training_plan_schemas.domain_v1 import (
    SessionApprovalStatus,
    SessionBlock,
    SessionReviewStatus,
    SourceType,
    TrainingSession,
    TrainingSet,
)

from services.extraction.models import ExtractedSegment, ExtractionOutput, SegmentType

from .models import NormalizationIssue, NormalizationIssueSeverity, NormalizationOutput

_REPS_DISTANCE_PATTERN = re.compile(r"(?P<reps>\d+)\s*[x×]\s*(?P<distance>\d+)\s*m?", re.IGNORECASE)
_DISTANCE_PATTERN = re.compile(r"\b(?P<distance>\d{2,5})\s*m\b", re.IGNORECASE)
_DURATION_PATTERN = re.compile(r"\b(?P<minutes>\d{1,3})\s*min\b", re.IGNORECASE)
_INTERVAL_PATTERN = re.compile(
    r"(?:@|abgang\s*)(?P<interval>\d{1,2}:\d{2}|\d{1,3}\s*s)",
    re.IGNORECASE,
)
_REST_PATTERN = re.compile(r"(?:pause|rest)\s*(?P<rest>\d{1,2}:\d{2}|\d{1,3}\s*s)", re.IGNORECASE)
_INTENSITY_PATTERN = re.compile(r"\b(easy|locker|aerob|tempo|race|sprint)\b", re.IGNORECASE)


def _parse_set(
    segment: ExtractedSegment,
) -> tuple[TrainingSet, list[NormalizationIssue], int | None, int | None]:
    line = segment.text
    issues: list[NormalizationIssue] = []

    reps_distance = _REPS_DISTANCE_PATTERN.search(line)
    single_distance = _DISTANCE_PATTERN.search(line)
    duration_match = _DURATION_PATTERN.search(line)
    interval_match = _INTERVAL_PATTERN.search(line)
    rest_match = _REST_PATTERN.search(line)
    intensity_match = _INTENSITY_PATTERN.search(line)

    repetitions: int | None = None
    distance_per_rep_m: int | None = None
    distance_m: int | None = None

    if reps_distance:
        repetitions = int(reps_distance.group("reps"))
        distance_per_rep_m = int(reps_distance.group("distance"))
        distance_m = repetitions * distance_per_rep_m
    elif single_distance:
        distance_m = int(single_distance.group("distance"))

    duration_sec: int | None = None
    if duration_match:
        duration_sec = int(duration_match.group("minutes")) * 60

    if distance_m is None and duration_sec is None:
        issues.append(
            NormalizationIssue(
                code="set_missing_primary_metric",
                message="Set line has no parseable distance or duration.",
                segment_index=segment.order_index,
                confidence_impact=0.2,
            )
        )

    details_json: dict[str, object] = {
        "source_line": segment.source_line,
        "segment_type": segment.segment_type.value,
    }
    if repetitions is not None:
        details_json["repetitions"] = repetitions
    if distance_per_rep_m is not None:
        details_json["distance_per_rep_m"] = distance_per_rep_m
    if interval_match:
        details_json["interval"] = interval_match.group("interval")
    if rest_match:
        details_json["rest"] = rest_match.group("rest")

    training_set = TrainingSet(
        order_index=segment.order_index,
        label=line,
        distance_m=distance_m,
        duration_sec=duration_sec,
        intensity_note=intensity_match.group(0).lower() if intensity_match else None,
        raw_snapshot={"segment_text": line},
        extraction_confidence=max(
            0.0,
            min(1.0, segment.confidence - sum(i.confidence_impact for i in issues)),
        ),
        details_json=details_json,
    )

    return training_set, issues, distance_m, duration_sec


def normalize_extraction_to_session(
    *,
    source_file_id: UUID,
    extraction: ExtractionOutput,
) -> NormalizationOutput:
    blocks: list[SessionBlock] = []
    issues: list[NormalizationIssue] = []

    active_block_title = "Imported Block"
    active_sets: list[TrainingSet] = []
    block_order = 0

    total_distance_m = 0
    total_duration_sec = 0

    def flush_block() -> None:
        nonlocal block_order, active_sets, active_block_title
        if not active_sets:
            return

        block_confidence = sum(
            s.extraction_confidence or 0.0 for s in active_sets
        ) / len(active_sets)
        blocks.append(
            SessionBlock(
                order_index=block_order,
                title=active_block_title,
                block_type="mixed",
                sets=active_sets,
                raw_snapshot={"source": "normalization-v1"},
                extraction_confidence=block_confidence,
            )
        )
        block_order += 1
        active_sets = []

    for segment in extraction.segments:
        if segment.segment_type == SegmentType.BLOCK_HEADER:
            flush_block()
            active_block_title = segment.text.rstrip(":").strip() or f"Block {block_order + 1}"
            continue

        training_set, set_issues, distance_m, duration_sec = _parse_set(segment)
        training_set.order_index = len(active_sets)
        active_sets.append(training_set)
        issues.extend(set_issues)

        if distance_m is not None:
            total_distance_m += distance_m
        if duration_sec is not None:
            total_duration_sec += duration_sec

        if segment.segment_type == SegmentType.FREE_TEXT:
            issues.append(
                NormalizationIssue(
                    code="inconsistent_set_format",
                    message="Free-text segment was mapped as a set and should be reviewed.",
                    segment_index=segment.order_index,
                    confidence_impact=0.1,
                )
            )

    flush_block()

    if not blocks:
        fallback_set = TrainingSet(
            order_index=0,
            label="Unstructured segment",
            raw_snapshot={"segment_text": extraction.raw_text},
            extraction_confidence=max(0.0, extraction.confidence - 0.3),
            details_json={"fallback": True},
        )
        blocks = [
            SessionBlock(
                order_index=0,
                title="Imported Block",
                block_type="mixed",
                sets=[fallback_set],
                raw_snapshot={"source": "normalization-v1-fallback"},
                extraction_confidence=fallback_set.extraction_confidence,
            )
        ]
        issues.append(
            NormalizationIssue(
                code="normalization_fallback",
                message="No segments could be mapped; fallback block created.",
                severity=NormalizationIssueSeverity.ERROR,
                confidence_impact=0.3,
            )
        )

    avg_issue_impact = sum(issue.confidence_impact for issue in issues)
    normalized_confidence = max(0.0, min(1.0, extraction.confidence - avg_issue_impact))

    duration_min = (
        total_duration_sec // 60
        if total_duration_sec > 0
        else max(20, len(blocks[0].sets) * 5)
    )

    session = TrainingSession(
        source_file_id=source_file_id,
        title="Imported Session",
        review_status=SessionReviewStatus.PENDING_REVIEW,
        approval_status=SessionApprovalStatus.NOT_SUBMITTED,
        total_distance_m=total_distance_m if total_distance_m > 0 else None,
        duration_min=duration_min,
        blocks=blocks,
        raw_snapshot={
            "segment_count": len(extraction.segments),
            "source_type": extraction.source_type.value,
        },
        extraction_confidence=normalized_confidence,
        tags=["historical", "auto-normalized"],
        notes="Auto-normalized from source import. Review recommended for uncertain fields.",
        details_json={
            "normalization_issues": [issue.model_dump() for issue in issues],
            "extraction_trace": extraction.trace,
        },
    )

    return NormalizationOutput(
        session=session,
        confidence=normalized_confidence,
        issues=issues,
        trace={
            "block_count": len(blocks),
            "set_count": sum(len(block.sets) for block in blocks),
            "issue_count": len(issues),
        },
    )


def normalize_segments_to_session(
    *,
    source_file_id: UUID,
    segments: Iterable[str],
) -> NormalizationOutput:
    segment_models = [
        ExtractedSegment(
            order_index=index,
            text=segment.strip(),
            segment_type=SegmentType.SET_LINE,
            confidence=0.8,
            source_line=index + 1,
        )
        for index, segment in enumerate(segment for segment in segments if segment.strip())
    ]

    extraction = ExtractionOutput(
        source_type=SourceType.TEXT,
        raw_text="\n".join(segment.text for segment in segment_models),
        segments=segment_models,
        confidence=0.8,
    )
    return normalize_extraction_to_session(source_file_id=source_file_id, extraction=extraction)
