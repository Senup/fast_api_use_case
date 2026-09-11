import pytest
from pydantic import ValidationError

from app.schemas.task import TaskCreate, TaskPriority, TaskStatus

# Verify that schema defaults are applied when optional fields are omitted.
def test_task_create_uses_default_values() -> None:
    # Construct the schema with only the required field to exercise default behavior.
    task = TaskCreate(title='Learn Pydantic')

    assert task.title == "Learn Pydantic"
    assert task.description is None
    assert task.status == TaskStatus.TODO
    assert task.priority == TaskPriority.MEDIUM
    assert task.due_date is None

# Verify that valid client input is accepted and converted into the schema's
# typed representations, including enums and a date object.
def test_task_create_accepts_valid_values() -> None:
    task = TaskCreate(
        title = "Build the task API",
        description = "Create pydantic schemas and respnse schemas",
        status="in_progress",
        priority="high",
        due_date="2026-08-20",

    )   

    assert task.status == TaskStatus.IN_PROGRESS
    assert task.priority == TaskPriority.HIGH
    assert task.due_date.isoformat() == "2026-08-20"


# Pydantic validates the title constraint and raises ValidationError for
# an empty value.
def test_task_create_rejects_an_empty_title() -> None:
    with pytest.raises(ValidationError):
        TaskCreate(title="")

# Treat invalid enum values as an input-validation failure rather than
# allowing unsupported task states into the application.
def test_task_create_rejects_invalid_status() -> None:
    # The context manager asserts that schema construction fails with the
    # expected validation exception.
    with pytest.raises(ValidationError):
        TaskCreate(title="Invalid task", status="blocked")
   

# def test_task_create_rejects_invalid_status() -> None:
   