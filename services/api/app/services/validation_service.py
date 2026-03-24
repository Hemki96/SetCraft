from __future__ import annotations

from uuid import UUID

from training_plan_schemas.domain_v1 import ValidationResult

from services.validation.rules import validate_generated_content


def validate_generated_plan(
    *,
    target_id: UUID,
    content_snapshot: dict[str, object],
    target_distance_m: int | None,
) -> list[ValidationResult]:
    return validate_generated_content(
        target_id=target_id,
        content_snapshot=content_snapshot,
        target_distance_m=target_distance_m,
    )
