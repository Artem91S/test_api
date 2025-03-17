from sqlalchemy import Column, Integer, Date, String
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    login = Column(String(40), unique=True, index=True)
    registration_date = Column(Date, default=datetime.now().date())

    def __repr__(self):
        return f"User(id={self.id}, login={self.login})"


