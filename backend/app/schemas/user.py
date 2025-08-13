from pydantic import BaseModel, EmailStr, validator
from typing import Optional, List
from datetime import datetime
from decimal import Decimal

# Enums for validation
class SportType(str):
    RUNNING = "running"
    CYCLING = "cycling"

class PaceType(str):
    CASUAL = "casual"
    MODERATE = "moderate"
    FAST = "fast"

class RideType(str):
    CASUAL = "casual"
    DROP_RIDE = "drop_ride"
    COMPETITIVE = "competitive"

class DayOfWeek(str):
    MONDAY = "monday"
    TUESDAY = "tuesday"
    WEDNESDAY = "wednesday"
    THURSDAY = "thursday"
    FRIDAY = "friday"
    SATURDAY = "saturday"
    SUNDAY = "sunday"

# Base schemas
class UserProfileBase(BaseModel):
    name: Optional[str] = None
    bio: Optional[str] = None
    location_lat: Optional[Decimal] = None
    location_lng: Optional[Decimal] = None
    location_name: Optional[str] = None

class UserPreferencesBase(BaseModel):
    sports: Optional[List[str]] = []
    preferred_pace: Optional[str] = None
    ride_type: Optional[str] = None
    distance_range_min: Optional[int] = None
    distance_range_max: Optional[int] = None
    availability: Optional[List[str]] = []
    
    @validator('sports')
    def validate_sports(cls, v):
        if v is not None:
            valid_sports = ['running', 'cycling']
            for sport in v:
                if sport not in valid_sports:
                    raise ValueError(f'Invalid sport: {sport}. Must be one of {valid_sports}')
        return v
    
    @validator('preferred_pace')
    def validate_pace(cls, v):
        if v is not None:
            valid_paces = ['casual', 'moderate', 'fast']
            if v not in valid_paces:
                raise ValueError(f'Invalid pace: {v}. Must be one of {valid_paces}')
        return v
    
    @validator('ride_type')
    def validate_ride_type(cls, v):
        if v is not None:
            valid_types = ['casual', 'drop_ride', 'competitive']
            if v not in valid_types:
                raise ValueError(f'Invalid ride type: {v}. Must be one of {valid_types}')
        return v
    
    @validator('availability')
    def validate_availability(cls, v):
        if v is not None:
            valid_days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
            for day in v:
                if day not in valid_days:
                    raise ValueError(f'Invalid day: {day}. Must be one of {valid_days}')
        return v

# Create schemas
class UserProfileCreate(UserProfileBase):
    user_id: str
    email: EmailStr

class UserPreferencesCreate(UserPreferencesBase):
    user_id: str

# Update schemas
class UserProfileUpdate(UserProfileBase):
    pass

class UserPreferencesUpdate(UserPreferencesBase):
    pass

# Response schemas (original - for internal use)
class UserProfileResponse(UserProfileBase):
    id: int
    user_id: str
    email: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class UserPreferencesResponse(UserPreferencesBase):
    id: int
    user_id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Simplified response schemas (for frontend - excludes unused fields)
class UserProfileSimpleResponse(BaseModel):
    id: int
    user_id: str
    email: str
    name: Optional[str] = None
    bio: Optional[str] = None
    location_lat: Optional[Decimal] = None
    location_lng: Optional[Decimal] = None
    location_name: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class UserPreferencesSimpleResponse(BaseModel):
    id: int
    user_id: str
    preferred_pace: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Combined schemas
class UserProfileWithPreferences(BaseModel):
    profile: UserProfileResponse
    preferences: Optional[UserPreferencesResponse] = None

class UserProfileWithPreferencesSimple(BaseModel):
    profile: UserProfileSimpleResponse
    preferences: Optional[UserPreferencesSimpleResponse] = None

class OnboardingRequest(BaseModel):
    profile: UserProfileUpdate
    preferences: UserPreferencesUpdate 