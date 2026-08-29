"""
Notification Service models.
"""

from datetime import datetime
from sqlalchemy import Column, String, DateTime, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Notification(Base):
    """Notification database model."""

    __tablename__ = "notifications"

    id = Column(String(36), primary_key=True, index=True)
    customer_id = Column(String(36), index=True, nullable=False)
    order_id = Column(String(36), index=True, nullable=True)
    event_type = Column(String(100), index=True, nullable=False)  # ORDER_CREATED, PAYMENT_SUCCESS, etc.
    event_id = Column(String(36), unique=True, index=True, nullable=False)
    notification_type = Column(String(50), nullable=False)  # email, in_app, sms
    channel = Column(String(50), nullable=False)  # email, push, sms
    subject = Column(String(255), nullable=True)
    message = Column(Text, nullable=False)
    recipient = Column(String(255), nullable=False)  # email, phone, user_id
    status = Column(String(50), default="pending", index=True)  # pending, sent, failed, read
    read = Column(Boolean, default=False)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    sent_at = Column(DateTime, nullable=True)
    read_at = Column(DateTime, nullable=True)

    def __repr__(self) -> str:
        return f"<Notification {self.id}: customer={self.customer_id}, event={self.event_type}, status={self.status}>"
