from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from enum import Enum

class TaskStatus(str, Enum):
    """Task status enumeration"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

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

    class Config:
        from_attributes = True

class TaskList(BaseModel):
    """Response model for list of tasks"""
    tasks: List[Task]
    total: int 