from datetime import datetime
from pydantic import BaseModel, Field


class TeacherClassBase(BaseModel):
    grade_level: str = Field(min_length=1, max_length=30)
    section: str = Field(min_length=1, max_length=50)


class TeacherClassCreate(TeacherClassBase):
    pass


class TeacherClassUpdate(BaseModel):
    grade_level: str | None = Field(default=None, min_length=1, max_length=30)
    section: str | None = Field(default=None, min_length=1, max_length=50)


class TeacherClassOut(TeacherClassBase):
    id: int
    teacher_id: int
    student_count: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
