from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from decimal import Decimal
from .base import TimestampMixin
from .items import ItemResponse, ItemCreate
from .attachments import AttachmentResponse
from .log_remarks import LogRemarksHeaderResponse
from .dimensions import CustomDropdownResponse


class HeaderBase(BaseModel):
    appkey: str = Field(..., description="Unique application key")
    keyid: Optional[str] = None
    kunnr: Optional[str] = Field(None, max_length=10, description="Customer number")
    update_shipcode: Optional[str] = Field(None, max_length=10)
    ship_name: Optional[str] = Field(None, max_length=225)
    ship_to: Optional[str] = Field(None, max_length=225)
    sdo_pao_remarks: Optional[str] = Field(None, max_length=225)
    ssa_remarks: Optional[str] = Field(None, max_length=225)
    approver_remarks: Optional[str] = Field(None, max_length=225)
    return_total: Optional[Decimal] = Field(None, decimal_places=2)
    replacement_total: Optional[Decimal] = Field(None, decimal_places=2)
    nsmemail: Optional[str] = Field(None, max_length=50)
    gsmemail: Optional[str] = Field(None, max_length=50)
    rsmemail: Optional[str] = Field(None, max_length=50)
    fspemail: Optional[str] = Field(None, max_length=50)
    code: Optional[str] = Field(None, max_length=4)
    date_submitted_ssa: Optional[datetime] = None
    date_sent_approval: Optional[datetime] = None
    fsp: Optional[str] = Field(None, max_length=225)
    rsm: Optional[str] = Field(None, max_length=225)
    total_amount: Optional[Decimal] = Field(None, decimal_places=2)
    atpo_number: Optional[int] = None
    wrr_number: Optional[int] = None
    creation_tat: Optional[str] = Field(None, max_length=225)
    approver: Optional[str] = Field(None, max_length=225)
    date_approval: Optional[datetime] = None
    processing_tat: Optional[int] = None
    total_tat: Optional[int] = None
    approval_tat: Optional[int] = None
    remarks_return: Optional[str] = Field(None, max_length=225)
    chanel: Optional[int] = None


class HeaderCreate(HeaderBase, TimestampMixin):
    # Foreign key IDs for creation
    fk_sr_typerequest_id: Optional[int] = None
    fk_sr_reasonofreturn_id: Optional[int] = None
    fk_sr_modeofreturn_id: Optional[int] = None
    fk_status_id: Optional[int] = None

    # Include items for creation
    items: List["ItemCreate"] = []


class HeaderUpdate(BaseModel):
    # Make all fields optional for updates
    keyid: Optional[str] = None
    fk_sr_type_of_request_id: Optional[int] = None
    fk_sr_reason_of_return_id: Optional[int] = None
    fk_sr_mode_of_return_id: Optional[int] = None
    fk_status_id: Optional[int] = None
    kunnr: Optional[str] = None
    update_shipcode: Optional[str] = None
    ship_name: Optional[str] = None
    ship_to: Optional[str] = None
    sdo_pao_remarks: Optional[str] = None
    ssa_remarks: Optional[str] = None
    approver_remarks: Optional[str] = None
    return_total: Optional[Decimal] = None
    replacement_total: Optional[Decimal] = None
    total_amount: Optional[Decimal] = None
    remarks_return: Optional[str] = None


class HeaderResponse(HeaderBase, TimestampMixin):
    sr_id_header: int

    # Foreign key IDs
    fk_sr_type_of_request_id: Optional[int] = None
    fk_sr_reason_of_return_id: Optional[int] = None
    fk_sr_mode_of_return_id: Optional[int] = None
    fk_status_id: Optional[int] = None

    # Related objects (populated via relationships)
    items: List[ItemResponse] = []
    attachments: List[AttachmentResponse] = []
    log_remarks_header: List[LogRemarksHeaderResponse] = []

    # Dimension relationships (optional - populate when needed)
    type_request: Optional[CustomDropdownResponse] = None
    reason_of_return: Optional[CustomDropdownResponse] = None
    mode_of_return: Optional[CustomDropdownResponse] = None
    status: Optional[CustomDropdownResponse] = None

    class Config:
        from_attributes = True
