import pytest
from uuid import UUID
from app.schemas.task import TaskCreate, TaskUpdate
from app.services.tasks import TaskNotFoundError, TaskService


def test_service_creates_and_retrieves_a_task() -> None:
    service = TaskService()

    task = service.create_task(TaskCreate(title="Learn service layers"))

    retrieved = service.get_task(task.id)

    assert retrieved == task


def test_service_updates_only_the_submitted_fields() -> None:
    service = TaskService()
    task = service.create_task(
        TaskCreate(
            title="Original title",
            description="Original description",
        )
    )

    updated = service.update_task(
        task.id,
        TaskUpdate(priority="high"),
    )

    assert updated.title == "Original title"
    assert updated.description == "Original description"
    assert updated.priority == "high"


def test_service_raises_error_for_an_unknown_task() -> None:
    service = TaskService()

    with pytest.raises(TaskNotFoundError):
        service.get_task(UUID("00000000-0000-0000-0000-000000000000"))