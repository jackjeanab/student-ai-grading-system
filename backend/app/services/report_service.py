from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.evaluation import Evaluation
from app.models.submission import Submission

LIGHTS = ("green", "blue", "yellow", "red")


def build_assignment_report(session: Session, assignment_id: int) -> dict[str, object]:
    rows: list[dict[str, object]] = []
    summary = {"total": 0, "evaluated": 0, **dict.fromkeys(LIGHTS, 0)}
    submissions = session.scalars(
        select(Submission)
        .where(Submission.assignment_id == assignment_id)
        .order_by(Submission.id)
    ).all()

    for submission in submissions:
        evaluation = session.scalar(
            select(Evaluation)
            .where(Evaluation.submission_id == submission.id)
            .order_by(Evaluation.created_at.desc(), Evaluation.id.desc())
            .limit(1)
        )
        row = _build_report_row(submission, evaluation)
        rows.append(row)
        _add_to_summary(summary, row)

    return {
        "assignment_id": assignment_id,
        "summary": summary,
        "rows": rows,
    }


def _build_report_row(
    submission: Submission,
    evaluation: Evaluation | None,
) -> dict[str, object]:
    return {
        "submission_id": submission.id,
        "student_id": submission.student_id,
        "activity_id": submission.activity_id,
        "assignment_id": submission.assignment_id,
        "status": submission.status,
        "light": evaluation.verdict if evaluation else None,
        "grade": evaluation.grade if evaluation else None,
        "feedback": evaluation.feedback if evaluation else None,
        "source": evaluation.source if evaluation else None,
    }


def _add_to_summary(summary: dict[str, int], row: dict[str, object]) -> None:
    summary["total"] += 1
    light = row.get("light")
    if light in LIGHTS:
        summary["evaluated"] += 1
        summary[str(light)] += 1
