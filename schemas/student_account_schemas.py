from pydantic import BaseModel
from enum import Enum
from datetime import datetime

class StudentBase(BaseModel):
    username: str
    password: str

class StudentType(str, Enum):
    regular = "regular"
    deaf = "deaf"

class StudentRegister(StudentBase):
    student_type: StudentType

class StudentLogin(StudentBase):
    pass

class StudentResponse(BaseModel):
    id: int
    username: str
    student_type: StudentType
    role: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
    