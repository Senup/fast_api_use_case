import pytest
from uuid import UUID
from app.schemas.task import TaskCreate, TaskUpdate
from app.services.tasks import TaskNotFoundError, TaskService

# Use a fresh service instance so the test exercises isolated in-memory state.
def test_service_creates_and_retrieves_a_task() -> None:
    service = TaskService()
    # Create a task through the service and use its generated ID for retrieval.
    task = service.create_task(TaskCreate(title="Learn service layers"))

    # Confirm that retrieval returns the same persisted task representation.
    retrieved = service.get_task(task.id)

    assert retrieved == task

# Verify that PATCH-style updates preserve fields that were not submitted.
def test_service_updates_only_the_submitted_fields() -> None:
    service = TaskService()
    task = service.create_task(
        TaskCreate(
            title="Original title",
            description="Original description",
        )
    )

    # Provide only the field being changed so preservation of omitted fields is tested.
    updated = service.update_task(
        task.id,
        TaskUpdate(priority="high"),
    )

    assert updated.title == "Original title"
    assert updated.description == "Original description"
    assert updated.priority == "high"

# Use a deterministic UUID that is guaranteed not to exist in fresh in-memory storage.
# The service should convert this missing-resource case into its domain exception.
def test_service_raises_error_for_an_unknown_task() -> None:
    service = TaskService()

    # Assert the service-layer contract for requests targeting a nonexistent task.
    with pytest.raises(TaskNotFoundError):
        service.get_task(UUID("00000000-0000-0000-0000-000000000000"))