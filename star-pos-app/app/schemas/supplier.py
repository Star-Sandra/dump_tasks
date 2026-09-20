from typing import Optional
from pydantic import BaseModel, ConfigDict


class SupplierCreate(BaseModel):
    name: str
    contact_phone: Optional[str] = None
    contact_email: Optional[str] = None


class SupplierUpdate(BaseModel):
    name: Optional[str] = None
    contact_phone: Optional[str] = None
    contact_email: Optional[str] = None


class SupplierOut(SupplierCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
