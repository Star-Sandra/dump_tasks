"""Seed demo data. Run: python seed.py"""
from database import Base, SessionLocal, engine
from app.core.security import hash_password
from app.models.category import Category
from app.models.supplier import Supplier
from app.models.product import Product
from app.models.user import User, UserRole

Base.metadata.create_all(bind=engine)


def run():
    db = SessionLocal()
    try:
        if db.query(User).filter(User.email == "admin@starpos.local").first():
            print("Seed data already present, skipping.")
            return
        admin = User(full_name="Admin User", email="admin@starpos.local",
                     hashed_password=hash_password("Admin123!"), role=UserRole.ADMIN)
        cashier = User(full_name="Jane Cashier", email="cashier@starpos.local",
                        hashed_password=hash_password("Cashier123!"), role=UserRole.CASHIER)
        db.add_all([admin, cashier])

        beverages = Category(name="Beverages", description="Drinks, sodas, juices")
        db.add(beverages)
        supplier = Supplier(name="Metro Distributors", contact_phone="0700000000")
        db.add(supplier)
        db.flush()

        db.add(Product(name="Coca-Cola 500ml", sku="BEV-COKE-500", barcode="6001234567890",
                        category_id=beverages.id, supplier_id=supplier.id,
                        cost_price=40, price=60, stock_quantity=100, low_stock_threshold=10))
        db.commit()
        print("Seed data created. Admin: admin@starpos.local / Admin123!  Cashier: cashier@starpos.local / Cashier123!")
    finally:
        db.close()


if __name__ == "__main__":
    run()
