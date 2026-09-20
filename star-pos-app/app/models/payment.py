import enum
import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Enum, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class PaymentMethod(str, enum.Enum):
    CASH = "cash"
    CARD = "card"
    MOBILE_MONEY = "mobile_money"


def generate_receipt_number() -> str:
    return f"RCPT-{uuid.uuid4().hex[:10].upper()}"


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    sale_id = Column(Integer, ForeignKey("sales.id"), nullable=False)
    receipt_number = Column(String(32), unique=True, index=True, default=generate_receipt_number)

    method = Column(Enum(PaymentMethod), nullable=False)
    amount = Column(Float, nullable=False)
    reference = Column(String(120), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    sale = relationship("Sale", back_populates="payments")
