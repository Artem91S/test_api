from sqlalchemy import Column, Integer, String

from .base import Base


class Dictionary(Base):
    __tablename__ = "dictionary"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(9), nullable=False)

    def __repr__(self):
        return f"Dictionary(id={self.id}, name={self.name})"
