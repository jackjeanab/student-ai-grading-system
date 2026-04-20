from pydantic import BaseModel


class EvaluationDecision(BaseModel):
    light: str
    grade: str
    source: str
