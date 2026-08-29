"""
Customer Service models.
"""

from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Customer(Base):
    """Customer database model."""

    __tablename__ = "customers"

    id = Column(String(36), primary_key=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    phone = Column(String(20), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self) -> str:
        return f"<Customer {self.id}: {self.first_name} {self.last_name}>"


class Address(Base):
    """Customer addresses model."""

    __tablename__ = "addresses"

    id = Column(String(36), primary_key=True, index=True)
    customer_id = Column(String(36), ForeignKey("customers.id"), index=True, nullable=False)
    type = Column(String(50), default="shipping")  # shipping, billing
    street_address = Column(String(255), nullable=False)
    city = Column(String(100), nullable=False)
    state_province = Column(String(100), nullable=False)
    postal_code = Column(String(20), nullable=False)
    country = Column(String(100), nullable=False)
    is_default = Column(String(1), default="N")  # Y or N
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self) -> str:
        return f"<Address {self.id}: {self.customer_id}, {self.city}, {self.country}>"
