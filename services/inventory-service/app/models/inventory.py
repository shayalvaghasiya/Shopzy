"""
Inventory Service models.
"""

from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Inventory(Base):
    """Inventory database model."""

    __tablename__ = "inventory"

    id = Column(String(36), primary_key=True, index=True)
    product_id = Column(String(36), unique=True, index=True, nullable=False)
    available_quantity = Column(Integer, default=0, nullable=False)
    reserved_quantity = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self) -> str:
        return f"<Inventory {self.product_id}: available={self.available_quantity}, reserved={self.reserved_quantity}>"


class InventoryReservation(Base):
    """Track inventory reservations for orders."""

    __tablename__ = "inventory_reservations"

    id = Column(String(36), primary_key=True, index=True)
    order_id = Column(String(36), index=True, nullable=False)
    product_id = Column(String(36), index=True, nullable=False)
    quantity = Column(Integer, nullable=False)
    status = Column(String(50), default="reserved")  # reserved, released, confirmed
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    released_at = Column(DateTime, nullable=True)

    def __repr__(self) -> str:
        return f"<InventoryReservation order={self.order_id}, product={self.product_id}, qty={self.quantity}>"
