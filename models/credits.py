from sqlalchemy import Integer, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional
from datetime import datetime
from .base import Base


class Credit(Base):
    __tablename__ = "credits"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    issuance_date: Mapped[datetime.date] = mapped_column(Date, default=datetime.now().date())
    return_date: Mapped[datetime.date]=mapped_column(Date)
    actual_return_date: Mapped[Optional[datetime.date]] = mapped_column(Date,nullable=True)
    body: Mapped[float]
    percent: Mapped[float]

    def __repr__(self):
        return f"Credit(id={self.id}, user_id={self.user_id}, body={self.body})"
