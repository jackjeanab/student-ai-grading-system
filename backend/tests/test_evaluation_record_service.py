from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base
from app.models.assignment import Assignment
from app.schemas.submission import SubmissionCreate
from app.services.evaluation_record_service import (
    get_assignment_prompt,
    get_submission_evaluation,
    save_submission_evaluation,
)


def make_session():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        future=True,
    )
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine, future=True)()


def test_get_assignment_prompt_uses_teacher_configured_text() -> None:
    session = make_session()
    session.add(Assignment(id=101, title="Blink LED", description="Use setup, loop, and delay."))
    session.commit()

    prompt = get_assignment_prompt(session, 101)

    assert "Blink LED" in prompt
    assert "Use setup, loop, and delay." in prompt


def test_save_and_query_submission_evaluation_does_not_expose_api_key() -> None:
    session = make_session()
    payload = SubmissionCreate(
        assignment_id=101,
        activity_id=7,
        xml_content="<xml xmlns=\"https://developers.google.com/blockly/xml\" />",
    )
    evaluation_payload = {
        "final_result": {
            "light": "blue",
            "grade": "良",
            "feedback": "Good structure; add clearer timing.",
            "source": "gemini",
        }
    }

    saved = save_submission_evaluation(session, payload, evaluation_payload, student_id=3)
    queried = get_submission_evaluation(session, int(saved["submission_id"]))

    assert queried == {
        "submission_id": saved["submission_id"],
        "activity_id": 7,
        "assignment_id": 101,
        "status": "evaluated",
        "light": "blue",
        "grade": "良",
        "feedback": "Good structure; add clearer timing.",
        "source": "gemini",
    }
    assert "api_key" not in queried
    assert "GEMINI_API_KEY" not in str(queried)
