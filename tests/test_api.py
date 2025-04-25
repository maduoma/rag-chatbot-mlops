# tests/test_api.py

from app.ui.flask_app import create_app

app = create_app()
client = app.test_client()

def test_root_route():
    response = client.get("/")
    assert response.status_code == 200

def test_upload_route():
    response = client.get("/upload")
    assert response.status_code == 200