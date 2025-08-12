from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from ..services.auth_service import AuthService
from ..schemas.auth import UserInfo

security = HTTPBearer()

async def get_auth_service() -> AuthService:
    """Dependency to get auth service instance"""
    return AuthService()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    auth_service: AuthService = Depends(get_auth_service)
) -> UserInfo:
    """Dependency to get current authenticated user"""
    try:
        token = credentials.credentials
        user_info = await auth_service.get_user_info(token)
        return user_info
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed",
            headers={"WWW-Authenticate": "Bearer"},
        )

async def get_optional_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    auth_service: AuthService = Depends(get_auth_service)
) -> Optional[UserInfo]:
    """Dependency to get current user (optional - doesn't fail if no token)"""
    if not credentials:
        return None
    
    try:
        token = credentials.credentials
        user_info = await auth_service.get_user_info(token)
        return user_info
    except (ValueError, Exception):
        return None 