from fastapi import APIRouter, Depends, Header, HTTPException

from app.schemas.review import OverrideRequest
from app.services.review_service import override_submission

router = APIRouter(prefix="/api/teacher", tags=["teacher"])


def require_teacher_authorization(authorization: str | None = Header(default=None)) -> None:
    if authorization != "Bearer dev-token":
        raise HTTPException(status_code=401, detail="Unauthorized")


@router.post("/submissions/{submission_id}/override")
def override_submission_endpoint(
    submission_id: int,
    payload: OverrideRequest,
    _: None = Depends(require_teacher_authorization),
) -> dict[str, object]:
    return override_submission(submission_id, payload.grade, payload.light, payload.reason)
