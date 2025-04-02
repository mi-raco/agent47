from typing import Generator
from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.main import app

async def get_db() -> Generator[AsyncIOMotorDatabase, None, None]:
    """
    Get database connection.
    """
    try:
        yield app.mongodb
    finally:
        # Connection is managed by FastAPI lifecycle events
        pass 