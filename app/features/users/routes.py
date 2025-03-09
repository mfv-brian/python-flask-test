from fastapi import APIRouter, HTTPException
from .models import User, UserCreate, UserList

router = APIRouter(prefix="/api", tags=["users"])

# Mock database (in a real application, this would be in a separate data layer)
users = [
    {"id": 1, "name": "John Doe", "email": "john@example.com"},
    {"id": 2, "name": "Jane Smith", "email": "jane@example.com"}
]

@router.get("/users", response_model=UserList)
async def get_users():
    """Get all users"""
    return {"users": users, "total": len(users)}

@router.post("/users", response_model=User, status_code=201)
async def create_user(user: UserCreate):
    """Create a new user"""
    new_user = {
        "id": max(user["id"] for user in users) + 1,
        **user.model_dump()
    }
    users.append(new_user)
    return new_user

@router.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int):
    """Get a specific user by ID"""
    if user := next((user for user in users if user["id"] == user_id), None):
        return user
    raise HTTPException(status_code=404, detail="User not found")

@router.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, user_update: UserCreate):
    """Update a user"""
    if user := next((user for user in users if user["id"] == user_id), None):
        user.update(user_update.model_dump())
        return user
    raise HTTPException(status_code=404, detail="User not found")

@router.delete("/users/{user_id}", status_code=204)
async def delete_user(user_id: int):
    """Delete a user"""
    if user := next((user for user in users if user["id"] == user_id), None):
        users.remove(user)
        return
    raise HTTPException(status_code=404, detail="User not found") 