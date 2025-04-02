from typing import List, Optional
from pydantic import EmailStr, Field
from datetime import datetime

from app.models.base import BaseDBModel

class StudentBase(BaseModel):
    email: EmailStr
    name: str
    learning_goals: List[str] = []
    current_subjects: List[str] = []
    learning_style: Optional[str] = None
    preferred_schedule: Optional[List[dict]] = []

class StudentCreate(StudentBase):
    pass

class StudentUpdate(StudentBase):
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    last_session: Optional[datetime] = None
    total_sessions: Optional[int] = None
    performance_metrics: Optional[dict] = None

class StudentInDB(StudentBase, BaseDBModel):
    last_session: Optional[datetime] = None
    total_sessions: int = 0
    performance_metrics: dict = Field(default_factory=dict)

    class Config:
        schema_extra = {
            "example": {
                "email": "student@example.com",
                "name": "John Doe",
                "learning_goals": ["Master Python", "Learn Data Structures"],
                "current_subjects": ["Programming", "Mathematics"],
                "learning_style": "visual",
                "preferred_schedule": [
                    {"day": "Monday", "time": "14:00"},
                    {"day": "Wednesday", "time": "15:00"}
                ],
                "last_session": "2024-03-27T10:00:00",
                "total_sessions": 5,
                "performance_metrics": {
                    "programming": {"score": 85, "progress": 0.7},
                    "mathematics": {"score": 90, "progress": 0.8}
                }
            }
        } 