from sqlalchemy import Column, Integer, Date, Float, ForeignKey

from datetime import datetime
from .base import Base


class Credit(Base):
    __tablename__ = "credits"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    issuance_date = Column(Date, default=datetime.now().date())
    return_date = Column(Date)
    actual_return_date = Column(Date, nullable=True)
    body = Column(Float)
    percent = Column(Float)

    def __repr__(self):
        return f"Credit(id={self.id}, user_id={self.user_id}, body={self.body})"
