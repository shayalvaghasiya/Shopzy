"""
Customer Service - Complete Test Suite
"""

import pytest
from uuid import uuid4
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from fastapi.testclient import TestClient


TEST_DATABASE_URL = "sqlite:///./test.db"


@pytest.fixture(scope="function")
def engine():
    from app.models.customer import Base
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


class TestCustomerAPI:
    """Customer Service API Tests"""

    @pytest.fixture
    def customer_data(self):
        return {
            "first_name": "John",
            "last_name": "Doe",
            "email": f"john{uuid4().hex[:4]}@example.com",
            "phone": "+1-555-0123"
        }

    def test_create_customer(self, client, customer_data):
        response = client.post("/customers", json=customer_data)
        assert response.status_code == 201
        assert response.json()["email"] == customer_data["email"]

    def test_get_customer(self, client, customer_data):
        create_resp = client.post("/customers", json=customer_data)
        customer_id = create_resp.json()["id"]

        get_resp = client.get(f"/customers/{customer_id}")
        assert get_resp.status_code == 200
        assert get_resp.json()["id"] == customer_id

    def test_update_customer(self, client, customer_data):
        create_resp = client.post("/customers", json=customer_data)
        customer_id = create_resp.json()["id"]

        update_data = {"first_name": "Jane", "email": customer_data["email"]}
        update_resp = client.put(f"/customers/{customer_id}", json=update_data)
        assert update_resp.status_code == 200
        assert update_resp.json()["first_name"] == "Jane"

    def test_delete_customer(self, client, customer_data):
        create_resp = client.post("/customers", json=customer_data)
        customer_id = create_resp.json()["id"]

        delete_resp = client.delete(f"/customers/{customer_id}")
        assert delete_resp.status_code == 204

    def test_add_address(self, client, customer_data):
        create_resp = client.post("/customers", json=customer_data)
        customer_id = create_resp.json()["id"]

        address_data = {
            "type": "shipping",
            "street_address": "123 Main St",
            "city": "Springfield",
            "state_province": "IL",
            "postal_code": "62701",
            "country": "USA"
        }

        addr_resp = client.post(f"/customers/{customer_id}/addresses", json=address_data)
        assert addr_resp.status_code == 201

    def test_list_customers(self, client, customer_data):
        client.post("/customers", json=customer_data)

        list_resp = client.get("/customers?page=1&page_size=10")
        assert list_resp.status_code == 200
        assert "items" in list_resp.json()

    def test_duplicate_email_error(self, client, customer_data):
        client.post("/customers", json=customer_data)

        duplicate_resp = client.post("/customers", json=customer_data)
        assert duplicate_resp.status_code == 409
