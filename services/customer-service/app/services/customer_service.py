"""
Customer Service business logic.
"""

from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.customer import Customer, Address
from app.schemas.customer import (
    CustomerCreate,
    CustomerUpdate,
    CustomerResponse,
    CustomerDetailResponse,
    AddressCreate,
    AddressUpdate,
    AddressResponse,
)
from app.repositories.customer_repository import CustomerRepository, AddressRepository


class CustomerService:
    """Business logic for customer operations."""

    def __init__(self, session: Session):
        self.customer_repository = CustomerRepository(session)
        self.address_repository = AddressRepository(session)

    def create_customer(self, customer_data: CustomerCreate) -> CustomerResponse:
        """Create a new customer."""
        # Check if email already exists
        existing = self.customer_repository.get_by_email(customer_data.email)
        if existing:
            raise ValueError(f"Customer with email {customer_data.email} already exists")

        customer = self.customer_repository.create(customer_data)
        return CustomerResponse.from_orm(customer)

    def get_customer(self, customer_id: str) -> Optional[CustomerResponse]:
        """Get customer by ID."""
        customer = self.customer_repository.get_by_id(customer_id)
        if not customer:
            return None
        return CustomerResponse.from_orm(customer)

    def get_customer_detail(self, customer_id: str) -> Optional[CustomerDetailResponse]:
        """Get customer with all addresses."""
        customer = self.customer_repository.get_by_id(customer_id)
        if not customer:
            return None

        addresses = self.address_repository.get_by_customer(customer_id)
        customer_dict = {
            "id": customer.id,
            "first_name": customer.first_name,
            "last_name": customer.last_name,
            "email": customer.email,
            "phone": customer.phone,
            "addresses": [AddressResponse.from_orm(addr) for addr in addresses],
            "created_at": customer.created_at,
            "updated_at": customer.updated_at,
        }
        return CustomerDetailResponse(**customer_dict)

    def get_all_customers(
        self, page: int = 1, page_size: int = 20
    ) -> dict:
        """Get all customers with pagination."""
        customers, total = self.customer_repository.get_all(page, page_size)
        total_pages = (total + page_size - 1) // page_size

        return {
            "items": [CustomerResponse.from_orm(c) for c in customers],
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages,
        }

    def update_customer(
        self, customer_id: str, customer_data: CustomerUpdate
    ) -> Optional[CustomerResponse]:
        """Update a customer."""
        customer = self.customer_repository.update(customer_id, customer_data)
        if not customer:
            return None
        return CustomerResponse.from_orm(customer)

    def delete_customer(self, customer_id: str) -> bool:
        """Delete a customer."""
        return self.customer_repository.delete(customer_id)

    def add_address(
        self, customer_id: str, address_data: AddressCreate
    ) -> AddressResponse:
        """Add an address to a customer."""
        # Verify customer exists
        customer = self.customer_repository.get_by_id(customer_id)
        if not customer:
            raise ValueError(f"Customer {customer_id} not found")

        address = self.address_repository.create(customer_id, address_data)
        return AddressResponse.from_orm(address)

    def update_address(
        self, address_id: str, address_data: AddressUpdate
    ) -> Optional[AddressResponse]:
        """Update an address."""
        address = self.address_repository.update(address_id, address_data)
        if not address:
            return None
        return AddressResponse.from_orm(address)

    def get_customer_addresses(self, customer_id: str) -> List[AddressResponse]:
        """Get all addresses for a customer."""
        # Verify customer exists
        customer = self.customer_repository.get_by_id(customer_id)
        if not customer:
            raise ValueError(f"Customer {customer_id} not found")

        addresses = self.address_repository.get_by_customer(customer_id)
        return [AddressResponse.from_orm(addr) for addr in addresses]

    def delete_address(self, address_id: str) -> bool:
        """Delete an address."""
        return self.address_repository.delete(address_id)
