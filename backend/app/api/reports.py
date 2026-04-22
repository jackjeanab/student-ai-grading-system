from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.api.submissions import get_db_session
from app.services.report_service import build_assignment_report

router = APIRouter(prefix="/api/reports", tags=["reports"])


@router.get("/assignments/{assignment_id}")
def get_assignment_report(
    assignment_id: int,
    session: Session = Depends(get_db_session),
) -> dict[str, object]:
    return build_assignment_report(session, assignment_id)
