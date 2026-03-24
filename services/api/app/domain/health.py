from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from app.core.config import Settings


class DatabaseProbe(Protocol):
    def is_reachable(self) -> bool:
        ...


@dataclass(frozen=True)
class HealthStatus:
    service: str
    version: str
    environment: str
    status: str = "ok"


@dataclass(frozen=True)
class DatabaseHealthStatus:
    status: str = "ok"
    database: str = "ok"


class HealthService:
    def __init__(self, settings: Settings, database_probe: DatabaseProbe) -> None:
        self._settings = settings
        self._database_probe = database_probe

    def get_service_health(self) -> HealthStatus:
        return HealthStatus(
            status="ok",
            service=self._settings.service_name,
            version=self._settings.api_version,
            environment=self._settings.environment,
        )

    def is_database_healthy(self) -> bool:
        return self._database_probe.is_reachable()

    def get_database_health(self) -> DatabaseHealthStatus:
        return DatabaseHealthStatus(status="ok", database="ok")
