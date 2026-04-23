from fastapi import APIRouter, Header, HTTPException, status

from app.core.database import get_session_local
from app.models.assignment import Assignment
from app.schemas.assignment import AssignmentCreate, AssignmentResponse

router = APIRouter(prefix="/api/assignments", tags=["assignments"])


@router.post("", response_model=AssignmentResponse, status_code=status.HTTP_201_CREATED)
def upsert_assignment(
    payload: AssignmentCreate,
    authorization: str | None = Header(default=None),
) -> AssignmentResponse:
    if authorization != "Bearer dev-token":
        raise HTTPException(status_code=401, detail="Unauthorized")

    with get_session_local()() as session:
        assignment = session.get(Assignment, payload.id) if payload.id is not None else None
        if assignment is None:
            assignment = Assignment(
                id=payload.id,
                title=payload.title,
                description=payload.description,
            )
            session.add(assignment)
        else:
            assignment.title = payload.title
            assignment.description = payload.description

        session.commit()
        session.refresh(assignment)
        return AssignmentResponse(
            id=assignment.id,
            title=assignment.title,
            description=assignment.description,
        )
