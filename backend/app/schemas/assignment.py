from pydantic import BaseModel


class AssignmentCreate(BaseModel):
    id: int | None = None
    title: str
    description: str | None = None


class AssignmentResponse(BaseModel):
    id: int
    title: str
    description: str | None = None
