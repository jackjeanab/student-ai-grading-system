from app.api.auth import router as auth_router
from app.api.activities import router as activities_router
from app.api.reports import router as reports_router
from app.api.teacher import router as teacher_router
from app.api.submissions import router as submissions_router

__all__ = [
    "auth_router",
    "activities_router",
    "reports_router",
    "teacher_router",
    "submissions_router",
]
