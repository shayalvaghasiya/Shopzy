"""
Product Service - Unit tests for service layer
"""

import pytest
from uuid import uuid4
from app.services.product_service import ProductService
from app.schemas.product import ProductCreate, ProductUpdate
from sqlalchemy.orm import Session


@pytest.fixture
def sample_product_data():
    """Sample product data for testing"""
    return {
        "name": "Test Product",
        "description": "Test description",
        "sku": f"TEST-{uuid4().hex[:8]}",
        "price": 99.99,
        "category": "Electronics",
        "brand": "TestBrand",
        "stock_count": 100
    }


class TestProductService:
    """Test ProductService business logic"""

    def test_create_product_success(self, db_session: Session, sample_product_data):
        """Test successful product creation"""
        service = ProductService(db_session)
        product_create = ProductCreate(**sample_product_data)

        result = service.create_product(product_create)

        assert result.id is not None
        assert result.name == sample_product_data["name"]
        assert result.sku == sample_product_data["sku"]

    def test_create_product_duplicate_sku_raises_error(self, db_session: Session, sample_product_data):
        """Test that duplicate SKU raises ValueError"""
        service = ProductService(db_session)
        product_create = ProductCreate(**sample_product_data)

        service.create_product(product_create)

        with pytest.raises(ValueError):
            service.create_product(product_create)

    def test_get_product(self, db_session: Session, sample_product_data):
        """Test retrieving a product"""
        service = ProductService(db_session)
        product_create = ProductCreate(**sample_product_data)
        created = service.create_product(product_create)

        retrieved = service.get_product(created.id)

        assert retrieved is not None
        assert retrieved.id == created.id

    def test_get_nonexistent_product_returns_none(self, db_session: Session):
        """Test retrieving nonexistent product returns None"""
        service = ProductService(db_session)

        result = service.get_product("nonexistent-id")

        assert result is None

    def test_update_product(self, db_session: Session, sample_product_data):
        """Test updating a product"""
        service = ProductService(db_session)
        product_create = ProductCreate(**sample_product_data)
        created = service.create_product(product_create)

        update = ProductUpdate(name="Updated Name", price=199.99)
        updated = service.update_product(created.id, update)

        assert updated is not None
        assert updated.name == "Updated Name"
        assert updated.price == 199.99

    def test_delete_product(self, db_session: Session, sample_product_data):
        """Test deleting a product"""
        service = ProductService(db_session)
        product_create = ProductCreate(**sample_product_data)
        created = service.create_product(product_create)

        success = service.delete_product(created.id)

        assert success is True

    def test_get_all_products_with_pagination(self, db_session: Session, sample_product_data):
        """Test getting all products with pagination"""
        service = ProductService(db_session)

        # Create 3 products
        for i in range(3):
            data = sample_product_data.copy()
            data["sku"] = f"TEST-{i}-{uuid4().hex[:4]}"
            product_create = ProductCreate(**data)
            service.create_product(product_create)

        result = service.get_all_products(page=1, page_size=10)

        assert result["page"] == 1
        assert result["page_size"] == 10
        assert len(result["items"]) > 0

    def test_search_products(self, db_session: Session, sample_product_data):
        """Test searching products"""
        service = ProductService(db_session)
        product_create = ProductCreate(**sample_product_data)
        service.create_product(product_create)

        result = service.search_products(
            query="Test",
            page=1,
            page_size=20
        )

        assert len(result["items"]) > 0
        assert result["total"] > 0

    def test_get_products_by_ids(self, db_session: Session, sample_product_data):
        """Test getting multiple products by IDs"""
        service = ProductService(db_session)
        product_create = ProductCreate(**sample_product_data)
        created = service.create_product(product_create)

        results = service.get_products_by_ids([created.id])

        assert len(results) > 0
        assert results[0].id == created.id
