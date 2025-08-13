from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from .base import TimestampMixin


# Custom Dropdown Schemas
class CustomDropdownBase(BaseModel):
    name: str = Field(..., description="Display name for the dropdown option")
    value: Optional[str] = Field(None, description="Value associated with the option")
    order_reason: Optional[str] = Field(
        None, description="Order reason based on PO supplement"
    )
    description: Optional[str] = Field(None, description="Detailed description")
    module: Optional[str] = Field(None, description="Module this dropdown belongs to")
    for_integration: Optional[int] = Field(1, description="1 = include in integration")
    active: Optional[str] = Field("1", description="Active status")
    for_sales_approval: Optional[int] = Field(None, description="Sales approval flag")
    tags: Optional[str] = Field(None, max_length=50)
    category: Optional[str] = Field(None, description="Category classification")
    subcategory: Optional[str] = Field(None, description="Subcategory classification")
    created_by: Optional[str] = None
    updated_by: Optional[str] = None


class CustomDropdownCreate(CustomDropdownBase, TimestampMixin):
    pass


class CustomDropdownResponse(CustomDropdownBase, TimestampMixin):
    id: int

    class Config:
        from_attributes = True


# Type Approval Status Schemas
class TypeApprstatBase(BaseModel):
    description: Optional[str] = None
    isactive: Optional[int] = None
    created_date: Optional[datetime] = None


class TypeApprstatResponse(TypeApprstatBase):
    pk_sr_typeapprstat_id: int

    class Config:
        from_attributes = True


# Color Coding Schemas
class ColorCodingBase(BaseModel):
    colo: Optional[str] = Field(None, max_length=20, description="Color value")
    text1: Optional[str] = Field(None, max_length=20, description="Text color")
    module: Optional[str] = Field(None, max_length=20, description="Module name")


class ColorCodingResponse(ColorCodingBase):
    id: int

    class Config:
        from_attributes = True
