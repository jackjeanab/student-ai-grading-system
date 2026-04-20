from enum import Enum

from pydantic import BaseModel


class ReviewGrade(str, Enum):
    excellent = "優"
    good = "良"
    fair = "可"
    needs_improvement = "待加強"


class ReviewLight(str, Enum):
    green = "green"
    blue = "blue"
    yellow = "yellow"
    red = "red"


class OverrideRequest(BaseModel):
    grade: ReviewGrade
    light: ReviewLight
    reason: str
