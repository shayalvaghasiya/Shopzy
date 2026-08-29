"""
Product Service business logic.
"""

from typing import Optional, List, Tuple
from sqlalchemy.orm import Session
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse
from app.repositories.product_repository import ProductRepository


class ProductService:
    """Business logic for product operations."""

    def __init__(self, session: Session):
        self.repository = ProductRepository(session)

    def create_product(self, product_data: ProductCreate) -> ProductResponse:
        """Create a new product."""
        # Check if SKU already exists
        existing = self.repository.get_by_sku(product_data.sku)
        if existing:
            raise ValueError(f"Product with SKU {product_data.sku} already exists")

        product = self.repository.create(product_data)
        return ProductResponse.from_orm(product)

    def get_product(self, product_id: str) -> Optional[ProductResponse]:
        """Get product by ID."""
        product = self.repository.get_by_id(product_id)
        if not product:
            return None
        return ProductResponse.from_orm(product)

    def get_all_products(
        self, page: int = 1, page_size: int = 20
    ) -> dict:
        """Get all products with pagination."""
        products, total = self.repository.get_all(page, page_size)
        total_pages = (total + page_size - 1) // page_size

        return {
            "items": [ProductResponse.from_orm(p) for p in products],
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages,
        }

    def update_product(
        self, product_id: str, product_data: ProductUpdate
    ) -> Optional[ProductResponse]:
        """Update a product."""
        product = self.repository.update(product_id, product_data)
        if not product:
            return None
        return ProductResponse.from_orm(product)

    def delete_product(self, product_id: str) -> bool:
        """Delete (soft delete) a product."""
        return self.repository.delete(product_id)

    def search_products(
        self,
        query: str,
        category: Optional[str] = None,
        brand: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        page: int = 1,
        page_size: int = 20,
    ) -> dict:
        """Search products."""
        products, total = self.repository.search(
            query, category, brand, min_price, max_price, page, page_size
        )
        total_pages = (total + page_size - 1) // page_size

        return {
            "items": [ProductResponse.from_orm(p) for p in products],
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages,
        }

    def get_products_by_ids(self, product_ids: List[str]) -> List[ProductResponse]:
        """Get multiple products by IDs (for order service)."""
        from sqlalchemy import select
        from sqlalchemy.orm import Session

        products = []
        for product_id in product_ids:
            product = self.repository.get_by_id(product_id)
            if product:
                products.append(ProductResponse.from_orm(product))

        return products
