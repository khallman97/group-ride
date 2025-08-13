from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional
from ..models.group_events import GroupEvent
from ..schemas.group_events import GroupEventCreate, GroupEventUpdate

class GroupEventService:
    def __init__(self, db: Session):
        self.db = db

    def create_group_event(self, group_event_data: GroupEventCreate, created_by: str) -> GroupEvent:
        """Create a new group event"""
        db_group_event = GroupEvent(
            name=group_event_data.name,
            sport_type=group_event_data.sport_type,
            start_at=group_event_data.start_at,
            lat=group_event_data.lat,
            lng=group_event_data.lng,
            access=group_event_data.access,
            event_type=group_event_data.event_type,
            distance=group_event_data.distance,
            gps_file_link=group_event_data.gps_file_link,
            created_by=created_by
        )
        
        self.db.add(db_group_event)
        self.db.commit()
        self.db.refresh(db_group_event)
        return db_group_event

    def get_all_group_events(self) -> List[GroupEvent]:
        """Get all group events ordered by creation date"""
        return self.db.query(GroupEvent).order_by(desc(GroupEvent.created_at)).all()

    def get_group_event_by_id(self, event_id: int) -> Optional[GroupEvent]:
        """Get a single group event by ID"""
        return self.db.query(GroupEvent).filter(GroupEvent.id == event_id).first()

    def update_group_event(self, event_id: int, group_event_data: GroupEventUpdate, user_id: str) -> Optional[GroupEvent]:
        """Update a group event (only by creator)"""
        db_group_event = self.get_group_event_by_id(event_id)
        if not db_group_event:
            return None
        
        # Check if user is the creator
        if db_group_event.created_by != user_id:
            return None
        
        update_data = group_event_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_group_event, field, value)
        
        self.db.commit()
        self.db.refresh(db_group_event)
        return db_group_event

    def delete_group_event(self, event_id: int, user_id: str) -> bool:
        """Delete a group event (only by creator)"""
        db_group_event = self.get_group_event_by_id(event_id)
        if not db_group_event:
            return False
        
        # Check if user is the creator
        if db_group_event.created_by != user_id:
            return False
        
        self.db.delete(db_group_event)
        self.db.commit()
        return True
