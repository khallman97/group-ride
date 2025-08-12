from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import Optional, List
from ..models.user import UserProfile, UserPreferences
from ..schemas.user import UserProfileCreate, UserProfileUpdate, UserPreferencesCreate, UserPreferencesUpdate
from ..schemas.auth import UserInfo

class UserService:
    def __init__(self, db: Session):
        self.db = db

    def create_user_profile(self, user_info: UserInfo) -> UserProfile:
        """Create a new user profile after successful authentication"""
        try:
            db_profile = UserProfile(
                user_id=user_info.user_id,
                email=user_info.email,
                name=user_info.name
            )
            self.db.add(db_profile)
            self.db.commit()
            self.db.refresh(db_profile)
            return db_profile
        except IntegrityError:
            self.db.rollback()
            # Profile already exists, return existing one
            return self.get_user_profile_by_user_id(user_info.user_id)

    def get_user_profile_by_user_id(self, user_id: str) -> Optional[UserProfile]:
        """Get user profile by Cognito user ID"""
        return self.db.query(UserProfile).filter(UserProfile.user_id == user_id).first()

    def get_user_profile_by_email(self, email: str) -> Optional[UserProfile]:
        """Get user profile by email"""
        return self.db.query(UserProfile).filter(UserProfile.email == email).first()

    def update_user_profile(self, user_id: str, profile_update: UserProfileUpdate) -> Optional[UserProfile]:
        """Update user profile"""
        db_profile = self.get_user_profile_by_user_id(user_id)
        if not db_profile:
            return None
        
        update_data = profile_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_profile, field, value)
        
        self.db.commit()
        self.db.refresh(db_profile)
        return db_profile

    def create_user_preferences(self, user_id: str, preferences_data: UserPreferencesUpdate) -> Optional[UserPreferences]:
        """Create or update user preferences"""
        # Check if preferences already exist
        db_preferences = self.get_user_preferences_by_user_id(user_id)
        
        if db_preferences:
            # Update existing preferences
            return self.update_user_preferences(user_id, preferences_data)
        else:
            # Create new preferences
            preferences_create = UserPreferencesCreate(
                user_id=user_id,
                **preferences_data.dict(exclude_unset=True)
            )
            
            db_preferences = UserPreferences(**preferences_create.dict())
            self.db.add(db_preferences)
            self.db.commit()
            self.db.refresh(db_preferences)
            return db_preferences

    def get_user_preferences_by_user_id(self, user_id: str) -> Optional[UserPreferences]:
        """Get user preferences by Cognito user ID"""
        return self.db.query(UserPreferences).filter(UserPreferences.user_id == user_id).first()

    def update_user_preferences(self, user_id: str, preferences_update: UserPreferencesUpdate) -> Optional[UserPreferences]:
        """Update user preferences"""
        db_preferences = self.get_user_preferences_by_user_id(user_id)
        if not db_preferences:
            return None
        
        update_data = preferences_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_preferences, field, value)
        
        self.db.commit()
        self.db.refresh(db_preferences)
        return db_preferences

    def get_user_with_preferences(self, user_id: str) -> Optional[dict]:
        """Get user profile with preferences"""
        profile = self.get_user_profile_by_user_id(user_id)
        if not profile:
            return None
        
        preferences = self.get_user_preferences_by_user_id(user_id)
        
        return {
            "profile": profile,
            "preferences": preferences
        }

    def complete_onboarding(self, user_id: str, profile_data: UserProfileUpdate, preferences_data: UserPreferencesUpdate) -> dict:
        """Complete user onboarding with profile and preferences"""
        # Update profile
        profile = self.update_user_profile(user_id, profile_data)
        if not profile:
            raise ValueError("User profile not found")
        
        # Create/update preferences
        preferences = self.create_user_preferences(user_id, preferences_data)
        
        return {
            "profile": profile,
            "preferences": preferences,
            "message": "Onboarding completed successfully"
        }

    def search_users_by_preferences(self, sports: List[str] = None, location_lat: float = None, location_lng: float = None, max_distance: float = None) -> List[UserProfile]:
        """Search users by preferences and location"""
        query = self.db.query(UserProfile).join(UserPreferences)
        
        if sports:
            query = query.filter(UserPreferences.sports.overlap(sports))
        
        # TODO: Add location-based search when we implement geospatial queries
        # For now, just return users with matching sports
        return query.all() 