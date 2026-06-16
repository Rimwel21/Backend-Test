from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from utils.utc_now import utc_now
from database.connection import Base

class TeacherProfile(Base):
    __tablename__ = "teacher_profiles"

    id = Column(Integer, primary_key=True, nullable=False, index=True)

    account_id = Column(Integer, ForeignKey("accounts.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)

    teacher_account = relationship("Accounts", back_populates="teacher_profile")

    name = Column(String(50), nullable=False)

    contact_no = Column(String(20), nullable=False)

    email_address = Column(String(50), nullable=False, unique=True)

    address = Column(String(50), nullable=False)

    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now, nullable=False)