from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), unique=True, nullable=False)
    contact_phone = Column(String(32), nullable=True)
    contact_email = Column(String(120), nullable=True)

    products = relationship("Product", back_populates="supplier")
