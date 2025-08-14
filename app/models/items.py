from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base


class SRFctItems(Base):
    __tablename__ = "sr_fct_items"

    pk_sr_items_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    appkey = Column(
        String(255), ForeignKey("sr_fct_header.appkey"), nullable=False, index=True
    )
    keyid = Column(String(255))
    matnr = Column(String(255))
    fk_sr_action_of_type = Column(Integer, ForeignKey("dim_custom_dropdown.id"))
    discount = Column(DECIMAL(18, 2), nullable=False, default=0.00)
    qty = Column(Integer, nullable=False, default=0)
    srp = Column(DECIMAL(11, 2))
    total_amount = Column(DECIMAL(11, 2))
    net_price = Column(DECIMAL(11, 2))
    net_total_amount = Column(DECIMAL(11, 2))
    fsp_remarks = Column(String(255))
    ssa_remarks = Column(String(255))
    dr_number = Column(String(100))
    dr_date = Column(DateTime)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(
        DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    m_created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    m_updated_at = Column(
        DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    code = Column(String(11))
    nsmemail = Column(String(50))
    gsmemail = Column(String(50))
    fspemail = Column(String(50))
    is_sdo = Column(Integer)

    # Relationships to parent and child tables
    header = relationship("SRFctHeader", back_populates="items")
    log_remarks_items = relationship(
        "SRFctLogSRemarksItems", back_populates="item", cascade="all, delete-orphan"
    )

    # Relationship to dimension table (pointing to dim_custom_dropdown)
    action_type = relationship(
        "DimCustomDropdown",
        foreign_keys=[fk_sr_action_of_type],
        back_populates="items_action_type",
    )
