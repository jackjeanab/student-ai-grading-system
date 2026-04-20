from fastapi import APIRouter, Header, HTTPException, status

from app.schemas.activity import ActivityCreate, ActivityResponse

router = APIRouter(prefix="/api/activities", tags=["activities"])


@router.post("", response_model=ActivityResponse, status_code=status.HTTP_201_CREATED)
def create_activity(
    payload: ActivityCreate,
    authorization: str | None = Header(default=None),
) -> ActivityResponse:
    if authorization != "Bearer dev-token":
        raise HTTPException(status_code=401, detail="Unauthorized")
    return ActivityResponse(id=1, **payload.model_dump())
