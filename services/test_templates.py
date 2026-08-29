"""
Generic test template for all services - copy and adapt for each service
"""

import pytest
from uuid import uuid4
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from fastapi.testclient import TestClient

# Configuration
TEST_DATABASE_URL = "sqlite:///./test.db"


@pytest.fixture(scope="function")
def engine():
    """Create test database engine"""
    from app.models import Base  # Import Base from service

    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session(engine):
    """Create test database session"""
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()


@pytest.fixture(scope="function")
def client(db_session: Session):
    """Create test client with dependency override"""
    from app.main import app
    from app.core.dependencies import get_db

    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


# Base test classes for each service type

class BaseRepositoryTests:
    """Base tests for all repository implementations"""

    # Override these in each service's test file
    repository_class = None
    model_class = None
    schema_create_class = None
    schema_update_class = None
    sample_data = {}

    def test_create(self, db_session):
        raise NotImplementedError

    def test_get_by_id(self, db_session):
        raise NotImplementedError

    def test_update(self, db_session):
        raise NotImplementedError

    def test_delete(self, db_session):
        raise NotImplementedError

    def test_get_all_with_pagination(self, db_session):
        raise NotImplementedError


class BaseServiceTests:
    """Base tests for all service implementations"""

    service_class = None
    schema_create_class = None
    sample_data = {}

    def test_create(self, db_session):
        raise NotImplementedError

    def test_get(self, db_session):
        raise NotImplementedError

    def test_update(self, db_session):
        raise NotImplementedError

    def test_delete(self, db_session):
        raise NotImplementedError

    def test_get_all(self, db_session):
        raise NotImplementedError


class BaseAPITests:
    """Base tests for all API endpoints"""

    create_endpoint = None
    list_endpoint = None
    get_endpoint = None
    update_endpoint = None
    delete_endpoint = None
    sample_data = {}

    def test_create_via_api(self, client):
        raise NotImplementedError

    def test_get_via_api(self, client):
        raise NotImplementedError

    def test_list_via_api(self, client):
        raise NotImplementedError

    def test_update_via_api(self, client):
        raise NotImplementedError

    def test_delete_via_api(self, client):
        raise NotImplementedError

    def test_validation_errors(self, client):
        raise NotImplementedError
