"""
Inventory Service repository - Data access layer.
"""

from sqlalchemy.orm import Session
from sqlalchemy import select, and_
from typing import Optional, List, Tuple
from app.models.inventory import Inventory, InventoryReservation
from app.schemas.inventory import InventoryCreate, InventoryUpdate


class InventoryRepository:
    """Repository for inventory data access."""

    def __init__(self, session: Session):
        self.session = session

    def create(self, product_id: str, inventory: InventoryCreate) -> Inventory:
        """Create inventory for a product."""
        db_inventory = Inventory(
            id=self._generate_id(),
            product_id=product_id,
            available_quantity=inventory.available_quantity,
            reserved_quantity=0,
        )
        self.session.add(db_inventory)
        self.session.commit()
        self.session.refresh(db_inventory)
        return db_inventory

    def get_by_id(self, inventory_id: str) -> Optional[Inventory]:
        """Get inventory by ID."""
        query = select(Inventory).where(Inventory.id == inventory_id)
        return self.session.execute(query).scalar_one_or_none()

    def get_by_product_id(self, product_id: str) -> Optional[Inventory]:
        """Get inventory by product ID."""
        query = select(Inventory).where(Inventory.product_id == product_id)
        return self.session.execute(query).scalar_one_or_none()

    def get_all(self, page: int = 1, page_size: int = 20) -> Tuple[List[Inventory], int]:
        """Get all inventory with pagination."""
        query = select(Inventory)
        total_count = self.session.execute(select(Inventory)).scalars().all()

        offset = (page - 1) * page_size
        inventory = self.session.execute(
            query.offset(offset).limit(page_size)
        ).scalars().all()

        return inventory, len(total_count)

    def update(self, inventory_id: str, update: InventoryUpdate) -> Optional[Inventory]:
        """Update inventory."""
        inventory = self.get_by_id(inventory_id)
        if not inventory:
            return None

        if update.available_quantity is not None:
            inventory.available_quantity = update.available_quantity

        self.session.commit()
        self.session.refresh(inventory)
        return inventory

    def check_availability(self, product_id: str, quantity: int) -> bool:
        """Check if product has sufficient available quantity."""
        inventory = self.get_by_product_id(product_id)
        if not inventory:
            return False
        return inventory.available_quantity >= quantity

    def get_available_quantity(self, product_id: str) -> int:
        """Get available quantity for a product."""
        inventory = self.get_by_product_id(product_id)
        if not inventory:
            return 0
        return inventory.available_quantity - inventory.reserved_quantity

    @staticmethod
    def _generate_id() -> str:
        """Generate a unique ID."""
        import uuid
        return str(uuid.uuid4())


class InventoryReservationRepository:
    """Repository for inventory reservation data access."""

    def __init__(self, session: Session):
        self.session = session

    def create(
        self, order_id: str, product_id: str, quantity: int
    ) -> InventoryReservation:
        """Create a reservation."""
        db_reservation = InventoryReservation(
            id=self._generate_id(),
            order_id=order_id,
            product_id=product_id,
            quantity=quantity,
            status="reserved",
        )
        self.session.add(db_reservation)
        self.session.commit()
        self.session.refresh(db_reservation)
        return db_reservation

    def get_by_id(self, reservation_id: str) -> Optional[InventoryReservation]:
        """Get reservation by ID."""
        query = select(InventoryReservation).where(InventoryReservation.id == reservation_id)
        return self.session.execute(query).scalar_one_or_none()

    def get_by_order(self, order_id: str) -> List[InventoryReservation]:
        """Get all reservations for an order."""
        query = select(InventoryReservation).where(InventoryReservation.order_id == order_id)
        return self.session.execute(query).scalars().all()

    def get_by_order_and_product(
        self, order_id: str, product_id: str
    ) -> Optional[InventoryReservation]:
        """Get reservation for specific order and product."""
        query = select(InventoryReservation).where(
            and_(
                InventoryReservation.order_id == order_id,
                InventoryReservation.product_id == product_id,
            )
        )
        return self.session.execute(query).scalar_one_or_none()

    def update_status(self, reservation_id: str, status: str) -> Optional[InventoryReservation]:
        """Update reservation status."""
        reservation = self.get_by_id(reservation_id)
        if not reservation:
            return None

        reservation.status = status
        if status == "released":
            from datetime import datetime
            reservation.released_at = datetime.utcnow()

        self.session.commit()
        self.session.refresh(reservation)
        return reservation

    def delete(self, reservation_id: str) -> bool:
        """Delete a reservation."""
        reservation = self.get_by_id(reservation_id)
        if not reservation:
            return False

        self.session.delete(reservation)
        self.session.commit()
        return True

    @staticmethod
    def _generate_id() -> str:
        """Generate a unique ID."""
        import uuid
        return str(uuid.uuid4())
