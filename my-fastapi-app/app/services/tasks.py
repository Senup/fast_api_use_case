from datetime import UTC, datetime
from uuid import UUID, uuid4

from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate


class TaskNotFoundError(Exception):
    """Raised when a requested task does not exist."""


class TaskService:
    """Manage tasks using temporary in-memory storage."""

    def __init__(self) -> None:
        self._tasks: dict[UUID, TaskResponse] = {}

    def create_task(self, payload: TaskCreate) -> TaskResponse:
        """Create and store a task."""
        now = datetime.now(UTC)

        task = TaskResponse(
            id=uuid4(),
            title=payload.title,
            description=payload.description,
            status=payload.status,
            priority=payload.priority,
            due_date=payload.due_date,
            created_at=now,
            updated_at=now,
        )

        self._tasks[task.id] = task
        return task

    def list_tasks(self) -> list[TaskResponse]:
        """Return all stored tasks."""
        return list(self._tasks.values())

    def get_task(self, task_id: UUID) -> TaskResponse:
        """Return one task or raise a domain-specific error."""
        task = self._tasks.get(task_id)

        if task is None:
            raise TaskNotFoundError

        return task

    def update_task(self, task_id: UUID, payload: TaskUpdate) -> TaskResponse:
        """Partially update one task."""
        task = self.get_task(task_id)
        updates = payload.model_dump(exclude_unset=True)

        updated_task = task.model_copy(
            update={
                **updates,
                "updated_at": datetime.now(UTC),
            }
        )

        self._tasks[task_id] = updated_task
        return updated_task

    def delete_task(self, task_id: UUID) -> None:
        """Delete one task."""
        self.get_task(task_id)
        del self._tasks[task_id]


    def clear_tasks(self) -> None:
        """Clear all tasks; used to isolate local tests."""
        self._tasks.clear()