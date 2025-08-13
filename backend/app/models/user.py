from sqlalchemy import Column, Integer, String, Text, DECIMAL, DateTime, ARRAY, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from ..database import Base

class UserProfile(Base):
    __tablename__ = "user_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(128), unique=True, nullable=False, index=True)  # Cognito user ID
    email = Column(String(255), nullable=False, index=True)
    name = Column(String(255))
    bio = Column(Text)
    location_lat = Column(DECIMAL(10, 8))
    location_lng = Column(DECIMAL(11, 8))
    location_name = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationship to preferences
    preferences = relationship("UserPreferences", back_populates="profile", uselist=False)
    
    # Relationship to group events
    group_events = relationship("GroupEvent", back_populates="creator")

class UserPreferences(Base):
    __tablename__ = "user_preferences"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(128), ForeignKey("user_profiles.user_id"), nullable=False)
    sports = Column(ARRAY(String))  # ['running', 'cycling']
    preferred_pace = Column(String(50))  # 'casual', 'moderate', 'fast'
    ride_type = Column(String(50))  # 'casual', 'drop_ride', 'competitive'
    distance_range_min = Column(Integer)  # in km
    distance_range_max = Column(Integer)  # in km
    availability = Column(ARRAY(String))  # ['monday', 'tuesday', ...]
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationship to profile
    profile = relationship("UserProfile", back_populates="preferences") 