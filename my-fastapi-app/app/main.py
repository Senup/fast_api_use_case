# Standard-library logging is used for application and unexpected-error logs.
import logging

# FastAPI creates the application and request type.
# JSONResponse lets exception handlers control the HTTP response body and status.
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

# Import the task router so its endpoints can be registered on the main app.
from app.api.tasks import router as tasks_router
# Settings centralize environment-based application configuration.
from app.core.config import settings
# AppError represents expected, application-level failures.
from app.core.errors import AppError
# Configure logging before the application starts handling requests.
from app.core.logging import configure_logging

configure_logging()

# Create a module-level logger whose name identifies this module in log output.
logger = logging.getLogger(__name__)

# Construct the FastAPI application using centralized configuration.
app = FastAPI(
    title=settings.app_name,
    description="A learning project for building production-minded REST APIs.",
    version=settings.app_version,
    debug=settings.debug,
)

# Mount the task endpoints under the main application.
app.include_router(tasks_router)

# Run this function when the FastAPI application starts.
@app.on_event("startup")
def log_application_startup() -> None:
    """Log startup without exposing configuration values or secrets."""
    logger.info("Application started")


# Convert expected application errors into the API's standard error format.
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


# Prevent unexpected internal details from being exposed to API clients.
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

# Expose a small endpoint used by clients or infrastructure to check availability.
@app.get("/health", tags=["Health"])
def health_check() -> dict[str, str]:
    """Return the API health status."""
    return {"status": "ok"}