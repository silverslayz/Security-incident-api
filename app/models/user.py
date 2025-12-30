"""
User model for authentication and authorization.
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum


class UserRole(str, enum.Enum):
    """
    User roles for RBAC (Role-Based Access Control).
    Based on typical security operations structure.
    """
    ADMIN = "admin"          # Full access, user management
    ANALYST = "analyst"      # Create/update incidents, view all
    VIEWER = "viewer"        # Read-only access


class User(Base):
    """
    User model with role-based access control.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)

    # Role-based access control
    role = Column(SQLEnum(UserRole), default=UserRole.VIEWER, nullable=False)
    is_active = Column(Boolean, default=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    incidents = relationship("Incident", back_populates="reporter")
    audit_logs = relationship("AuditLog", back_populates="user")

    def __repr__(self):
        return f"<User(username='{self.username}', role='{self.role}')>"
