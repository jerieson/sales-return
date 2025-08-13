from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class TimestampMixin(BaseModel):
    """Common timestamp fields used across multiple models"""

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    m_created_at: Optional[datetime] = None
    m_updated_at: Optional[datetime] = None
