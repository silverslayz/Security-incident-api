"""
Audit log model for compliance and security tracking.
Logs all important actions for accountability and forensics.
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class AuditLog(Base):
    """
    Audit log for tracking all security-relevant actions.
    Immutable - records are never updated or deleted.
    """
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)

    # Who did it
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    # What they did
    action = Column(String(100), nullable=False, index=True)  # e.g., "incident.create", "user.login"
    resource_type = Column(String(50))  # e.g., "incident", "user"
    resource_id = Column(Integer)       # ID of affected resource

    # Context
    ip_address = Column(String(45))     # Who, from where
    user_agent = Column(String(255))    # Browser/client info
    details = Column(JSON)              # Additional context as JSON

    # When
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    # Relationships
    user = relationship("User", back_populates="audit_logs")

    def __repr__(self):
        return f"<AuditLog(action='{self.action}', user_id={self.user_id})>"
