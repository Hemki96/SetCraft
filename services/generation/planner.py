from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from training_plan_schemas.domain_v1 import TrainingSession, TrainingSet


@dataclass(frozen=True)
class GenerateSetInput:
    reference_sessions: list[TrainingSession]
    target_distance_m: int | None
    focus_tags: list[str]


@dataclass(frozen=True)
class GenerateSessionInput:
    reference_sessions: list[TrainingSession]
    target_distance_m: int | None
    target_duration_min: int | None
    focus_tags: list[str]


@dataclass(frozen=True)
class GenerateWeekInput:
    reference_sessions: list[TrainingSession]
    sessions_per_week: int
    target_total_distance_m: int | None
    focus_tags: list[str]


def _collect_sets(reference_sessions: list[TrainingSession]) -> list[tuple[UUID, TrainingSet]]:
    items: list[tuple[UUID, TrainingSet]] = []
    for session in reference_sessions:
        for block in session.blocks:
            for training_set in block.sets:
                items.append((session.id, training_set))
    return items


def _focus_match_score(focus_tags: list[str], tags: list[str]) -> int:
    normalized_focus = {tag.lower() for tag in focus_tags}
    normalized_tags = {tag.lower() for tag in tags}
    return len(normalized_focus & normalized_tags)


def _pick_base_set(reference_sessions: list[TrainingSession], focus_tags: list[str]) -> tuple[UUID, TrainingSet] | None:
    candidates = _collect_sets(reference_sessions)
    if not candidates:
        return None

    def sort_key(item: tuple[UUID, TrainingSet]) -> tuple[int, int]:
        _, training_set = item
        return (_focus_match_score(focus_tags, training_set.tags), training_set.distance_m or 0)

    return max(candidates, key=sort_key)


def _clone_generated_set(
    *,
    order_index: int,
    base_session_id: UUID | None,
    base_set: TrainingSet | None,
    distance_m: int,
    suffix: str,
) -> dict[str, object]:
    if base_set is None:
        label = f"Generated {suffix}"
        intensity_note = "steady"
        tags = ["generated"]
        base_set_id: str | None = None
    else:
        label = base_set.label or f"Generated {suffix}"
        intensity_note = base_set.intensity_note or "steady"
        tags = sorted(set(base_set.tags + ["generated"]))
        base_set_id = str(base_set.id)

    return {
        "order_index": order_index,
        "label": f"{label} (generated)",
        "distance_m": max(distance_m, 0),
        "intensity_note": intensity_note,
        "tags": tags,
        "details_json": {
            "generated_from_session_id": str(base_session_id) if base_session_id else None,
            "generated_from_set_id": base_set_id,
        },
    }


def build_set_content(payload: GenerateSetInput) -> dict[str, object]:
    base = _pick_base_set(payload.reference_sessions, payload.focus_tags)
    base_session_id = base[0] if base else None
    base_set = base[1] if base else None

    target_distance = payload.target_distance_m
    if target_distance is None:
        target_distance = base_set.distance_m if base_set and base_set.distance_m else 200

    generated_set = _clone_generated_set(
        order_index=0,
        base_session_id=base_session_id,
        base_set=base_set,
        distance_m=target_distance,
        suffix="set",
    )

    return {
        "is_generated": True,
        "generator_version": "v1",
        "generation_kind": "set",
        "rules_applied": ["structured_reference_selection", "target_distance_passthrough"],
        "focus_tags": payload.focus_tags,
        "blocks": [
            {
                "order_index": 0,
                "title": "Generated Block",
                "block_type": "main",
                "sets": [generated_set],
            }
        ],
    }


def build_session_content(payload: GenerateSessionInput) -> dict[str, object]:
    base = _pick_base_set(payload.reference_sessions, payload.focus_tags)
    base_session_id = base[0] if base else None
    base_set = base[1] if base else None

    target_distance = payload.target_distance_m or 1800
    warmup_distance = int(target_distance * 0.2)
    main_distance = int(target_distance * 0.6)
    cooldown_distance = max(target_distance - warmup_distance - main_distance, 0)

    warmup_set = _clone_generated_set(
        order_index=0,
        base_session_id=base_session_id,
        base_set=base_set,
        distance_m=warmup_distance,
        suffix="warmup",
    )
    warmup_set["intensity_note"] = "easy"

    main_set = _clone_generated_set(
        order_index=0,
        base_session_id=base_session_id,
        base_set=base_set,
        distance_m=main_distance,
        suffix="main",
    )
    main_set["intensity_note"] = "threshold"

    cooldown_set = _clone_generated_set(
        order_index=0,
        base_session_id=base_session_id,
        base_set=base_set,
        distance_m=cooldown_distance,
        suffix="cooldown",
    )
    cooldown_set["intensity_note"] = "easy"

    return {
        "is_generated": True,
        "generator_version": "v1",
        "generation_kind": "session",
        "rules_applied": ["distance_split_20_60_20", "structured_reference_selection"],
        "focus_tags": payload.focus_tags,
        "target_duration_min": payload.target_duration_min,
        "blocks": [
            {
                "order_index": 0,
                "title": "Warmup",
                "block_type": "warmup",
                "sets": [warmup_set],
            },
            {
                "order_index": 1,
                "title": "Main",
                "block_type": "main",
                "sets": [main_set],
            },
            {
                "order_index": 2,
                "title": "Cooldown",
                "block_type": "cooldown",
                "sets": [cooldown_set],
            },
        ],
    }


def build_week_content(payload: GenerateWeekInput) -> dict[str, object]:
    sessions_per_week = max(1, payload.sessions_per_week)
    target_total_distance = payload.target_total_distance_m or (sessions_per_week * 1800)

    progression = [0.8, 1.0, 1.1, 0.9, 1.0, 0.85, 0.75]
    generated_sessions: list[dict[str, object]] = []

    for day_index in range(sessions_per_week):
        ratio = progression[day_index % len(progression)]
        day_target = max(int((target_total_distance / sessions_per_week) * ratio), 0)

        session_content = build_session_content(
            GenerateSessionInput(
                reference_sessions=payload.reference_sessions,
                target_distance_m=day_target,
                target_duration_min=None,
                focus_tags=payload.focus_tags,
            )
        )
        generated_sessions.append(
            {
                "day_index": day_index,
                "title": f"Week Session {day_index + 1}",
                "total_distance_m": day_target,
                "blocks": session_content.get("blocks", []),
            }
        )

    return {
        "is_generated": True,
        "generator_version": "v1",
        "generation_kind": "week",
        "rules_applied": [
            "session_progression_profile",
            "structured_reference_selection",
            "session_generation_v1",
        ],
        "focus_tags": payload.focus_tags,
        "sessions": generated_sessions,
    }
