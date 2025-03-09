from pydantic import BaseModel, EmailStr
from typing import List, Optional
from sqlalchemy import Column, Integer, String
from app.database import Base

# SQLAlchemy model
class UserModel(Base):
    """SQLAlchemy model for users table"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)

# Pydantic models for API
class UserBase(BaseModel):
    """Base model for user data"""
    name: str
    email: EmailStr

class UserCreate(UserBase):
    """Model for creating a new user"""
    pass

class User(UserBase):
    """Model for user response"""
    id: int

    class Config:
        from_attributes = True

class UserList(BaseModel):
    """Model for list of users response"""
    users: List[User]
    total: int 