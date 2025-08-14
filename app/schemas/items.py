from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from decimal import Decimal
from .base import TimestampMixin
from .dimensions import CustomDropdownResponse

# from .header import LogRemarksItemsResponse


class ItemBase(BaseModel):
    appkey: str = Field(..., description="Reference to header appkey")
    keyid: Optional[str] = None
    matnr: Optional[str] = Field(None, description="Material number")
    discount: Decimal = Field(default=Decimal("0.00"), decimal_places=2)
    qty: int = Field(default=0, description="Quantity")
    srp: Optional[Decimal] = Field(
        None, decimal_places=2, description="Suggested retail price"
    )
    total_amount: Optional[Decimal] = Field(None, decimal_places=2)
    net_price: Optional[Decimal] = Field(None, decimal_places=2)
    net_total_amount: Optional[Decimal] = Field(None, decimal_places=2)
    fsp_remarks: Optional[str] = Field(None, max_length=255)
    ssa_remarks: Optional[str] = Field(None, max_length=255)
    dr_number: Optional[str] = Field(
        None, max_length=100, description="Delivery receipt number"
    )
    dr_date: Optional[datetime] = None
    code: Optional[str] = Field(None, max_length=11)
    nsmemail: Optional[str] = Field(None, max_length=50)
    gsmemail: Optional[str] = Field(None, max_length=50)
    fspemail: Optional[str] = Field(None, max_length=50)
    is_sdo: Optional[int] = None


class ItemCreate(ItemBase, TimestampMixin):
    # Foreign key for creation
    fk_sr_action_of_type: Optional[int] = None


class ItemUpdate(BaseModel):
    # Make all fields optional for updates
    keyid: Optional[str] = None
    matnr: Optional[str] = None
    fk_sr_action_of_type: Optional[int] = None
    discount: Optional[Decimal] = None
    qty: Optional[int] = None
    srp: Optional[Decimal] = None
    total_amount: Optional[Decimal] = None
    net_price: Optional[Decimal] = None
    net_total_amount: Optional[Decimal] = None
    fsp_remarks: Optional[str] = None
    ssa_remarks: Optional[str] = None
    dr_number: Optional[str] = None
    dr_date: Optional[datetime] = None


class ItemResponse(ItemBase, TimestampMixin):
    pk_sr_items_id: int
    fk_sr_action_of_type: Optional[int] = None

    # Related objects
    log_remarks_items: List["LogRemarksItemsResponse"] = []

    # Dimension relationship
    action_type: Optional[CustomDropdownResponse] = None

    class Config:
        from_attributes = True
