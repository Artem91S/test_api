from sqlalchemy import String
from sqlalchemy.orm import relationship,mapped_column,Mapped
from typing import List
from .base import Base


class Dictionary(Base):
    __tablename__ = "dictionary"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(9), nullable=False)

    plans: Mapped[List["Plan"]] = relationship("Plan", back_populates="category")

    def __repr__(self):
        return f"Dictionary(id={self.id}, name={self.name})"
