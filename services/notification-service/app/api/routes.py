"""
Notification Service API routes.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.services.notification_service import NotificationService
from app.schemas.notification import NotificationCreate, NotificationResponse
from app.core.dependencies import get_db
import logging

router = APIRouter(prefix="/notifications", tags=["notifications"])
logger = logging.getLogger(__name__)


@router.get("", response_model=dict)
async def list_notifications(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """List all notifications with pagination."""
    service = NotificationService(db)
    result = service.get_all_notifications(page, page_size)
    return result


@router.get("/customer/{customer_id}", response_model=dict)
async def get_customer_notifications(
    customer_id: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """Get notifications for a customer."""
    service = NotificationService(db)
    result = service.get_customer_notifications(customer_id, page, page_size)
    return result


@router.get("/{notification_id}", response_model=NotificationResponse)
async def get_notification(notification_id: str, db: Session = Depends(get_db)):
    """Get notification by ID."""
    service = NotificationService(db)
    notification = service.get_notification(notification_id)
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    return notification


@router.post("", response_model=NotificationResponse, status_code=201)
async def create_notification(
    notification: NotificationCreate, db: Session = Depends(get_db)
):
    """Create a new notification."""
    service = NotificationService(db)
    try:
        return service.create_notification(notification)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{notification_id}/read", response_model=NotificationResponse)
async def mark_as_read(notification_id: str, db: Session = Depends(get_db)):
    """Mark notification as read."""
    service = NotificationService(db)
    notification = service.mark_as_read(notification_id)
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    return notification


@router.patch("/{notification_id}/status/{status}", response_model=NotificationResponse)
async def update_status(
    notification_id: str, status: str, db: Session = Depends(get_db)
):
    """Update notification status."""
    service = NotificationService(db)
    try:
        notification = service.update_status(notification_id, status)
        if not notification:
            raise HTTPException(status_code=404, detail="Notification not found")
        return notification
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{notification_id}", status_code=204)
async def delete_notification(notification_id: str, db: Session = Depends(get_db)):
    """Delete a notification."""
    service = NotificationService(db)
    success = service.delete_notification(notification_id)
    if not success:
        raise HTTPException(status_code=404, detail="Notification not found")
    return None
