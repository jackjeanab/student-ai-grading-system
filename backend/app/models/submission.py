from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Submission(Base):
    __tablename__ = "submissions"

    id: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    activity_id: Mapped[int | None] = mapped_column(ForeignKey("class_activities.id"), nullable=True)
    assignment_id: Mapped[int | None] = mapped_column(ForeignKey("assignments.id"), nullable=True)
    xml_content: Mapped[str] = mapped_column(Text())
    status: Mapped[str] = mapped_column(String(50), default="queued")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

    activity: Mapped["ClassActivity"] = relationship(back_populates="submissions")
    assignment: Mapped["Assignment"] = relationship(back_populates="submissions")
    evaluations: Mapped[list["Evaluation"]] = relationship(back_populates="submission")
