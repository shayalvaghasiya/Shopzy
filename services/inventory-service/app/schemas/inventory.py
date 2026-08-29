"""
Inventory Service schemas.
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class InventoryCreate(BaseModel):
    """Schema for creating inventory."""

    product_id: str = Field(..., min_length=1)
    available_quantity: int = Field(default=0, ge=0)


class InventoryUpdate(BaseModel):
    """Schema for updating inventory."""

    available_quantity: Optional[int] = Field(None, ge=0)


class InventoryReserveRequest(BaseModel):
    """Schema for reserving inventory."""

    order_id: str = Field(..., min_length=1)
    quantity: int = Field(..., gt=0)


class InventoryReleaseRequest(BaseModel):
    """Schema for releasing inventory."""

    order_id: str = Field(..., min_length=1)
    quantity: int = Field(..., gt=0)


class InventoryResponse(BaseModel):
    """Schema for inventory responses."""

    id: str
    product_id: str
    available_quantity: int
    reserved_quantity: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
