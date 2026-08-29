"""
Order Service schemas for request/response validation.
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class OrderItemCreate(BaseModel):
    """Schema for creating order items."""

    product_id: str = Field(..., min_length=1)
    product_name: str = Field(..., min_length=1)
    quantity: int = Field(..., gt=0)
    unit_price: float = Field(..., gt=0)


class OrderItemResponse(BaseModel):
    """Schema for order item responses."""

    id: str
    order_id: str
    product_id: str
    product_name: str
    quantity: int
    unit_price: float
    total_price: float
    created_at: datetime

    class Config:
        from_attributes = True


class OrderCreate(BaseModel):
    """Schema for creating an order."""

    customer_id: str = Field(..., min_length=1)
    items: List[OrderItemCreate]
    idempotency_key: Optional[str] = None


class OrderUpdate(BaseModel):
    """Schema for updating an order."""

    status: Optional[str] = None
    notes: Optional[str] = None


class OrderResponse(BaseModel):
    """Schema for order responses."""

    id: str
    customer_id: str
    status: str
    subtotal: float
    tax: float
    shipping_cost: float
    total_amount: float
    currency: str
    payment_id: Optional[str]
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
