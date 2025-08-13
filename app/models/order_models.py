from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Header(Base):
    __tablename__ = "headers"

    appkey = Column(String(50), primary_key=True, index=True)
    customer_name = Column(String(100), nullable=False)
    customer_email = Column(String(100))
    customer_phone = Column(String(20))
    order_date = Column(DateTime, default=datetime.utcnow)
    status = Column(String(20), default="pending")
    total_amount = Column(Float, default=0.0)

    # Relationship to items
    items = relationship("Item", back_populates="header", cascade="all, delete-orphan")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    key_id = Column(String(50), ForeignKey("headers.appkey"), nullable=False)
    product_name = Column(String(100), nullable=False)
    product_code = Column(String(50))
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    total_price = Column(Float, nullable=False)

    # Relationship to header
    header = relationship("Header", back_populates="items")
