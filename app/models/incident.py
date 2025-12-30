"""
Incident model for tracking security incidents.
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Enum as SQLEnum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum


class IncidentSeverity(str, enum.Enum):
    """
    Incident severity levels based on military/security operations.
    """
    CRITICAL = "critical"    # Immediate threat, requires instant response
    HIGH = "high"           # Serious threat, response within 1 hour
    MEDIUM = "medium"       # Moderate threat, response within 4 hours
    LOW = "low"            # Minor issue, response within 24 hours
    INFO = "info"          # Informational only


class IncidentStatus(str, enum.Enum):
    """
    Incident lifecycle status.
    """
    OPEN = "open"                    # Newly created
    IN_PROGRESS = "in_progress"      # Being investigated
    RESOLVED = "resolved"            # Issue fixed
    CLOSED = "closed"                # Completed and reviewed


class IncidentCategory(str, enum.Enum):
    """
    Types of security incidents.
    """
    UNAUTHORIZED_ACCESS = "unauthorized_access"
    DATA_BREACH = "data_breach"
    MALWARE = "malware"
    PHISHING = "phishing"
    DOS_ATTACK = "dos_attack"
    POLICY_VIOLATION = "policy_violation"
    PHYSICAL_SECURITY = "physical_security"
    OTHER = "other"


class Incident(Base):
    """
    Security incident tracking model.
    """
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, index=True)
    description = Column(Text, nullable=False)

    # Classification
    severity = Column(SQLEnum(IncidentSeverity), nullable=False, index=True)
    status = Column(SQLEnum(IncidentStatus), default=IncidentStatus.OPEN, index=True)
    category = Column(SQLEnum(IncidentCategory), nullable=False)

    # Assignment
    reporter_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    assigned_to = Column(String)  # Can be user or team name

    # Location/Source
    source_ip = Column(String(45))  # Supports IPv6
    affected_systems = Column(Text)  # Comma-separated or JSON

    # Resolution
    resolution_notes = Column(Text)
    resolved_at = Column(DateTime(timezone=True))

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    reporter = relationship("User", back_populates="incidents")
    attachments = relationship("Attachment", back_populates="incident", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Incident(id={self.id}, title='{self.title}', severity='{self.severity}')>"
