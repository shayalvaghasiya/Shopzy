"""
Notification Service schemas for request/response validation.
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class NotificationCreate(BaseModel):
    """Schema for creating a notification."""

    customer_id: str = Field(..., min_length=1)
    order_id: Optional[str] = Field(None, min_length=1)
    event_type: str = Field(..., min_length=1)
    event_id: str = Field(..., min_length=1)
    notification_type: str = Field(default="email", pattern="^(email|in_app|sms)$")
    channel: str = Field(default="email", pattern="^(email|push|sms)$")
    subject: Optional[str] = None
    message: str = Field(..., min_length=1)
    recipient: str = Field(..., min_length=1)


class NotificationResponse(BaseModel):
    """Schema for notification responses."""

    id: str
    customer_id: str
    order_id: Optional[str]
    event_type: str
    event_id: str
    notification_type: str
    channel: str
    subject: Optional[str]
    message: str
    recipient: str
    status: str
    read: bool
    created_at: datetime
    sent_at: Optional[datetime]
    read_at: Optional[datetime]

    class Config:
        from_attributes = True
