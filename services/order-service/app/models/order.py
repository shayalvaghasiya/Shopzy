"""
Order Service models.
"""

from datetime import datetime
from sqlalchemy import Column, String, Float, DateTime, Integer, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
import enum

Base = declarative_base()


class OrderStatus(str, enum.Enum):
    """Order status enum."""

    PENDING = "PENDING"
    PAYMENT_PENDING = "PAYMENT_PENDING"
    CONFIRMED = "CONFIRMED"
    PROCESSING = "PROCESSING"
    SHIPPED = "SHIPPED"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"
    FAILED = "FAILED"


class Order(Base):
    """Order database model."""

    __tablename__ = "orders"

    id = Column(String(36), primary_key=True, index=True)
    customer_id = Column(String(36), index=True, nullable=False)
    status = Column(String(50), default=OrderStatus.PENDING, index=True)
    subtotal = Column(Float, nullable=False)
    tax = Column(Float, default=0)
    shipping_cost = Column(Float, default=0)
    total_amount = Column(Float, nullable=False)
    currency = Column(String(3), default="USD")
    payment_id = Column(String(36), nullable=True)
    notes = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self) -> str:
        return f"<Order {self.id}: customer={self.customer_id}, status={self.status}, total={self.total_amount}>"


class OrderItem(Base):
    """Order items model."""

    __tablename__ = "order_items"

    id = Column(String(36), primary_key=True, index=True)
    order_id = Column(String(36), ForeignKey("orders.id"), index=True, nullable=False)
    product_id = Column(String(36), index=True, nullable=False)
    product_name = Column(String(255), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    total_price = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self) -> str:
        return f"<OrderItem order={self.order_id}, product={self.product_id}, qty={self.quantity}>"


class IdempotencyRecord(Base):
    """Track idempotent requests to prevent duplicates."""

    __tablename__ = "idempotency_records"

    id = Column(String(36), primary_key=True, index=True)
    idempotency_key = Column(String(255), unique=True, index=True, nullable=False)
    service = Column(String(100), nullable=False)
    endpoint = Column(String(255), nullable=False)
    request_hash = Column(String(64), nullable=False)
    response_data = Column(String(5000), nullable=True)  # JSON response
    status_code = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    expires_at = Column(DateTime, nullable=False)  # Records expire after 24 hours

    def __repr__(self) -> str:
        return f"<IdempotencyRecord key={self.idempotency_key}, service={self.service}>"
