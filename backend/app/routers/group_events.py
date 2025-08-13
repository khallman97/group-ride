from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..schemas.group_events import GroupEventCreate, GroupEventResponse
from ..services.group_event_service import GroupEventService
from ..utils.auth_dependencies import get_current_user
from ..schemas.auth import UserInfo

router = APIRouter(prefix="/group_events", tags=["group_events"])

def get_group_event_service(db: Session = Depends(get_db)) -> GroupEventService:
    return GroupEventService(db)

@router.post("/", response_model=GroupEventResponse)
async def create_group_event(
    group_event_data: GroupEventCreate,
    current_user: UserInfo = Depends(get_current_user),
    group_event_service: GroupEventService = Depends(get_group_event_service)
):
    """Create a new group event"""
    try:
        group_event = group_event_service.create_group_event(
            group_event_data, 
            current_user.user_id
        )
        return group_event
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create group event: {str(e)}"
        )

@router.get("/", response_model=List[GroupEventResponse])
async def get_all_group_events(
    group_event_service: GroupEventService = Depends(get_group_event_service)
):
    """Get all group events"""
    try:
        group_events = group_event_service.get_all_group_events()
        return group_events
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve group events: {str(e)}"
        )

@router.get("/{event_id}", response_model=GroupEventResponse)
async def get_group_event(
    event_id: int,
    group_event_service: GroupEventService = Depends(get_group_event_service)
):
    """Get a single group event by ID"""
    try:
        group_event = group_event_service.get_group_event_by_id(event_id)
        if not group_event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Group event not found"
            )
        return group_event
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve group event: {str(e)}"
        )