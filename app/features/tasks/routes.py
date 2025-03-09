from fastapi import APIRouter, HTTPException
from .models import Task, TaskCreate, TaskList
from datetime import datetime

router = APIRouter(prefix="/api", tags=["tasks"])

# Mock database (in a real application, this would be in a separate data layer)
tasks = [
    {
        "id": 1,
        "title": "Complete project",
        "description": "Finish the API implementation",
        "status": "in_progress",
        "created_at": datetime.fromisoformat("2024-03-09T10:00:00+00:00")
    }
]

@router.get("/tasks", response_model=TaskList)
async def get_tasks():
    """Get all tasks"""
    return {"tasks": tasks, "total": len(tasks)}

@router.post("/tasks", response_model=Task, status_code=201)
async def create_task(task: TaskCreate):
    """Create a new task"""
    new_task = {
        "id": max(task["id"] for task in tasks) + 1,
        **task.model_dump(),
        "created_at": datetime.utcnow()
    }
    tasks.append(new_task)
    return new_task

@router.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: int):
    """Get a specific task by ID"""
    if task := next((task for task in tasks if task["id"] == task_id), None):
        return task
    raise HTTPException(status_code=404, detail="Task not found")

@router.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int, task_update: TaskCreate):
    """Update a task"""
    if task := next((task for task in tasks if task["id"] == task_id), None):
        task.update(task_update.model_dump())
        return task
    raise HTTPException(status_code=404, detail="Task not found")

@router.delete("/tasks/{task_id}", status_code=204)
async def delete_task(task_id: int):
    """Delete a task"""
    if task := next((task for task in tasks if task["id"] == task_id), None):
        tasks.remove(task)
        return
    raise HTTPException(status_code=404, detail="Task not found") 