# Import timezone-aware date and time utilities.
from datetime import UTC, datetime
# Import UUID for task IDs and uuid4 for generating new unique IDs.
from uuid import UUID, uuid4
from app.core.errors import ResourceNotFoundError
# Import the Pydantic schemas used for task input and output.
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate


class TaskNotFoundError(Exception):
    """Raised when a requested task does not exist."""


class TaskService:
    """Manage tasks using temporary in-memory storage."""

    def __init__(self) -> None:
        # Store tasks in a dictionary using each task's UUID as the key.
        # This storage exists only while the application is running.
        self._tasks: dict[UUID, TaskResponse] = {}

    def create_task(self, payload: TaskCreate) -> TaskResponse:
        """Create and store a task."""
        # Create one timezone-aware timestamp for both task timestamps.
        now = datetime.now(UTC)

         # Build a validated response model from the validated create payload.
        task = TaskResponse(
            # Generate a unique ID for the new task.
            id=uuid4(),
            # Copy the user-provided and default values from the request schema.
            title=payload.title,
            description=payload.description,
            status=payload.status,
            priority=payload.priority,
            due_date=payload.due_date,
            # Record when the task was created and last updated.
            created_at=now,
            updated_at=now,
        )

        # Store the task using its UUID as the dictionary key.
        self._tasks[task.id] = task
        # Return the newly created task to the caller.
        return task

    def list_tasks(self) -> list[TaskResponse]:
        """Return all stored tasks."""

        # Convert the dictionary values into a list of task responses.
        return list(self._tasks.values())

    def get_task(self, task_id: UUID) -> TaskResponse:
        """Return one task or raise a domain-specific error."""
        # Look up the task by its UUID.
        task = self._tasks.get(task_id)

        # Stop execution when no task exists with the requested ID.
        if task is None:
            raise TaskNotFoundError

        # Return the matching task.
        return task

    def update_task(self, task_id: UUID, payload: TaskUpdate) -> TaskResponse:
        """Partially update one task."""
         # Retrieve the existing task or raise TaskNotFoundError.
        task = self.get_task(task_id)
        # Convert only explicitly submitted fields into a dictionary.
        # This preserves fields that were not included in the PATCH request.
        updates = payload.model_dump(exclude_unset=True)

        # Create a new Pydantic model containing the updated values.
        updated_task = task.model_copy(
            update={
                **updates,
                # Refresh the modification timestamp.
                "updated_at": datetime.now(UTC),
            }
        )

        # Replace the old task with the updated task.
        self._tasks[task_id] = updated_task
        # Return the updated task.
        return updated_task

    def delete_task(self, task_id: UUID) -> None:
        """Delete one task."""
        # Confirm that the task exists before attempting deletion.
        self.get_task(task_id)
        # Remove the task from the dictionary.
        del self._tasks[task_id]


    def clear_tasks(self) -> None:
        """Clear all tasks; used to isolate local tests."""
        # Empty the in-memory storage.
        self._tasks.clear()



# A few improvements are worth considering:

# 1- Avoid exposing mutable stored models. 
# create_task, get_task, and list_tasks return the same TaskResponse objects held in _tasks (tasks.py:29, tasks.py:35). Any non-HTTP caller could mutate a returned task and silently change storage without updating updated_at. Make TaskResponse immutable (ConfigDict(frozen=True)) or return model_copy() values at service boundaries.

# 2- Define empty PATCH behavior. TaskUpdate allows {}, and update_task will then only change updated_at (tasks.py:44). That can be acceptable, but APIs often reject an empty partial update with 422, usually via a schema validator. Decide and test the intended contract.

# 3- Raise an exception instance with context. raise TaskNotFoundError works in Python, but raise TaskNotFoundError(f"Task {task_id} was not found") (tasks.py:39) is clearer for logs, reuse outside this router, and debugging.
# 4- Concurrency is intentionally unsupported. The singleton service is shared by the app, while a read-modify-write update is not atomic (tasks.py:44). Fine for temporary learning storage, as the docstring says; move to a database/repository or add synchronization before treating it as production storage.
# 5- Minor cleanup: remove the extra blank lines before clear_tasks (tasks.py:63). The test-only clear_tasks method itself is practical given the shared dependency.