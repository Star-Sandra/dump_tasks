from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.security import require_any_staff
from database import get_db
from app.models.payment import Payment
from app.schemas.payment import PaymentOut

router = APIRouter(prefix="/payments", tags=["Payments & Receipts"], dependencies=[Depends(require_any_staff)])


@router.get("/{receipt_number}", response_model=PaymentOut)
def get_receipt(receipt_number: str, db: Session = Depends(get_db)):
    """Look up a payment/receipt by its unique receipt number."""
    payment = db.query(Payment).filter(Payment.receipt_number == receipt_number).first()
    if not payment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Receipt not found")
    return payment
