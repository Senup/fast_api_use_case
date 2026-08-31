import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.tasks import router as tasks_router
from app.core.config import settings
from app.core.errors import AppError
from app.core.logging import configure_logging

configure_logging()

logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.app_name,
    description="A learning project for building production-minded REST APIs.",
    version=settings.app_version,
    debug=settings.debug,
)

app.include_router(tasks_router)


@app.on_event("startup")
def log_application_startup() -> None:
    """Log startup without exposing configuration values or secrets."""
    logger.info("Application started")


@app.exception_handler(AppError)
def handle_app_error(_: Request, exc: AppError) -> JSONResponse:
    """Convert expected application errors into a predictable API response."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.code,
                "message": exc.message,
            }
        },
    )


@app.exception_handler(Exception)
def handle_unexpected_error(_: Request, exc: Exception) -> JSONResponse:
    """Log unexpected failures and return a safe response to clients."""
    logger.exception("Unexpected application error", exc_info=exc)

    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": "internal_server_error",
                "message": "An unexpected error occurred.",
            }
        },
    )


@app.get("/health", tags=["Health"])
def health_check() -> dict[str, str]:
    """Return the API health status."""
    return {"status": "ok"}