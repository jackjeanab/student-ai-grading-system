from pydantic import BaseModel


class ActivityCreate(BaseModel):
    title: str
    assignment_ids: list[int]
    status: str


class ActivityResponse(ActivityCreate):
    id: int
