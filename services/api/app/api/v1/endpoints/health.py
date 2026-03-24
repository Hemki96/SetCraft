from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.core.config import get_settings
from app.domain.health import HealthService
from app.infra.health import SqlalchemyDatabaseProbe
from app.schemas.health import DatabaseHealthResponse, HealthResponse

router = APIRouter()


def _health_service() -> HealthService:
    return HealthService(settings=get_settings(), database_probe=SqlalchemyDatabaseProbe())


def check_database_connection() -> bool:
    return _health_service().is_database_healthy()


@router.get("", response_model=HealthResponse)
def get_health() -> HealthResponse:
    health = _health_service().get_service_health()
    return HealthResponse(
        status=health.status,
        service=health.service,
        version=health.version,
        environment=health.environment,
    )


@router.get("/db", response_model=DatabaseHealthResponse)
def get_database_health() -> DatabaseHealthResponse:
    if not check_database_connection():
        raise HTTPException(status_code=503, detail="Database unavailable")

    health = _health_service().get_database_health()
    return DatabaseHealthResponse(status=health.status, database=health.database)
