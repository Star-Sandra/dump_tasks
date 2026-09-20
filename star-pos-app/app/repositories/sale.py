from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from app.models.sale import Sale


def get_sale(db: Session, sale_id: int) -> Optional[Sale]:
    return (
        db.query(Sale)
        .options(joinedload(Sale.items), joinedload(Sale.payments))
        .filter(Sale.id == sale_id)
        .first()
    )


def list_sales(db: Session, skip: int = 0, limit: int = 100,
                cashier_id: Optional[int] = None) -> List[Sale]:
    query = db.query(Sale).options(joinedload(Sale.items), joinedload(Sale.payments))
    if cashier_id is not None:
        query = query.filter(Sale.cashier_id == cashier_id)
    return query.order_by(Sale.created_at.desc()).offset(skip).limit(limit).all()
