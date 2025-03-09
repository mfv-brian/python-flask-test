import uvicorn
import logging
from sqlalchemy.exc import SQLAlchemyError
from app import app

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    try:
        logger.info("Starting FastAPI application")
        uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
    except SQLAlchemyError as e:
        logger.error(f"Database error: {e}")
    except Exception as e:
        logger.error(f"Application error: {e}") 