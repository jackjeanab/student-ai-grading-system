from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base
from app.models.evaluation import Evaluation
from app.models.submission import Submission
from app.services.report_service import build_assignment_report


def make_session():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        future=True,
    )
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine, future=True)()


def test_assignment_report_returns_latest_evaluations_and_light_summary() -> None:
    session = make_session()
    first_submission = Submission(
        student_id=10,
        activity_id=7,
        assignment_id=101,
        xml_content="<xml />",
        status="evaluated",
    )
    second_submission = Submission(
        student_id=11,
        activity_id=7,
        assignment_id=101,
        xml_content="<xml />",
        status="evaluated",
    )
    other_assignment_submission = Submission(
        student_id=12,
        activity_id=7,
        assignment_id=202,
        xml_content="<xml />",
        status="evaluated",
    )
    session.add_all([first_submission, second_submission, other_assignment_submission])
    session.flush()
    session.add_all(
        [
            Evaluation(
                submission_id=first_submission.id,
                verdict="yellow",
                grade="可",
                feedback="Older result",
                source="gemini",
            ),
            Evaluation(
                submission_id=first_submission.id,
                verdict="green",
                grade="優",
                feedback="Latest result",
                source="gemini",
            ),
            Evaluation(
                submission_id=second_submission.id,
                verdict="red",
                grade="待加強",
                feedback="Missing required blocks",
                source="rule_engine",
            ),
            Evaluation(
                submission_id=other_assignment_submission.id,
                verdict="blue",
                grade="良",
                feedback="Different assignment",
                source="gemini",
            ),
        ]
    )
    session.commit()

    report = build_assignment_report(session, assignment_id=101)

    assert report["assignment_id"] == 101
    assert report["summary"] == {
        "total": 2,
        "evaluated": 2,
        "green": 1,
        "blue": 0,
        "yellow": 0,
        "red": 1,
    }
    assert report["rows"] == [
        {
            "submission_id": first_submission.id,
            "student_id": 10,
            "activity_id": 7,
            "assignment_id": 101,
            "status": "evaluated",
            "light": "green",
            "grade": "優",
            "feedback": "Latest result",
            "source": "gemini",
        },
        {
            "submission_id": second_submission.id,
            "student_id": 11,
            "activity_id": 7,
            "assignment_id": 101,
            "status": "evaluated",
            "light": "red",
            "grade": "待加強",
            "feedback": "Missing required blocks",
            "source": "rule_engine",
        },
    ]
