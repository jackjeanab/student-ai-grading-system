from pydantic import BaseModel


class AssignmentResponse(BaseModel):
    id: int
    title: str
    description: str | None = None
