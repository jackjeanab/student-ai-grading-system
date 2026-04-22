from app.models.activity import ClassActivity
from app.models.assignment import Assignment
from app.models.submission import Submission
from app.core import database
from app.core.database import get_engine, normalize_database_url


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


def test_normalize_database_url_removes_supabase_pgbouncer_flag() -> None:
    url = "postgresql://postgres:secret@example.pooler.supabase.com:6543/postgres?pgbouncer=true&sslmode=require"

    normalized = normalize_database_url(url)

    assert normalized == (
        "postgresql+psycopg://postgres:secret@example.pooler.supabase.com:6543/postgres?sslmode=require"
    )


def test_get_engine_disables_psycopg_prepared_statements(monkeypatch) -> None:
    calls: list[dict] = []

    def fake_create_engine(*args, **kwargs):
        calls.append({"args": args, "kwargs": kwargs})
        return object()

    get_engine.cache_clear()
    monkeypatch.setattr(database.settings, "database_url", "postgresql://example.com/postgres")
    monkeypatch.setattr(database, "create_engine", fake_create_engine)

    get_engine()

    assert calls[0]["kwargs"]["connect_args"] == {"prepare_threshold": None}
    assert calls[0]["kwargs"]["future"] is True
    get_engine.cache_clear()
