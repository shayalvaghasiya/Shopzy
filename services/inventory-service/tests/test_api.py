"""
Inventory Service - Complete Test Suite
"""

import pytest
from uuid import uuid4
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from fastapi.testclient import TestClient


TEST_DATABASE_URL = "sqlite:///./test.db"


@pytest.fixture(scope="function")
def engine():
    from app.models.inventory import Base
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


class TestInventoryAPI:
    """Inventory Service API Tests"""

    @pytest.fixture
    def inventory_data(self):
        return {
            "product_id": str(uuid4()),
            "available_quantity": 100
        }

    def test_create_inventory(self, client, inventory_data):
        response = client.post("/inventory", json=inventory_data)
        assert response.status_code == 201

    def test_get_inventory_by_product(self, client, inventory_data):
        create_resp = client.post("/inventory", json=inventory_data)
        product_id = inventory_data["product_id"]

        get_resp = client.get(f"/inventory/product/{product_id}")
        assert get_resp.status_code == 200

    def test_reserve_inventory(self, client, inventory_data):
        client.post("/inventory", json=inventory_data)
        product_id = inventory_data["product_id"]

        reserve_resp = client.post(
            f"/inventory/reserve?order_id={uuid4()}&product_id={product_id}&quantity=10"
        )
        assert reserve_resp.status_code == 200

    def test_check_stock_availability(self, client, inventory_data):
        client.post("/inventory", json=inventory_data)
        product_id = inventory_data["product_id"]

        check_resp = client.get(f"/inventory/check/{product_id}?quantity=50")
        assert check_resp.status_code == 200
        assert check_resp.json()["available"] == True

    def test_insufficient_stock(self, client, inventory_data):
        client.post("/inventory", json=inventory_data)
        product_id = inventory_data["product_id"]

        check_resp = client.get(f"/inventory/check/{product_id}?quantity=1000")
        assert check_resp.status_code == 200
        assert check_resp.json()["available"] == False

    def test_list_inventory(self, client, inventory_data):
        client.post("/inventory", json=inventory_data)

        list_resp = client.get("/inventory?page=1&page_size=10")
        assert list_resp.status_code == 200

    def test_get_available_quantity(self, client, inventory_data):
        client.post("/inventory", json=inventory_data)
        product_id = inventory_data["product_id"]

        qty_resp = client.get(f"/inventory/available/{product_id}")
        assert qty_resp.status_code == 200
