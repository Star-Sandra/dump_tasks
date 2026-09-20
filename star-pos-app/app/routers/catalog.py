from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.security import require_any_staff, require_manager_or_admin
from database import get_db
from app.repositories import category as category_repo, supplier as supplier_repo
from app.schemas.category import CategoryCreate, CategoryOut, CategoryUpdate
from app.schemas.supplier import SupplierCreate, SupplierOut, SupplierUpdate

router = APIRouter(prefix="/catalog", tags=["Catalog Lookups"])


@router.post("/categories", response_model=CategoryOut, status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(require_manager_or_admin)])
def create_category(category_in: CategoryCreate, db: Session = Depends(get_db)):
    return category_repo.create_category(db, category_in)


@router.get("/categories", response_model=list[CategoryOut], dependencies=[Depends(require_any_staff)])
def list_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return category_repo.list_categories(db, skip=skip, limit=limit)


@router.patch("/categories/{category_id}", response_model=CategoryOut,
              dependencies=[Depends(require_manager_or_admin)])
def update_category(category_id: int, category_in: CategoryUpdate, db: Session = Depends(get_db)):
    category = category_repo.get_category(db, category_id)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return category_repo.update_category(db, category, category_in)


@router.delete("/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(require_manager_or_admin)])
def delete_category(category_id: int, db: Session = Depends(get_db)):
    category = category_repo.get_category(db, category_id)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    category_repo.delete_category(db, category)


@router.post("/suppliers", response_model=SupplierOut, status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(require_manager_or_admin)])
def create_supplier(supplier_in: SupplierCreate, db: Session = Depends(get_db)):
    return supplier_repo.create_supplier(db, supplier_in)


@router.get("/suppliers", response_model=list[SupplierOut], dependencies=[Depends(require_any_staff)])
def list_suppliers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return supplier_repo.list_suppliers(db, skip=skip, limit=limit)


@router.patch("/suppliers/{supplier_id}", response_model=SupplierOut,
              dependencies=[Depends(require_manager_or_admin)])
def update_supplier(supplier_id: int, supplier_in: SupplierUpdate, db: Session = Depends(get_db)):
    supplier = supplier_repo.get_supplier(db, supplier_id)
    if not supplier:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Supplier not found")
    return supplier_repo.update_supplier(db, supplier, supplier_in)


@router.delete("/suppliers/{supplier_id}", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(require_manager_or_admin)])
def delete_supplier(supplier_id: int, db: Session = Depends(get_db)):
    supplier = supplier_repo.get_supplier(db, supplier_id)
    if not supplier:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Supplier not found")
    supplier_repo.delete_supplier(db, supplier)
