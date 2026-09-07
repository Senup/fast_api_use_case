#Import the TaskService class so this module can create and provide it.
from app.services.tasks import TaskService
# Create one shared TaskService instance for the application.
# Its in-memory task data is reused across incoming requests.
task_service = TaskService()


def get_task_service() -> TaskService:
    """Provide the shared task service for request handlers."""
    return task_service