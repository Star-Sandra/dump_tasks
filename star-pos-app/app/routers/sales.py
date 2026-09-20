from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.security import get_current_user, require_any_staff, require_manager_or_admin
from database import get_db
from app.models.user import User
from app.repositories import sale as sale_repo
from app.schemas.sale import SaleCreate, SaleOut
from app.services.sale_service import create_sale, void_sale

router = APIRouter(prefix="/sales", tags=["Sales Checkout"], dependencies=[Depends(require_any_staff)])


@router.post("", response_model=SaleOut, status_code=status.HTTP_201_CREATED)
def checkout(sale_in: SaleCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Submit a shopping cart: validates stock, computes totals safely, deducts stock, records payment(s)."""
    return create_sale(db, sale_in, cashier_id=current_user.id)


@router.get("", response_model=list[SaleOut])
def list_sales(skip: int = 0, limit: int = 100, cashier_id: Optional[int] = None, db: Session = Depends(get_db)):
    return sale_repo.list_sales(db, skip=skip, limit=limit, cashier_id=cashier_id)


@router.get("/{sale_id}", response_model=SaleOut)
def get_sale(sale_id: int, db: Session = Depends(get_db)):
    sale = sale_repo.get_sale(db, sale_id)
    if not sale:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sale not found")
    return sale


@router.post("/{sale_id}/void", response_model=SaleOut, dependencies=[Depends(require_manager_or_admin)])
def void_a_sale(sale_id: int, db: Session = Depends(get_db)):
    sale = sale_repo.get_sale(db, sale_id)
    if not sale:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sale not found")
    return void_sale(db, sale)
