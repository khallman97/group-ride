"""
Pytest configuration and common fixtures for testing
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from typing import Generator

from app.main import app
from app.database import Base, get_db
from app.config import get_settings

# Test database URL - use in-memory SQLite for testing
TEST_DATABASE_URL = "sqlite:///:memory:"

# Create test engine
test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

# Create test session
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

@pytest.fixture(scope="session")
def db_engine():
    """Create test database engine"""
    # Create all tables
    Base.metadata.create_all(bind=test_engine)
    yield test_engine
    # Clean up
    Base.metadata.drop_all(bind=test_engine)

@pytest.fixture
def db_session(db_engine):
    """Create test database session"""
    connection = db_engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture
def client(db_session) -> Generator:
    """Create test client with test database"""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

@pytest.fixture
def test_user_data():
    """Sample user data for testing"""
    return {
        "user_id": "test-user-123",
        "email": "test@example.com",
        "name": "Test User",
        "bio": "Test bio",
        "location_lat": 40.7128,
        "location_lng": -74.0060,
        "location_name": "New York, NY"
    }

@pytest.fixture
def test_group_event_data():
    """Sample group event data for testing"""
    from datetime import datetime, timedelta
    return {
        "name": "Saturday Morning Ride",
        "sport_type": "cycling",
        "start_at": (datetime.now() + timedelta(days=1)).isoformat(),
        "lat": 40.7128,
        "lng": -74.0060,
        "access": "public",
        "event_type": "casual",
        "distance": 50,
        "gps_file_link": "https://example.com/route.gpx"
    }

@pytest.fixture
def mock_auth_token():
    """Mock authentication token for testing"""
    return "mock-jwt-token"

@pytest.fixture
def mock_user_info():
    """Mock user info for testing"""
    from app.schemas.auth import UserInfo
    return UserInfo(
        user_id="test-user-123",
        email="test@example.com",
        name="Test User"
    )
