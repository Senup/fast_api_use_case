class AppError(Exception):
    """Base class for expected application-level errors."""

    status_code = 400
    code = "application_error"

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class ResourceNotFoundError(AppError):
    """Raised when a requested resource does not exist."""

    status_code = 404
    code = "resource_not_found"