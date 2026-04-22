from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import create_db_tables
from app.core.rate_limit import InMemoryRateLimitMiddleware
from app.api.reports import router as reports_router
from app.api.teacher import router as teacher_router
from app.api.activities import router as activities_router
from app.api.auth import router as auth_router
from app.api.ws import router as ws_router
from app.api.submissions import router as submissions_router
from app import models as _models


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    create_db_tables()
    yield


def create_app() -> FastAPI:
    app = FastAPI(title="Student AI Grading System", lifespan=lifespan)
    app.add_middleware(
        InMemoryRateLimitMiddleware,
        requests_per_minute=settings.rate_limit_per_minute,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            origin.strip()
            for origin in settings.frontend_origins.split(",")
            if origin.strip()
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(auth_router)
    app.include_router(activities_router)
    app.include_router(teacher_router)
    app.include_router(reports_router)
    app.include_router(submissions_router)
    app.include_router(ws_router)

    @app.get("/health")
    def healthcheck() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()
