"""
Inventory Service API routes.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.services.inventory_service import InventoryService
from app.schemas.inventory import (
    InventoryCreate,
    InventoryUpdate,
    InventoryResponse,
    InventoryReserveRequest,
    InventoryReleaseRequest,
)
from app.core.dependencies import get_db
import logging

router = APIRouter(prefix="/inventory", tags=["inventory"])
logger = logging.getLogger(__name__)


@router.get("", response_model=dict)
async def list_inventory(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """List all inventory with pagination."""
    service = InventoryService(db)
    result = service.get_all_inventory(page, page_size)
    return result


@router.get("/product/{product_id}", response_model=InventoryResponse)
async def get_inventory_by_product(product_id: str, db: Session = Depends(get_db)):
    """Get inventory by product ID."""
    service = InventoryService(db)
    inventory = service.get_inventory_by_product(product_id)
    if not inventory:
        raise HTTPException(status_code=404, detail="Inventory not found")
    return inventory


@router.get("/available/{product_id}", response_model=dict)
async def get_available_quantity(product_id: str, db: Session = Depends(get_db)):
    """Get available quantity for a product."""
    service = InventoryService(db)
    available = service.get_available_quantity(product_id)
    return {"product_id": product_id, "available_quantity": available}


@router.post("", response_model=InventoryResponse, status_code=201)
async def create_inventory(
    product_id: str,
    inventory: InventoryCreate,
    db: Session = Depends(get_db),
):
    """Create inventory for a product."""
    service = InventoryService(db)
    try:
        return service.create_inventory(product_id, inventory)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.put("/{inventory_id}", response_model=InventoryResponse)
async def update_inventory(
    inventory_id: str, inventory: InventoryUpdate, db: Session = Depends(get_db)
):
    """Update inventory."""
    service = InventoryService(db)
    updated = service.update_inventory(inventory_id, inventory)
    if not updated:
        raise HTTPException(status_code=404, detail="Inventory not found")
    return updated


@router.post("/reserve", response_model=InventoryResponse)
async def reserve_inventory(
    order_id: str,
    product_id: str,
    quantity: int = Query(..., gt=0),
    db: Session = Depends(get_db),
):
    """Reserve inventory for an order."""
    service = InventoryService(db)
    try:
        return service.reserve_inventory(order_id, product_id, quantity)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/release", response_model=InventoryResponse)
async def release_inventory(
    order_id: str, product_id: str, db: Session = Depends(get_db)
):
    """Release reserved inventory."""
    service = InventoryService(db)
    try:
        return service.release_inventory(order_id, product_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/confirm/{order_id}", status_code=200)
async def confirm_reservation(order_id: str, db: Session = Depends(get_db)):
    """Confirm all reservations for an order."""
    service = InventoryService(db)
    success = service.confirm_reservation(order_id)
    if not success:
        raise HTTPException(status_code=404, detail="Order reservations not found")
    return {"status": "confirmed", "order_id": order_id}


@router.get("/check/{product_id}", response_model=dict)
async def check_stock(
    product_id: str, quantity: int = Query(..., gt=0), db: Session = Depends(get_db)
):
    """Check if product has sufficient stock."""
    service = InventoryService(db)
    has_stock = service.check_stock(product_id, quantity)
    return {"product_id": product_id, "quantity_requested": quantity, "available": has_stock}
