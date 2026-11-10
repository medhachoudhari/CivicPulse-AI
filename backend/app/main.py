
from fastapi import FastAPI
from sqlalchemy import text

from app.database import Base, engine
from app.models.complaint import Complaint
from app.routes.complaints import router as complaint_router
from app.routes.status import router as status_router
from app.models.status_history import ComplaintStatusHistory


app = FastAPI(
    title="CivicPulse AI",
    description="Intelligent Civic Complaint Prioritization and Resolution Tracking System",
    version="1.0.0"
)

# Create database tables
Base.metadata.create_all(bind=engine)

# Register routers
app.include_router(complaint_router)
app.include_router(status_router)


@app.get("/")
def home():
    return {
        "message": "Welcome to CivicPulse AI Backend!",
        "status": "running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "application": "CivicPulse AI"
    }


@app.get("/health/database")
def database_health():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return {
            "database": "connected",
            "status": "healthy"
        }

    except Exception as error:
        return {
            "database": "disconnected",
            "error": str(error)
        }
