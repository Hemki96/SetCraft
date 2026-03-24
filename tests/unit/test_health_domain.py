from __future__ import annotations

from app.core.config import Settings
from app.domain.health import HealthService


class _Probe:
    def __init__(self, reachable: bool) -> None:
        self._reachable = reachable

    def is_reachable(self) -> bool:
        return self._reachable


def test_health_service_returns_expected_status_payload() -> None:
    settings = Settings(database_url="postgresql+psycopg://example")
    service = HealthService(settings=settings, database_probe=_Probe(reachable=True))

    payload = service.get_service_health()

    assert payload.status == "ok"
    assert payload.service == "setcraft-api"
    assert payload.version == "v1"
    assert payload.environment == "development"


def test_health_service_reports_database_unavailable() -> None:
    settings = Settings(database_url="postgresql+psycopg://example")
    service = HealthService(settings=settings, database_probe=_Probe(reachable=False))

    assert service.is_database_healthy() is False

