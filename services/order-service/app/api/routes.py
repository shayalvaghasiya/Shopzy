"""
Order Service API routes.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.services.order_service import OrderService
from app.schemas.order import OrderCreate, OrderUpdate, OrderResponse
from app.core.dependencies import get_db
import logging

router = APIRouter(prefix="/orders", tags=["orders"])
logger = logging.getLogger(__name__)


@router.get("", response_model=dict)
async def list_orders(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """List all orders with pagination."""
    service = OrderService(db)
    result = service.get_all_orders(page, page_size)
    return result


@router.get("/customer/{customer_id}", response_model=dict)
async def get_customer_orders(
    customer_id: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """Get orders for a customer."""
    service = OrderService(db)
    result = service.get_customer_orders(customer_id, page, page_size)
    return result


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(order_id: str, db: Session = Depends(get_db)):
    """Get order by ID."""
    service = OrderService(db)
    order = service.get_order(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.post("", response_model=OrderResponse, status_code=201)
async def create_order(
    order: OrderCreate, db: Session = Depends(get_db)
):
    """Create a new order."""
    service = OrderService(db)
    try:
        return service.create_order(order)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{order_id}/status/{status}", response_model=OrderResponse)
async def update_order_status(
    order_id: str, status: str, db: Session = Depends(get_db)
):
    """Update order status."""
    service = OrderService(db)
    try:
        updated = service.update_order_status(order_id, status)
        if not updated:
            raise HTTPException(status_code=404, detail="Order not found")
        return updated
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{order_id}/cancel", response_model=OrderResponse)
async def cancel_order(order_id: str, db: Session = Depends(get_db)):
    """Cancel an order."""
    service = OrderService(db)
    try:
        cancelled = service.cancel_order(order_id)
        if not cancelled:
            raise HTTPException(status_code=404, detail="Order not found")
        return cancelled
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{order_id}/items", response_model=OrderResponse)
async def add_items(
    order_id: str, items: list, db: Session = Depends(get_db)
):
    """Add items to an order."""
    service = OrderService(db)
    try:
        return service.add_items(order_id, items)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
