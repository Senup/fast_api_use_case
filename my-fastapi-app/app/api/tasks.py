# Import UUID so FastAPI can validate task IDs from the URL.
from uuid import UUID

# Import FastAPI tools used to define routes and responses:
# APIRouter groups related endpoints,
# Depends provides dependency injection,
# Response creates an HTTP response,
# status provides readable HTTP status constants.
from fastapi import APIRouter, Depends, Response, status

# Import the dependency that provides the shared TaskService instance.
from app.api.dependencies import get_task_service
# Import schemas used to validate request data and format responses.
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate
# Import TaskService for type annotations and service access.
# The service contains the application's task business logic.
from app.services.tasks import TaskService

# Create a router for task-related endpoints.
# Every route in this router begins with /api/v1/tasks.
# The "Tasks" tag groups these endpoints in the OpenAPI documentation.
router = APIRouter(prefix="/api/v1/tasks", tags=["Tasks"])

# Register an endpoint for creating a new task.
@router.post(
    "",  # The complete URL is POST /api/v1/tasks.
    response_model=TaskResponse,  # Serialize the result using TaskResponse.
    status_code=status.HTTP_201_CREATED,  # Return 201 when creation succeeds.
)
def create_task(
    # Validate the incoming JSON body using the TaskCreate schema.
    payload: TaskCreate,
    # Ask FastAPI to inject the shared TaskService instance.
    service: TaskService = Depends(get_task_service),
) -> TaskResponse:
    """Create a task."""
    # Pass the validated task data to the service layer.
    return service.create_task(payload)


# Register an endpoint for retrieving all tasks.
@router.get("", response_model=list[TaskResponse])
def list_tasks(
    # Inject the shared TaskService instance into the route.
    service: TaskService = Depends(get_task_service),
) -> list[TaskResponse]:
    """List every task."""
    # Ask the service layer to retrieve every stored task.
    return service.list_tasks()


# Register an endpoint for retrieving one task by its ID.
@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    # Read task_id from the URL and validate it as a UUID.
    task_id: UUID,
    # Inject the shared TaskService instance.
    service: TaskService = Depends(get_task_service),
) -> TaskResponse:
    """Return one task."""
     # Ask the service layer to find the requested task.
    return service.get_task(task_id)


# Register an endpoint for partially updating an existing task.
@router.patch("/{task_id}", response_model=TaskResponse)
def update_task(
     # Read and validate the task ID from the URL.
    task_id: UUID,
    # Validate only the fields submitted by the client.
    payload: TaskUpdate,
    # Inject the shared TaskService instance.
    service: TaskService = Depends(get_task_service),
) -> TaskResponse:
    """Partially update one task."""
     # Pass the task ID and validated update data to the service layer.
    return service.update_task(task_id, payload)


# Register an endpoint for deleting a task.
# Return HTTP 204 when deletion succeeds.
    # A 204 response does not contain a response body.
@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
     # Read and validate the task ID from the URL.
    task_id: UUID,
     # Inject the shared TaskService instance.
    service: TaskService = Depends(get_task_service),
) -> Response:
    """Delete one task."""
    # Ask the service layer to remove the task.
    service.delete_task(task_id)
    service.delete_task(task_id)
     # Return an empty HTTP 204 response after successful deletion.
    return Response(status_code=status.HTTP_204_NO_CONTENT)