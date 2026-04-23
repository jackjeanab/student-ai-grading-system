from pydantic import BaseModel


class SubmissionCreate(BaseModel):
    assignment_id: int
    activity_id: int
    assignment_prompt: str | None = None
    xml_content: str
