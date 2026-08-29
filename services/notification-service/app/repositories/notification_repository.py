"""
Notification Service repository - Data access layer.
"""

from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import Optional, List, Tuple
from app.models.notification import Notification
from app.schemas.notification import NotificationCreate


class NotificationRepository:
    """Repository for notification data access."""

    def __init__(self, session: Session):
        self.session = session

    def create(self, notification: NotificationCreate) -> Notification:
        """Create a new notification."""
        db_notification = Notification(
            id=self._generate_id(),
            customer_id=notification.customer_id,
            order_id=notification.order_id,
            event_type=notification.event_type,
            event_id=notification.event_id,
            notification_type=notification.notification_type,
            channel=notification.channel,
            subject=notification.subject,
            message=notification.message,
            recipient=notification.recipient,
            status="pending",
            read=False,
        )
        self.session.add(db_notification)
        self.session.commit()
        self.session.refresh(db_notification)
        return db_notification

    def get_by_id(self, notification_id: str) -> Optional[Notification]:
        """Get notification by ID."""
        query = select(Notification).where(Notification.id == notification_id)
        return self.session.execute(query).scalar_one_or_none()

    def get_by_event_id(self, event_id: str) -> Optional[Notification]:
        """Get notification by event ID."""
        query = select(Notification).where(Notification.event_id == event_id)
        return self.session.execute(query).scalar_one_or_none()

    def get_all(self, page: int = 1, page_size: int = 20) -> Tuple[List[Notification], int]:
        """Get all notifications with pagination."""
        query = select(Notification)
        total_count = self.session.execute(select(Notification)).scalars().all()

        offset = (page - 1) * page_size
        notifications = self.session.execute(
            query.offset(offset).limit(page_size)
        ).scalars().all()

        return notifications, len(total_count)

    def get_by_customer(
        self, customer_id: str, page: int = 1, page_size: int = 20
    ) -> Tuple[List[Notification], int]:
        """Get notifications for a customer."""
        query = select(Notification).where(Notification.customer_id == customer_id)
        total_count = self.session.execute(query).scalars().all()

        offset = (page - 1) * page_size
        notifications = self.session.execute(
            query.offset(offset).limit(page_size)
        ).scalars().all()

        return notifications, len(total_count)

    def delete(self, notification_id: str) -> bool:
        """Delete a notification."""
        notification = self.get_by_id(notification_id)
        if not notification:
            return False

        self.session.delete(notification)
        self.session.commit()
        return True

    @staticmethod
    def _generate_id() -> str:
        """Generate a unique ID."""
        import uuid
        return str(uuid.uuid4())
