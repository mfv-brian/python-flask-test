from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from .models import Order, OrderCreate, OrderList, OrderStatus
from . import repository
from app.database import get_db

router = APIRouter(prefix="/api", tags=["orders"])

@router.get("/orders", response_model=OrderList)
async def get_orders(
    skip: int = 0, 
    limit: int = 100, 
    user_id: Optional[int] = None,
    status: Optional[OrderStatus] = None,
    db: Session = Depends(get_db)
):
    """
    Get all orders with optional filtering by user_id and status.
    
    - **skip**: Number of records to skip (pagination)
    - **limit**: Maximum number of records to return
    - **user_id**: Filter orders by user ID
    - **status**: Filter orders by status (pending, processing, completed, cancelled)
    """
    orders = repository.get_orders(db, skip=skip, limit=limit, user_id=user_id, status=status)
    return {"orders": orders, "total": len(orders)}

@router.post("/orders", response_model=Order, status_code=201)
async def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    """
    Create a new order.
    
    - **item_name**: Name of the ordered item
    - **quantity**: Number of items ordered
    - **price**: Price per item
    - **status**: Order status (default: pending)
    - **user_id**: ID of the user placing the order (optional)
    """
    return repository.create_order(db, order)

@router.get("/orders/{order_id}", response_model=Order)
async def get_order(order_id: int, db: Session = Depends(get_db)):
    """
    Get a specific order by ID.
    
    - **order_id**: The ID of the order to retrieve
    """
    return repository.get_order_by_id(db, order_id)

@router.put("/orders/{order_id}", response_model=Order)
async def update_order(order_id: int, order_update: OrderCreate, db: Session = Depends(get_db)):
    """
    Update an order.
    
    - **order_id**: The ID of the order to update
    - **order_update**: The updated order data
    """
    return repository.update_order(db, order_id, order_update)

@router.patch("/orders/{order_id}/status", response_model=Order)
async def update_order_status(order_id: int, status: OrderStatus, db: Session = Depends(get_db)):
    """
    Update only the status of an order.
    
    - **order_id**: The ID of the order to update
    - **status**: The new status (pending, processing, completed, cancelled)
    """
    return repository.update_order_status(db, order_id, status)

@router.delete("/orders/{order_id}", status_code=204)
async def delete_order(order_id: int, db: Session = Depends(get_db)):
    """
    Delete an order.
    
    - **order_id**: The ID of the order to delete
    """
    repository.delete_order(db, order_id)
    return None 