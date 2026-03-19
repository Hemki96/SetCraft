from __future__ import annotations

from enum import StrEnum
from typing import Any

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.schemas.error import ErrorResponse


class ErrorCode(StrEnum):
    VALIDATION_ERROR = "VALIDATION_ERROR"
    NOT_FOUND = "NOT_FOUND"
    HTTP_ERROR = "HTTP_ERROR"
    INTERNAL_ERROR = "INTERNAL_ERROR"


def _build_error_response(
    *, code: ErrorCode, message: str, details: dict[str, Any] | None = None
) -> dict[str, Any]:
    return ErrorResponse(code=code, message=message, details=details).model_dump()


def configure_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(StarletteHTTPException)
    async def handle_http_exception(
        request: Request, exc: StarletteHTTPException
    ) -> JSONResponse:
        del request
        code = ErrorCode.NOT_FOUND if exc.status_code == 404 else ErrorCode.HTTP_ERROR
        message = str(exc.detail)
        payload = _build_error_response(code=code, message=message)
        return JSONResponse(status_code=exc.status_code, content=payload)

    @app.exception_handler(RequestValidationError)
    async def handle_validation_exception(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        del request
        payload = _build_error_response(
            code=ErrorCode.VALIDATION_ERROR,
            message="Request validation failed",
            details={"errors": exc.errors()},
        )
        return JSONResponse(status_code=422, content=payload)

    @app.exception_handler(Exception)
    async def handle_unexpected_exception(request: Request, exc: Exception) -> JSONResponse:
        del request
        del exc
        payload = _build_error_response(
            code=ErrorCode.INTERNAL_ERROR,
            message="Internal server error",
        )
        return JSONResponse(status_code=500, content=payload)
