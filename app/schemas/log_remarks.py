from pydantic import BaseModel, Field
from typing import Optional
from .base import TimestampMixin
from .dimensions import TypeApprstatResponse

# from typing import TYPE_CHECKING
# from .items import ItemResponse


class LogRemarksItemsBase(BaseModel):
    appkey: str = Field(..., max_length=50)
    keyid: Optional[str] = Field(None, max_length=50)
    remarks: Optional[str] = Field(None, max_length=255)
    type_remarks: Optional[str] = Field(None, max_length=255)
    created_by: Optional[str] = None


class LogRemarksItemsCreate(LogRemarksItemsBase, TimestampMixin):
    pk_sr_type_of_approval_status_id: Optional[int] = None


class LogRemarksItemsResponse(LogRemarksItemsBase, TimestampMixin):
    pk_sr_logs_of_remarks_items_id: int
    pk_sr_type_of_approval_status_id: Optional[int] = None

    # Related object
    type_approval_status: Optional[TypeApprstatResponse] = None

    class Config:
        from_attributes = True


class LogRemarksHeaderBase(BaseModel):
    appkey: str = Field(..., max_length=50)
    keyid: Optional[str] = Field(None, max_length=50)
    remarks: Optional[str] = Field(None, max_length=255)
    type_remarks: Optional[str] = Field(None, max_length=255)
    created_by: Optional[str] = None


class LogRemarksHeaderCreate(LogRemarksHeaderBase, TimestampMixin):
    pk_sr_type_of_approval_status_id: Optional[int] = None


class LogRemarksHeaderResponse(LogRemarksHeaderBase, TimestampMixin):
    pk_sr_logs_of_remarks_header_id: int
    pk_sr_type_of_approval_status_id: Optional[int] = None

    # Related object
    type_approval_status: Optional[TypeApprstatResponse] = None

    class Config:
        from_attributes = True


# if TYPE_CHECKING:
#     from .header import HeaderCreate

#     # from .items import ItemCreate
#     # from .log_remarks import LogRemarksItemsResponse

# # Update forward references
# # HeaderCreate.model_rebuild()
# # ItemResponse.model_rebuild()
