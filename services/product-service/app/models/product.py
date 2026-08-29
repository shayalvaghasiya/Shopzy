"""
Product Service - Manages product catalog.
"""

from datetime import datetime
from typing import Optional
from sqlalchemy import Column, String, Float, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Product(Base):
    """Product database model."""

    __tablename__ = "products"

    id = Column(String(36), primary_key=True, index=True)
    sku = Column(String(100), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False, index=True)
    description = Column(String(2000))
    category = Column(String(100), index=True)
    subcategory = Column(String(100))
    brand = Column(String(100))
    price = Column(Float, nullable=False)
    status = Column(String(50), default="active", index=True)  # active, inactive, discontinued
    image_url = Column(String(500))
    stock_count = Column(Integer, default=0)  # Denormalized for quick access
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self) -> str:
        return f"<Product {self.id}: {self.name}>"
