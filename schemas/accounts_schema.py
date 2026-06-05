from pydantic import BaseModel, EmailStr
from datetime import datetime
from enum import Enum

class RoleEnum(str, Enum):
    student = "student"
    teacher = "teacher"
    admin = "admin"

class StudentRegister(BaseModel):
    username: str
    password: str

class StudentLogin(BaseModel):
    username: str
    password: str

class TeacherRegister(BaseModel):
    email: EmailStr
    password: str

class TeacherLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class AccountResponse(BaseModel):
    id: int
    username: str | None
    email: str | None
    role: RoleEnum
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
    