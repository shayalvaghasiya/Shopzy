"""
Customer Service API routes.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.services.customer_service import CustomerService
from app.schemas.customer import (
    CustomerCreate,
    CustomerUpdate,
    CustomerResponse,
    CustomerDetailResponse,
    AddressCreate,
    AddressUpdate,
    AddressResponse,
)
from app.core.dependencies import get_db
import logging

router = APIRouter(prefix="/customers", tags=["customers"])
logger = logging.getLogger(__name__)


@router.get("", response_model=dict)
async def list_customers(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """List all customers with pagination."""
    service = CustomerService(db)
    result = service.get_all_customers(page, page_size)
    return result


@router.get("/{customer_id}", response_model=CustomerDetailResponse)
async def get_customer(customer_id: str, db: Session = Depends(get_db)):
    """Get customer by ID with addresses."""
    service = CustomerService(db)
    customer = service.get_customer_detail(customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


@router.post("", response_model=CustomerResponse, status_code=201)
async def create_customer(
    customer: CustomerCreate, db: Session = Depends(get_db)
):
    """Create a new customer."""
    service = CustomerService(db)
    try:
        return service.create_customer(customer)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.put("/{customer_id}", response_model=CustomerResponse)
async def update_customer(
    customer_id: str, customer: CustomerUpdate, db: Session = Depends(get_db)
):
    """Update a customer."""
    service = CustomerService(db)
    updated = service.update_customer(customer_id, customer)
    if not updated:
        raise HTTPException(status_code=404, detail="Customer not found")
    return updated


@router.delete("/{customer_id}", status_code=204)
async def delete_customer(customer_id: str, db: Session = Depends(get_db)):
    """Delete a customer."""
    service = CustomerService(db)
    success = service.delete_customer(customer_id)
    if not success:
        raise HTTPException(status_code=404, detail="Customer not found")
    return None


@router.get("/{customer_id}/addresses", response_model=list)
async def get_customer_addresses(
    customer_id: str, db: Session = Depends(get_db)
):
    """Get all addresses for a customer."""
    service = CustomerService(db)
    try:
        addresses = service.get_customer_addresses(customer_id)
        return addresses
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/{customer_id}/addresses", response_model=AddressResponse, status_code=201)
async def add_address(
    customer_id: str, address: AddressCreate, db: Session = Depends(get_db)
):
    """Add an address to a customer."""
    service = CustomerService(db)
    try:
        return service.add_address(customer_id, address)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/addresses/{address_id}", response_model=AddressResponse)
async def update_address(
    address_id: str, address: AddressUpdate, db: Session = Depends(get_db)
):
    """Update an address."""
    service = CustomerService(db)
    updated = service.update_address(address_id, address)
    if not updated:
        raise HTTPException(status_code=404, detail="Address not found")
    return updated


@router.delete("/addresses/{address_id}", status_code=204)
async def delete_address(address_id: str, db: Session = Depends(get_db)):
    """Delete an address."""
    service = CustomerService(db)
    success = service.delete_address(address_id)
    if not success:
        raise HTTPException(status_code=404, detail="Address not found")
    return None
