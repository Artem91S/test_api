from sqlalchemy import ForeignKey,Date
from sqlalchemy.orm import relationship,Mapped,mapped_column
from datetime import datetime
from .base import Base


class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(primary_key=True)
    sum: Mapped[float] = mapped_column(nullable=False)
    payment_date: Mapped[datetime.date] = mapped_column(Date, default=datetime.now().date())
    credit_id: Mapped[int] = mapped_column(ForeignKey("credits.id"), nullable=False)
    type_id: Mapped[int] = mapped_column(ForeignKey("dictionary.id"), nullable=False)

    credit: Mapped["Credit"] = relationship("Credit")
    payment_type: Mapped["Dictionary"] = relationship("Dictionary")


    def __repr__(self):
        return f"Payment(id={self.id}, sum={self.sum}, payment_date={self.payment_date}, credit_id={self.credit_id})"
