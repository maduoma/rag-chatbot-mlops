# tests/test_api.py

from fastapi.testclient import TestClient
from app.api.main import app

client = TestClient(app)

def test_root_route():
    response = client.get("/")
    assert response.status_code == 200

def test_chat_endpoint():
    response = client.post("/chat", json={"query": "Define AI"})
    assert response.status_code == 200
    assert "answer" in response.json()
