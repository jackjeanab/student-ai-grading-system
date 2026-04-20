from fastapi import APIRouter

from app.services.report_service import build_assignment_report

router = APIRouter(prefix="/api/reports", tags=["reports"])


@router.get("/assignments/{assignment_id}")
def get_assignment_report(assignment_id: int) -> dict[str, object]:
    return build_assignment_report(assignment_id)
