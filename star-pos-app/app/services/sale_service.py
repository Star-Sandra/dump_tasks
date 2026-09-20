import os
from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload
from app.models.payment import Payment
from app.models.product import Product
from app.models.sale import Sale, SaleStatus
from app.models.sale_item import SaleItem
from app.schemas.sale import SaleCreate

DEFAULT_TAX_RATE = float(os.getenv("DEFAULT_TAX_RATE", "0.16"))

def create_sale(db: Session, sale_in: SaleCreate, cashier_id: int) -> Sale:
    line_items = []
    subtotal = 0.0

    for item in sale_in.items:
        query = db.query(Product).filter(Product.id == item.product_id, Product.is_active.is_(True))
        if db.bind.dialect.name != "sqlite":
            query = query.with_for_update()
        product = query.first()
        if product is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                 detail=f"Product {item.product_id} not found or inactive")
        if product.stock_quantity < item.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Insufficient stock for '{product.name}': requested {item.quantity}, "
                       f"available {product.stock_quantity}",
            )
        line_subtotal = round(product.price * item.quantity, 2)
        subtotal += line_subtotal
        line_items.append((product, item.quantity, line_subtotal))

    discount_amount = round(sale_in.discount_amount, 2)
    if discount_amount > subtotal:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Discount cannot exceed subtotal")

    taxable_amount = subtotal - discount_amount
    tax_amount = round(taxable_amount * DEFAULT_TAX_RATE, 2)
    total_amount = round(taxable_amount + tax_amount, 2)

    total_paid = round(sum(p.amount for p in sale_in.payments), 2)
    if total_paid < total_amount:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                             detail=f"Payments ({total_paid}) do not cover total owed ({total_amount})")

    sale = Sale(cashier_id=cashier_id, subtotal=round(subtotal, 2), tax_amount=tax_amount,
                discount_amount=discount_amount, total_amount=total_amount, status=SaleStatus.COMPLETED)
    db.add(sale)
    db.flush()

    for product, quantity, line_subtotal in line_items:
        db.add(SaleItem(sale_id=sale.id, product_id=product.id, quantity=quantity,
                         unit_price=product.price, subtotal=line_subtotal))
        product.stock_quantity -= quantity

    for payment in sale_in.payments:
        db.add(Payment(sale_id=sale.id, method=payment.method, amount=payment.amount,
                        reference=payment.reference))

    try:
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to record sale")

    return (
        db.query(Sale)
        .options(joinedload(Sale.items), joinedload(Sale.payments))
        .filter(Sale.id == sale.id)
        .first()
    )

def void_sale(db: Session, sale: Sale) -> Sale:
    if sale.status != SaleStatus.COMPLETED:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only completed sales can be voided")
    for item in sale.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if product:
            product.stock_quantity += item.quantity
    sale.status = SaleStatus.VOIDED
    db.commit()
    db.refresh(sale)
    return sale
