from __future__ import annotations

from app.core.config import Settings
from app.schemas.health import HealthResponse


def build_health_response(settings: Settings) -> HealthResponse:
    return HealthResponse(
        status="ok",
        service=settings.service_name,
        version=settings.api_version,
        environment=settings.environment,
    )
