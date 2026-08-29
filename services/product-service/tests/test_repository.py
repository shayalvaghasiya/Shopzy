"""
Product Service - Unit tests for repository layer
"""

import pytest
from uuid import uuid4
from app.models.product import Product
from app.repositories.product_repository import ProductRepository
from app.schemas.product import ProductCreate, ProductUpdate
from sqlalchemy.orm import Session


@pytest.fixture
def sample_product_data():
    """Sample product data for testing"""
    return {
        "name": "Test Laptop",
        "description": "High-performance laptop",
        "sku": f"LAPTOP-{uuid4().hex[:8]}",
        "price": 1299.99,
        "category": "Electronics",
        "brand": "TestBrand",
        "image_url": "https://example.com/laptop.jpg",
        "stock_count": 50
    }


class TestProductRepository:
    """Test ProductRepository CRUD operations"""

    def test_create_product(self, db_session: Session, sample_product_data):
        """Test creating a product"""
        repo = ProductRepository(db_session)
        product_create = ProductCreate(**sample_product_data)

        product = repo.create(product_create)

        assert product.id is not None
        assert product.name == sample_product_data["name"]
        assert product.sku == sample_product_data["sku"]
        assert product.price == sample_product_data["price"]
        assert product.status == "active"

    def test_get_product_by_id(self, db_session: Session, sample_product_data):
        """Test retrieving product by ID"""
        repo = ProductRepository(db_session)
        product_create = ProductCreate(**sample_product_data)
        created_product = repo.create(product_create)

        retrieved = repo.get_by_id(created_product.id)

        assert retrieved is not None
        assert retrieved.id == created_product.id
        assert retrieved.name == sample_product_data["name"]

    def test_get_product_by_sku(self, db_session: Session, sample_product_data):
        """Test retrieving product by SKU"""
        repo = ProductRepository(db_session)
        product_create = ProductCreate(**sample_product_data)
        repo.create(product_create)

        retrieved = repo.get_by_sku(sample_product_data["sku"])

        assert retrieved is not None
        assert retrieved.sku == sample_product_data["sku"]

    def test_update_product(self, db_session: Session, sample_product_data):
        """Test updating a product"""
        repo = ProductRepository(db_session)
        product_create = ProductCreate(**sample_product_data)
        created_product = repo.create(product_create)

        update_data = ProductUpdate(name="Updated Laptop", price=999.99)
        updated = repo.update(created_product.id, update_data)

        assert updated is not None
        assert updated.name == "Updated Laptop"
        assert updated.price == 999.99

    def test_delete_product_soft_delete(self, db_session: Session, sample_product_data):
        """Test soft delete of product"""
        repo = ProductRepository(db_session)
        product_create = ProductCreate(**sample_product_data)
        created_product = repo.create(product_create)

        success = repo.delete(created_product.id)
        deleted = repo.get_by_id(created_product.id)

        assert success is True
        assert deleted.status == "inactive"

    def test_get_all_products_pagination(self, db_session: Session, sample_product_data):
        """Test pagination of products"""
        repo = ProductRepository(db_session)

        # Create 5 products
        for i in range(5):
            data = sample_product_data.copy()
            data["sku"] = f"LAPTOP-{i}-{uuid4().hex[:4]}"
            product_create = ProductCreate(**data)
            repo.create(product_create)

        # Test pagination
        page1, total1 = repo.get_all(page=1, page_size=2)

        assert len(page1) == 2
        assert total1 >= 5

    def test_search_products_by_name(self, db_session: Session, sample_product_data):
        """Test searching products by name"""
        repo = ProductRepository(db_session)
        product_create = ProductCreate(**sample_product_data)
        repo.create(product_create)

        results, total = repo.search(query="Laptop", page=1, page_size=20)

        assert len(results) > 0
        assert total > 0

    def test_search_products_by_category(self, db_session: Session, sample_product_data):
        """Test searching products by category"""
        repo = ProductRepository(db_session)
        product_create = ProductCreate(**sample_product_data)
        repo.create(product_create)

        results, total = repo.search(query="", category="Electronics", page=1, page_size=20)

        assert len(results) > 0

    def test_search_products_by_price_range(self, db_session: Session, sample_product_data):
        """Test searching products by price range"""
        repo = ProductRepository(db_session)
        product_create = ProductCreate(**sample_product_data)
        repo.create(product_create)

        results, total = repo.search(
            query="",
            min_price=1000,
            max_price=1500,
            page=1,
            page_size=20
        )

        assert len(results) > 0

    def test_get_nonexistent_product(self, db_session: Session):
        """Test retrieving nonexistent product"""
        repo = ProductRepository(db_session)

        result = repo.get_by_id("nonexistent-id")

        assert result is None

    def test_duplicate_sku_raises_error(self, db_session: Session, sample_product_data):
        """Test that duplicate SKU is handled"""
        repo = ProductRepository(db_session)
        product_create = ProductCreate(**sample_product_data)
        repo.create(product_create)

        # Try to create another with same SKU
        duplicate_create = ProductCreate(**sample_product_data)

        with pytest.raises(Exception):
            repo.create(duplicate_create)
