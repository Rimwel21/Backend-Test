from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from database.dependencies import get_db
from core.config import settings
from auth.account_auth import hash_password, verify_password, create_access_token, create_refresh_token
from models.accounts import Accounts
from schemas.accounts_schema import StudentRegister, StudentLogin, TeacherRegister, TeacherLogin, AccountResponse, RoleEnum, TokenResponse

router = APIRouter(prefix="/auth", tags=["Auth"])

# Student Registration
@router.post("/student/register", response_model=AccountResponse)
def student_register(student: StudentRegister, db: Session = Depends(get_db)):
    
    existing = db.query(Accounts).filter(Accounts.username == student.username).first()

    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists!")
    
    new_student = Accounts(
        username=student.username,
        hashed_password=hash_password(student.password),
        role=RoleEnum.student
    )
    
    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return new_student

# Student Login
@router.post("/student/login", response_model=TokenResponse)
def student_login(student: StudentLogin, response: Response, db: Session = Depends(get_db)):

    db_student = db.query(Accounts).filter(Accounts.username == student.username).first()

    # find student account
    if not db_student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid username!")
    
    # verify student password
    if not verify_password(student.password, db_student.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password!")
    
    # medyo useless security, pero ok narin para maka sigurado
    if db_student.role != RoleEnum.student:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Must a student account!")
    
    
    access_token = create_access_token(
        data={
        "sub":str(db_student.id),
        "username":db_student.username,
        "role":db_student.role
        }
    )

    refresh_token = create_refresh_token(
        data={
            "sub":str(db_student.id)
        }
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,  # True kapag HTTPS na
        samesite="lax",
        max_age=7 * 24 * 60 * 60,
        path="/api/refresh"
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# Teacher Register 
@router.post("/teacher/register", response_model=AccountResponse)
def teacher_register(teacher: TeacherRegister, db: Session = Depends(get_db)):

    existing = db.query(Accounts).filter(Accounts.email == teacher.email).first()

    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists!")
    
    new_teacher = Accounts(
        email=teacher.email,
        hashed_password=hash_password(teacher.password),
        role=RoleEnum.teacher
    )

    db.add(new_teacher)
    db.commit()
    db.refresh(new_teacher)

    return new_teacher

# Teacher Login
@router.post("/teacher/login", response_model=TokenResponse)
def teacher_login(teacher:TeacherLogin, response: Response, db: Session = Depends(get_db)):

    db_teacher = db.query(Accounts).filter(Accounts.email == teacher.email).first()

    if not db_teacher:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Email!")
    
    if not verify_password(teacher.password, db_teacher.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password!")
    
    # medyo useless security, pero ok narin para maka sigurado
    if db_teacher.role != RoleEnum.teacher:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Must a teacher account!")
    
    access_token = create_access_token(
        data={
            "sub":str(db_teacher.id),
            "email":db_teacher.email,
            "role":db_teacher.role
        }
    )

    refresh_token = create_refresh_token(
        data={
            "sub":str(db_teacher.id)
        }
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,  # True kapag HTTPS na
        samesite="lax",
        max_age=7 * 24 * 60 * 60,
        path="/api/refresh"
    )

    return {
        "access_token":access_token,
        "token_type": "bearer"
    }
