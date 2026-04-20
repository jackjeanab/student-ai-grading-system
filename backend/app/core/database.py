from functools import lru_cache

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import settings


class Base(DeclarativeBase):
    pass


@lru_cache(maxsize=1)
def get_engine() -> Engine:
    return create_engine(settings.database_url, future=True)


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    future=True,
)


def get_session_local() -> sessionmaker:
    SessionLocal.configure(bind=get_engine())
    return SessionLocal
