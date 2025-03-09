"""
Task repository for database operations
"""
from sqlalchemy.orm import Session
from . import models
from fastapi import HTTPException
from datetime import datetime

def get_tasks(db: Session, skip: int = 0, limit: int = 100):
    """Get all tasks with pagination"""
    return db.query(models.TaskModel).offset(skip).limit(limit).all()

def get_task_by_id(db: Session, task_id: int):
    """Get a task by ID"""
    task = db.query(models.TaskModel).filter(models.TaskModel.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

def create_task(db: Session, task: models.TaskCreate, user_id: int = None):
    """Create a new task"""
    db_task = models.TaskModel(
        title=task.title,
        description=task.description,
        status=task.status,
        user_id=user_id,
        created_at=datetime.utcnow()
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def update_task(db: Session, task_id: int, task_data: models.TaskCreate):
    """Update a task"""
    db_task = get_task_by_id(db, task_id)
    
    # Update task attributes
    for key, value in task_data.model_dump().items():
        setattr(db_task, key, value)
    
    db.commit()
    db.refresh(db_task)
    return db_task

def delete_task(db: Session, task_id: int):
    """Delete a task"""
    db_task = get_task_by_id(db, task_id)
    db.delete(db_task)
    db.commit()
    return True 