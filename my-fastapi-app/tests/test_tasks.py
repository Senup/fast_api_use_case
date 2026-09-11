from fastapi.testclient import TestClient
from datetime import UTC, datetime
from uuid import UUID, uuid4
from app.api.dependencies import task_service
from app.main import app

client = TestClient(app)

# Reset the shared in-memory service before each test to prevent state leakage
# between tests and keep test results independent of execution order.
def setup_function() -> None:
    """Start every test with empty in-memory storage."""
    task_service.clear_tasks()

# Create a task through the public API and return its response body for tests
# that need a valid persisted resource and generated task ID.
def create_test_task() -> dict[str, object]:
    response = client.post(
        "/api/v1/tasks",
        json={
            "title": "Original task",
            "description": "Keep this description during a partial update.",
            "priority": "medium",
        },
    )

    assert response.status_code == 201
    return response.json()

# Verify the complete create-task response, including validated input,
# generated identifiers, and server-managed timestamps.
def test_create_task_returns_created_task() -> None:
    # Submit all supported client-controlled fields to verify their values survive
    # request validation and response serialization.
    response = client.post(
        "/api/v1/tasks",
        json={
            "title": "Build task endpoints",
            "description": "Implement create and list routes.",
            "status": "in_progress",
            "priority": "high",
            "due_date": "2026-08-20",
        },
    )

    assert response.status_code == 201

    body = response.json()
    assert body["title"] == "Build task endpoints"
    assert body["description"] == "Implement create and list routes."
    assert body["status"] == "in_progress"
    assert body["priority"] == "high"
    assert body["due_date"] == "2026-08-20"
    assert body["id"]
    assert body["created_at"]
    assert body["updated_at"]

# Verify that omitted fields receive the schema's documented defaults and that
# the newly created task is returned by the collection endpoint.
def test_list_tasks_returns_previously_created_task() -> None:
    client.post("/api/v1/tasks", json={"title": "First task"})

    response = client.get("/api/v1/tasks")

    assert response.status_code == 200

    body = response.json()
    assert len(body) == 1
    assert body[0]["title"] == "First task"
    assert body[0]["status"] == "todo"
    assert body[0]["priority"] == "medium"

# Send invalid values together to confirm request validation rejects the payload
# before the service layer creates any task.
def test_create_task_rejects_invalid_payload() -> None:
    response = client.post(
        "/api/v1/tasks",
        json={"title": "", "status": "blocked"},
    )

    assert response.status_code == 422


# Use a previously created resource so this test validates retrieval of an
# existing task through its public identifier.
def test_get_task_returns_created_task() -> None:
    task = create_test_task()

    response = client.get(f"/api/v1/tasks/{task['id']}")

    assert response.status_code == 200
    assert response.json()["id"] == task["id"]
    assert response.json()["title"] == "Original task"

# Use a deterministic UUID that is not present in the reset in-memory store to
# verify the API's missing-resource behavior.
def test_get_task_returns_not_found_for_unknown_id() -> None:
    response = client.get("/api/v1/tasks/00000000-0000-0000-0000-000000000000")

    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}

# Send only one field to verify PATCH semantics: omitted fields must remain
# unchanged while the submitted field is updated.
def test_update_task_changes_only_sent_fields() -> None:
    task = create_test_task()

    response = client.patch(
        f"/api/v1/tasks/{task['id']}",
        json={"priority": "high"},
    )

    assert response.status_code == 200

    body = response.json()
    assert body["title"] == "Original task"
    assert body["description"] == "Keep this description during a partial update."
    assert body["priority"] == "high"
    # Confirm that an update changes the modification timestamp, providing evidence
    # that the service records the mutation rather than returning the original task.
    assert body["updated_at"] != task["updated_at"]

# Verify that updating a nonexistent resource returns a client-visible not-found
# response instead of creating a new task.
def test_update_task_returns_not_found_for_unknown_id() -> None:
    response = client.patch(
        "/api/v1/tasks/00000000-0000-0000-0000-000000000000",
        json={"title": "Does not exist"},
    )

    assert response.status_code == 404

# Verify successful deletion through both the HTTP status and the required
# empty response body for a 204 No Content response.
def test_delete_task_removes_task() -> None:
    task = create_test_task()

    delete_response = client.delete(f"/api/v1/tasks/{task['id']}")

    assert delete_response.status_code == 204
    assert delete_response.content == b""

    # Perform a follow-up read to confirm deletion has an observable effect and the
    # resource is no longer available through the API.
    get_response = client.get(f"/api/v1/tasks/{task['id']}")
    assert get_response.status_code == 404

# Confirm that deleting an unknown identifier returns the same not-found
# contract as retrieval and update operations.
def test_delete_task_returns_not_found_for_unknown_id() -> None:
    response = client.delete("/api/v1/tasks/00000000-0000-0000-0000-000000000000")

    assert response.status_code == 404