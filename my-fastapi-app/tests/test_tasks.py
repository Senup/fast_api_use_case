from fastapi.testclient import TestClient

from api.tasks import tasks
from main import app

client = TestClient(app)


def setup_function() -> None:
    """Start every test with empty in-memory storage."""
    tasks.clear()


def test_create_task_returns_created_task() -> None:
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


def test_list_tasks_returns_previously_created_task() -> None:
    client.post("/api/v1/tasks", json={"title": "First task"})

    response = client.get("/api/v1/tasks")

    assert response.status_code == 200

    body = response.json()
    assert len(body) == 1
    assert body[0]["title"] == "First task"
    assert body[0]["status"] == "todo"
    assert body[0]["priority"] == "medium"


def test_create_task_rejects_invalid_payload() -> None:
    response = client.post(
        "/api/v1/tasks",
        json={"title": "", "status": "blocked"},
    )

    assert response.status_code == 422