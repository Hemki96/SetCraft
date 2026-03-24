from __future__ import annotations

from uuid import UUID

from training_plan_schemas.domain_v1 import (
    ReviewTargetType,
    ValidationResult,
    ValidationSeverity,
)

_INTENSITY_LEVELS: dict[str, int] = {
    "easy": 1,
    "steady": 2,
    "threshold": 3,
    "race": 4,
    "max": 5,
}


def _to_validation(
    *,
    target_id: UUID,
    severity: ValidationSeverity,
    rule_code: str,
    message: str,
    details: dict[str, object] | None = None,
    field_path: str | None = None,
) -> ValidationResult:
    return ValidationResult(
        target_type=ReviewTargetType.GENERATED_PLAN,
        target_id=target_id,
        severity=severity,
        rule_code=rule_code,
        message=message,
        field_path=field_path,
        details_json=details or {},
    )


def _extract_blocks(content_snapshot: dict[str, object]) -> list[dict[str, object]]:
    blocks = content_snapshot.get("blocks")
    if isinstance(blocks, list):
        return [block for block in blocks if isinstance(block, dict)]

    sessions = content_snapshot.get("sessions")
    if not isinstance(sessions, list):
        return []

    collected: list[dict[str, object]] = []
    for session in sessions:
        if not isinstance(session, dict):
            continue
        session_blocks = session.get("blocks")
        if not isinstance(session_blocks, list):
            continue
        for block in session_blocks:
            if isinstance(block, dict):
                collected.append(block)

    return collected


def _collect_set_distances_and_intensities(
    blocks: list[dict[str, object]],
) -> tuple[int, list[tuple[str, int]]]:
    total_distance = 0
    intensities: list[tuple[str, int]] = []

    for block in blocks:
        sets = block.get("sets")
        if not isinstance(sets, list):
            continue
        for item in sets:
            if not isinstance(item, dict):
                continue
            distance = item.get("distance_m")
            if isinstance(distance, int):
                total_distance += distance

            intensity = item.get("intensity_note")
            if isinstance(intensity, str):
                level = _INTENSITY_LEVELS.get(intensity.lower())
                if level is not None:
                    intensities.append((intensity.lower(), level))

    return total_distance, intensities


def validate_generated_content(
    *,
    target_id: UUID,
    content_snapshot: dict[str, object],
    target_distance_m: int | None,
) -> list[ValidationResult]:
    results: list[ValidationResult] = []

    blocks = _extract_blocks(content_snapshot)
    if not blocks:
        results.append(
            _to_validation(
                target_id=target_id,
                severity=ValidationSeverity.ERROR,
                rule_code="missing_structure",
                message="Generated content must include blocks or week sessions with blocks.",
            )
        )
        return results

    for block_index, block in enumerate(blocks):
        sets = block.get("sets")
        if not isinstance(sets, list) or len(sets) == 0:
            results.append(
                _to_validation(
                    target_id=target_id,
                    severity=ValidationSeverity.ERROR,
                    rule_code="block_without_sets",
                    message="Each block must contain at least one set.",
                    field_path=f"blocks[{block_index}].sets",
                )
            )

    total_distance, intensities = _collect_set_distances_and_intensities(blocks)

    if target_distance_m and total_distance > 0:
        delta_ratio = abs(total_distance - target_distance_m) / target_distance_m
        if delta_ratio > 0.10:
            results.append(
                _to_validation(
                    target_id=target_id,
                    severity=ValidationSeverity.WARNING,
                    rule_code="distance_tolerance",
                    message="Total distance differs from target by more than 10%.",
                    details={
                        "target_distance_m": target_distance_m,
                        "actual_distance_m": total_distance,
                        "delta_ratio": round(delta_ratio, 4),
                    },
                )
            )

    for index in range(1, len(intensities)):
        prev_intensity, prev_level = intensities[index - 1]
        curr_intensity, curr_level = intensities[index]
        if curr_level - prev_level > 1:
            results.append(
                _to_validation(
                    target_id=target_id,
                    severity=ValidationSeverity.WARNING,
                    rule_code="intensity_jump",
                    message="Intensity jump between consecutive sets is larger than one level.",
                    details={
                        "from": prev_intensity,
                        "to": curr_intensity,
                    },
                )
            )
            break

    sessions = content_snapshot.get("sessions")
    if isinstance(sessions, list) and len(sessions) >= 2:
        session_distances = [
            session.get("total_distance_m")
            for session in sessions
            if isinstance(session, dict) and isinstance(session.get("total_distance_m"), int)
        ]
        for index in range(1, len(session_distances)):
            prev_distance = session_distances[index - 1]
            curr_distance = session_distances[index]
            if prev_distance <= 0:
                continue
            increase_ratio = (curr_distance - prev_distance) / prev_distance
            if increase_ratio > 0.35:
                results.append(
                    _to_validation(
                        target_id=target_id,
                        severity=ValidationSeverity.WARNING,
                        rule_code="weekly_load_jump",
                        message="Week plan contains a day-to-day load jump above 35%.",
                        details={
                            "from_distance_m": prev_distance,
                            "to_distance_m": curr_distance,
                            "increase_ratio": round(increase_ratio, 4),
                        },
                    )
                )
                break

    results.append(
        _to_validation(
            target_id=target_id,
            severity=ValidationSeverity.WARNING,
            rule_code="manual_review_required",
            message="Trainer review is required before approval.",
        )
    )

    return results
