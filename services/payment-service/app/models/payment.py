"""
Payment Service models.
"""

from datetime import datetime
from sqlalchemy import Column, String, Float, DateTime, Enum
from sqlalchemy.ext.declarative import declarative_base
import enum

Base = declarative_base()


class PaymentStatus(str, enum.Enum):
    """Payment status enum."""

    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    REFUNDED = "REFUNDED"
    CANCELLED = "CANCELLED"


class Payment(Base):
    """Payment database model."""

    __tablename__ = "payments"

    id = Column(String(36), primary_key=True, index=True)
    order_id = Column(String(36), unique=True, index=True, nullable=False)
    customer_id = Column(String(36), index=True, nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String(3), default="USD")
    status = Column(String(50), default=PaymentStatus.PENDING, index=True)
    transaction_reference = Column(String(255), unique=True, nullable=True)
    failure_reason = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    processed_at = Column(DateTime, nullable=True)

    def __repr__(self) -> str:
        return f"<Payment {self.id}: order={self.order_id}, amount={self.amount}, status={self.status}>"
