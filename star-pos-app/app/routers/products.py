from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.security import require_any_staff, require_manager_or_admin
from database import get_db
from app.repositories import product as product_repo
from app.schemas.product import ProductCreate, ProductOut, ProductUpdate, StockAdjustment

router = APIRouter(prefix="/products", tags=["Inventory Control"])


@router.post("", response_model=ProductOut, status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(require_manager_or_admin)])
def create_product(product_in: ProductCreate, db: Session = Depends(get_db)):
    if product_repo.get_product_by_sku(db, product_in.sku):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="SKU already exists")
    return product_repo.create_product(db, product_in)


@router.get("", response_model=list[ProductOut], dependencies=[Depends(require_any_staff)])
def list_products(skip: int = 0, limit: int = 100, category_id: Optional[int] = None,
                   search: Optional[str] = None, db: Session = Depends(get_db)):
    return product_repo.list_products(db, skip=skip, limit=limit, category_id=category_id, search=search)


@router.get("/low-stock", response_model=list[ProductOut], dependencies=[Depends(require_any_staff)])
def low_stock_products(db: Session = Depends(get_db)):
    return product_repo.list_low_stock_products(db)


@router.get("/barcode/{barcode}", response_model=ProductOut, dependencies=[Depends(require_any_staff)])
def get_product_by_barcode(barcode: str, db: Session = Depends(get_db)):
    product = product_repo.get_product_by_barcode(db, barcode)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found for that barcode")
    return product


@router.get("/{product_id}", response_model=ProductOut, dependencies=[Depends(require_any_staff)])
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = product_repo.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product


@router.patch("/{product_id}", response_model=ProductOut, dependencies=[Depends(require_manager_or_admin)])
def update_product(product_id: int, product_in: ProductUpdate, db: Session = Depends(get_db)):
    product = product_repo.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product_repo.update_product(db, product, product_in)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(require_manager_or_admin)])
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = product_repo.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    product_repo.delete_product(db, product)


@router.post("/{product_id}/restock", response_model=ProductOut, dependencies=[Depends(require_manager_or_admin)])
def restock_product(product_id: int, adjustment: StockAdjustment, db: Session = Depends(get_db)):
    """Positive quantity_change restocks; negative removes stock (e.g. damage)."""
    product = product_repo.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    new_qty = product.stock_quantity + adjustment.quantity_change
    if new_qty < 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Adjustment would result in negative stock")
    product.stock_quantity = new_qty
    db.commit()
    db.refresh(product)
    return product
