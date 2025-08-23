from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from database import get_db
from auth_service import AuthService
from auth_models import TokenData

# Security scheme
security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Get current authenticated user from JWT token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Verify token
        auth_service = AuthService(db)
        email = auth_service.verify_token(credentials.credentials)
        if email is None:
            raise credentials_exception
        
        # Get user from database
        user = auth_service.get_user_by_email(email)
        if user is None:
            raise credentials_exception
        
        return user
    except Exception:
        raise credentials_exception

def get_current_active_user(current_user = Depends(get_current_user)):
    """Get current active user (not disabled)"""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

def get_current_verified_user(current_user = Depends(get_current_active_user)):
    """Get current verified user"""
    if not current_user.is_verified:
        raise HTTPException(status_code=400, detail="User not verified")
    return current_user
