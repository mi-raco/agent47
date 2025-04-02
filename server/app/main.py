from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Dict, Any

from app.config import settings
from app.api.v1 import students, tutors, sessions

app = FastAPI(
    title="Virtual Tutoring System",
    description="An AI-powered virtual tutoring system",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database connection
@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = AsyncIOMotorClient(settings.MONGODB_URL)
    app.mongodb = app.mongodb_client[settings.MONGODB_DB_NAME]

@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()

# Global exception handler
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()}
    )

# Include routers
app.include_router(students.router, prefix="/api/v1/students", tags=["students"])
app.include_router(tutors.router, prefix="/api/v1/tutors", tags=["tutors"])
app.include_router(sessions.router, prefix="/api/v1/sessions", tags=["sessions"])

@app.get("/")
async def root() -> Dict[str, Any]:
    return {
        "message": "Welcome to Virtual Tutoring System API",
        "version": "1.0.0",
        "status": "operational"
    } 