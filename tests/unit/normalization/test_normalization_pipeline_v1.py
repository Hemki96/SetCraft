from __future__ import annotations

from uuid import uuid4

from training_plan_schemas.domain_v1 import SourceType

from services.extraction import extract_from_source
from services.normalization import normalize_extraction_to_session


def test_normalization_maps_segments_to_blocks_and_sets() -> None:
    extraction = extract_from_source(
        source_type=SourceType.TEXT,
        content="Warmup:\n4x100m easy @1:40\nMain:\n6x50m race pace",
    )

    normalized = normalize_extraction_to_session(source_file_id=uuid4(), extraction=extraction)

    session = normalized.session
    assert len(session.blocks) == 2
    assert session.blocks[0].title == "Warmup"
    assert session.blocks[0].sets[0].distance_m == 400
    assert session.blocks[1].sets[0].distance_m == 300
    assert session.total_distance_m == 700


def test_normalization_stores_uncertainty_for_unstructured_line() -> None:
    extraction = extract_from_source(
        source_type=SourceType.TEXT,
        content="Main:\nTechnikfokus heute",
    )

    normalized = normalize_extraction_to_session(source_file_id=uuid4(), extraction=extraction)

    assert any(issue.code == "set_missing_primary_metric" for issue in normalized.issues)
    mapped_set = normalized.session.blocks[0].sets[0]
    assert mapped_set.distance_m is None
    assert mapped_set.extraction_confidence is not None
    assert mapped_set.extraction_confidence < extraction.confidence
    issues = normalized.session.details_json.get("normalization_issues")
    assert isinstance(issues, list)
    assert any(issue["code"] == "set_missing_primary_metric" for issue in issues)


def test_normalization_handles_empty_segments_with_fallback() -> None:
    extraction = extract_from_source(source_type=SourceType.TEXT, content="\n\n")

    normalized = normalize_extraction_to_session(source_file_id=uuid4(), extraction=extraction)

    assert normalized.session.blocks[0].sets[0].label == "Unstructured segment"
    assert any(issue.code == "normalization_fallback" for issue in normalized.issues)
