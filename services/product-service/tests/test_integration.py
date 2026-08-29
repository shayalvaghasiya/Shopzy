"""
Product Service - Integration tests
"""

import pytest
from uuid import uuid4
from app.schemas.product import ProductCreate
from sqlalchemy.orm import Session


@pytest.fixture
def sample_product_data():
    """Sample product data"""
    return {
        "name": "Integration Test Product",
        "description": "Testing product",
        "sku": f"INT-{uuid4().hex[:8]}",
        "price": 299.99,
        "category": "Electronics",
        "brand": "TestBrand",
        "stock_count": 50
    }


class TestProductIntegration:
    """Integration tests for Product Service"""

    def test_create_and_retrieve_product(self, client, sample_product_data):
        """Test creating and retrieving a product via API"""
        # Create product
        response = client.post(
            "/products",
            json=sample_product_data
        )
        assert response.status_code == 201
        product_id = response.json()["id"]

        # Retrieve product
        response = client.get(f"/products/{product_id}")
        assert response.status_code == 200
        assert response.json()["name"] == sample_product_data["name"]

    def test_create_update_and_retrieve(self, client, sample_product_data):
        """Test create, update, and retrieve workflow"""
        # Create
        response = client.post("/products", json=sample_product_data)
        product_id = response.json()["id"]

        # Update
        update_data = {"name": "Updated Product", "price": 399.99}
        response = client.put(f"/products/{product_id}", json=update_data)
        assert response.status_code == 200
        assert response.json()["name"] == "Updated Product"

        # Retrieve and verify
        response = client.get(f"/products/{product_id}")
        assert response.json()["name"] == "Updated Product"
        assert response.json()["price"] == 399.99

    def test_list_products_with_pagination(self, client, sample_product_data):
        """Test listing products with pagination"""
        # Create multiple products
        for i in range(3):
            data = sample_product_data.copy()
            data["sku"] = f"PAGE-{i}-{uuid4().hex[:4]}"
            client.post("/products", json=data)

        # List with pagination
        response = client.get("/products?page=1&page_size=2")
        assert response.status_code == 200
        data = response.json()
        assert data["page"] == 1
        assert data["page_size"] == 2
        assert len(data["items"]) > 0

    def test_search_products(self, client, sample_product_data):
        """Test searching products"""
        # Create product
        client.post("/products", json=sample_product_data)

        # Search
        response = client.get(
            "/products/search?"
            "query=Integration&"
            "category=Electronics&"
            "page=1&page_size=20"
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) > 0

    def test_delete_product(self, client, sample_product_data):
        """Test deleting a product"""
        # Create
        response = client.post("/products", json=sample_product_data)
        product_id = response.json()["id"]

        # Delete
        response = client.delete(f"/products/{product_id}")
        assert response.status_code == 204

        # Verify deletion (should return 404)
        response = client.get(f"/products/{product_id}")
        assert response.status_code == 404

    def test_create_product_validation(self, client):
        """Test product creation validation"""
        invalid_data = {
            "name": "",  # Empty name
            "sku": "TEST",
            "price": -100,  # Negative price
            "category": "Electronics"
        }

        response = client.post("/products", json=invalid_data)
        assert response.status_code in [400, 422]

    def test_search_by_price_range(self, client, sample_product_data):
        """Test searching by price range"""
        # Create product
        client.post("/products", json=sample_product_data)

        # Search in price range
        response = client.get(
            "/products/search?"
            "query=&"
            "min_price=200&"
            "max_price=400&"
            "page=1&page_size=20"
        )
        assert response.status_code == 200
        results = response.json()["items"]

        for product in results:
            assert 200 <= product["price"] <= 400

    def test_nonexistent_product_returns_404(self, client):
        """Test that nonexistent product returns 404"""
        response = client.get("/products/nonexistent-id")
        assert response.status_code == 404
