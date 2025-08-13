from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class ItemBase(BaseModel):
    product_name: str
    product_code: Optional[str] = None
    quantity: int
    unit_price: float
    total_price: float


class ItemCreate(ItemBase):
    pass


class ItemResponse(ItemBase):
    id: int
    key_id: str

    class Config:
        from_attributes = True  # Updated for Pydantic v2


class HeaderBase(BaseModel):
    customer_name: str
    customer_email: Optional[str] = None
    customer_phone: Optional[str] = None
    status: Optional[str] = "pending"
    total_amount: Optional[float] = 0.0


class HeaderCreate(HeaderBase):
    appkey: str
    items: List[ItemCreate] = []


class HeaderResponse(HeaderBase):
    appkey: str
    order_date: datetime
    items: List[ItemResponse] = []

    class Config:
        from_attributes = True  # Updated for Pydantic v2
