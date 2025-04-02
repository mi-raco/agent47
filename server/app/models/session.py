from typing import List, Optional
from pydantic import Field
from datetime import datetime

from app.models.base import BaseDBModel

class Session(BaseDBModel):
    student_id: str
    tutor_id: str
    subject: str
    start_time: datetime
    end_time: Optional[datetime] = None
    status: str = "scheduled"  # scheduled, in_progress, completed, cancelled
    session_type: str = "regular"  # regular, assessment, review
    topics_covered: List[str] = []
    materials_used: List[str] = []
    student_feedback: Optional[str] = None
    tutor_notes: Optional[str] = None
    performance_score: Optional[float] = None
    next_steps: List[str] = []
    
    class Config:
        schema_extra = {
            "example": {
                "student_id": "507f1f77bcf86cd799439011",
                "tutor_id": "507f1f77bcf86cd799439012",
                "subject": "Programming",
                "start_time": "2024-03-27T14:00:00",
                "end_time": "2024-03-27T15:00:00",
                "status": "completed",
                "session_type": "regular",
                "topics_covered": ["Python Functions", "Error Handling"],
                "materials_used": ["practice_problems.pdf", "code_examples.py"],
                "student_feedback": "Great session, learned a lot about functions",
                "tutor_notes": "Student shows good understanding of basic concepts",
                "performance_score": 85.5,
                "next_steps": ["Practice more complex functions", "Review decorators"]
            }
        } 