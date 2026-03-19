from __future__ import annotations

from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import get_settings
from app.core.errors import configure_exception_handlers


def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title=settings.service_name,
        version=settings.api_version,
        debug=settings.debug,
    )
    app.include_router(api_router)
    configure_exception_handlers(app)
    return app


app = create_app()
