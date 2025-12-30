"""
Incident management API endpoints.
Handles CRUD operations for security incidents.
"""
from fastapi import APIRouter, Depends, HTTPException, status, Request, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List, Optional
from datetime import datetime
from app.core.database import get_db
from app.core.dependencies import get_current_user, require_role
from app.models.user import User, UserRole
from app.models.incident import Incident, IncidentStatus
from app.schemas.incident import (
    IncidentCreate,
    IncidentUpdate,
    IncidentResponse,
    IncidentListResponse,
    IncidentStats
)
from app.utils.audit import log_action, AuditAction

router = APIRouter(prefix="/incidents", tags=["Incidents"])


@router.post("/", response_model=IncidentResponse, status_code=status.HTTP_201_CREATED)
def create_incident(
    incident_data: IncidentCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.ANALYST]))
):
    """
    Create a new security incident.

    Requires: Admin or Analyst role

    - **title**: Brief incident title (5-200 chars)
    - **description**: Detailed description
    - **severity**: critical, high, medium, low, info
    - **category**: Type of incident
    """
    # Create incident
    new_incident = Incident(
        title=incident_data.title,
        description=incident_data.description,
        severity=incident_data.severity,
        category=incident_data.category,
        source_ip=incident_data.source_ip,
        affected_systems=incident_data.affected_systems,
        assigned_to=incident_data.assigned_to,
        reporter_id=current_user.id
    )

    db.add(new_incident)
    db.commit()
    db.refresh(new_incident)

    # Log action
    log_action(
        db=db,
        user=current_user,
        action=AuditAction.INCIDENT_CREATE,
        resource_type="incident",
        resource_id=new_incident.id,
        details={
            "severity": new_incident.severity.value,
            "category": new_incident.category.value
        },
        request=request
    )

    return new_incident


@router.get("/", response_model=List[IncidentListResponse])
def list_incidents(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    severity: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    List all incidents with optional filtering.

    Requires: Any authenticated user

    Query parameters:
    - **skip**: Number of records to skip (pagination)
    - **limit**: Max records to return (1-100)
    - **severity**: Filter by severity
    - **status**: Filter by status
    """
    query = db.query(Incident)

    # Apply filters
    if severity:
        query = query.filter(Incident.severity == severity)
    if status:
        query = query.filter(Incident.status == status)

    # Order by created date (newest first) and paginate
    incidents = query.order_by(desc(Incident.created_at)).offset(skip).limit(limit).all()

    return incidents


@router.get("/{incident_id}", response_model=IncidentResponse)
def get_incident(
    incident_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get a specific incident by ID.

    Requires: Any authenticated user
    """
    incident = db.query(Incident).filter(Incident.id == incident_id).first()

    if not incident:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Incident {incident_id} not found"
        )

    # Log view action
    log_action(
        db=db,
        user=current_user,
        action=AuditAction.INCIDENT_VIEW,
        resource_type="incident",
        resource_id=incident_id,
        request=request
    )

    return incident


@router.patch("/{incident_id}", response_model=IncidentResponse)
def update_incident(
    incident_id: int,
    incident_data: IncidentUpdate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.ANALYST]))
):
    """
    Update an existing incident.

    Requires: Admin or Analyst role

    Can update any field. Only provided fields will be updated.
    """
    incident = db.query(Incident).filter(Incident.id == incident_id).first()

    if not incident:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Incident {incident_id} not found"
        )

    # Track what changed for audit log
    changes = {}

    # Update fields if provided
    update_data = incident_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if value is not None:
            old_value = getattr(incident, field)
            setattr(incident, field, value)
            changes[field] = {"old": str(old_value), "new": str(value)}

    # If status changed to resolved, set resolved timestamp
    if incident_data.status == IncidentStatus.RESOLVED and incident.resolved_at is None:
        incident.resolved_at = datetime.utcnow()

    db.commit()
    db.refresh(incident)

    # Log update
    log_action(
        db=db,
        user=current_user,
        action=AuditAction.INCIDENT_UPDATE,
        resource_type="incident",
        resource_id=incident_id,
        details={"changes": changes},
        request=request
    )

    return incident


@router.delete("/{incident_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_incident(
    incident_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN]))
):
    """
    Delete an incident.

    Requires: Admin role only

    Warning: This permanently deletes the incident and all associated data.
    """
    incident = db.query(Incident).filter(Incident.id == incident_id).first()

    if not incident:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Incident {incident_id} not found"
        )

    # Log deletion before deleting
    log_action(
        db=db,
        user=current_user,
        action=AuditAction.INCIDENT_DELETE,
        resource_type="incident",
        resource_id=incident_id,
        details={"title": incident.title, "severity": incident.severity.value},
        request=request
    )

    db.delete(incident)
    db.commit()

    return None


@router.get("/stats/summary", response_model=IncidentStats)
def get_incident_statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get incident statistics and analytics.

    Requires: Any authenticated user

    Returns counts by status, severity, and category plus avg resolution time.
    """
    # Total counts
    total = db.query(Incident).count()
    open_count = db.query(Incident).filter(Incident.status == IncidentStatus.OPEN).count()
    in_progress = db.query(Incident).filter(Incident.status == IncidentStatus.IN_PROGRESS).count()
    resolved = db.query(Incident).filter(Incident.status == IncidentStatus.RESOLVED).count()
    closed = db.query(Incident).filter(Incident.status == IncidentStatus.CLOSED).count()

    # Severity counts
    from app.models.incident import IncidentSeverity
    critical = db.query(Incident).filter(Incident.severity == IncidentSeverity.CRITICAL).count()
    high = db.query(Incident).filter(Incident.severity == IncidentSeverity.HIGH).count()

    # By category
    category_counts = {}
    from app.models.incident import IncidentCategory
    for category in IncidentCategory:
        count = db.query(Incident).filter(Incident.category == category).count()
        category_counts[category.value] = count

    # Average resolution time (in hours)
    avg_resolution = None
    resolved_incidents = db.query(Incident).filter(
        Incident.resolved_at.isnot(None)
    ).all()

    if resolved_incidents:
        total_hours = 0
        for inc in resolved_incidents:
            delta = inc.resolved_at - inc.created_at
            total_hours += delta.total_seconds() / 3600
        avg_resolution = total_hours / len(resolved_incidents)

    return IncidentStats(
        total_incidents=total,
        open_incidents=open_count,
        in_progress_incidents=in_progress,
        resolved_incidents=resolved,
        closed_incidents=closed,
        critical_incidents=critical,
        high_incidents=high,
        incidents_by_category=category_counts,
        avg_resolution_time_hours=round(avg_resolution, 2) if avg_resolution else None
    )
