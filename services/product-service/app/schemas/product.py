"""
Product Service schemas for request/response validation.
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class ProductCreate(BaseModel):
    """Schema for creating a product."""

    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=2000)
    sku: str = Field(..., min_length=1, max_length=100)
    price: float = Field(..., gt=0)
    category: str = Field(..., min_length=1, max_length=100)
    subcategory: Optional[str] = Field(None, max_length=100)
    brand: Optional[str] = Field(None, max_length=100)
    image_url: Optional[str] = None
    stock_count: int = Field(default=0, ge=0)


class ProductUpdate(BaseModel):
    """Schema for updating a product."""

    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=2000)
    price: Optional[float] = Field(None, gt=0)
    category: Optional[str] = Field(None, min_length=1, max_length=100)
    subcategory: Optional[str] = None
    brand: Optional[str] = None
    image_url: Optional[str] = None
    status: Optional[str] = Field(None, pattern="^(active|inactive|discontinued)$")
    stock_count: Optional[int] = Field(None, ge=0)


class ProductResponse(BaseModel):
    """Schema for product responses."""

    id: str
    name: str
    description: Optional[str]
    sku: str
    price: float
    category: str
    subcategory: Optional[str]
    brand: Optional[str]
    image_url: Optional[str]
    status: str
    stock_count: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProductListResponse(BaseModel):
    """Schema for product list responses."""

    items: List[ProductResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


class SearchProductsRequest(BaseModel):
    """Schema for product search."""

    query: str = Field(..., min_length=1)
    category: Optional[str] = None
    brand: Optional[str] = None
    min_price: Optional[float] = Field(None, ge=0)
    max_price: Optional[float] = Field(None, ge=0)
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)
