from functools import lru_cache

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
        return database_url.replace("postgresql://", "postgresql+psycopg://", 1)
    return database_url


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
