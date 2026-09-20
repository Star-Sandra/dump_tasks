from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.supplier import Supplier
from app.schemas.supplier import SupplierCreate, SupplierUpdate


def get_supplier(db: Session, supplier_id: int) -> Optional[Supplier]:
    return db.query(Supplier).filter(Supplier.id == supplier_id).first()


def list_suppliers(db: Session, skip: int = 0, limit: int = 100) -> List[Supplier]:
    return db.query(Supplier).offset(skip).limit(limit).all()


def create_supplier(db: Session, supplier_in: SupplierCreate) -> Supplier:
    supplier = Supplier(**supplier_in.model_dump())
    db.add(supplier)
    db.commit()
    db.refresh(supplier)
    return supplier


def update_supplier(db: Session, supplier: Supplier, supplier_in: SupplierUpdate) -> Supplier:
    for field, value in supplier_in.model_dump(exclude_unset=True).items():
        setattr(supplier, field, value)
    db.commit()
    db.refresh(supplier)
    return supplier


def delete_supplier(db: Session, supplier: Supplier) -> None:
    db.delete(supplier)
    db.commit()
