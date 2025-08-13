from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base


class SRFctLogSRemarksItems(Base):
    __tablename__ = "sr_fct_logs_of_remarks_items"

    pk_sr_logsremarkitems_id = Column(
        Integer, primary_key=True, index=True, autoincrement=True
    )
    appkey = Column(
        String(50), ForeignKey("sr_fct_items.appkey"), nullable=False, index=True
    )
    keyid = Column(String(50))
    pk_sr_typeapprstat_id = Column(
        Integer,
        ForeignKey("sr_dim_type_of_approval_status.pk_sr_type_of_approval_status_id"),
    )
    remarks = Column(String(255))
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(
        DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    m_created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    m_updated_at = Column(
        DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    type_remarks = Column(String(255))
    created_by = Column(String(255))

    # Relationships
    item = relationship("SRFctItems", back_populates="log_remarks_items")
    type_approval_status = relationship(
        "SRDimTypeApprstat", back_populates="log_remarks_items"
    )


class SRFctLogSRemarksHeader(Base):
    __tablename__ = "sr_fct_logs_of_remarks_header"

    pk_sr_logs_of_remarks_header_id = Column(
        Integer, primary_key=True, index=True, autoincrement=True
    )
    appkey = Column(
        String(50), ForeignKey("sr_fct_header.appkey"), nullable=False, index=True
    )
    keyid = Column(String(50))
    pk_sr_typeapprstat_id = Column(
        Integer,
        ForeignKey("sr_dim_type_of_approval_status.pk_sr_type_of_approval_status_id"),
    )
    remarks = Column(String(255))
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(
        DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    m_created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    m_updated_at = Column(
        DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    type_remarks = Column(String(255))
    created_by = Column(String(255))

    # Relationships
    header = relationship("SRFctHeader", back_populates="log_remarks_header")
    type_approval_status = relationship(
        "SRDimTypeApprstat", back_populates="log_remarks_header"
    )
