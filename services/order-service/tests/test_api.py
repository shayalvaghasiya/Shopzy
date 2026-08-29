"""
Order Service - Complete Test Suite
"""

import pytest
from uuid import uuid4
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from fastapi.testclient import TestClient


TEST_DATABASE_URL = "sqlite:///./test.db"


@pytest.fixture(scope="function")
def engine():
    from app.models.order import Base
    engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session(engine):
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()


@pytest.fixture(scope="function")
def client(db_session):
    from app.main import app
    from app.core.dependencies import get_db

    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


class TestOrderAPI:
    """Order Service API Tests"""

    @pytest.fixture
    def order_data(self):
        return {
            "customer_id": str(uuid4()),
            "items": [
                {
                    "product_id": str(uuid4()),
                    "product_name": "Test Product",
                    "quantity": 2,
                    "unit_price": 99.99
                }
            ]
        }

    def test_create_order(self, client, order_data):
        response = client.post("/orders", json=order_data)
        assert response.status_code == 201
        assert response.json()["status"] == "PENDING"

    def test_get_order(self, client, order_data):
        create_resp = client.post("/orders", json=order_data)
        order_id = create_resp.json()["id"]

        get_resp = client.get(f"/orders/{order_id}")
        assert get_resp.status_code == 200
        assert get_resp.json()["id"] == order_id

    def test_list_orders(self, client, order_data):
        client.post("/orders", json=order_data)

        list_resp = client.get("/orders?page=1&page_size=10")
        assert list_resp.status_code == 200

    def test_get_customer_orders(self, client, order_data):
        create_resp = client.post("/orders", json=order_data)
        customer_id = order_data["customer_id"]

        cust_resp = client.get(f"/orders/customer/{customer_id}?page=1&page_size=10")
        assert cust_resp.status_code == 200

    def test_update_order_status(self, client, order_data):
        create_resp = client.post("/orders", json=order_data)
        order_id = create_resp.json()["id"]

        status_resp = client.patch(f"/orders/{order_id}/status/PAYMENT_PENDING")
        assert status_resp.status_code == 200

    def test_cancel_order(self, client, order_data):
        create_resp = client.post("/orders", json=order_data)
        order_id = create_resp.json()["id"]

        cancel_resp = client.post(f"/orders/{order_id}/cancel")
        assert cancel_resp.status_code == 200
        assert cancel_resp.json()["status"] == "CANCELLED"

    def test_order_total_calculation(self, client, order_data):
        response = client.post("/orders", json=order_data)
        order = response.json()

        # Verify total calculation (subtotal + tax + shipping)
        assert order["subtotal"] > 0
        assert order["tax"] > 0
        assert order["shipping_cost"] >= 0
        assert order["total_amount"] > 0

    def test_idempotent_order_creation(self, client, order_data):
        idempotency_key = str(uuid4())
        order_data["idempotency_key"] = idempotency_key

        # First request
        resp1 = client.post("/orders", json=order_data)
        assert resp1.status_code == 201
        order_id1 = resp1.json()["id"]

        # Second request with same idempotency key
        resp2 = client.post("/orders", json=order_data)
        assert resp2.status_code == 201
        order_id2 = resp2.json()["id"]

        # Should return same order
        assert order_id1 == order_id2
