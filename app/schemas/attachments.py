from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class AttachmentBase(BaseModel):
    appkey: str = Field(..., max_length=20, description="Reference to header appkey")
    keyid: Optional[str] = Field(None, max_length=20)
    image: Optional[str] = Field(
        None, max_length=255, description="Image file path/URL"
    )
    image_tag: Optional[str] = Field(None, max_length=50)
    active: Optional[bool] = None
    table_name: Optional[str] = Field(None, max_length=255)
    upload_state: Optional[int] = None
    uploaded_by: Optional[str] = Field(None, max_length=255)


class AttachmentCreate(AttachmentBase):
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    m_created_at: Optional[datetime] = None
    m_updated_at: Optional[datetime] = None


class AttachmentResponse(AttachmentBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    m_created_at: Optional[datetime] = None
    m_updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
