from functools import lru_cache
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import settings


class Base(DeclarativeBase):
    pass


@lru_cache(maxsize=1)
def get_engine() -> Engine:
    return create_engine(normalize_database_url(settings.database_url), future=True)


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
    Base.metadata.create_all(bind=get_engine())
