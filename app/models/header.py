from sqlalchemy import Column, String, Integer, DateTime, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base


class SRFctHeader(Base):
    __tablename__ = "sr_fct_header"

    sr_id_header = Column(Integer, primary_key=True, index=True, autoincrement=True)
    appkey = Column(String(255), nullable=False, unique=True, index=True)
    keyid = Column(String(255))
    fk_sr_type_of_request_id = Column(Integer, ForeignKey("dim_custom_dropdown.id"))
    fk_sr_reason_of_return_id = Column(Integer, ForeignKey("dim_custom_dropdown.id"))
    fk_sr_mode_of_return_id = Column(Integer, ForeignKey("dim_custom_dropdown.id"))
    fk_status_id = Column(Integer, ForeignKey("dim_custom_dropdown.id"))
    kunnr = Column(String(10))
    update_shipcode = Column(String(10))
    ship_name = Column(String(225))
    ship_to = Column(String(225))
    sdo_pao_remarks = Column(String(225))
    ssa_remarks = Column(String(225))
    approver_remarks = Column(String(225))
    return_total = Column(DECIMAL(18, 2))
    replacement_total = Column(DECIMAL(18, 2))
    nsmemail = Column(String(50))
    gsmemail = Column(String(50))
    rsmemail = Column(String(50))
    fspemail = Column(String(50))
    code = Column(String(4))
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    m_created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    m_updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    date_submitted_ssa = Column(DateTime)
    date_sent_approval = Column(DateTime)
    fsp = Column(String(225))
    rsm = Column(String(225))
    total_amount = Column(DECIMAL(18, 2))
    atpo_number = Column(Integer)
    wrr_number = Column(Integer)
    creation_tat = Column(String(225))
    approver = Column(String(225))
    date_approval = Column(DateTime)
    processing_tat = Column(Integer)
    total_tat = Column(Integer)
    approval_tat = Column(Integer)
    remarks_return = Column(String(225))
    channel = Column(Integer)

    # Relationships to child tables
    items = relationship(
        "SRFctItems", back_populates="header", cascade="all, delete-orphan"
    )
    attachments = relationship(
        "SRFctAttachment", back_populates="header", cascade="all, delete-orphan"
    )
    log_remarks_header = relationship(
        "SRFctLogSRemarksHeader", back_populates="header", cascade="all, delete-orphan"
    )

    # Relationships to dimension tables
    type_request = relationship(
        "DimCustomDropdown",
        foreign_keys=[fk_sr_type_of_request_id],
        back_populates="headers_type_request",
    )
    reason_of_return = relationship(
        "DimCustomDropdown",
        foreign_keys=[fk_sr_reason_of_return_id],
        back_populates="headers_reason_return",
    )
    mode_of_return = relationship(
        "DimCustomDropdown",
        foreign_keys=[fk_sr_mode_of_return_id],
        back_populates="headers_mode_return",
    )
    status = relationship(
        "DimCustomDropdown",
        foreign_keys=[fk_status_id],
        back_populates="headers_status",
    )
