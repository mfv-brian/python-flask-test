from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from enum import Enum
from sqlalchemy import Column, Integer, String, Text, Enum as SQLAlchemyEnum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class TaskStatus(str, Enum):
    """Task status enumeration"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

# SQLAlchemy model
class TaskModel(Base):
    """SQLAlchemy model for tasks table"""
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    status = Column(SQLAlchemyEnum(TaskStatus), default=TaskStatus.PENDING)
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

# Pydantic models for API
class TaskBase(BaseModel):
    """Base Task model with common attributes"""
    title: str
    description: str
    status: TaskStatus = TaskStatus.PENDING

class TaskCreate(TaskBase):
    """Task creation model"""
    pass

class Task(TaskBase):
    """Task response model"""
    id: int
    created_at: datetime
    user_id: Optional[int] = None

    class Config:
        from_attributes = True

class TaskList(BaseModel):
    """Response model for list of tasks"""
    tasks: List[Task]
    total: int 