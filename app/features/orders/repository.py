"""
Order repository for database operations
"""
from sqlalchemy.orm import Session
from . import models
from fastapi import HTTPException
from typing import List, Optional
from datetime import datetime

def get_orders(db: Session, skip: int = 0, limit: int = 100, user_id: Optional[int] = None, status: Optional[models.OrderStatus] = None):
    """Get all orders with optional filtering"""
    query = db.query(models.OrderModel)
    
    # Apply filters if provided
    if user_id is not None:
        query = query.filter(models.OrderModel.user_id == user_id)
    if status is not None:
        query = query.filter(models.OrderModel.status == status)
        
    # Apply pagination and return results
    return query.order_by(models.OrderModel.created_at.desc()).offset(skip).limit(limit).all()

def get_order_by_id(db: Session, order_id: int):
    """Get an order by ID"""
    order = db.query(models.OrderModel).filter(models.OrderModel.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

def create_order(db: Session, order: models.OrderCreate):
    """Create a new order"""
    db_order = models.OrderModel(
        item_name=order.item_name,
        quantity=order.quantity,
        price=order.price,
        status=order.status,
        user_id=order.user_id,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def update_order(db: Session, order_id: int, order_data: models.OrderCreate):
    """Update an order"""
    db_order = get_order_by_id(db, order_id)
    
    # Update order attributes
    for key, value in order_data.model_dump().items():
        if value is not None:  # Only update provided values
            setattr(db_order, key, value)
    
    # Always update the updated_at timestamp
    db_order.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(db_order)
    return db_order

def update_order_status(db: Session, order_id: int, status: models.OrderStatus):
    """Update only the status of an order"""
    db_order = get_order_by_id(db, order_id)
    db_order.status = status
    db_order.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_order)
    return db_order

def delete_order(db: Session, order_id: int):
    """Delete an order"""
    db_order = get_order_by_id(db, order_id)
    db.delete(db_order)
    db.commit()
    return True 