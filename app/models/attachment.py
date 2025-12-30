"""
Attachment model for incident file uploads (screenshots, logs, etc.)
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, BigInteger
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Attachment(Base):
    """
    File attachments for incidents (stored in S3).
    """
    __tablename__ = "attachments"

    id = Column(Integer, primary_key=True, index=True)
    incident_id = Column(Integer, ForeignKey("incidents.id"), nullable=False)

    # File information
    filename = Column(String, nullable=False)
    file_size = Column(BigInteger)  # in bytes
    content_type = Column(String)   # MIME type (image/png, application/pdf, etc.)

    # S3 storage
    s3_key = Column(String, nullable=False, unique=True)  # S3 object key
    s3_bucket = Column(String, nullable=False)

    # Metadata
    uploaded_by = Column(Integer, ForeignKey("users.id"))
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    incident = relationship("Incident", back_populates="attachments")

    def __repr__(self):
        return f"<Attachment(filename='{self.filename}', incident_id={self.incident_id})>"
