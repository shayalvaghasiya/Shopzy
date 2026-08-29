"""
Product Service API routes.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.services.product_service import ProductService
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse, ProductListResponse
from app.core.dependencies import get_db
import logging

router = APIRouter(prefix="/products", tags=["products"])
logger = logging.getLogger(__name__)


@router.get("", response_model=ProductListResponse)
async def list_products(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """List all active products with pagination."""
    service = ProductService(db)
    result = service.get_all_products(page, page_size)
    return result


@router.get("/search", response_model=ProductListResponse)
async def search_products(
    query: str = Query(..., min_length=1),
    category: str = Query(None),
    brand: str = Query(None),
    min_price: float = Query(None, ge=0),
    max_price: float = Query(None, ge=0),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """Search products."""
    service = ProductService(db)
    result = service.search_products(
        query, category, brand, min_price, max_price, page, page_size
    )
    return result


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: str, db: Session = Depends(get_db)):
    """Get product by ID."""
    service = ProductService(db)
    product = service.get_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.post("", response_model=ProductResponse, status_code=201)
async def create_product(
    product: ProductCreate, db: Session = Depends(get_db)
):
    """Create a new product (admin only)."""
    service = ProductService(db)
    try:
        return service.create_product(product)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: str, product: ProductUpdate, db: Session = Depends(get_db)
):
    """Update a product (admin only)."""
    service = ProductService(db)
    updated = service.update_product(product_id, product)
    if not updated:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated


@router.delete("/{product_id}", status_code=204)
async def delete_product(product_id: str, db: Session = Depends(get_db)):
    """Delete (soft delete) a product (admin only)."""
    service = ProductService(db)
    success = service.delete_product(product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
    return None
