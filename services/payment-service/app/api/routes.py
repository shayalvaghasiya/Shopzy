"""
Payment Service API routes.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.services.payment_service import PaymentService
from app.schemas.payment import PaymentCreate, PaymentUpdateStatus, PaymentResponse
from app.core.dependencies import get_db
import logging

router = APIRouter(prefix="/payments", tags=["payments"])
logger = logging.getLogger(__name__)


@router.get("", response_model=dict)
async def list_payments(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """List all payments with pagination."""
    service = PaymentService(db)
    result = service.get_all_payments(page, page_size)
    return result


@router.get("/{payment_id}", response_model=PaymentResponse)
async def get_payment(payment_id: str, db: Session = Depends(get_db)):
    """Get payment by ID."""
    service = PaymentService(db)
    payment = service.get_payment(payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment


@router.get("/order/{order_id}", response_model=PaymentResponse)
async def get_payment_by_order(order_id: str, db: Session = Depends(get_db)):
    """Get payment by order ID."""
    service = PaymentService(db)
    payment = service.get_payment_by_order(order_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found for order")
    return payment


@router.post("", response_model=PaymentResponse, status_code=201)
async def create_payment(
    payment: PaymentCreate, db: Session = Depends(get_db)
):
    """Create a new payment."""
    service = PaymentService(db)
    try:
        return service.create_payment(payment)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.post("/{payment_id}/process", response_model=PaymentResponse)
async def process_payment(payment_id: str, db: Session = Depends(get_db)):
    """Process a payment."""
    service = PaymentService(db)
    try:
        return service.process_payment(payment_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{payment_id}/refund", response_model=PaymentResponse)
async def refund_payment(payment_id: str, db: Session = Depends(get_db)):
    """Refund a payment."""
    service = PaymentService(db)
    try:
        return service.refund_payment(payment_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{payment_id}/cancel", response_model=PaymentResponse)
async def cancel_payment(payment_id: str, db: Session = Depends(get_db)):
    """Cancel a payment."""
    service = PaymentService(db)
    try:
        return service.cancel_payment(payment_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
