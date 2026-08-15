import pytest
from pydantic import ValidationError

from schemas.task import TaskCreate, TaskPriority, TaskStatus


def test_task_create_uses_default_values() -> None:
    task = TaskCreate(title='Learn Pydantic')

    assert task.title == "Learn Pydantic"
    assert task.description is None
    assert task.status == TaskStatus.TODO
    assert task.priority == TaskPriority.MEDIUM
    assert task.due_date is None

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



def test_task_create_rejects_an_empty_title() -> None:
    with pytest.raises(ValidationError):
        TaskCreate(title="")

def test_task_create_rejects_invalid_status() -> None:
    with pytest.raises(ValidationError):
        TaskCreate(title="Invalid task", status="blocked")
   

# def test_task_create_rejects_invalid_status() -> None:
   