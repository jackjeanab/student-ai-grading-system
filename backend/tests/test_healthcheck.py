from fastapi.testclient import TestClient

from app.main import app, create_app


def test_healthcheck_returns_ok() -> None:
    client = TestClient(app)

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_app_startup_creates_database_tables(monkeypatch) -> None:
    calls: list[str] = []

    def fake_create_db_tables() -> None:
        calls.append("create_db_tables")

    monkeypatch.setattr("app.main.create_db_tables", fake_create_db_tables)

    with TestClient(create_app()) as client:
        response = client.get("/health")

    assert response.status_code == 200
    assert calls == ["create_db_tables"]
