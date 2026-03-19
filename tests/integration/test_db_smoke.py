from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest

pytest.importorskip("alembic")
pytest.importorskip("sqlalchemy")
from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, inspect
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

API_ROOT = Path(__file__).resolve().parents[2] / "services" / "api"
if str(API_ROOT) not in sys.path:
    sys.path.insert(0, str(API_ROOT))

from app.infra.db.models import (  # noqa: E402
    GeneratedPlanORM,
    SessionBlockORM,
    SourceFileORM,
    TrainingSessionORM,
    TrainingSetORM,
    ValidationResultORM,
)


@pytest.fixture
def db_url(monkeypatch: pytest.MonkeyPatch) -> str:
    configured = os.getenv("TEST_DATABASE_URL") or os.getenv("DATABASE_URL")
    if not configured:
        pytest.skip("Set TEST_DATABASE_URL or DATABASE_URL for integration DB smoke tests")

    monkeypatch.setenv("DATABASE_URL", configured)
    return configured


@pytest.fixture
def migrated_engine(db_url: str):
    config = Config(str(Path(__file__).resolve().parents[2] / "migrations" / "alembic.ini"))
    command.upgrade(config, "head")

    engine = create_engine(db_url, future=True)
    try:
        yield engine
    finally:
        engine.dispose()


def test_migrations_create_expected_tables(migrated_engine) -> None:
    inspector = inspect(migrated_engine)

    expected_tables = {
        "source_files",
        "training_sessions",
        "session_blocks",
        "training_sets",
        "generated_plans",
        "validation_results",
    }

    assert expected_tables.issubset(set(inspector.get_table_names()))


def test_core_entities_can_be_persisted_and_generated_marker_is_enforced(
    migrated_engine,
) -> None:
    with Session(migrated_engine) as session:
        source = SourceFileORM(source_type="text", original_filename="plan.txt")
        session.add(source)
        session.flush()

        training_session = TrainingSessionORM(source_file_id=source.id, title="Monday")
        session.add(training_session)
        session.flush()

        block = SessionBlockORM(session_id=training_session.id, order_index=0, title="Warmup")
        session.add(block)
        session.flush()

        training_set = TrainingSetORM(block_id=block.id, order_index=0, label="4x50 drill")
        session.add(training_set)

        generated_plan = GeneratedPlanORM(plan_type="week_plan", is_generated=True)
        session.add(generated_plan)
        session.flush()

        validation_result = ValidationResultORM(
            target_type="generated_plan",
            target_id=generated_plan.id,
            severity="warning",
            rule_code="distance_tolerance",
            message="Distance differs from target",
        )
        session.add(validation_result)

        session.commit()

    with Session(migrated_engine) as session:
        violating_plan = GeneratedPlanORM(plan_type="session_plan", is_generated=False)
        session.add(violating_plan)
        with pytest.raises(IntegrityError):
            session.flush()
