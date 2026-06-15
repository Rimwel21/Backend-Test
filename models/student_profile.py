from sqlalchemy import Column, Integer, String, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship
from database.connection import Base
from utils.utc_now import utc_now
from utils.enum import StudentType

class StudentProfile(Base):
    __tablename__ = "student_profiles"

    id = Column(Integer, primary_key=True, nullable=False, index=True)

    name = Column(String, nullable=False)

    student_type = Column(Enum(StudentType), nullable=False)

    account_id = Column(Integer, ForeignKey("accounts.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)

    student_account = relationship("Accounts", back_populates="student_profile")

    # avatar_upload ("add later, upload image")

    guardians_name = Column(String, nullable=True)

    guardians_contact_no = Column(String(20), nullable=True)

    address = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)

    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now, nullable=False)


