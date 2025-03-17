from sqlalchemy import Column, Integer, Float, ForeignKey, Date
from sqlalchemy.orm import relationship
from .base import Base


class Plan(Base):
    __tablename__ = "plans"

    id = Column(Integer, primary_key=True, index=True)
    period = Column(Date, nullable=False)
    sum = Column(Float, nullable=False)
    category_id = Column(Integer, ForeignKey("dictionary.id"), nullable=False)

    category = relationship("Dictionary")

    def __repr__(self):
        return f"Plan(id={self.id}, period={self.period}, sum={self.sum}, category_id={self.category_id})"
