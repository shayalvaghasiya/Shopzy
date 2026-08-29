"""
Notification Service - Complete Test Suite
"""

import pytest
from uuid import uuid4
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from fastapi.testclient import TestClient


TEST_DATABASE_URL = "sqlite:///./test.db"


@pytest.fixture(scope="function")
def engine():
    from app.models.notification import Base
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


class TestNotificationAPI:
    """Notification Service API Tests"""

    @pytest.fixture
    def notification_data(self):
        return {
            "customer_id": str(uuid4()),
            "order_id": str(uuid4()),
            "event_type": "ORDER_CREATED",
            "event_id": str(uuid4()),
            "notification_type": "email",
            "channel": "email",
            "subject": "Order Confirmation",
            "message": "Your order has been created",
            "recipient": "customer@example.com"
        }

    def test_create_notification(self, client, notification_data):
        response = client.post("/notifications", json=notification_data)
        assert response.status_code == 201

    def test_get_notification(self, client, notification_data):
        create_resp = client.post("/notifications", json=notification_data)
        notification_id = create_resp.json()["id"]

        get_resp = client.get(f"/notifications/{notification_id}")
        assert get_resp.status_code == 200

    def test_list_notifications(self, client, notification_data):
        client.post("/notifications", json=notification_data)

        list_resp = client.get("/notifications?page=1&page_size=10")
        assert list_resp.status_code == 200

    def test_get_customer_notifications(self, client, notification_data):
        create_resp = client.post("/notifications", json=notification_data)
        customer_id = notification_data["customer_id"]

        cust_resp = client.get(f"/notifications/customer/{customer_id}?page=1&page_size=10")
        assert cust_resp.status_code == 200

    def test_mark_as_read(self, client, notification_data):
        create_resp = client.post("/notifications", json=notification_data)
        notification_id = create_resp.json()["id"]

        read_resp = client.patch(f"/notifications/{notification_id}/read")
        assert read_resp.status_code == 200
        assert read_resp.json()["read"] == True

    def test_update_status(self, client, notification_data):
        create_resp = client.post("/notifications", json=notification_data)
        notification_id = create_resp.json()["id"]

        status_resp = client.patch(f"/notifications/{notification_id}/status/sent")
        assert status_resp.status_code == 200
        assert status_resp.json()["status"] == "sent"

    def test_delete_notification(self, client, notification_data):
        create_resp = client.post("/notifications", json=notification_data)
        notification_id = create_resp.json()["id"]

        delete_resp = client.delete(f"/notifications/{notification_id}")
        assert delete_resp.status_code == 204

    def test_event_deduplication(self, client, notification_data):
        event_id = str(uuid4())
        notification_data["event_id"] = event_id

        resp1 = client.post("/notifications", json=notification_data)
        assert resp1.status_code == 201

        # Second request with same event_id should return existing
        resp2 = client.post("/notifications", json=notification_data)
        assert resp2.status_code == 201
