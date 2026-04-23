from fastapi.testclient import TestClient

from app.api import assignments
from app.main import app


def test_teacher_can_create_assignment_prompt(monkeypatch) -> None:
    client = TestClient(app)

    class FakeSession:
        def __init__(self) -> None:
            self.assignment = None

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, traceback) -> None:
            return None

        def get(self, model, item_id: int):
            return None

        def add(self, assignment) -> None:
            self.assignment = assignment

        def commit(self) -> None:
            if self.assignment.id is None:
                self.assignment.id = 101

        def refresh(self, assignment) -> None:
            return None

    fake_session = FakeSession()
    monkeypatch.setattr(assignments, "get_session_local", lambda: lambda: fake_session)

    response = client.post(
        "/api/assignments",
        json={
            "id": 101,
            "title": "LED 控制任務",
            "description": "請設計 LED 每 1 秒閃爍一次。",
        },
        headers={"Authorization": "Bearer dev-token"},
    )

    assert response.status_code == 201
    assert response.json() == {
        "id": 101,
        "title": "LED 控制任務",
        "description": "請設計 LED 每 1 秒閃爍一次。",
    }
    assert fake_session.assignment.title == "LED 控制任務"
