from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from app.models.payment import PaymentMethod


class PaymentCreate(BaseModel):
    method: PaymentMethod
    amount: float = Field(gt=0)
    reference: Optional[str] = None


class PaymentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    receipt_number: str
    method: PaymentMethod
    amount: float
    reference: Optional[str] = None
    created_at: datetime
