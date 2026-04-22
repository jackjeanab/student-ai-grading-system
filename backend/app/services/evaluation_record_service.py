from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.activity import ClassActivity
from app.models.assignment import Assignment
from app.models.evaluation import Evaluation
from app.models.submission import Submission
from app.models.user import User
from app.schemas.submission import SubmissionCreate


def get_assignment_prompt(session: Session, assignment_id: int) -> str:
    assignment = session.get(Assignment, assignment_id)
    if assignment is None:
        return ""

    parts = [assignment.title, assignment.description or ""]
    return "\n".join(part for part in parts if part).strip()


def save_submission_evaluation(
    session: Session,
    payload: SubmissionCreate,
    evaluation_payload: dict[str, object],
    student_id: int,
) -> dict[str, object]:
    final_result = evaluation_payload["final_result"]
    if not isinstance(final_result, dict):
        raise ValueError("final_result must be a dictionary")

    _ensure_demo_relations(session, payload, student_id)
    submission = Submission(
        student_id=student_id,
        activity_id=payload.activity_id,
        assignment_id=payload.assignment_id,
        xml_content=payload.xml_content,
        status="evaluated",
    )
    session.add(submission)
    session.flush()

    evaluation = Evaluation(
        submission_id=submission.id,
        verdict=str(final_result.get("light", "")),
        grade=str(final_result.get("grade", "")),
        source=str(final_result.get("source", "")),
        feedback=str(final_result.get("feedback", "")),
    )
    session.add(evaluation)
    session.commit()
    session.refresh(submission)
    session.refresh(evaluation)

    return _to_evaluation_response(submission, evaluation)


def _ensure_demo_relations(
    session: Session,
    payload: SubmissionCreate,
    student_id: int,
) -> None:
    if session.get(User, student_id) is None:
        session.add(
            User(
                id=student_id,
                email=f"student-{student_id}@example.local",
                full_name="Demo Student",
                role="student",
            )
        )

    teacher_id = 999
    if session.get(User, teacher_id) is None:
        session.add(
            User(
                id=teacher_id,
                email="teacher@example.local",
                full_name="Demo Teacher",
                role="teacher",
            )
        )

    if session.get(Assignment, payload.assignment_id) is None:
        session.add(
            Assignment(
                id=payload.assignment_id,
                title=f"Assignment {payload.assignment_id}",
                description="Auto-created assignment placeholder.",
            )
        )

    if session.get(ClassActivity, payload.activity_id) is None:
        session.add(
            ClassActivity(
                id=payload.activity_id,
                title=f"Activity {payload.activity_id}",
                status="active",
                teacher_id=teacher_id,
            )
        )

    session.flush()


def get_submission_evaluation(
    session: Session,
    submission_id: int,
) -> dict[str, object] | None:
    submission = session.get(Submission, submission_id)
    if submission is None:
        return None

    evaluation = session.scalar(
        select(Evaluation)
        .where(Evaluation.submission_id == submission_id)
        .order_by(Evaluation.created_at.desc(), Evaluation.id.desc())
        .limit(1)
    )
    if evaluation is None:
        return None

    return _to_evaluation_response(submission, evaluation)


def _to_evaluation_response(
    submission: Submission,
    evaluation: Evaluation,
) -> dict[str, object]:
    return {
        "submission_id": submission.id,
        "activity_id": submission.activity_id,
        "assignment_id": submission.assignment_id,
        "status": submission.status,
        "light": evaluation.verdict,
        "grade": evaluation.grade,
        "feedback": evaluation.feedback,
        "source": evaluation.source,
    }
