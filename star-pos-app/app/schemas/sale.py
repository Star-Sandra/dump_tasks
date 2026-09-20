from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field, model_validator
from app.models.sale import SaleStatus
from app.schemas.payment import PaymentCreate, PaymentOut


class SaleItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)


class SaleItemOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    product_id: int
    quantity: int
    unit_price: float
    subtotal: float


class SaleCreate(BaseModel):
    items: List[SaleItemCreate]
    payments: List[PaymentCreate]
    discount_amount: float = Field(ge=0, default=0.0)

    @model_validator(mode="after")
    def check_items_not_empty(self):
        if not self.items:
            raise ValueError("A sale must contain at least one item")
        return self


class SaleOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    sale_number: str
    cashier_id: int
    subtotal: float
    tax_amount: float
    discount_amount: float
    total_amount: float
    status: SaleStatus
    created_at: datetime
    items: List[SaleItemOut]
    payments: List[PaymentOut]
