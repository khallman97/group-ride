from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from ..database import get_db
from ..schemas.user import (
    UserProfileResponse, UserProfileUpdate, UserPreferencesResponse, 
    UserPreferencesUpdate, UserProfileWithPreferences, OnboardingRequest,
    UserProfileSimpleResponse, UserPreferencesSimpleResponse, UserProfileWithPreferencesSimple
)
from ..schemas.auth import UserInfo
from ..services.user_service import UserService
from ..utils.auth_dependencies import get_current_user

router = APIRouter(prefix="/users", tags=["users"])

def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(db)

@router.get("/profile", response_model=UserProfileSimpleResponse)
async def get_user_profile(
    current_user: UserInfo = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service)
):
    """Get current user's profile"""
    profile = user_service.get_user_profile_by_user_id(current_user.user_id)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User profile not found"
        )
    return profile

@router.put("/profile", response_model=UserProfileSimpleResponse)
async def update_user_profile(
    profile_update: UserProfileUpdate,
    current_user: UserInfo = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service)
):
    """Update current user's profile"""
    profile = user_service.update_user_profile(current_user.user_id, profile_update)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User profile not found"
        )
    return profile

@router.get("/preferences", response_model=UserPreferencesSimpleResponse)
async def get_user_preferences(
    current_user: UserInfo = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service)
):
    """Get current user's preferences"""
    preferences = user_service.get_user_preferences_by_user_id(current_user.user_id)
    if not preferences:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User preferences not found"
        )
    return preferences

@router.put("/preferences", response_model=UserPreferencesSimpleResponse)
async def update_user_preferences(
    preferences_update: UserPreferencesUpdate,
    current_user: UserInfo = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service)
):
    """Update current user's preferences"""
    preferences = user_service.create_user_preferences(current_user.user_id, preferences_update)
    if not preferences:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User profile not found"
        )
    return preferences

@router.get("/me", response_model=UserProfileWithPreferencesSimple)
async def get_user_with_preferences(
    current_user: UserInfo = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service)
):
    """Get current user's profile with preferences"""
    user_data = user_service.get_user_with_preferences(current_user.user_id)
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User profile not found"
        )
    return user_data

@router.post("/onboarding")
async def complete_onboarding(
    onboarding_data: OnboardingRequest,
    current_user: UserInfo = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service)
):
    """Complete user onboarding with profile and preferences"""
   
    try:
        result = user_service.complete_onboarding(
            current_user.user_id,
            onboarding_data.profile,
            onboarding_data.preferences
        )
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/profile/auto-create")
async def auto_create_profile(
    current_user: UserInfo = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service)
):
    """Automatically create user profile after first login"""
    try:
        profile = user_service.create_user_profile(current_user)
        return {
            "message": "Profile created successfully",
            "profile": profile
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create profile: {str(e)}"
        ) 