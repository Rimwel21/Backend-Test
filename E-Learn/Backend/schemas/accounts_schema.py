from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from utils.enum import RoleEnum


class AccountRegister(BaseModel):
    username: str | None = Field(None, min_length=5, max_length=50)
    email: EmailStr | None = Field(None, min_length=5, max_length=50)
    password: str = Field(min_length=8, max_length=30)
    role: RoleEnum

class AccountLogin(BaseModel):
    username: str | None = Field(None, min_length=5, max_length=50)
    email: EmailStr | None = Field(None, min_length=5, max_length=50)
    password: str = Field(min_length=8, max_length=30)

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    profile_completed: bool

class AccountResponse(BaseModel):
    id: int
    username: str | None
    email: EmailStr | None
    role: RoleEnum
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
    