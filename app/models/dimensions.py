from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base


class SRDimTypeApprstat(Base):
    __tablename__ = "sr_dim_typeapprstat"

    pk_sr_typeapprstat_id = Column(
        Integer, primary_key=True, index=True, autoincrement=True
    )
    isactive = Column(Integer)
    created_date = Column(DateTime)
    description = Column(String(255))

    # Relationships
    log_remarks_items = relationship(
        "SRFctLogSRemarksItems", back_populates="type_approval_status"
    )
    log_remarks_header = relationship(
        "SRFctLogSRemarksHeader", back_populates="type_approval_status"
    )


class DimCustomDropdown(Base):
    __tablename__ = "dim_custom_dropdown"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    value = Column(String(255))
    order_reason = Column(String(100))  # order reason based on po supplement
    description = Column(String(255))
    module = Column(String(255))
    for_integration = Column(Integer, default=1)  # 1 = include integration
    active = Column(String(255), default="1")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime)
    for_sales_approval = Column(Integer)
    tags = Column(String(50))
    category = Column(String(255))
    subcategory = Column(String(255))
    created_by = Column(String(255))
    updated_by = Column(String(255))

    # Relationships to headers (different foreign keys reference this table)
    headers_type_request = relationship(
        "SRFctHeader",
        foreign_keys="SRFctHeader.fk_sr_type_of_request_id",
        back_populates="type_request",
    )
    headers_reason_return = relationship(
        "SRFctHeader",
        foreign_keys="SRFctHeader.fk_sr_reason_of_return_id",
        back_populates="reason_of_return",
    )
    headers_mode_return = relationship(
        "SRFctHeader",
        foreign_keys="SRFctHeader.fk_sr_mode_of_return_id",
        back_populates="mode_of_return",
    )
    headers_status = relationship(
        "SRFctHeader", foreign_keys="SRFctHeader.fk_status_id", back_populates="status"
    )

    # Relationship to items
    items_action_type = relationship(
        "SRFctItems",
        foreign_keys="SRFctItems.fk_sr_actiontype",
        back_populates="action_type",
    )


class DimColorCoding(Base):
    __tablename__ = "dim_color_coding"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    colo = Column(String(20))  # Note: seems like a typo in your DB, should be 'color'
    text1 = Column(String(20))
    module = Column(String(20))
