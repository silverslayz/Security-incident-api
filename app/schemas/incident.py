"""
Pydantic schemas for Incident data validation and serialization.
"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from app.models.incident import IncidentSeverity, IncidentStatus, IncidentCategory


# Base schema
class IncidentBase(BaseModel):
    """Base incident schema"""
    title: str = Field(..., min_length=5, max_length=200)
    description: str = Field(..., min_length=10)
    severity: IncidentSeverity
    category: IncidentCategory
    source_ip: Optional[str] = None
    affected_systems: Optional[str] = None


# Schema for creating incidents
class IncidentCreate(IncidentBase):
    """Schema for creating a new incident"""
    assigned_to: Optional[str] = None


# Schema for updating incidents
class IncidentUpdate(BaseModel):
    """Schema for updating an incident"""
    title: Optional[str] = Field(None, min_length=5, max_length=200)
    description: Optional[str] = Field(None, min_length=10)
    severity: Optional[IncidentSeverity] = None
    status: Optional[IncidentStatus] = None
    category: Optional[IncidentCategory] = None
    assigned_to: Optional[str] = None
    source_ip: Optional[str] = None
    affected_systems: Optional[str] = None
    resolution_notes: Optional[str] = None


# Schema for incident responses
class IncidentResponse(IncidentBase):
    """Schema for incident data in API responses"""
    id: int
    status: IncidentStatus
    reporter_id: int
    assigned_to: Optional[str] = None
    resolution_notes: Optional[str] = None
    resolved_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Schema for incident list (lighter version)
class IncidentListResponse(BaseModel):
    """Lighter schema for incident lists"""
    id: int
    title: str
    severity: IncidentSeverity
    status: IncidentStatus
    category: IncidentCategory
    reporter_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Schema for incident statistics (for analytics)
class IncidentStats(BaseModel):
    """Statistics for incident analytics"""
    total_incidents: int
    open_incidents: int
    in_progress_incidents: int
    resolved_incidents: int
    closed_incidents: int
    critical_incidents: int
    high_incidents: int
    incidents_by_category: dict
    avg_resolution_time_hours: Optional[float] = None
