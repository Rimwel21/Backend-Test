from pydantic import BaseModel, EmailStr
from datetime import datetime

class TeacherProfileBase(BaseModel):
    name: str
    contact_no: str
    address: str

class TeacherProfileCreate(TeacherProfileBase):
    pass

class TeacherProfileUpdate(BaseModel):
    name: str | None = None
    contact_no: str | None = None
    address: str | None = None

class TeacherProfileOut(BaseModel):
    id: int
    account_id: int
    profile_image_id: int | None = None
    name: str
    contact_no: str
    email_address: EmailStr
    address: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True