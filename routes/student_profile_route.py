from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from utils.dependencies import get_db, get_current_user
from utils.enum import RoleEnum
from models.student_profile import StudentProfile
from models.accounts import Accounts
from schemas.student_profile_schema import StudentProfileCreate, StudentProfileUpdate, StudentProfileOut

router = APIRouter(prefix="/student", tags=["Student-Profile"])

@router.post("/profile", response_model=StudentProfileOut)
def create_profile(student: StudentProfileCreate, db: Session = Depends(get_db), current_user: Accounts = Depends(get_current_user)):
    if current_user.role != RoleEnum.student:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Student only")
    
    existing_profile = db.query(StudentProfile).filter(StudentProfile.account_id == current_user.id).first()

    if existing_profile:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Student profile already exists")

    new_student_profile = StudentProfile(
        name=student.name,
        account_id=current_user.id,
        student_type=student.student_type,
        guardians_name=student.guardians_name,
        guardians_contact_no=student.guardians_contact_no,
        address=student.address
    )

    db.add(new_student_profile)
    db.commit()
    db.refresh(new_student_profile)

    return new_student_profile


