"""
Tests for Group Events API endpoints
"""
import pytest
from fastapi import status
from datetime import datetime, timedelta
from decimal import Decimal

from app.services.group_event_service import GroupEventService
from app.schemas.group_events import GroupEventCreate
from app.models.group_events import GroupEvent
from app.models.user import UserProfile


class TestGroupEventsAPI:
    """Test group events API endpoints"""
    
    def test_get_all_group_events_empty(self, client):
        """Test getting all group events when none exist"""
        response = client.get("/group_events/")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []
    
    def test_get_all_group_events_with_data(self, client, db_session, test_user_data):
        """Test getting all group events when they exist"""
        # Create a test user first
        user = UserProfile(**test_user_data)
        db_session.add(user)
        db_session.commit()
        
        # Create test group events
        event1 = GroupEvent(
            name="Morning Ride",
            sport_type="cycling",
            start_at=datetime.now() + timedelta(days=1),
            lat=Decimal("40.7128"),
            lng=Decimal("-74.0060"),
            access="public",
            event_type="casual",
            distance=30,
            created_by=test_user_data["user_id"]
        )
        
        event2 = GroupEvent(
            name="Evening Run",
            sport_type="running",
            start_at=datetime.now() + timedelta(days=2),
            lat=Decimal("40.7589"),
            lng=Decimal("-73.9851"),
            access="public",
            event_type="competitive",
            distance=10,
            created_by=test_user_data["user_id"]
        )
        
        db_session.add_all([event1, event2])
        db_session.commit()
        
        response = client.get("/group_events/")
        assert response.status_code == status.HTTP_200_OK
        
        events = response.json()
        assert len(events) == 2
        assert events[0]["name"] == "Evening Run"  # Should be ordered by created_at desc
        assert events[1]["name"] == "Morning Ride"
    
    def test_get_group_event_by_id_success(self, client, db_session, test_user_data):
        """Test getting a single group event by ID"""
        # Create a test user first
        user = UserProfile(**test_user_data)
        db_session.add(user)
        db_session.commit()
        
        # Create test group event
        event = GroupEvent(
            name="Test Ride",
            sport_type="cycling",
            start_at=datetime.now() + timedelta(days=1),
            lat=Decimal("40.7128"),
            lng=Decimal("-74.0060"),
            access="public",
            event_type="casual",
            distance=25,
            created_by=test_user_data["user_id"]
        )
        
        db_session.add(event)
        db_session.commit()
        
        response = client.get(f"/group_events/{event.id}")
        assert response.status_code == status.HTTP_200_OK
        
        event_data = response.json()
        assert event_data["name"] == "Test Ride"
        assert event_data["sport_type"] == "cycling"
        assert event_data["distance"] == 25
        assert event_data["created_by"] == test_user_data["user_id"]
    
    def test_get_group_event_by_id_not_found(self, client):
        """Test getting a group event that doesn't exist"""
        response = client.get("/group_events/999")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "Group event not found" in response.json()["detail"]
    
    def test_create_group_event_unauthorized(self, client, test_group_event_data):
        """Test creating a group event without authentication"""
        response = client.post("/group_events/", json=test_group_event_data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_create_group_event_success(self, client, db_session, test_user_data, test_group_event_data, mock_user_info):
        """Test creating a group event with authentication"""
        # Create a test user first
        user = UserProfile(**test_user_data)
        db_session.add(user)
        db_session.commit()
        
        # Mock authentication
        from app.utils.auth_dependencies import get_current_user
        def mock_get_current_user():
            return mock_user_info
        
        client.app.dependency_overrides[get_current_user] = mock_get_current_user
        
        try:
            response = client.post("/group_events/", json=test_group_event_data)
            assert response.status_code == status.HTTP_200_OK
            
            event_data = response.json()
            assert event_data["name"] == test_group_event_data["name"]
            assert event_data["sport_type"] == test_group_event_data["sport_type"]
            assert event_data["distance"] == test_group_event_data["distance"]
            assert event_data["created_by"] == test_user_data["user_id"]
            assert "id" in event_data
            assert "created_at" in event_data
            assert "updated_at" in event_data
        finally:
            client.app.dependency_overrides.clear()
    
    def test_create_group_event_invalid_data(self, client, db_session, test_user_data, mock_user_info):
        """Test creating a group event with invalid data"""
        # Create a test user first
        user = UserProfile(**test_user_data)
        db_session.add(user)
        db_session.commit()
        
        # Mock authentication
        from app.utils.auth_dependencies import get_current_user
        def mock_get_current_user():
            return mock_user_info
        
        client.app.dependency_overrides[get_current_user] = mock_get_current_user
        
        try:
            # Test with missing required fields
            invalid_data = {
                "name": "Test Event",
                # Missing sport_type, start_at, etc.
            }
            
            response = client.post("/group_events/", json=invalid_data)
            assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
            
            # Test with invalid distance
            invalid_data = {
                "name": "Test Event",
                "sport_type": "cycling",
                "start_at": (datetime.now() + timedelta(days=1)).isoformat(),
                "access": "public",
                "event_type": "casual",
                "distance": -5,  # Invalid negative distance
            }
            
            response = client.post("/group_events/", json=invalid_data)
            assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        finally:
            client.app.dependency_overrides.clear()


class TestGroupEventService:
    """Test group event service methods"""
    
    def test_create_group_event(self, db_session, test_user_data):
        """Test creating a group event via service"""
        # Create a test user first
        user = UserProfile(**test_user_data)
        db_session.add(user)
        db_session.commit()
        
        service = GroupEventService(db_session)
        
        event_data = GroupEventCreate(
            name="Service Test Ride",
            sport_type="cycling",
            start_at=datetime.now() + timedelta(days=1),
            lat=Decimal("40.7128"),
            lng=Decimal("-74.0060"),
            access="public",
            event_type="casual",
            distance=35,
            gps_file_link="https://example.com/route.gpx"
        )
        
        event = service.create_group_event(event_data, test_user_data["user_id"])
        
        assert event.name == "Service Test Ride"
        assert event.sport_type == "cycling"
        assert event.distance == 35
        assert event.created_by == test_user_data["user_id"]
        assert event.id is not None
    
    def test_get_all_group_events(self, db_session, test_user_data):
        """Test getting all group events via service"""
        # Create a test user first
        user = UserProfile(**test_user_data)
        db_session.add(user)
        db_session.commit()
        
        service = GroupEventService(db_session)
        
        # Create multiple events
        event1 = GroupEvent(
            name="First Event",
            sport_type="cycling",
            start_at=datetime.now() + timedelta(days=1),
            access="public",
            event_type="casual",
            distance=20,
            created_by=test_user_data["user_id"]
        )
        
        event2 = GroupEvent(
            name="Second Event",
            sport_type="running",
            start_at=datetime.now() + timedelta(days=2),
            access="public",
            event_type="competitive",
            distance=15,
            created_by=test_user_data["user_id"]
        )
        
        db_session.add_all([event1, event2])
        db_session.commit()
        
        events = service.get_all_group_events()
        assert len(events) == 2
        # Should be ordered by created_at desc
        assert events[0].name == "Second Event"
        assert events[1].name == "First Event"
    
    def test_get_group_event_by_id(self, db_session, test_user_data):
        """Test getting a single group event by ID via service"""
        # Create a test user first
        user = UserProfile(**test_user_data)
        db_session.add(user)
        db_session.commit()
        
        service = GroupEventService(db_session)
        
        event = GroupEvent(
            name="Test Event",
            sport_type="cycling",
            start_at=datetime.now() + timedelta(days=1),
            access="public",
            event_type="casual",
            distance=25,
            created_by=test_user_data["user_id"]
        )
        
        db_session.add(event)
        db_session.commit()
        
        # Test getting existing event
        found_event = service.get_group_event_by_id(event.id)
        assert found_event is not None
        assert found_event.name == "Test Event"
        
        # Test getting non-existent event
        not_found = service.get_group_event_by_id(999)
        assert not_found is None
