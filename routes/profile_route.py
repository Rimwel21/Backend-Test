from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from utils.dependencies import get_db, get_current_user
from utils.enum import RoleEnum
from models.student_profile import StudentProfile
from models.teacher_profile import TeacherProfile
from models.accounts import Accounts
from schemas.student_profile_schema import StudentProfileCreate, StudentProfileOut
from schemas.teacher_profile_schema import TeacherProfileCreate, TeacherProfileOut

router = APIRouter(prefix="/profile", tags=["Profiling"])

@router.post("/student", response_model=StudentProfileOut)
def create_student_profile(student: StudentProfileCreate, db: Session = Depends(get_db), current_user: Accounts = Depends(get_current_user)):
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

@router.post("/teacher", response_model=TeacherProfileOut)
def create_teacher_profile(teacher: TeacherProfileCreate, db: Session = Depends(get_db), current_user: Accounts = Depends(get_current_user)):
    if current_user.role != RoleEnum.teacher:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Teacher only")
    
    existing_profile = db.query(TeacherProfile).filter(TeacherProfile.account_id == current_user.id).first()

    if existing_profile:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Teacher profile already exists")
    
    new_teacher_profile = TeacherProfile(
        account_id=current_user.id,
        name=teacher.name,
        contact_no=teacher.contact_no,
        email_address=current_user.email,
        address=teacher.address,
    )

    db.add(new_teacher_profile)
    db.commit()
    db.refresh(new_teacher_profile)

    return new_teacher_profile

