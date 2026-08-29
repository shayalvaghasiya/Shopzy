"""
Customer Service repository - Data access layer.
"""

from sqlalchemy.orm import Session
from sqlalchemy import select, and_
from typing import Optional, List, Tuple
from app.models.customer import Customer, Address
from app.schemas.customer import CustomerCreate, CustomerUpdate, AddressCreate, AddressUpdate


class CustomerRepository:
    """Repository for customer data access."""

    def __init__(self, session: Session):
        self.session = session

    def create(self, customer: CustomerCreate) -> Customer:
        """Create a new customer."""
        db_customer = Customer(
            id=self._generate_id(),
            first_name=customer.first_name,
            last_name=customer.last_name,
            email=customer.email,
            phone=customer.phone,
        )
        self.session.add(db_customer)
        self.session.commit()
        self.session.refresh(db_customer)
        return db_customer

    def get_by_id(self, customer_id: str) -> Optional[Customer]:
        """Get customer by ID."""
        query = select(Customer).where(Customer.id == customer_id)
        return self.session.execute(query).scalar_one_or_none()

    def get_by_email(self, email: str) -> Optional[Customer]:
        """Get customer by email."""
        query = select(Customer).where(Customer.email == email)
        return self.session.execute(query).scalar_one_or_none()

    def get_all(self, page: int = 1, page_size: int = 20) -> Tuple[List[Customer], int]:
        """Get all customers with pagination."""
        query = select(Customer)
        total_count = self.session.execute(select(Customer)).scalars().all()

        offset = (page - 1) * page_size
        customers = self.session.execute(
            query.offset(offset).limit(page_size)
        ).scalars().all()

        return customers, len(total_count)

    def update(self, customer_id: str, update: CustomerUpdate) -> Optional[Customer]:
        """Update a customer."""
        customer = self.get_by_id(customer_id)
        if not customer:
            return None

        update_data = update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            if value is not None:
                setattr(customer, field, value)

        self.session.commit()
        self.session.refresh(customer)
        return customer

    def delete(self, customer_id: str) -> bool:
        """Delete a customer."""
        customer = self.get_by_id(customer_id)
        if not customer:
            return False

        self.session.delete(customer)
        self.session.commit()
        return True


class AddressRepository:
    """Repository for address data access."""

    def __init__(self, session: Session):
        self.session = session

    def create(self, customer_id: str, address: AddressCreate) -> Address:
        """Create a new address."""
        db_address = Address(
            id=self._generate_id(),
            customer_id=customer_id,
            type=address.type,
            street_address=address.street_address,
            city=address.city,
            state_province=address.state_province,
            postal_code=address.postal_code,
            country=address.country,
            is_default=address.is_default,
        )
        self.session.add(db_address)
        self.session.commit()
        self.session.refresh(db_address)
        return db_address

    def get_by_id(self, address_id: str) -> Optional[Address]:
        """Get address by ID."""
        query = select(Address).where(Address.id == address_id)
        return self.session.execute(query).scalar_one_or_none()

    def get_by_customer(self, customer_id: str) -> List[Address]:
        """Get all addresses for a customer."""
        query = select(Address).where(Address.customer_id == customer_id)
        return self.session.execute(query).scalars().all()

    def update(self, address_id: str, update: AddressUpdate) -> Optional[Address]:
        """Update an address."""
        address = self.get_by_id(address_id)
        if not address:
            return None

        update_data = update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            if value is not None:
                setattr(address, field, value)

        self.session.commit()
        self.session.refresh(address)
        return address

    def delete(self, address_id: str) -> bool:
        """Delete an address."""
        address = self.get_by_id(address_id)
        if not address:
            return False

        self.session.delete(address)
        self.session.commit()
        return True

    @staticmethod
    def _generate_id() -> str:
        """Generate a unique ID for address."""
        import uuid
        return str(uuid.uuid4())
