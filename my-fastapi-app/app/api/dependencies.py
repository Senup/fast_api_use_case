from app.services.tasks import TaskService

task_service = TaskService()


def get_task_service() -> TaskService:
    """Provide the shared task service for request handlers."""
    return task_service