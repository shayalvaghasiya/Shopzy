"""
Notification Service business logic.
"""

import logging
from typing import Optional, List
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.notification import Notification
from app.schemas.notification import NotificationCreate, NotificationResponse
from app.repositories.notification_repository import NotificationRepository

logger = logging.getLogger(__name__)


class NotificationService:
    """Business logic for notification operations."""

    def __init__(self, session: Session):
        self.repository = NotificationRepository(session)

    def create_notification(self, notification_data: NotificationCreate) -> NotificationResponse:
        """Create a new notification."""
        # Check if notification already exists for event
        existing = self.repository.get_by_event_id(notification_data.event_id)
        if existing:
            logger.info(f"Notification already exists for event {notification_data.event_id}")
            return NotificationResponse.from_orm(existing)

        notification = self.repository.create(notification_data)

        # Simulate sending notification
        self._send_notification(notification)

        return NotificationResponse.from_orm(notification)

    def get_notification(self, notification_id: str) -> Optional[NotificationResponse]:
        """Get notification by ID."""
        notification = self.repository.get_by_id(notification_id)
        if not notification:
            return None
        return NotificationResponse.from_orm(notification)

    def get_all_notifications(self, page: int = 1, page_size: int = 20) -> dict:
        """Get all notifications with pagination."""
        notifications, total = self.repository.get_all(page, page_size)
        total_pages = (total + page_size - 1) // page_size

        return {
            "items": [NotificationResponse.from_orm(n) for n in notifications],
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages,
        }

    def get_customer_notifications(
        self, customer_id: str, page: int = 1, page_size: int = 20
    ) -> dict:
        """Get notifications for a customer."""
        notifications, total = self.repository.get_by_customer(customer_id, page, page_size)
        total_pages = (total + page_size - 1) // page_size

        return {
            "items": [NotificationResponse.from_orm(n) for n in notifications],
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages,
        }

    def mark_as_read(self, notification_id: str) -> Optional[NotificationResponse]:
        """Mark notification as read."""
        notification = self.repository.get_by_id(notification_id)
        if not notification:
            return None

        notification.read = True
        notification.read_at = datetime.utcnow()
        self.repository.session.commit()
        self.repository.session.refresh(notification)

        logger.info(f"Notification {notification_id} marked as read")
        return NotificationResponse.from_orm(notification)

    def update_status(self, notification_id: str, status: str) -> Optional[NotificationResponse]:
        """Update notification status."""
        valid_statuses = ["pending", "sent", "failed", "read"]
        if status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of: {', '.join(valid_statuses)}")

        notification = self.repository.get_by_id(notification_id)
        if not notification:
            return None

        notification.status = status
        if status == "sent":
            notification.sent_at = datetime.utcnow()

        self.repository.session.commit()
        self.repository.session.refresh(notification)

        logger.info(f"Notification {notification_id} status updated to {status}")
        return NotificationResponse.from_orm(notification)

    def delete_notification(self, notification_id: str) -> bool:
        """Delete a notification."""
        return self.repository.delete(notification_id)

    def _send_notification(self, notification: Notification) -> None:
        """Send notification (simulated or real)."""
        logger.info(
            f"Sending {notification.channel} notification to {notification.recipient}: "
            f"{notification.message}"
        )

        # Update status to sent
        notification.status = "sent"
        notification.sent_at = datetime.utcnow()
        self.repository.session.commit()
