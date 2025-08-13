from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.order_models import Header, Item
from app.schemas.order_schemas import (
    HeaderResponse,
    HeaderCreate,
    ItemResponse,
    HeaderBase,
)

router = APIRouter(prefix="/orders", tags=["orders"])


@router.get("/{appkey}", response_model=HeaderResponse)
def get_order_by_appkey(appkey: str, db: Session = Depends(get_db)):
    """Get order details by appkey including all items"""
    header = db.query(Header).filter(Header.appkey == appkey).first()
    if not header:
        raise HTTPException(
            status_code=404, detail=f"Order with appkey '{appkey}' not found"
        )
    return header


@router.get("/{appkey}/items", response_model=List[ItemResponse])
def get_order_items(appkey: str, db: Session = Depends(get_db)):
    """Get only the items for a specific order"""
    header = db.query(Header).filter(Header.appkey == appkey).first()
    if not header:
        raise HTTPException(
            status_code=404, detail=f"Order with appkey '{appkey}' not found"
        )

    items = db.query(Item).filter(Item.key_id == appkey).all()
    return items


@router.get("/", response_model=List[HeaderResponse])
def get_all_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all orders with pagination"""
    headers = db.query(Header).offset(skip).limit(limit).all()
    return headers


@router.post("/", response_model=HeaderResponse)
def create_order(order: HeaderCreate, db: Session = Depends(get_db)):
    """Create a new order with items"""
    # Check if appkey already exists
    existing = db.query(Header).filter(Header.appkey == order.appkey).first()
    if existing:
        raise HTTPException(
            status_code=400, detail=f"Order with appkey '{order.appkey}' already exists"
        )

    # Create header
    db_header = Header(**order.model_dump(exclude={"items"}))
    db.add(db_header)
    db.flush()  # Flush to get the appkey available for items

    # Create items
    for item_data in order.items:
        db_item = Item(**item_data.model_dump(), key_id=order.appkey)
        db.add(db_item)

    db.commit()
    db.refresh(db_header)
    return db_header


@router.put("/{appkey}", response_model=HeaderResponse)
def update_order(appkey: str, order: HeaderBase, db: Session = Depends(get_db)):
    """Update order header information"""
    header = db.query(Header).filter(Header.appkey == appkey).first()
    if not header:
        raise HTTPException(
            status_code=404, detail=f"Order with appkey '{appkey}' not found"
        )

    # Update fields
    for field, value in order.model_dump().items():
        setattr(header, field, value)

    db.commit()
    db.refresh(header)
    return header


@router.delete("/{appkey}")
def delete_order(appkey: str, db: Session = Depends(get_db)):
    """Delete an order and all its items"""
    header = db.query(Header).filter(Header.appkey == appkey).first()
    if not header:
        raise HTTPException(
            status_code=404, detail=f"Order with appkey '{appkey}' not found"
        )

    # Delete items first (due to foreign key constraint)
    db.query(Item).filter(Item.key_id == appkey).delete()

    # Delete header
    db.delete(header)
    db.commit()

    return {"message": f"Order with appkey '{appkey}' deleted successfully"}
