"""
Pydantic schemas for file attachments.
"""
from pydantic import BaseModel
from datetime import datetime


class AttachmentResponse(BaseModel):
    """Schema for attachment data in API responses"""
    id: int
    incident_id: int
    filename: str
    file_size: int
    content_type: str
    uploaded_at: datetime

    class Config:
        from_attributes = True


class AttachmentUpload(BaseModel):
    """Schema for file upload response"""
    id: int
    filename: str
    file_size: int
    s3_key: str
    message: str = "File uploaded successfully"
