# tests/test_flask_ui.py

from app.ui.flask_app import create_app

def test_flask_routes():
    app = create_app()
    client = app.test_client()

    response = client.get("/")
    assert response.status_code == 200

    response = client.get("/upload")
    assert response.status_code == 200
