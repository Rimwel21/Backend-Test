from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from enum import Enum

class RoleEnum(str, Enum):
    student = "student"
    teacher = "teacher"
    admin = "admin"

class AccountRegister(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    password: str = Field(min_length=8, max_length=30)
    role: RoleEnum

class AccountLogin(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    password: str = Field(min_length=8, max_length=30)

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class AccountResponse(BaseModel):
    id: int
    username: str | None
    email: EmailStr | None
    role: RoleEnum
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
    