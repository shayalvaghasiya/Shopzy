"""
API Gateway routing logic.
"""

from fastapi import APIRouter, HTTPException, Query, Header
from typing import Optional
import httpx
import logging
from app.core.config import get_settings

router = APIRouter()
logger = logging.getLogger(__name__)
settings = get_settings()

# Service URLs mapping
SERVICE_URLS = {
    "products": settings.PRODUCT_SERVICE_URL,
    "inventory": settings.INVENTORY_SERVICE_URL,
    "customers": settings.CUSTOMER_SERVICE_URL,
    "orders": settings.ORDER_SERVICE_URL,
    "payments": settings.PAYMENT_SERVICE_URL,
    "notifications": settings.NOTIFICATION_SERVICE_URL,
}


@router.get("/products")
async def list_products(page: int = Query(1), page_size: int = Query(20)):
    """Proxy to Product Service."""
    return await proxy_request(
        "products",
        f"/products?page={page}&page_size={page_size}",
        "GET"
    )


@router.get("/products/{product_id}")
async def get_product(product_id: str):
    """Proxy to Product Service."""
    return await proxy_request(
        "products",
        f"/products/{product_id}",
        "GET"
    )


@router.post("/products")
async def create_product(data: dict):
    """Proxy to Product Service."""
    return await proxy_request(
        "products",
        "/products",
        "POST",
        json=data
    )


@router.get("/customers")
async def list_customers(page: int = Query(1), page_size: int = Query(20)):
    """Proxy to Customer Service."""
    return await proxy_request(
        "customers",
        f"/customers?page={page}&page_size={page_size}",
        "GET"
    )


@router.get("/customers/{customer_id}")
async def get_customer(customer_id: str):
    """Proxy to Customer Service."""
    return await proxy_request(
        "customers",
        f"/customers/{customer_id}",
        "GET"
    )


@router.post("/customers")
async def create_customer(data: dict):
    """Proxy to Customer Service."""
    return await proxy_request(
        "customers",
        "/customers",
        "POST",
        json=data
    )


@router.get("/orders")
async def list_orders(page: int = Query(1), page_size: int = Query(20)):
    """Proxy to Order Service."""
    return await proxy_request(
        "orders",
        f"/orders?page={page}&page_size={page_size}",
        "GET"
    )


@router.get("/orders/{order_id}")
async def get_order(order_id: str):
    """Proxy to Order Service."""
    return await proxy_request(
        "orders",
        f"/orders/{order_id}",
        "GET"
    )


@router.post("/orders")
async def create_order(data: dict):
    """Proxy to Order Service."""
    return await proxy_request(
        "orders",
        "/orders",
        "POST",
        json=data
    )


@router.get("/inventory/product/{product_id}")
async def get_inventory(product_id: str):
    """Proxy to Inventory Service."""
    return await proxy_request(
        "inventory",
        f"/inventory/product/{product_id}",
        "GET"
    )


@router.get("/payments/{payment_id}")
async def get_payment(payment_id: str):
    """Proxy to Payment Service."""
    return await proxy_request(
        "payments",
        f"/payments/{payment_id}",
        "GET"
    )


@router.get("/notifications")
async def list_notifications(page: int = Query(1), page_size: int = Query(20)):
    """Proxy to Notification Service."""
    return await proxy_request(
        "notifications",
        f"/notifications?page={page}&page_size={page_size}",
        "GET"
    )


@router.get("/health")
async def gateway_health():
    """Check health of all services."""
    health_status = {}

    for service_name, url in SERVICE_URLS.items():
        try:
            async with httpx.AsyncClient(timeout=5) as client:
                response = await client.get(f"{url}/health")
                health_status[service_name] = {
                    "status": "healthy" if response.status_code == 200 else "unhealthy",
                    "url": url
                }
        except Exception as e:
            health_status[service_name] = {
                "status": "unreachable",
                "error": str(e),
                "url": url
            }

    return {
        "gateway": "healthy",
        "services": health_status
    }


async def proxy_request(
    service: str,
    path: str,
    method: str = "GET",
    json: Optional[dict] = None,
    headers: Optional[dict] = None,
) -> dict:
    """Proxy request to a service."""
    if service not in SERVICE_URLS:
        raise HTTPException(status_code=400, detail=f"Unknown service: {service}")

    url = f"{SERVICE_URLS[service]}{path}"

    try:
        async with httpx.AsyncClient(timeout=settings.REQUEST_TIMEOUT) as client:
            if method == "GET":
                response = await client.get(url, headers=headers)
            elif method == "POST":
                response = await client.post(url, json=json, headers=headers)
            elif method == "PUT":
                response = await client.put(url, json=json, headers=headers)
            elif method == "DELETE":
                response = await client.delete(url, headers=headers)
            else:
                raise HTTPException(status_code=400, detail=f"Unsupported method: {method}")

            if response.status_code >= 400:
                logger.error(f"Service error: {service} {path} - {response.status_code}")
                raise HTTPException(
                    status_code=response.status_code,
                    detail=response.text
                )

            return response.json()

    except httpx.TimeoutException:
        logger.error(f"Timeout calling {service}: {url}")
        raise HTTPException(
            status_code=504,
            detail=f"Service timeout: {service}"
        )
    except Exception as e:
        logger.error(f"Error calling {service}: {str(e)}")
        raise HTTPException(
            status_code=503,
            detail=f"Service unavailable: {service}"
        )
