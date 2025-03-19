from sqlalchemy import Column, Integer, Date, String
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from .base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(String(40), unique=True)
    registration_date: Mapped[datetime.date] = mapped_column(Date, default=datetime.now().date())
    def __repr__(self):
        return f"User(id={self.id}, login={self.login})"


