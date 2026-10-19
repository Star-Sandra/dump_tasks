from fastapi.testclient import TestClient

from main import app


def test_system_status_reports_ok():
    with TestClient(app) as client:
        response = client.get("/system-status")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_app_title():
    assert app.title == "Dump Tasks API"
