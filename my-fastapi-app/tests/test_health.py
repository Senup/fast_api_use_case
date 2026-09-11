from fastapi.testclient import TestClient
from app.main import app

# Use an in-process client to exercise the configured FastAPI application
# without starting an external server.
client = TestClient(app)

def test_health_check_returns_ok() -> None:
    # Call the health endpoint through the same application interface used by clients.
    response = client.get("/health")

    assert response.status_code == 200
    # Protect the endpoint's response contract so unexpected payload changes fail the test.
    assert response.json() == {"status": "ok"}