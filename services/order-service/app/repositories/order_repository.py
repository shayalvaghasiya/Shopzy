"""
Order Service repository - Data access layer.
"""

from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import Optional, List, Tuple
from app.models.order import Order, OrderItem, IdempotencyRecord
from app.schemas.order import OrderCreate
import uuid
from datetime import datetime, timedelta


class OrderRepository:
    """Repository for order data access."""

    def __init__(self, session: Session):
        self.session = session

    def create(self, order: OrderCreate) -> Order:
        """Create a new order."""
        db_order = Order(
            id=self._generate_id(),
            customer_id=order.customer_id,
            status="PENDING",
            subtotal=0,
            tax=0,
            shipping_cost=0,
            total_amount=0,
            currency="USD",
        )
        self.session.add(db_order)

        # Add items
        for item in order.items:
            order_item = OrderItem(
                id=self._generate_id(),
                order_id=db_order.id,
                product_id=item.product_id,
                product_name=item.product_name,
                quantity=item.quantity,
                unit_price=item.unit_price,
                total_price=item.quantity * item.unit_price,
            )
            self.session.add(order_item)

        # Calculate totals
        subtotal = sum(item.quantity * item.unit_price for item in order.items)
        db_order.subtotal = subtotal
        db_order.tax = subtotal * 0.10
        db_order.shipping_cost = 10.0 if subtotal > 0 else 0
        db_order.total_amount = subtotal + db_order.tax + db_order.shipping_cost

        self.session.commit()
        self.session.refresh(db_order)
        return db_order

    def get_by_id(self, order_id: str) -> Optional[Order]:
        """Get order by ID."""
        query = select(Order).where(Order.id == order_id)
        return self.session.execute(query).scalar_one_or_none()

    def get_all(self, page: int = 1, page_size: int = 20) -> Tuple[List[Order], int]:
        """Get all orders with pagination."""
        query = select(Order)
        total_count = self.session.execute(select(Order)).scalars().all()

        offset = (page - 1) * page_size
        orders = self.session.execute(
            query.offset(offset).limit(page_size)
        ).scalars().all()

        return orders, len(total_count)

    def get_by_customer(
        self, customer_id: str, page: int = 1, page_size: int = 20
    ) -> Tuple[List[Order], int]:
        """Get orders for a customer."""
        query = select(Order).where(Order.customer_id == customer_id)
        total_count = self.session.execute(query).scalars().all()

        offset = (page - 1) * page_size
        orders = self.session.execute(
            query.offset(offset).limit(page_size)
        ).scalars().all()

        return orders, len(total_count)

    def get_items(self, order_id: str) -> List[OrderItem]:
        """Get all items for an order."""
        query = select(OrderItem).where(OrderItem.order_id == order_id)
        return self.session.execute(query).scalars().all()

    def add_item(
        self,
        order_id: str,
        product_id: str,
        product_name: str,
        quantity: int,
        unit_price: float,
    ) -> OrderItem:
        """Add item to order."""
        item = OrderItem(
            id=self._generate_id(),
            order_id=order_id,
            product_id=product_id,
            product_name=product_name,
            quantity=quantity,
            unit_price=unit_price,
            total_price=quantity * unit_price,
        )
        self.session.add(item)
        self.session.commit()
        self.session.refresh(item)
        return item

    def record_idempotency(
        self,
        idempotency_key: str,
        service: str,
        endpoint: str,
        response_id: str,
    ) -> IdempotencyRecord:
        """Record idempotent request."""
        record = IdempotencyRecord(
            id=self._generate_id(),
            idempotency_key=idempotency_key,
            service=service,
            endpoint=endpoint,
            request_hash="",
            response_data=response_id,
            status_code=201,
            expires_at=datetime.utcnow() + timedelta(hours=24),
        )
        self.session.add(record)
        self.session.commit()
        return record

    def get_by_idempotency_key(self, key: str) -> Optional[Order]:
        """Get order by idempotency key."""
        query = select(IdempotencyRecord).where(IdempotencyRecord.idempotency_key == key)
        record = self.session.execute(query).scalar_one_or_none()
        if not record:
            return None

        # Return the order
        return self.get_by_id(record.response_data)

    @staticmethod
    def _generate_id() -> str:
        """Generate a unique ID."""
        return str(uuid.uuid4())
