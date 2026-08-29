"""
Inventory Service business logic.
"""

from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.inventory import Inventory, InventoryReservation
from app.schemas.inventory import (
    InventoryCreate,
    InventoryUpdate,
    InventoryResponse,
    InventoryReserveRequest,
    InventoryReleaseRequest,
)
from app.repositories.inventory_repository import (
    InventoryRepository,
    InventoryReservationRepository,
)


class InventoryService:
    """Business logic for inventory operations."""

    def __init__(self, session: Session):
        self.repository = InventoryRepository(session)
        self.reservation_repository = InventoryReservationRepository(session)
        self.session = session

    def create_inventory(self, product_id: str, inventory_data: InventoryCreate) -> InventoryResponse:
        """Create inventory for a product."""
        # Check if inventory already exists
        existing = self.repository.get_by_product_id(product_id)
        if existing:
            raise ValueError(f"Inventory for product {product_id} already exists")

        inventory = self.repository.create(product_id, inventory_data)
        return InventoryResponse.from_orm(inventory)

    def get_inventory(self, inventory_id: str) -> Optional[InventoryResponse]:
        """Get inventory by ID."""
        inventory = self.repository.get_by_id(inventory_id)
        if not inventory:
            return None
        return InventoryResponse.from_orm(inventory)

    def get_inventory_by_product(self, product_id: str) -> Optional[InventoryResponse]:
        """Get inventory by product ID."""
        inventory = self.repository.get_by_product_id(product_id)
        if not inventory:
            return None
        return InventoryResponse.from_orm(inventory)

    def get_all_inventory(
        self, page: int = 1, page_size: int = 20
    ) -> dict:
        """Get all inventory with pagination."""
        inventory, total = self.repository.get_all(page, page_size)
        total_pages = (total + page_size - 1) // page_size

        return {
            "items": [InventoryResponse.from_orm(i) for i in inventory],
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages,
        }

    def update_inventory(
        self, inventory_id: str, inventory_data: InventoryUpdate
    ) -> Optional[InventoryResponse]:
        """Update inventory."""
        inventory = self.repository.update(inventory_id, inventory_data)
        if not inventory:
            return None
        return InventoryResponse.from_orm(inventory)

    def reserve_inventory(
        self, order_id: str, product_id: str, quantity: int
    ) -> InventoryResponse:
        """Reserve inventory for an order."""
        # Check if sufficient inventory is available
        if not self.repository.check_availability(product_id, quantity):
            raise ValueError(
                f"Insufficient inventory for product {product_id}. Requested: {quantity}"
            )

        # Get inventory
        inventory = self.repository.get_by_product_id(product_id)
        if not inventory:
            raise ValueError(f"Inventory not found for product {product_id}")

        # Create reservation
        self.reservation_repository.create(order_id, product_id, quantity)

        # Update reserved quantity
        inventory.reserved_quantity += quantity
        self.session.commit()
        self.session.refresh(inventory)

        return InventoryResponse.from_orm(inventory)

    def release_inventory(self, order_id: str, product_id: str) -> InventoryResponse:
        """Release reserved inventory."""
        # Get reservation
        reservation = self.reservation_repository.get_by_order_and_product(order_id, product_id)
        if not reservation:
            raise ValueError(f"Reservation not found for order {order_id}, product {product_id}")

        # Get inventory
        inventory = self.repository.get_by_product_id(product_id)
        if not inventory:
            raise ValueError(f"Inventory not found for product {product_id}")

        # Release inventory
        inventory.reserved_quantity -= reservation.quantity
        self.reservation_repository.update_status(reservation.id, "released")
        self.session.commit()
        self.session.refresh(inventory)

        return InventoryResponse.from_orm(inventory)

    def confirm_reservation(self, order_id: str) -> bool:
        """Confirm all reservations for an order."""
        reservations = self.reservation_repository.get_by_order(order_id)
        for reservation in reservations:
            self.reservation_repository.update_status(reservation.id, "confirmed")
        return True

    def get_available_quantity(self, product_id: str) -> int:
        """Get available quantity for a product."""
        return self.repository.get_available_quantity(product_id)

    def check_stock(self, product_id: str, quantity: int) -> bool:
        """Check if product has sufficient stock."""
        return self.repository.check_availability(product_id, quantity)
