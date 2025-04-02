from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
from pydantic import EmailStr

from app.models.student import Student
from app.services.base import BaseService
from app.schemas.student import StudentCreate, StudentUpdate

class StudentService(BaseService[Student, StudentCreate, StudentUpdate]):
    def __init__(self, db: AsyncIOMotorDatabase):
        super().__init__(Student, db)

    async def get_by_email(self, email: EmailStr) -> Optional[Student]:
        if (doc := await self.collection.find_one({"email": email})) is not None:
            return Student(**doc)
        return None

    async def update_learning_goals(
        self, *, student_id: str, goals: List[str]
    ) -> Optional[Student]:
        student = await self.get(student_id)
        if not student:
            return None
        student.learning_goals = goals
        return await self.update(db_obj=student, obj_in={"learning_goals": goals})

    async def update_performance_metrics(
        self, *, student_id: str, subject: str, score: float, progress: float
    ) -> Optional[Student]:
        student = await self.get(student_id)
        if not student:
            return None
        student.performance_metrics[subject] = {
            "score": score,
            "progress": progress
        }
        return await self.update(
            db_obj=student,
            obj_in={"performance_metrics": student.performance_metrics}
        )

    async def get_students_by_subject(
        self, *, subject: str, skip: int = 0, limit: int = 100
    ) -> List[Student]:
        return await self.get_multi(
            skip=skip,
            limit=limit,
            query={"current_subjects": subject}
        )

    async def update_session_count(self, *, student_id: str) -> Optional[Student]:
        student = await self.get(student_id)
        if not student:
            return None
        student.total_sessions += 1
        return await self.update(
            db_obj=student,
            obj_in={"total_sessions": student.total_sessions}
        ) 