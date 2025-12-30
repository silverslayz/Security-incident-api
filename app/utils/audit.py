"""
Audit logging utilities for compliance tracking.
"""
from sqlalchemy.orm import Session
from fastapi import Request
from typing import Optional, Dict, Any
from app.models.audit_log import AuditLog
from app.models.user import User


def log_action(
    db: Session,
    user: User,
    action: str,
    resource_type: Optional[str] = None,
    resource_id: Optional[int] = None,
    details: Optional[Dict[str, Any]] = None,
    request: Optional[Request] = None
) -> AuditLog:
    """
    Create an audit log entry.

    Args:
        db: Database session
        user: User performing the action
        action: Action being performed (e.g., "incident.create", "user.login")
        resource_type: Type of resource affected (e.g., "incident", "user")
        resource_id: ID of the affected resource
        details: Additional context as dictionary
        request: FastAPI request object (to extract IP, user agent)

    Returns:
        Created AuditLog object

    Example:
        log_action(
            db,
            current_user,
            action="incident.create",
            resource_type="incident",
            resource_id=new_incident.id,
            details={"severity": "critical", "category": "data_breach"},
            request=request
        )
    """
    # Extract request information if provided
    ip_address = None
    user_agent = None
    if request:
        # Get real IP (handles proxies)
        ip_address = request.headers.get("X-Forwarded-For", request.client.host)
        user_agent = request.headers.get("User-Agent")

    # Create audit log entry
    audit_log = AuditLog(
        user_id=user.id,
        action=action,
        resource_type=resource_type,
        resource_id=resource_id,
        ip_address=ip_address,
        user_agent=user_agent,
        details=details
    )

    db.add(audit_log)
    db.commit()

    return audit_log


# Common audit actions (for consistency)
class AuditAction:
    """Standardized audit action names"""

    # User actions
    USER_LOGIN = "user.login"
    USER_LOGOUT = "user.logout"
    USER_CREATE = "user.create"
    USER_UPDATE = "user.update"
    USER_DELETE = "user.delete"

    # Incident actions
    INCIDENT_CREATE = "incident.create"
    INCIDENT_VIEW = "incident.view"
    INCIDENT_UPDATE = "incident.update"
    INCIDENT_DELETE = "incident.delete"
    INCIDENT_RESOLVE = "incident.resolve"

    # Attachment actions
    ATTACHMENT_UPLOAD = "attachment.upload"
    ATTACHMENT_DOWNLOAD = "attachment.download"
    ATTACHMENT_DELETE = "attachment.delete"
