import enum
import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Enum, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class SaleStatus(str, enum.Enum):
    COMPLETED = "completed"
    VOIDED = "voided"


def generate_sale_number() -> str:
    return f"SALE-{uuid.uuid4().hex[:10].upper()}"


class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    sale_number = Column(String(32), unique=True, index=True, default=generate_sale_number)
    cashier_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    subtotal = Column(Float, nullable=False, default=0.0)
    tax_amount = Column(Float, nullable=False, default=0.0)
    discount_amount = Column(Float, nullable=False, default=0.0)
    total_amount = Column(Float, nullable=False, default=0.0)

    status = Column(Enum(SaleStatus), default=SaleStatus.COMPLETED, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    cashier = relationship("User", back_populates="sales")
    items = relationship("SaleItem", back_populates="sale", cascade="all, delete-orphan")
    payments = relationship("Payment", back_populates="sale", cascade="all, delete-orphan")
