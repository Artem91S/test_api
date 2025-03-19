from sqlalchemy import ForeignKey,Date
from sqlalchemy.orm import relationship,Mapped, mapped_column
from datetime import datetime
from .base import Base


class Plan(Base):
    __tablename__ = "plans"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    period: Mapped[datetime.date] = mapped_column(Date,nullable=False)
    sum: Mapped[float] = mapped_column(nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey("dictionary.id"), nullable=False)

    category: Mapped["Dictionary"] = relationship("Dictionary", back_populates="plans")

    def __repr__(self):
        return f"Plan(id={self.id}, period={self.period}, sum={self.sum}, category_id={self.category_id})"
