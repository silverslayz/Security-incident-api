"""
Pydantic schemas for audit logs.
"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Any


class AuditLogResponse(BaseModel):
    """Schema for audit log data in API responses"""
    id: int
    user_id: int
    action: str
    resource_type: Optional[str] = None
    resource_id: Optional[int] = None
    ip_address: Optional[str] = None
    timestamp: datetime
    details: Optional[Any] = None

    class Config:
        from_attributes = True
