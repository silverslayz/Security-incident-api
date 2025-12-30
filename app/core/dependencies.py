"""
FastAPI dependencies for authentication and authorization.
These functions are used to protect API endpoints.
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.security import decode_access_token
from app.models.user import User, UserRole
from app.schemas.user import TokenData

# HTTP Bearer token scheme (Authorization: Bearer <token>)
security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Get the current authenticated user from JWT token.

    Usage:
        @app.get("/protected")
        def protected_route(current_user: User = Depends(get_current_user)):
            return {"user": current_user.username}

    Raises:
        HTTPException: If token is invalid or user not found
    """
    token = credentials.credentials

    # Decode the token
    token_data: TokenData = decode_access_token(token)
    if token_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Get user from database
    user = db.query(User).filter(User.id == token_data.user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    # Check if user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )

    return user


def require_role(allowed_roles: List[UserRole]):
    """
    Dependency factory for role-based access control (RBAC).

    Usage:
        # Only admins can access
        @app.delete("/users/{user_id}")
        def delete_user(
            user_id: int,
            current_user: User = Depends(require_role([UserRole.ADMIN]))
        ):
            pass

        # Admins and analysts can access
        @app.post("/incidents")
        def create_incident(
            incident: IncidentCreate,
            current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.ANALYST]))
        ):
            pass

    Args:
        allowed_roles: List of roles that can access the endpoint

    Returns:
        Dependency function that checks user role
    """
    def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required roles: {[role.value for role in allowed_roles]}"
            )
        return current_user

    return role_checker
