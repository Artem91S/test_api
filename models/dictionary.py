from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .base import Base


class Dictionary(Base):
    __tablename__ = "dictionary"

    id = Column(Integer, primary_key=True)
    name = Column(String(9), nullable=False)

    plans = relationship("Plan", back_populates="category")
    def __repr__(self):
        return f"Dictionary(id={self.id}, name={self.name})"
