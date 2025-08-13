from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from .base import Base


class SRFctAttachment(Base):
    __tablename__ = "sr_fct_attachment"

    id = Column(Integer, unique=True, autoincrement=True)
    appkey = Column(String(20), ForeignKey("sr_fct_header.appkey"), primary_key=True)
    keyid = Column(String(20))
    image = Column(String(255))
    image_tag = Column(String(50))
    active = Column(Boolean)
    table_name = Column(String(255))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    m_created_at = Column(DateTime)
    m_updated_at = Column(DateTime)
    upload_state = Column(Integer)
    uploaded_by = Column(String(255))

    # Relationships
    header = relationship("SRFctHeader", back_populates="attachments")
