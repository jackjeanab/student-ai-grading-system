from fastapi.testclient import TestClient

from app.main import app


def test_teacher_can_create_activity_with_assignments() -> None:
    client = TestClient(app)

    response = client.post(
        "/api/activities",
        json={
            "title": "Chapter 2 Practice",
            "assignment_ids": [101, 102],
            "status": "draft",
        },
        headers={"Authorization": "Bearer dev-token"},
    )

    assert response.status_code == 201
    assert response.json()["assignment_ids"] == [101, 102]
