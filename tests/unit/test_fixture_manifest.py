from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
MANIFEST_PATH = REPO_ROOT / "tests" / "fixtures" / "fixture-manifest.json"


def _read_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def test_fixture_manifest_has_required_cases_per_source_type() -> None:
    manifest = _read_json(MANIFEST_PATH)
    cases = manifest["cases"]
    assert isinstance(cases, list)

    by_type_and_quality: dict[tuple[str, str], int] = {}
    for case in cases:
        assert isinstance(case, dict)
        source_type = case["source_type"]
        quality = case["quality"]
        assert isinstance(source_type, str)
        assert isinstance(quality, str)
        by_type_and_quality[(source_type, quality)] = (
            by_type_and_quality.get((source_type, quality), 0) + 1
        )

    for source_type in ("docx", "pdf", "text"):
        assert by_type_and_quality.get((source_type, "clean"), 0) >= 1
        assert by_type_and_quality.get((source_type, "problematic"), 0) >= 1


def test_manifest_paths_exist_and_have_expected_shape() -> None:
    manifest = _read_json(MANIFEST_PATH)
    cases = manifest["cases"]
    assert isinstance(cases, list)

    for case in cases:
        assert isinstance(case, dict)
        raw_path = REPO_ROOT / str(case["raw_file"])
        normalized_path = REPO_ROOT / str(case["normalized_file"])
        expected_path = REPO_ROOT / str(case["expected_file"])

        assert raw_path.exists(), f"missing raw fixture: {raw_path}"
        assert normalized_path.exists(), f"missing normalized fixture: {normalized_path}"
        assert expected_path.exists(), f"missing expected fixture: {expected_path}"

        normalized = _read_json(normalized_path)
        expected = _read_json(expected_path)

        assert "source_file" in normalized
        assert "training_session" in normalized
        assert "expected_status" in expected
        assert "expected_validation_flags" in expected


def test_manifest_expected_matches_normalized_structure() -> None:
    manifest = _read_json(MANIFEST_PATH)
    cases = manifest["cases"]
    assert isinstance(cases, list)

    for case in cases:
        assert isinstance(case, dict)
        normalized_path = REPO_ROOT / str(case["normalized_file"])
        expected_path = REPO_ROOT / str(case["expected_file"])

        normalized = _read_json(normalized_path)
        expected = _read_json(expected_path)

        source_file = normalized["source_file"]
        training_session = normalized["training_session"]
        assert isinstance(source_file, dict)
        assert isinstance(training_session, dict)

        actual_status = source_file.get("source_status")
        assert actual_status == expected["expected_status"]

        blocks = training_session.get("blocks")
        assert isinstance(blocks, list)
        assert len(blocks) == expected["expected_block_count"]

        set_count = 0
        for block in blocks:
            assert isinstance(block, dict)
            sets = block.get("sets")
            assert isinstance(sets, list)
            set_count += len(sets)

        assert set_count == expected["expected_set_count"]
        assert isinstance(expected["expected_validation_flags"], list)
