"""
Shared utilities for all services.
"""

import uuid
import json
from typing import Optional, Any, Dict
from datetime import datetime
from enum import Enum


class ResponseFormat:
    """Standardized API response format for all services."""

    @staticmethod
    def success(data: Any, request_id: Optional[str] = None) -> Dict[str, Any]:
        """Create a success response."""
        return {
            "success": True,
            "data": data,
            "error": None,
            "request_id": request_id or str(uuid.uuid4()),
        }

    @staticmethod
    def error(
        code: str,
        message: str,
        request_id: Optional[str] = None,
        details: Optional[Dict] = None,
    ) -> Dict[str, Any]:
        """Create an error response."""
        return {
            "success": False,
            "data": None,
            "error": {
                "code": code,
                "message": message,
                **({"details": details} if details else {}),
            },
            "request_id": request_id or str(uuid.uuid4()),
        }


class ErrorCode(str, Enum):
    """Standard error codes across all services."""

    # Generic
    INTERNAL_SERVER_ERROR = "INTERNAL_SERVER_ERROR"
    INVALID_REQUEST = "INVALID_REQUEST"
    VALIDATION_ERROR = "VALIDATION_ERROR"
    SERVICE_UNAVAILABLE = "SERVICE_UNAVAILABLE"

    # Resource errors
    RESOURCE_NOT_FOUND = "RESOURCE_NOT_FOUND"
    RESOURCE_ALREADY_EXISTS = "RESOURCE_ALREADY_EXISTS"
    RESOURCE_CONFLICT = "RESOURCE_CONFLICT"

    # Business logic errors
    INSUFFICIENT_INVENTORY = "INSUFFICIENT_INVENTORY"
    PAYMENT_FAILED = "PAYMENT_FAILED"
    INVALID_ORDER_STATE = "INVALID_ORDER_STATE"
    INVALID_CUSTOMER = "INVALID_CUSTOMER"
    INVALID_PRODUCT = "INVALID_PRODUCT"

    # Idempotency
    DUPLICATE_REQUEST = "DUPLICATE_REQUEST"


def generate_request_id() -> str:
    """Generate a unique request ID."""
    return str(uuid.uuid4())


def generate_correlation_id() -> str:
    """Generate a unique correlation ID."""
    return str(uuid.uuid4())


class StructuredLogger:
    """
    Structured logging utility for JSON logs with correlation IDs.
    """

    @staticmethod
    def log(
        level: str,
        message: str,
        service: str,
        request_id: Optional[str] = None,
        correlation_id: Optional[str] = None,
        endpoint: Optional[str] = None,
        method: Optional[str] = None,
        status_code: Optional[int] = None,
        latency_ms: Optional[float] = None,
        **extra: Any,
    ) -> str:
        """Create a structured log entry."""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": level,
            "message": message,
            "service": service,
            "request_id": request_id,
            "correlation_id": correlation_id,
            "endpoint": endpoint,
            "method": method,
            "status_code": status_code,
            "latency_ms": latency_ms,
            **extra,
        }
        # Remove None values
        log_entry = {k: v for k, v in log_entry.items() if v is not None}
        return json.dumps(log_entry)


class IdempotencyKey:
    """Utilities for idempotent request handling."""

    @staticmethod
    def create() -> str:
        """Create a new idempotency key."""
        return str(uuid.uuid4())
