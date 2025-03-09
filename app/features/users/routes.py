from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from .models import User, UserCreate, UserList
from . import repository
from app.database import get_db

router = APIRouter(prefix="/api", tags=["users"])

@router.get("/users", response_model=UserList)
async def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all users"""
    users = repository.get_users(db, skip=skip, limit=limit)
    return {"users": users, "total": len(users)}

@router.post("/users", response_model=User, status_code=201)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Create a new user"""
    return repository.create_user(db, user)

@router.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    """Get a specific user by ID"""
    return repository.get_user_by_id(db, user_id)

@router.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, user_update: UserCreate, db: Session = Depends(get_db)):
    """Update a user"""
    return repository.update_user(db, user_id, user_update)

@router.delete("/users/{user_id}", status_code=204)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    """Delete a user"""
    repository.delete_user(db, user_id)
    return None 