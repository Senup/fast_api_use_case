# Import date for date-only values such as a task's due date.
# Import datetime for timestamps such as created_at and updated_at.
from datetime import date,datetime
# Import StrEnum to define string-based enumerations.
from enum import StrEnum
# Import UUID for uniquely identifying each task.
from uuid import UUID

# Import Pydantic tools:
# BaseModel creates validated data models,
# ConfigDict configures model behavior,
# Field adds validation rules to model fields.
from pydantic import BaseModel, ConfigDict, Field

class TaskStatus(StrEnum):
    """Allowed lifecycle states for a task."""

# A task that has not started.
    TODO = "todo"
    # A task currently being worked on.
    IN_PROGRESS = "in_progress"
    # A completed task.
    DONE = "done"

class TaskPriority(StrEnum):
    """Allowed Proirity levels for a task."""

    # The task has low urgency.
    LOW = "low"
    # The task has normal urgency.
    MEDIUM = "medium"
    # The task has high urgency.
    HIGH = "high"

class TaskCreate(BaseModel):
    """Payload accepted when creating a task"""

    # Require a title with between 1 and 200 characters.
    title: str = Field(min_length=1, max_length=200)
    # Allow an optional description with a maximum of 2,000 characters.
    description: str | None = Field(default= None,max_length=2_000)
    # Use TODO when the client does not provide a status.
    status: TaskStatus = TaskStatus.TODO
    # Use MEDIUM when the client does not provide a priority.
    priority: TaskPriority = TaskPriority.MEDIUM
    # Allow an optional date on which the task should be completed.
    due_date: date | None = None



class TaskUpdate(BaseModel):
    # If supplied, require a title with between 1 and 200 characters.
    title: str | None = Field(default=None, min_length=1, max_length=200)
    # If supplied, limit the description to 2,000 characters.
    description: str | None = Field(default=None, max_length=2_000)
    # If supplied, require one of the defined TaskStatus values.
    status: TaskStatus | None = None
    # If supplied, require one of the defined TaskPriority values.
    priority: TaskPriority | None = None
    # If supplied, require a valid date.
    due_date: date | None = None


class TaskResponse(BaseModel):
    """Task representation returned by the API"""

    # Allow Pydantic to build this schema from object attributes.
    # This is useful when the service returns model-like objects.
    model_config = ConfigDict(from_attributes=True)

    # Unique identifier generated for the task.
    id: UUID
    # Title of the task.
    title: str
    # Optional task description.
    description: str | None
    # Current lifecycle status.
    status: TaskStatus
    # Current priority level.
    priority: TaskPriority
    # Optional deadline.
    due_date: date | None
    # Time when the task was created.
    created_at: datetime
    # Time when the task was most recently updated.
    updated_at: datetime