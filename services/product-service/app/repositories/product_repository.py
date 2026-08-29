"""
Product Service repository - Data access layer.
"""

from sqlalchemy.orm import Session
from sqlalchemy import select, or_, and_
from typing import Optional, List, Tuple
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate


class ProductRepository:
    """Repository for product data access."""

    def __init__(self, session: Session):
        self.session = session

    def create(self, product: ProductCreate) -> Product:
        """Create a new product."""
        db_product = Product(
            id=self._generate_id(),
            name=product.name,
            description=product.description,
            sku=product.sku,
            price=product.price,
            category=product.category,
            subcategory=product.subcategory,
            brand=product.brand,
            image_url=product.image_url,
            stock_count=product.stock_count,
            status="active",
        )
        self.session.add(db_product)
        self.session.commit()
        self.session.refresh(db_product)
        return db_product

    def get_by_id(self, product_id: str) -> Optional[Product]:
        """Get product by ID."""
        query = select(Product).where(Product.id == product_id)
        return self.session.execute(query).scalar_one_or_none()

    def get_by_sku(self, sku: str) -> Optional[Product]:
        """Get product by SKU."""
        query = select(Product).where(Product.sku == sku)
        return self.session.execute(query).scalar_one_or_none()

    def get_all(self, page: int = 1, page_size: int = 20) -> Tuple[List[Product], int]:
        """Get all active products with pagination."""
        query = select(Product).where(Product.status == "active")
        total = self.session.execute(select(Product).where(Product.status == "active")).scalar()

        offset = (page - 1) * page_size
        products = self.session.execute(
            query.offset(offset).limit(page_size)
        ).scalars().all()

        total_count = self.session.execute(
            select(Product).where(Product.status == "active")
        ).scalars().all()

        return products, len(total_count)

    def update(self, product_id: str, update: ProductUpdate) -> Optional[Product]:
        """Update a product."""
        product = self.get_by_id(product_id)
        if not product:
            return None

        update_data = update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            if value is not None:
                setattr(product, field, value)

        self.session.commit()
        self.session.refresh(product)
        return product

    def delete(self, product_id: str) -> bool:
        """Soft delete a product (mark as inactive)."""
        product = self.get_by_id(product_id)
        if not product:
            return False

        product.status = "inactive"
        self.session.commit()
        return True

    def search(
        self,
        query: str,
        category: Optional[str] = None,
        brand: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        page: int = 1,
        page_size: int = 20,
    ) -> Tuple[List[Product], int]:
        """Search products."""
        filters = [Product.status == "active"]

        if query:
            filters.append(
                or_(
                    Product.name.ilike(f"%{query}%"),
                    Product.description.ilike(f"%{query}%"),
                )
            )

        if category:
            filters.append(Product.category.ilike(f"%{category}%"))

        if brand:
            filters.append(Product.brand.ilike(f"%{brand}%"))

        if min_price is not None:
            filters.append(Product.price >= min_price)

        if max_price is not None:
            filters.append(Product.price <= max_price)

        query_obj = select(Product).where(and_(*filters))

        total_count = len(self.session.execute(query_obj).scalars().all())

        offset = (page - 1) * page_size
        products = self.session.execute(
            query_obj.offset(offset).limit(page_size)
        ).scalars().all()

        return products, total_count

    @staticmethod
    def _generate_id() -> str:
        """Generate a unique ID for product."""
        import uuid
        return str(uuid.uuid4())
