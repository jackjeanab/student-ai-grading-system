from functools import lru_cache
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from sqlalchemy import create_engine, inspect, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import settings


class Base(DeclarativeBase):
    pass


@lru_cache(maxsize=1)
def get_engine() -> Engine:
    return create_engine(
        normalize_database_url(settings.database_url),
        connect_args={"prepare_threshold": None},
        future=True,
    )


def normalize_database_url(database_url: str) -> str:
    if database_url.startswith("postgresql://"):
        database_url = database_url.replace("postgresql://", "postgresql+psycopg://", 1)

    parsed = urlsplit(database_url)
    if parsed.scheme not in {"postgresql+psycopg", "postgresql"}:
        return database_url

    query = [
        (key, value)
        for key, value in parse_qsl(parsed.query, keep_blank_values=True)
        if key != "pgbouncer"
    ]
    return urlunsplit(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path,
            urlencode(query),
            parsed.fragment,
        )
    )


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    future=True,
)


def get_session_local() -> sessionmaker:
    SessionLocal.configure(bind=get_engine())
    return SessionLocal


def create_db_tables() -> None:
    engine = get_engine()
    Base.metadata.create_all(bind=engine)
    ensure_schema_compatibility(engine)


def ensure_schema_compatibility(engine: Engine) -> None:
    inspector = inspect(engine)
    if "evaluations" not in inspector.get_table_names():
        return

    columns = {column["name"] for column in inspector.get_columns("evaluations")}
    statements = []
    if "grade" not in columns:
        statements.append("ALTER TABLE evaluations ADD COLUMN grade VARCHAR(50)")
    if "source" not in columns:
        statements.append("ALTER TABLE evaluations ADD COLUMN source VARCHAR(50)")

    if not statements:
        return

    with engine.begin() as connection:
        for statement in statements:
            connection.execute(text(statement))
