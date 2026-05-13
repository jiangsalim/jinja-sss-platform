"""
Jinja SSS Platform - Request Validators
Pydantic schemas for input validation
"""

from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import date


class PaginationParams(BaseModel):
    page: int = Field(default=1, ge=1, le=100)
    limit: int = Field(default=20, ge=1, le=100)
    sort_by: str = Field(default="created_at")
    sort_order: str = Field(default="desc", pattern="^(asc|desc)$")


class DateRangeParams(BaseModel):
    date_from: Optional[date] = None
    date_to: Optional[date] = None


class UserCreateSchema(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=100)
    email: Optional[str] = None
    role: str = Field(..., pattern="^(student|teacher|hod|admin|parent|alumni|nurse|counselor|chaplain|social_worker)$")
    phone: Optional[str] = None
    identifier: str = Field(..., min_length=3, max_length=20)


class GradeCreateSchema(BaseModel):
    student_id: int = Field(..., gt=0)
    subject_id: int = Field(..., gt=0)
    exam_type: str = Field(..., pattern="^(CAT1|CAT2|End of Term|Final|Assignment|Quiz)$")
    term_id: int = Field(..., gt=0)
    score: float = Field(..., ge=0, le=100)
    remarks: Optional[str] = Field(default=None, max_length=500)


class AttendanceBulkSchema(BaseModel):
    date: date
    period: int = Field(..., ge=1, le=8)
    subject_id: int
    class_id: int
    attendance: list
