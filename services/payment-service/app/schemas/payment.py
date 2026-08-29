"""
Payment Service schemas for request/response validation.
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class PaymentCreate(BaseModel):
    """Schema for creating a payment."""

    order_id: str = Field(..., min_length=1)
    customer_id: str = Field(..., min_length=1)
    amount: float = Field(..., gt=0)
    currency: str = Field(default="USD", pattern="^[A-Z]{3}$")


class PaymentUpdateStatus(BaseModel):
    """Schema for updating payment status."""

    status: str = Field(..., pattern="^(PENDING|PROCESSING|SUCCESS|FAILED|REFUNDED|CANCELLED)$")


class PaymentResponse(BaseModel):
    """Schema for payment responses."""

    id: str
    order_id: str
    customer_id: str
    amount: float
    currency: str
    status: str
    transaction_reference: Optional[str]
    failure_reason: Optional[str]
    created_at: datetime
    updated_at: datetime
    processed_at: Optional[datetime]

    class Config:
        from_attributes = True
