"""
Pydantic schemas for User data validation and serialization.
Schemas define the shape of data in requests and responses.
"""
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional
from app.models.user import UserRole


# Base schema with common fields
class UserBase(BaseModel):
    """Base user schema with common fields"""
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    full_name: Optional[str] = None


# Schema for user creation (includes password)
class UserCreate(UserBase):
    """Schema for creating a new user"""
    password: str = Field(..., min_length=8, max_length=100)
    role: UserRole = UserRole.VIEWER


# Schema for user updates
class UserUpdate(BaseModel):
    """Schema for updating user information"""
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None


# Schema for user responses (what API returns)
class UserResponse(UserBase):
    """Schema for user data in API responses"""
    id: int
    role: UserRole
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        """Pydantic config - allows reading from ORM models"""
        from_attributes = True


# Schema for user login
class UserLogin(BaseModel):
    """Schema for user login request"""
    username: str
    password: str


# Schema for authentication tokens
class Token(BaseModel):
    """JWT token response"""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Data stored in JWT token"""
    user_id: int
    username: str
    role: UserRole
