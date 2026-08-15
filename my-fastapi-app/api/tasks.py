from datetime import UTC, datetime
from uuid import UUID, uuid4

from fastapi import APIRouter, status
from schemas.task import TaskCreate, TaskResponse

router = APIRouter(prefix="/api/v1/tasks",tags=["Tasks"])

tasks: dict[UUID, TaskResponse] = {}

@router.post("", response_model=TaskResponse,
             status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate) -> TaskResponse:
    """Create a Task in temporary in-memory storage"""
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

    tasks[task.id] = task
    return task

@router.get("", response_model=list[TaskResponse])
def list_tasks() -> list[TaskResponse]:
    """Return every task stored during this application process."""
    return list(tasks.values())