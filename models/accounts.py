from sqlalchemy import String, Integer, Column, DateTime, Enum
from database.connection import Base
from datetime import datetime, timezone
from schemas.accounts_schema import RoleEnum

def utc_now():
    return datetime.now(timezone.utc)

class Accounts(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(String(100), unique=True, nullable=True, index=True)
    # username for students only

    email = Column(String(100),unique=True, nullable=True, index=True)
    # email only for teacher and admin
    
    hashed_password = Column(String(255), nullable=False)

    role = Column(Enum(RoleEnum), default=RoleEnum.student, nullable=False)
    # Student | Teacher | Admin

    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)

    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now, nullable=False)


