from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.features.users.routes import router as users_router
from app.features.tasks.routes import router as tasks_router
from app.database import engine
from app.features.users.models import UserModel
from app.features.tasks.models import TaskModel

# Create database tables
UserModel.metadata.create_all(bind=engine)
TaskModel.metadata.create_all(bind=engine)

def create_app() -> FastAPI:
    """Create and configure the FastAPI application"""
    app = FastAPI(
        title="FastAPI REST API",
        description="A modern REST API built with FastAPI",
        version="1.0.0",
    )

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(users_router)
    app.include_router(tasks_router)

    return app

# Create the application instance
app = create_app() 