import pytest
from pydantic import ValidationError

from schemas.task import TaskCreate, TaskPriority, TaskStatus


def test_task_create_uses_default_values() -> None:
    


def test_task_create_accepts_valid_values() -> None:
   


def test_task_create_rejects_an_empty_title() -> None:
   

def test_task_create_rejects_invalid_status() -> None:
   