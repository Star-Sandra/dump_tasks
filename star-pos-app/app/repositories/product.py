from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate


def get_product(db: Session, product_id: int) -> Optional[Product]:
    return db.query(Product).filter(Product.id == product_id).first()


def get_product_by_sku(db: Session, sku: str) -> Optional[Product]:
    return db.query(Product).filter(Product.sku == sku).first()


def get_product_by_barcode(db: Session, barcode: str) -> Optional[Product]:
    return db.query(Product).filter(Product.barcode == barcode).first()


def list_products(db: Session, skip: int = 0, limit: int = 100,
                   category_id: Optional[int] = None, active_only: bool = True,
                   search: Optional[str] = None) -> List[Product]:
    query = db.query(Product)
    if active_only:
        query = query.filter(Product.is_active.is_(True))
    if category_id is not None:
        query = query.filter(Product.category_id == category_id)
    if search:
        query = query.filter(Product.name.ilike(f"%{search}%"))
    return query.offset(skip).limit(limit).all()


def list_low_stock_products(db: Session) -> List[Product]:
    return (
        db.query(Product)
        .filter(Product.is_active.is_(True), Product.stock_quantity <= Product.low_stock_threshold)
        .all()
    )


def create_product(db: Session, product_in: ProductCreate) -> Product:
    product = Product(**product_in.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def update_product(db: Session, product: Product, product_in: ProductUpdate) -> Product:
    for field, value in product_in.model_dump(exclude_unset=True).items():
        setattr(product, field, value)
    db.commit()
    db.refresh(product)
    return product


def delete_product(db: Session, product: Product) -> None:
    product.is_active = False
    db.commit()
