from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from decimal import Decimal

class GroupEventBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, description="Name of the event")
    sport_type: str = Field(..., description="Type of event (ride/run etc)")
    start_at: datetime = Field(..., description="Start time of the event")
    lat: Optional[Decimal] = Field(None, description="Latitude of event location")
    lng: Optional[Decimal] = Field(None, description="Longitude of event location")
    access: str = Field(..., description="Access level: public/private/invite_only")
    event_type: str = Field(..., description="Event type: casual/race/competitive etc")
    distance: int = Field(..., ge=0, description="Distance of event in km")
    gps_file_link: Optional[str] = Field(None, description="Link to GPS file")

class GroupEventCreate(GroupEventBase):
    pass

class GroupEventUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    sport_type: Optional[str] = None
    start_at: Optional[datetime] = None
    lat: Optional[Decimal] = None
    lng: Optional[Decimal] = None
    access: Optional[str] = None
    event_type: Optional[str] = None
    distance: Optional[int] = Field(None, ge=0)
    gps_file_link: Optional[str] = None

class GroupEventResponse(GroupEventBase):
    id: int
    created_at: datetime
    updated_at: datetime
    created_by: str

    class Config:
        from_attributes = True
