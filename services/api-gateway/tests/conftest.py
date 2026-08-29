"""
API Gateway - Test Configuration
"""

import pytest
from fastapi.testclient import TestClient


@pytest.fixture(scope="function")
def client():
    from app.main import app
    client = TestClient(app)
    return client
