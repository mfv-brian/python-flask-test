"""
Database connection module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pymysql
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Add PyMySQL support for MySQL
pymysql.install_as_MySQLdb()

# Database connection string
MYSQL_USER = os.getenv("MYSQL_USER", "app_user")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "app_password")
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_PORT = os.getenv("MYSQL_PORT", "3308")
MYSQL_DB = os.getenv("MYSQL_DB", "app_db")

DATABASE_URL = f"mysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create declarative base for models
Base = declarative_base()

# Dependency for getting database session
def get_db():
    """
    Get database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 