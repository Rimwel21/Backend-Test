from sqlalchemy import String, Integer, Column, Enum, DateTime
from database.connection import Base
from schemas.student_account_schemas import StudentType
from datetime import datetime, UTC

def utc_now():
    return datetime.now(UTC)

class StudentAccount(Base):
    __tablename__ = "student_accounts"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(String(50), nullable=False, unique=True, index=True)

    password = Column(String(255), nullable=False)

    student_type = Column(Enum(StudentType), nullable=False)

    role = Column(String, default="student", nullable=False)

    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)

    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now, nullable=False)
