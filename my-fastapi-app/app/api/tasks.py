from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.api.dependencies import get_task_service
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate
from app.services.tasks import TaskNotFoundError, TaskService

router = APIRouter(prefix="/api/v1/tasks", tags=["Tasks"])

tasks: dict[UUID, TaskResponse] = {}


@router.post(
    "",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_task(payload: TaskCreate) -> TaskResponse:
    """Create a task in temporary in-memory storage."""
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


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: UUID) -> TaskResponse:
    """Return one task by its identifier."""
    task = tasks.get(task_id)

    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    return task


@router.patch("/{task_id}", response_model=TaskResponse)
def update_task(task_id: UUID, payload: TaskUpdate) -> TaskResponse:
    """Partially update one task by its identifier."""
    task = tasks.get(task_id)

    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    updates = payload.model_dump(exclude_unset=True)
    updated_task = task.model_copy(
        update={
            **updates,
            "updated_at": datetime.now(UTC),
        }
    )

    tasks[task_id] = updated_task
    return updated_task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: UUID) -> Response:
    """Delete one task by its identifier."""
    if task_id not in tasks:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    del tasks[task_id]
    return Response(status_code=status.HTTP_204_NO_CONTENT)