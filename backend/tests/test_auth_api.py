from fastapi.testclient import TestClient

from app.main import app


def test_login_returns_role_and_token() -> None:
    client = TestClient(app)

    response = client.post(
        "/api/auth/login",
        json={"account": "teacher01", "password": "secret123"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["role"] == "teacher"
    assert "access_token" in data
