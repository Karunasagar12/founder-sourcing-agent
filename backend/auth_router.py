from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from auth_service import AuthService
from auth_dependencies import get_current_active_user
from auth_models import (
    UserCreate, UserLogin, UserResponse, Token, 
    UserUpdate, PasswordReset, PasswordResetConfirm, ForgotPasswordResponse
)
from datetime import timedelta

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/signup", response_model=Token)
async def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    try:
        auth_service = AuthService(db)
        user = auth_service.create_user(user_data)
        
        # Create access token
        access_token = auth_service.create_access_token(
            data={"sub": user.email}
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": UserResponse.from_orm(user)
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/login", response_model=Token)
async def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    """Authenticate user and return access token"""
    auth_service = AuthService(db)
    user = auth_service.authenticate_user(user_credentials.email, user_credentials.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    # Create access token
    access_token = auth_service.create_access_token(
        data={"sub": user.email}
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserResponse.from_orm(user)
    }

@router.post("/logout")
async def logout():
    """Logout user (client should discard token)"""
    return {"message": "Successfully logged out"}

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user = Depends(get_current_active_user)):
    """Get current user information"""
    return UserResponse.from_orm(current_user)

@router.put("/profile", response_model=UserResponse)
async def update_profile(
    user_data: UserUpdate,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update user profile"""
    auth_service = AuthService(db)
    updated_user = auth_service.update_user(current_user.id, user_data)
    
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return UserResponse.from_orm(updated_user)

@router.post("/forgot-password", response_model=ForgotPasswordResponse)
async def forgot_password(reset_data: PasswordReset, db: Session = Depends(get_db)):
    """Request password reset (placeholder - would send email in production)"""
    auth_service = AuthService(db)
    user = auth_service.get_user_by_email(reset_data.email)
    
    if user:
        # In production, this would:
        # 1. Generate a reset token
        # 2. Send email with reset link
        # 3. Store token with expiration
        return {"message": "If an account with this email exists, a password reset link has been sent"}
    
    # Don't reveal if email exists or not (security best practice)
    return {"message": "If an account with this email exists, a password reset link has been sent"}

@router.post("/reset-password")
async def reset_password(reset_data: PasswordResetConfirm, db: Session = Depends(get_db)):
    """Reset password with token (placeholder implementation)"""
    # In production, this would:
    # 1. Verify the reset token
    # 2. Update the user's password
    # 3. Invalidate the token
    
    return {"message": "Password has been reset successfully"}

@router.post("/refresh")
async def refresh_token(current_user = Depends(get_current_active_user), db: Session = Depends(get_db)):
    """Refresh access token"""
    auth_service = AuthService(db)
    
    # Create new access token
    access_token = auth_service.create_access_token(
        data={"sub": current_user.email}
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserResponse.from_orm(current_user)
    }
