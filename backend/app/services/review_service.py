from __future__ import annotations

from app.schemas.review import ReviewGrade, ReviewLight


def override_submission(
    submission_id: int,
    grade: ReviewGrade,
    light: ReviewLight,
    reason: str,
) -> dict[str, object]:
    return {
        "submission_id": submission_id,
        "grade": grade.value,
        "light": light.value,
        "reason": reason,
        "teacher_revised": True,
    }
