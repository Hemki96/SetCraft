from __future__ import annotations

import sys
from pathlib import Path

API_ROOT = Path(__file__).resolve().parents[2] / "services" / "api"
sys.path.insert(0, str(API_ROOT))

from app.core.config import get_settings


def test_settings_use_defaults_when_env_is_missing(monkeypatch) -> None:
    monkeypatch.delenv("APP_NAME", raising=False)
    monkeypatch.delenv("API_VERSION", raising=False)
    monkeypatch.delenv("APP_ENV", raising=False)
    monkeypatch.delenv("APP_DEBUG", raising=False)
    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.delenv("POSTGRES_DB", raising=False)
    monkeypatch.delenv("POSTGRES_USER", raising=False)
    monkeypatch.delenv("POSTGRES_PASSWORD", raising=False)
    monkeypatch.delenv("POSTGRES_HOST", raising=False)
    monkeypatch.delenv("POSTGRES_PORT", raising=False)

    get_settings.cache_clear()
    settings = get_settings()

    assert settings.service_name == "setcraft-api"
    assert settings.api_version == "v1"
    assert settings.environment == "development"
    assert settings.debug is False
    assert (
        settings.database_url
        == "postgresql+psycopg://postgres:postgres@localhost:5432/training_plan_platform"
    )


def test_settings_read_environment_values(monkeypatch) -> None:
    monkeypatch.setenv("APP_NAME", "setcraft-api-test")
    monkeypatch.setenv("API_VERSION", "v1")
    monkeypatch.setenv("APP_ENV", "test")
    monkeypatch.setenv("APP_DEBUG", "true")
    monkeypatch.setenv("POSTGRES_DB", "setcraft")
    monkeypatch.setenv("POSTGRES_USER", "setcraft_user")
    monkeypatch.setenv("POSTGRES_PASSWORD", "secret")
    monkeypatch.setenv("POSTGRES_HOST", "db")
    monkeypatch.setenv("POSTGRES_PORT", "5433")

    get_settings.cache_clear()
    settings = get_settings()

    assert settings.service_name == "setcraft-api-test"
    assert settings.api_version == "v1"
    assert settings.environment == "test"
    assert settings.debug is True
    assert settings.database_url == "postgresql+psycopg://setcraft_user:secret@db:5433/setcraft"


def test_database_url_prefers_explicit_value(monkeypatch) -> None:
    monkeypatch.setenv("DATABASE_URL", "postgresql+psycopg://custom:custom@custom-host:5432/custom_db")

    get_settings.cache_clear()
    settings = get_settings()

    assert (
        settings.database_url
        == "postgresql+psycopg://custom:custom@custom-host:5432/custom_db"
    )
