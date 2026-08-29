"""
Payment Service - Complete Test Suite
"""

import pytest
from uuid import uuid4
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from fastapi.testclient import TestClient


TEST_DATABASE_URL = "sqlite:///./test.db"


@pytest.fixture(scope="function")
def engine():
    from app.models.payment import Base
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


class TestPaymentAPI:
    """Payment Service API Tests"""

    @pytest.fixture
    def payment_data(self):
        return {
            "order_id": str(uuid4()),
            "customer_id": str(uuid4()),
            "amount": 299.99,
            "currency": "USD"
        }

    def test_create_payment(self, client, payment_data):
        response = client.post("/payments", json=payment_data)
        assert response.status_code == 201
        assert response.json()["status"] == "PENDING"

    def test_get_payment(self, client, payment_data):
        create_resp = client.post("/payments", json=payment_data)
        payment_id = create_resp.json()["id"]

        get_resp = client.get(f"/payments/{payment_id}")
        assert get_resp.status_code == 200

    def test_get_payment_by_order(self, client, payment_data):
        create_resp = client.post("/payments", json=payment_data)
        order_id = payment_data["order_id"]

        get_resp = client.get(f"/payments/order/{order_id}")
        assert get_resp.status_code == 200

    def test_process_payment(self, client, payment_data):
        create_resp = client.post("/payments", json=payment_data)
        payment_id = create_resp.json()["id"]

        process_resp = client.post(f"/payments/{payment_id}/process")
        assert process_resp.status_code == 200
        # Status should be either SUCCESS or FAILED
        assert process_resp.json()["status"] in ["SUCCESS", "FAILED"]

    def test_refund_payment(self, client, payment_data):
        # Create and process payment first
        create_resp = client.post("/payments", json=payment_data)
        payment_id = create_resp.json()["id"]

        client.post(f"/payments/{payment_id}/process")

        # Refund
        refund_resp = client.post(f"/payments/{payment_id}/refund")
        assert refund_resp.status_code == 200
        assert refund_resp.json()["status"] == "REFUNDED"

    def test_cancel_payment(self, client, payment_data):
        create_resp = client.post("/payments", json=payment_data)
        payment_id = create_resp.json()["id"]

        cancel_resp = client.post(f"/payments/{payment_id}/cancel")
        assert cancel_resp.status_code == 200
        assert cancel_resp.json()["status"] == "CANCELLED"

    def test_list_payments(self, client, payment_data):
        client.post("/payments", json=payment_data)

        list_resp = client.get("/payments?page=1&page_size=10")
        assert list_resp.status_code == 200
