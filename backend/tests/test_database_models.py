from app.models.activity import ClassActivity
from app.models.assignment import Assignment
from app.models.submission import Submission
from app.core.database import normalize_database_url


def test_submission_belongs_to_activity_and_assignment() -> None:
    activity = ClassActivity(title="Week 1", status="active", teacher_id=1)
    assignment = Assignment(title="Blink", description="Use led blocks")
    submission = Submission(
        student_id=2,
        activity=activity,
        assignment=assignment,
        xml_content="<xml />",
        status="queued",
    )

    assert submission.activity.title == "Week 1"
    assert submission.assignment.title == "Blink"


def test_normalize_database_url_uses_psycopg_driver_for_postgres() -> None:
    url = "postgresql://postgres:secret@example.supabase.co:5432/postgres"

    normalized = normalize_database_url(url)

    assert normalized == "postgresql+psycopg://postgres:secret@example.supabase.co:5432/postgres"
