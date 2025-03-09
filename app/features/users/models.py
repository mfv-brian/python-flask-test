from pydantic import BaseModel, EmailStr
from typing import List

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