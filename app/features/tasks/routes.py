from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from .models import Task, TaskCreate, TaskList
from . import repository
from app.database import get_db

router = APIRouter(prefix="/api", tags=["tasks"])

@router.get("/tasks", response_model=TaskList)
async def get_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all tasks"""
    tasks = repository.get_tasks(db, skip=skip, limit=limit)
    return {"tasks": tasks, "total": len(tasks)}

@router.post("/tasks", response_model=Task, status_code=201)
async def create_task(task: TaskCreate, user_id: int = None, db: Session = Depends(get_db)):
    """Create a new task"""
    return repository.create_task(db, task, user_id)

@router.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: int, db: Session = Depends(get_db)):
    """Get a specific task by ID"""
    return repository.get_task_by_id(db, task_id)

@router.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int, task_update: TaskCreate, db: Session = Depends(get_db)):
    """Update a task"""
    return repository.update_task(db, task_id, task_update)

@router.delete("/tasks/{task_id}", status_code=204)
async def delete_task(task_id: int, db: Session = Depends(get_db)):
    """Delete a task"""
    repository.delete_task(db, task_id)
    return None 