from fastapi.testclient import TestClient
from backend.backend import app

client = TestClient(app)

def test_app_loads():
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code in (404, 200)  # accetta che "/" non esista ancora
