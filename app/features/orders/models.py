from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship
from app.database import Base

class OrderStatus(str, Enum):
    """Order status enumeration"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

# SQLAlchemy model
class OrderModel(Base):
    """SQLAlchemy model for orders table"""
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    item_name = Column(String(255), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float(precision=10, scale=2), nullable=False)
    status = Column(SQLAlchemyEnum(OrderStatus), default=OrderStatus.PENDING)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

# Pydantic models for API
class OrderBase(BaseModel):
    """Base Order model with common attributes"""
    item_name: str
    quantity: int
    price: float = Field(..., gt=0)
    status: OrderStatus = OrderStatus.PENDING

class OrderCreate(OrderBase):
    """Order creation model"""
    user_id: Optional[int] = None

class Order(OrderBase):
    """Order response model"""
    id: int
    created_at: datetime
    updated_at: datetime
    user_id: Optional[int] = None

    class Config:
        from_attributes = True

class OrderList(BaseModel):
    """Response model for list of orders"""
    orders: List[Order]
    total: int 