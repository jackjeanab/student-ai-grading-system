from fastapi.testclient import TestClient

from app.main import app


def test_teacher_can_override_final_grade() -> None:
    client = TestClient(app)

    response = client.post(
        "/api/teacher/submissions/1/override",
        json={"grade": "優", "light": "green", "reason": "Teacher review"},
        headers={"Authorization": "Bearer dev-token"},
    )

    assert response.status_code == 200
    assert response.json()["teacher_revised"] is True


def test_teacher_override_rejects_invalid_grade() -> None:
    client = TestClient(app)

    response = client.post(
        "/api/teacher/submissions/1/override",
        json={"grade": "A", "light": "green", "reason": "Teacher review"},
        headers={"Authorization": "Bearer dev-token"},
    )

    assert response.status_code == 422


def test_teacher_override_rejects_invalid_light() -> None:
    client = TestClient(app)

    response = client.post(
        "/api/teacher/submissions/1/override",
        json={"grade": "優", "light": "purple", "reason": "Teacher review"},
        headers={"Authorization": "Bearer dev-token"},
    )

    assert response.status_code == 422
