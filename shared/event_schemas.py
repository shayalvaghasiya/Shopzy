"""
Shared event schemas for all services.
These define the contract for events published to RabbitMQ.
"""

from enum import Enum
from typing import Any, Dict
from datetime import datetime
from pydantic import BaseModel, Field


class EventType(str, Enum):
    """All event types in the system."""

    # Order events
    ORDER_CREATED = "ORDER_CREATED"
    ORDER_CONFIRMED = "ORDER_CONFIRMED"
    ORDER_PAYMENT_PENDING = "ORDER_PAYMENT_PENDING"
    ORDER_CANCELLED = "ORDER_CANCELLED"
    ORDER_SHIPPED = "ORDER_SHIPPED"
    ORDER_DELIVERED = "ORDER_DELIVERED"

    # Payment events
    PAYMENT_INITIATED = "PAYMENT_INITIATED"
    PAYMENT_SUCCESS = "PAYMENT_SUCCESS"
    PAYMENT_FAILED = "PAYMENT_FAILED"
    PAYMENT_REFUNDED = "PAYMENT_REFUNDED"

    # Inventory events
    INVENTORY_RESERVED = "INVENTORY_RESERVED"
    INVENTORY_RELEASED = "INVENTORY_RELEASED"

    # Notification events (internal)
    SEND_EMAIL = "SEND_EMAIL"
    SEND_IN_APP = "SEND_IN_APP"


class Event(BaseModel):
    """
    Base event model that all events should follow.
    Enables proper event versioning and tracing.
    """

    event_id: str = Field(..., description="Unique event identifier (UUID)")
    event_type: EventType = Field(..., description="Type of event")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="When event occurred")
    source: str = Field(..., description="Service that published the event")
    version: str = Field(default="1.0", description="Event schema version")
    correlation_id: str = Field(..., description="Request correlation ID for tracing")
    data: Dict[str, Any] = Field(..., description="Event payload")

    class Config:
        use_enum_values = True


# Event-specific models with typed data
class OrderCreatedEvent(Event):
    """Published when an order is created."""
    event_type: EventType = EventType.ORDER_CREATED

    class EventData(BaseModel):
        order_id: str
        customer_id: str
        total_amount: float
        currency: str
        items_count: int

    data: Dict[str, Any]


class OrderConfirmedEvent(Event):
    """Published when order is confirmed after payment."""
    event_type: EventType = EventType.ORDER_CONFIRMED

    class EventData(BaseModel):
        order_id: str
        customer_id: str
        transaction_id: str

    data: Dict[str, Any]


class OrderCancelledEvent(Event):
    """Published when order is cancelled."""
    event_type: EventType = EventType.ORDER_CANCELLED

    class EventData(BaseModel):
        order_id: str
        customer_id: str
        reason: str

    data: Dict[str, Any]


class PaymentSuccessEvent(Event):
    """Published when payment is successful."""
    event_type: EventType = PaymentSuccessEvent = PAYMENT_SUCCESS

    class EventData(BaseModel):
        payment_id: str
        order_id: str
        customer_id: str
        amount: float
        transaction_reference: str

    data: Dict[str, Any]


class PaymentFailedEvent(Event):
    """Published when payment fails."""
    event_type: EventType = EventType.PAYMENT_FAILED

    class EventData(BaseModel):
        payment_id: str
        order_id: str
        customer_id: str
        amount: float
        reason: str

    data: Dict[str, Any]


class InventoryReservedEvent(Event):
    """Published when inventory is reserved."""
    event_type: EventType = EventType.INVENTORY_RESERVED

    class EventData(BaseModel):
        order_id: str
        product_id: str
        quantity: int
        correlation_id: str

    data: Dict[str, Any]


class InventoryReleasedEvent(Event):
    """Published when inventory reservation is released."""
    event_type: EventType = EventType.INVENTORY_RELEASED

    class EventData(BaseModel):
        order_id: str
        product_id: str
        quantity: int
        reason: str

    data: Dict[str, Any]
