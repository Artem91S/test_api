from sqlalchemy import Column, Integer, Float, ForeignKey, Date
from sqlalchemy.orm import relationship
from datetime import datetime

from .base import Base


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    sum = Column(Float, nullable=False)
    payment_date = Column(Date, default=datetime.now().date())
    credit_id = Column(Integer, ForeignKey("credits.id"), nullable=False)
    type_id = Column(Integer, ForeignKey("dictionary.id"), nullable=False)

    credit = relationship("Credit")
    payment_type = relationship("Dictionary")

    def __repr__(self):
        return f"Payment(id={self.id}, sum={self.sum}, payment_date={self.payment_date}, credit_id={self.credit_id})"
