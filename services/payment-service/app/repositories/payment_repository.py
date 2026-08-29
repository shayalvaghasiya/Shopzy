"""
Payment Service repository - Data access layer.
"""

from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import Optional, List, Tuple
from app.models.payment import Payment
from app.schemas.payment import PaymentCreate


class PaymentRepository:
    """Repository for payment data access."""

    def __init__(self, session: Session):
        self.session = session

    def create(self, payment: PaymentCreate) -> Payment:
        """Create a new payment."""
        db_payment = Payment(
            id=self._generate_id(),
            order_id=payment.order_id,
            customer_id=payment.customer_id,
            amount=payment.amount,
            currency=payment.currency,
            status="PENDING",
        )
        self.session.add(db_payment)
        self.session.commit()
        self.session.refresh(db_payment)
        return db_payment

    def get_by_id(self, payment_id: str) -> Optional[Payment]:
        """Get payment by ID."""
        query = select(Payment).where(Payment.id == payment_id)
        return self.session.execute(query).scalar_one_or_none()

    def get_by_order_id(self, order_id: str) -> Optional[Payment]:
        """Get payment by order ID."""
        query = select(Payment).where(Payment.order_id == order_id)
        return self.session.execute(query).scalar_one_or_none()

    def get_all(self, page: int = 1, page_size: int = 20) -> Tuple[List[Payment], int]:
        """Get all payments with pagination."""
        query = select(Payment)
        total_count = self.session.execute(select(Payment)).scalars().all()

        offset = (page - 1) * page_size
        payments = self.session.execute(
            query.offset(offset).limit(page_size)
        ).scalars().all()

        return payments, len(total_count)

    @staticmethod
    def _generate_id() -> str:
        """Generate a unique ID."""
        import uuid
        return str(uuid.uuid4())
