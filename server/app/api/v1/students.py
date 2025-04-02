from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.models.student import Student
from app.schemas.student import StudentCreate, StudentUpdate, StudentInDB
from app.services.student_service import StudentService
from app.api.dependencies import get_db

router = APIRouter()

@router.post("/", response_model=StudentInDB)
async def create_student(
    *,
    db: AsyncIOMotorDatabase = Depends(get_db),
    student_in: StudentCreate,
) -> Student:
    """
    Create new student.
    """
    student_service = StudentService(db)
    student = await student_service.get_by_email(email=student_in.email)
    if student:
        raise HTTPException(
            status_code=400,
            detail="A student with this email already exists.",
        )
    return await student_service.create(obj_in=student_in)

@router.get("/", response_model=List[StudentInDB])
async def read_students(
    db: AsyncIOMotorDatabase = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
) -> List[Student]:
    """
    Retrieve students.
    """
    student_service = StudentService(db)
    return await student_service.get_multi(skip=skip, limit=limit)

@router.get("/{student_id}", response_model=StudentInDB)
async def read_student(
    *,
    db: AsyncIOMotorDatabase = Depends(get_db),
    student_id: str,
) -> Student:
    """
    Get student by ID.
    """
    student_service = StudentService(db)
    student = await student_service.get(id=student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@router.put("/{student_id}", response_model=StudentInDB)
async def update_student(
    *,
    db: AsyncIOMotorDatabase = Depends(get_db),
    student_id: str,
    student_in: StudentUpdate,
) -> Student:
    """
    Update student.
    """
    student_service = StudentService(db)
    student = await student_service.get(id=student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return await student_service.update(db_obj=student, obj_in=student_in)

@router.delete("/{student_id}")
async def delete_student(
    *,
    db: AsyncIOMotorDatabase = Depends(get_db),
    student_id: str,
) -> dict:
    """
    Delete student.
    """
    student_service = StudentService(db)
    student = await student_service.get(id=student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    await student_service.delete(id=student_id)
    return {"status": "success"}

@router.get("/subject/{subject}", response_model=List[StudentInDB])
async def read_students_by_subject(
    *,
    db: AsyncIOMotorDatabase = Depends(get_db),
    subject: str,
    skip: int = 0,
    limit: int = 100,
) -> List[Student]:
    """
    Get students by subject.
    """
    student_service = StudentService(db)
    return await student_service.get_students_by_subject(
        subject=subject,
        skip=skip,
        limit=limit
    ) 