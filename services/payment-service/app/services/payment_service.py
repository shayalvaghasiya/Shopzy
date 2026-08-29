"""
Payment Service business logic.
"""

from typing import Optional
import random
import time
import logging
from sqlalchemy.orm import Session
from app.models.payment import Payment, PaymentStatus
from app.schemas.payment import PaymentCreate, PaymentUpdateStatus, PaymentResponse
from app.repositories.payment_repository import PaymentRepository
from app.core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class PaymentService:
    """Business logic for payment operations."""

    def __init__(self, session: Session):
        self.repository = PaymentRepository(session)

    def create_payment(self, payment_data: PaymentCreate) -> PaymentResponse:
        """Create a new payment."""
        # Check if payment already exists for order
        existing = self.repository.get_by_order_id(payment_data.order_id)
        if existing:
            raise ValueError(f"Payment already exists for order {payment_data.order_id}")

        payment = self.repository.create(payment_data)
        return PaymentResponse.from_orm(payment)

    def get_payment(self, payment_id: str) -> Optional[PaymentResponse]:
        """Get payment by ID."""
        payment = self.repository.get_by_id(payment_id)
        if not payment:
            return None
        return PaymentResponse.from_orm(payment)

    def get_payment_by_order(self, order_id: str) -> Optional[PaymentResponse]:
        """Get payment by order ID."""
        payment = self.repository.get_by_order_id(order_id)
        if not payment:
            return None
        return PaymentResponse.from_orm(payment)

    def get_all_payments(self, page: int = 1, page_size: int = 20) -> dict:
        """Get all payments with pagination."""
        payments, total = self.repository.get_all(page, page_size)
        total_pages = (total + page_size - 1) // page_size

        return {
            "items": [PaymentResponse.from_orm(p) for p in payments],
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages,
        }

    def process_payment(self, payment_id: str) -> PaymentResponse:
        """Process a payment (simulated)."""
        payment = self.repository.get_by_id(payment_id)
        if not payment:
            raise ValueError(f"Payment {payment_id} not found")

        if payment.status != PaymentStatus.PENDING:
            raise ValueError(f"Payment {payment_id} is already processed")

        # Simulate payment processing delay
        delay_ms = int(settings.PAYMENT_PROCESSING_DELAY_MS)
        time.sleep(delay_ms / 1000)

        # Simulate payment success/failure
        success_rate = float(settings.PAYMENT_SUCCESS_RATE)
        is_success = random.random() < success_rate

        if is_success:
            payment.status = PaymentStatus.SUCCESS
            payment.transaction_reference = self._generate_transaction_ref()
            logger.info(f"Payment {payment_id} succeeded: {payment.transaction_reference}")
        else:
            payment.status = PaymentStatus.FAILED
            payment.failure_reason = "Simulated payment failure"
            logger.info(f"Payment {payment_id} failed: {payment.failure_reason}")

        from datetime import datetime
        payment.processed_at = datetime.utcnow()
        self.repository.session.commit()
        self.repository.session.refresh(payment)

        return PaymentResponse.from_orm(payment)

    def refund_payment(self, payment_id: str) -> PaymentResponse:
        """Refund a payment."""
        payment = self.repository.get_by_id(payment_id)
        if not payment:
            raise ValueError(f"Payment {payment_id} not found")

        if payment.status != PaymentStatus.SUCCESS:
            raise ValueError(f"Can only refund successful payments. Current status: {payment.status}")

        payment.status = PaymentStatus.REFUNDED
        self.repository.session.commit()
        self.repository.session.refresh(payment)

        logger.info(f"Payment {payment_id} refunded")
        return PaymentResponse.from_orm(payment)

    def cancel_payment(self, payment_id: str) -> PaymentResponse:
        """Cancel a payment."""
        payment = self.repository.get_by_id(payment_id)
        if not payment:
            raise ValueError(f"Payment {payment_id} not found")

        if payment.status in [PaymentStatus.SUCCESS, PaymentStatus.REFUNDED]:
            raise ValueError(f"Cannot cancel {payment.status} payment")

        payment.status = PaymentStatus.CANCELLED
        self.repository.session.commit()
        self.repository.session.refresh(payment)

        logger.info(f"Payment {payment_id} cancelled")
        return PaymentResponse.from_orm(payment)

    @staticmethod
    def _generate_transaction_ref() -> str:
        """Generate a transaction reference."""
        import uuid
        return f"TXN-{str(uuid.uuid4())[:8].upper()}"
