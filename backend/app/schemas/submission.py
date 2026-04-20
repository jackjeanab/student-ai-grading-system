from pydantic import BaseModel


class SubmissionCreate(BaseModel):
    assignment_id: int
    activity_id: int
    xml_content: str
