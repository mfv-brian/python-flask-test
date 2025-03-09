"""
User repository for database operations
"""
from sqlalchemy.orm import Session
from . import models
from fastapi import HTTPException

def get_users(db: Session, skip: int = 0, limit: int = 100):
    """Get all users with pagination"""
    return db.query(models.UserModel).offset(skip).limit(limit).all()

def get_user_by_id(db: Session, user_id: int):
    """Get a user by ID"""
    user = db.query(models.UserModel).filter(models.UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def get_user_by_email(db: Session, email: str):
    """Get a user by email"""
    return db.query(models.UserModel).filter(models.UserModel.email == email).first()

def create_user(db: Session, user: models.UserCreate):
    """Create a new user"""
    # Check if email already exists
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create new user
    db_user = models.UserModel(name=user.name, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user_data: models.UserCreate):
    """Update a user"""
    db_user = get_user_by_id(db, user_id)
    
    # Check if email is being changed and already exists
    if user_data.email != db_user.email and get_user_by_email(db, user_data.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Update user attributes
    for key, value in user_data.model_dump().items():
        setattr(db_user, key, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    """Delete a user"""
    db_user = get_user_by_id(db, user_id)
    db.delete(db_user)
    db.commit()
    return True 