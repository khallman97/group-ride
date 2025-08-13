"""
Tests for Users API endpoints
"""
import pytest
from fastapi import status
from decimal import Decimal

from app.services.user_service import UserService
from app.schemas.user import UserProfileUpdate, UserPreferencesUpdate, OnboardingRequest
from app.models.user import UserProfile, UserPreferences


class TestUsersAPI:
    """Test users API endpoints"""
    
    def test_get_user_profile_unauthorized(self, client):
        """Test getting user profile without authentication"""
        response = client.get("/users/profile")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_get_user_profile_success(self, client, db_session, test_user_data, mock_user_info):
        """Test getting user profile with authentication"""
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
            response = client.get("/users/profile")
            assert response.status_code == status.HTTP_200_OK
            
            profile_data = response.json()
            assert profile_data["user_id"] == test_user_data["user_id"]
            assert profile_data["email"] == test_user_data["email"]
            assert profile_data["name"] == test_user_data["name"]
        finally:
            client.app.dependency_overrides.clear()
    
    def test_get_user_profile_not_found(self, client, mock_user_info):
        """Test getting user profile that doesn't exist"""
        # Mock authentication
        from app.utils.auth_dependencies import get_current_user
        def mock_get_current_user():
            return mock_user_info
        
        client.app.dependency_overrides[get_current_user] = mock_get_current_user
        
        try:
            response = client.get("/users/profile")
            assert response.status_code == status.HTTP_404_NOT_FOUND
            assert "User profile not found" in response.json()["detail"]
        finally:
            client.app.dependency_overrides.clear()
    
    def test_update_user_profile_success(self, client, db_session, test_user_data, mock_user_info):
        """Test updating user profile with authentication"""
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
            update_data = {
                "name": "Updated Name",
                "bio": "Updated bio",
                "location_lat": 40.7589,
                "location_lng": -73.9851,
                "location_name": "Updated Location"
            }
            
            response = client.put("/users/profile", json=update_data)
            assert response.status_code == status.HTTP_200_OK
            
            profile_data = response.json()
            assert profile_data["name"] == "Updated Name"
            assert profile_data["bio"] == "Updated bio"
            assert profile_data["location_name"] == "Updated Location"
        finally:
            client.app.dependency_overrides.clear()
    
    def test_get_user_preferences_unauthorized(self, client):
        """Test getting user preferences without authentication"""
        response = client.get("/users/preferences")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_get_user_preferences_success(self, client, db_session, test_user_data, mock_user_info):
        """Test getting user preferences with authentication"""
        # Create a test user first
        user = UserProfile(**test_user_data)
        db_session.add(user)
        db_session.commit()
        
        # Create user preferences
        preferences = UserPreferences(
            user_id=test_user_data["user_id"],
            sports=["cycling", "running"],
            preferred_pace="moderate",
            ride_type="casual",
            distance_range_min=10,
            distance_range_max=50,
            availability=["monday", "wednesday", "saturday"]
        )
        db_session.add(preferences)
        db_session.commit()
        
        # Mock authentication
        from app.utils.auth_dependencies import get_current_user
        def mock_get_current_user():
            return mock_user_info
        
        client.app.dependency_overrides[get_current_user] = mock_get_current_user
        
        try:
            response = client.get("/users/preferences")
            assert response.status_code == status.HTTP_200_OK
            
            prefs_data = response.json()
            assert prefs_data["sports"] == ["cycling", "running"]
            assert prefs_data["preferred_pace"] == "moderate"
            assert prefs_data["distance_range_min"] == 10
            assert prefs_data["distance_range_max"] == 50
        finally:
            client.app.dependency_overrides.clear()
    
    def test_update_user_preferences_success(self, client, db_session, test_user_data, mock_user_info):
        """Test updating user preferences with authentication"""
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
            update_data = {
                "sports": ["cycling"],
                "preferred_pace": "fast",
                "ride_type": "competitive",
                "distance_range_min": 20,
                "distance_range_max": 100,
                "availability": ["tuesday", "thursday", "sunday"]
            }
            
            response = client.put("/users/preferences", json=update_data)
            assert response.status_code == status.HTTP_200_OK
            
            prefs_data = response.json()
            assert prefs_data["sports"] == ["cycling"]
            assert prefs_data["preferred_pace"] == "fast"
            assert prefs_data["ride_type"] == "competitive"
            assert prefs_data["distance_range_min"] == 20
            assert prefs_data["distance_range_max"] == 100
        finally:
            client.app.dependency_overrides.clear()
    
    def test_get_user_with_preferences_success(self, client, db_session, test_user_data, mock_user_info):
        """Test getting user with preferences"""
        # Create a test user first
        user = UserProfile(**test_user_data)
        db_session.add(user)
        db_session.commit()
        
        # Create user preferences
        preferences = UserPreferences(
            user_id=test_user_data["user_id"],
            sports=["cycling"],
            preferred_pace="moderate",
            ride_type="casual",
            distance_range_min=15,
            distance_range_max=40,
            availability=["monday", "friday"]
        )
        db_session.add(preferences)
        db_session.commit()
        
        # Mock authentication
        from app.utils.auth_dependencies import get_current_user
        def mock_get_current_user():
            return mock_user_info
        
        client.app.dependency_overrides[get_current_user] = mock_get_current_user
        
        try:
            response = client.get("/users/me")
            assert response.status_code == status.HTTP_200_OK
            
            user_data = response.json()
            assert user_data["profile"]["user_id"] == test_user_data["user_id"]
            assert user_data["profile"]["name"] == test_user_data["name"]
            assert user_data["preferences"]["sports"] == ["cycling"]
            assert user_data["preferences"]["preferred_pace"] == "moderate"
        finally:
            client.app.dependency_overrides.clear()
    
    def test_complete_onboarding_success(self, client, db_session, mock_user_info):
        """Test completing user onboarding"""
        # Mock authentication
        from app.utils.auth_dependencies import get_current_user
        def mock_get_current_user():
            return mock_user_info
        
        client.app.dependency_overrides[get_current_user] = mock_get_current_user
        
        try:
            onboarding_data = {
                "profile": {
                    "name": "New User",
                    "bio": "New user bio",
                    "location_lat": 40.7128,
                    "location_lng": -74.0060,
                    "location_name": "New York, NY"
                },
                "preferences": {
                    "sports": ["running", "cycling"],
                    "preferred_pace": "casual",
                    "ride_type": "casual",
                    "distance_range_min": 5,
                    "distance_range_max": 25,
                    "availability": ["saturday", "sunday"]
                }
            }
            
            response = client.post("/users/onboarding", json=onboarding_data)
            assert response.status_code == status.HTTP_200_OK
            
            result = response.json()
            assert result["profile"]["name"] == "New User"
            assert result["profile"]["bio"] == "New user bio"
            assert result["preferences"]["sports"] == ["running", "cycling"]
            assert result["preferences"]["distance_range_min"] == 5
        finally:
            client.app.dependency_overrides.clear()


class TestUserService:
    """Test user service methods"""
    
    def test_get_user_profile_by_user_id(self, db_session, test_user_data):
        """Test getting user profile by user ID"""
        service = UserService(db_session)
        
        # Create a test user
        user = UserProfile(**test_user_data)
        db_session.add(user)
        db_session.commit()
        
        # Test getting existing user
        profile = service.get_user_profile_by_user_id(test_user_data["user_id"])
        assert profile is not None
        assert profile.name == test_user_data["name"]
        assert profile.email == test_user_data["email"]
        
        # Test getting non-existent user
        not_found = service.get_user_profile_by_user_id("non-existent")
        assert not_found is None
    
    def test_update_user_profile(self, db_session, test_user_data):
        """Test updating user profile"""
        service = UserService(db_session)
        
        # Create a test user
        user = UserProfile(**test_user_data)
        db_session.add(user)
        db_session.commit()
        
        # Update profile
        update_data = UserProfileUpdate(
            name="Updated Name",
            bio="Updated bio",
            location_lat=Decimal("40.7589"),
            location_lng=Decimal("-73.9851"),
            location_name="Updated Location"
        )
        
        updated_profile = service.update_user_profile(test_user_data["user_id"], update_data)
        assert updated_profile.name == "Updated Name"
        assert updated_profile.bio == "Updated bio"
        assert updated_profile.location_name == "Updated Location"
    
    def test_get_user_preferences_by_user_id(self, db_session, test_user_data):
        """Test getting user preferences by user ID"""
        service = UserService(db_session)
        
        # Create a test user
        user = UserProfile(**test_user_data)
        db_session.add(user)
        db_session.commit()
        
        # Create user preferences
        preferences = UserPreferences(
            user_id=test_user_data["user_id"],
            sports=["cycling"],
            preferred_pace="moderate",
            ride_type="casual",
            distance_range_min=10,
            distance_range_max=30,
            availability=["monday", "wednesday"]
        )
        db_session.add(preferences)
        db_session.commit()
        
        # Test getting existing preferences
        found_prefs = service.get_user_preferences_by_user_id(test_user_data["user_id"])
        assert found_prefs is not None
        assert found_prefs.sports == ["cycling"]
        assert found_prefs.preferred_pace == "moderate"
        
        # Test getting non-existent preferences
        not_found = service.get_user_preferences_by_user_id("non-existent")
        assert not_found is None
    
    def test_create_user_preferences(self, db_session, test_user_data):
        """Test creating user preferences"""
        service = UserService(db_session)
        
        # Create a test user
        user = UserProfile(**test_user_data)
        db_session.add(user)
        db_session.commit()
        
        # Create preferences
        prefs_data = UserPreferencesUpdate(
            sports=["running", "cycling"],
            preferred_pace="fast",
            ride_type="competitive",
            distance_range_min=20,
            distance_range_max=80,
            availability=["tuesday", "thursday", "saturday"]
        )
        
        created_prefs = service.create_user_preferences(test_user_data["user_id"], prefs_data)
        assert created_prefs.sports == ["running", "cycling"]
        assert created_prefs.preferred_pace == "fast"
        assert created_prefs.distance_range_min == 20
        assert created_prefs.distance_range_max == 80
