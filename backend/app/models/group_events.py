from sqlalchemy import Column, Integer, String, Text, DECIMAL, DateTime, ARRAY, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from ..database import Base

class GroupEvent(Base):
    __tablename__ = "group_events"
    
    id = Column(Integer, primary_key=True, index=True) # event id
    name = Column(String(255), nullable=False) # name of event
    sport_type = Column(Text, nullable=False) # type of event (ride/run etc)
    start_at = Column(DateTime, nullable=False) 
    lat = Column(DECIMAL(10, 8)) # latitude of event    
    lng = Column(DECIMAL(11, 8)) # longitude of event
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    access = Column(Text, nullable=False) # public/private/invite_only
    created_by = Column(String(128), ForeignKey("user_profiles.user_id"), nullable=False) # user id of creator

    # ride/pace/distance/type
    event_type = Column(Text, nullable=False) # causal/race/competitive etc
    distance = Column(Integer, nullable=False) # distance of event in km aprox.
    gps_file_link = Column(Text) # link to gps file 
    
    # Relationship to user profile
    creator = relationship("UserProfile", back_populates="group_events")