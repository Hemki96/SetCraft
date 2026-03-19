from __future__ import annotations

from app.core.config import Settings
from app.infra.db.session import ping_database
from app.schemas.health import DatabaseHealthResponse, HealthResponse


def build_health_response(settings: Settings) -> HealthResponse:
    return HealthResponse(
        status="ok",
        service=settings.service_name,
        version=settings.api_version,
        environment=settings.environment,
    )


def check_database_connection() -> bool:
    try:
        return ping_database()
    except Exception:
        return False


def build_database_health_response() -> DatabaseHealthResponse:
    return DatabaseHealthResponse(status="ok", database="ok")
