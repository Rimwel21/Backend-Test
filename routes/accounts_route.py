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
    
    db_student = db.query(Accounts).filter(Accounts.username == student.username).first()

    if db_student:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="student username already exists!")
    
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
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="username not registered!")
    
    # verify student password
    if not verify_password(student.password, db_student.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password!")
    
    # check if user is student
    if db_student.role != RoleEnum.student:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not a student account!")
    
    
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


