"""
Order Service business logic with orchestration.
"""

import logging
from typing import Optional, List, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.order import Order, OrderItem, OrderStatus
from app.schemas.order import (
    OrderCreate,
    OrderUpdate,
    OrderResponse,
    OrderItemResponse,
)
from app.repositories.order_repository import OrderRepository

logger = logging.getLogger(__name__)


class OrderService:
    """Business logic for order operations."""

    def __init__(self, session: Session):
        self.repository = OrderRepository(session)
        self.session = session

    def create_order(self, order_data: OrderCreate) -> OrderResponse:
        """Create a new order."""
        # Check if idempotency key already processed
        if order_data.idempotency_key:
            existing_order = self.repository.get_by_idempotency_key(order_data.idempotency_key)
            if existing_order:
                logger.info(f"Order already created for idempotency key {order_data.idempotency_key}")
                return OrderResponse.from_orm(existing_order)

        # Create order
        order = self.repository.create(order_data)

        # Record idempotency
        if order_data.idempotency_key:
            self.repository.record_idempotency(
                order_data.idempotency_key,
                "order-service",
                "/orders",
                order.id
            )

        logger.info(f"Order {order.id} created successfully")
        return OrderResponse.from_orm(order)

    def get_order(self, order_id: str) -> Optional[OrderResponse]:
        """Get order by ID with items."""
        order = self.repository.get_by_id(order_id)
        if not order:
            return None
        return OrderResponse.from_orm(order)

    def get_all_orders(
        self, page: int = 1, page_size: int = 20
    ) -> dict:
        """Get all orders with pagination."""
        orders, total = self.repository.get_all(page, page_size)
        total_pages = (total + page_size - 1) // page_size

        return {
            "items": [OrderResponse.from_orm(o) for o in orders],
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages,
        }

    def get_customer_orders(
        self, customer_id: str, page: int = 1, page_size: int = 20
    ) -> dict:
        """Get orders for a customer."""
        orders, total = self.repository.get_by_customer(customer_id, page, page_size)
        total_pages = (total + page_size - 1) // page_size

        return {
            "items": [OrderResponse.from_orm(o) for o in orders],
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages,
        }

    def update_order_status(
        self, order_id: str, new_status: str
    ) -> Optional[OrderResponse]:
        """Update order status with state machine validation."""
        order = self.repository.get_by_id(order_id)
        if not order:
            return None

        # Validate state transition
        current_status = OrderStatus(order.status)
        try:
            target_status = OrderStatus(new_status)
        except ValueError:
            raise ValueError(f"Invalid status: {new_status}")

        # Define valid transitions
        valid_transitions = {
            OrderStatus.PENDING: [OrderStatus.PAYMENT_PENDING, OrderStatus.CANCELLED],
            OrderStatus.PAYMENT_PENDING: [OrderStatus.CONFIRMED, OrderStatus.FAILED, OrderStatus.CANCELLED],
            OrderStatus.CONFIRMED: [OrderStatus.PROCESSING, OrderStatus.CANCELLED],
            OrderStatus.PROCESSING: [OrderStatus.SHIPPED, OrderStatus.CANCELLED],
            OrderStatus.SHIPPED: [OrderStatus.DELIVERED],
            OrderStatus.DELIVERED: [],
            OrderStatus.CANCELLED: [],
            OrderStatus.FAILED: [OrderStatus.PENDING],  # Allow retry
        }

        if target_status not in valid_transitions.get(current_status, []):
            raise ValueError(
                f"Invalid transition from {current_status} to {target_status}"
            )

        order.status = target_status.value
        order.updated_at = datetime.utcnow()
        self.session.commit()
        self.session.refresh(order)

        logger.info(f"Order {order_id} status updated to {new_status}")
        return OrderResponse.from_orm(order)

    def cancel_order(self, order_id: str) -> Optional[OrderResponse]:
        """Cancel an order."""
        order = self.repository.get_by_id(order_id)
        if not order:
            return None

        # Can cancel if in certain states
        cancellable_statuses = [
            OrderStatus.PENDING,
            OrderStatus.PAYMENT_PENDING,
            OrderStatus.CONFIRMED,
            OrderStatus.PROCESSING,
        ]

        if order.status not in [s.value for s in cancellable_statuses]:
            raise ValueError(f"Cannot cancel order with status {order.status}")

        order.status = OrderStatus.CANCELLED.value
        order.updated_at = datetime.utcnow()
        self.session.commit()
        self.session.refresh(order)

        logger.info(f"Order {order_id} cancelled")
        return OrderResponse.from_orm(order)

    def add_items(self, order_id: str, items: List[Dict[str, Any]]) -> OrderResponse:
        """Add items to an order."""
        order = self.repository.get_by_id(order_id)
        if not order:
            raise ValueError(f"Order {order_id} not found")

        # Only allow adding items to PENDING orders
        if order.status != OrderStatus.PENDING.value:
            raise ValueError(f"Cannot add items to {order.status} order")

        for item in items:
            self.repository.add_item(
                order_id,
                item["product_id"],
                item.get("product_name", ""),
                item["quantity"],
                item["unit_price"],
            )

        # Recalculate totals
        self._recalculate_totals(order)

        logger.info(f"Added {len(items)} items to order {order_id}")
        return OrderResponse.from_orm(order)

    def _recalculate_totals(self, order: Order) -> None:
        """Recalculate order totals."""
        items = self.repository.get_items(order.id)
        subtotal = sum(item.total_price for item in items)

        # Calculate tax (example: 10%)
        tax = subtotal * 0.10

        # Calculate shipping (example: flat rate)
        shipping_cost = 10.0 if subtotal > 0 else 0

        order.subtotal = subtotal
        order.tax = tax
        order.shipping_cost = shipping_cost
        order.total_amount = subtotal + tax + shipping_cost

        self.session.commit()
