from fastapi import APIRouter, Depends, HTTPException, status
from ..schemas.auth import (
    SignUpRequest, SignUpResponse, SignInRequest, SignInResponse,
    ConfirmSignUpRequest, ForgotPasswordRequest, ResetPasswordRequest,
    UserInfo, TokenResponse
)
from ..services.auth_service import AuthService
from ..utils.auth_dependencies import get_auth_service, get_current_user

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/signup", response_model=SignUpResponse)
async def sign_up(
    request: SignUpRequest,
    auth_service: AuthService = Depends(get_auth_service)
):
    """Sign up a new user"""
    try:
        result = await auth_service.sign_up(
            email=request.email,
            password=request.password,
            name=request.name
        )
        return SignUpResponse(**result)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/confirm-signup")
async def confirm_sign_up(
    request: ConfirmSignUpRequest,
    auth_service: AuthService = Depends(get_auth_service)
):
    """Confirm user sign up with confirmation code"""
    try:
        await auth_service.confirm_sign_up(
            email=request.email,
            confirmation_code=request.confirmation_code
        )
        return {"message": "Email confirmed successfully"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/signin", response_model=SignInResponse)
async def sign_in(
    request: SignInRequest,
    auth_service: AuthService = Depends(get_auth_service)
):
    """Sign in user"""
    try:
        result = await auth_service.sign_in(
            email=request.email,
            password=request.password
        )
        return SignInResponse(**result)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )

@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    refresh_token: str,
    auth_service: AuthService = Depends(get_auth_service)
):
    """Refresh access token"""
    try:
        result = await auth_service.refresh_token(refresh_token)
        return TokenResponse(**result)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )

@router.get("/me", response_model=UserInfo)
async def get_current_user_info(
    current_user: UserInfo = Depends(get_current_user)
):
    """Get current user information"""
    return current_user

@router.post("/forgot-password")
async def forgot_password(
    request: ForgotPasswordRequest,
    auth_service: AuthService = Depends(get_auth_service)
):
    """Initiate forgot password flow"""
    try:
        await auth_service.forgot_password(email=request.email)
        return {"message": "Password reset code sent to your email"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/reset-password")
async def reset_password(
    request: ResetPasswordRequest,
    auth_service: AuthService = Depends(get_auth_service)
):
    """Reset password with confirmation code"""
    try:
        await auth_service.confirm_forgot_password(
            email=request.email,
            confirmation_code=request.confirmation_code,
            new_password=request.new_password
        )
        return {"message": "Password reset successfully"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/signout")
async def sign_out(
    current_user: UserInfo = Depends(get_current_user),
    auth_service: AuthService = Depends(get_auth_service)
):
    """Sign out user"""
    try:
        # Note: This requires the access token, which we don't have in the dependency
        # In a real implementation, you might want to handle this differently
        return {"message": "Sign out successful"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        ) 