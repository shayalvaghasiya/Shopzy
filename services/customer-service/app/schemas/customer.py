"""
Customer Service schemas for request/response validation.
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime


class AddressCreate(BaseModel):
    """Schema for creating an address."""

    type: str = Field(default="shipping", regex="^(shipping|billing)$")
    street_address: str = Field(..., min_length=1, max_length=255)
    city: str = Field(..., min_length=1, max_length=100)
    state_province: str = Field(..., min_length=1, max_length=100)
    postal_code: str = Field(..., min_length=1, max_length=20)
    country: str = Field(..., min_length=1, max_length=100)
    is_default: Optional[str] = Field(default="N", regex="^[YN]$")


class AddressUpdate(BaseModel):
    """Schema for updating an address."""

    type: Optional[str] = Field(None, regex="^(shipping|billing)$")
    street_address: Optional[str] = Field(None, min_length=1, max_length=255)
    city: Optional[str] = Field(None, min_length=1, max_length=100)
    state_province: Optional[str] = Field(None, min_length=1, max_length=100)
    postal_code: Optional[str] = Field(None, min_length=1, max_length=20)
    country: Optional[str] = Field(None, min_length=1, max_length=100)
    is_default: Optional[str] = Field(None, regex="^[YN]$")


class AddressResponse(BaseModel):
    """Schema for address responses."""

    id: str
    customer_id: str
    type: str
    street_address: str
    city: str
    state_province: str
    postal_code: str
    country: str
    is_default: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CustomerCreate(BaseModel):
    """Schema for creating a customer."""

    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    phone: Optional[str] = Field(None, max_length=20)


class CustomerUpdate(BaseModel):
    """Schema for updating a customer."""

    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=20)


class CustomerResponse(BaseModel):
    """Schema for customer responses."""

    id: str
    first_name: str
    last_name: str
    email: str
    phone: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CustomerDetailResponse(BaseModel):
    """Schema for detailed customer response with addresses."""

    id: str
    first_name: str
    last_name: str
    email: str
    phone: Optional[str]
    addresses: List[AddressResponse]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
