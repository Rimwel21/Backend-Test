from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from utils.dependencies import get_db
from auth.account_auth import hash_password, verify_password, create_access_token, create_refresh_token
from models.accounts import Accounts
from utils.enum import RoleEnum
from schemas.accounts_schema import AccountRegister, AccountLogin, AccountResponse,TokenResponse
router = APIRouter(prefix="/auth", tags=["Auth"])

# Account Registration
@router.post("/account/register", response_model=AccountResponse)
def account_register(user: AccountRegister, db: Session = Depends(get_db)):

    if user.role == RoleEnum.student:
        if not user.username:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username is required for student accounts")
        
        existing = db.query(Accounts).filter(Accounts.username == user.username).first()
        
    elif user.role == RoleEnum.teacher:
        if not user.email:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email is required for teacher accounts")

        existing = db.query(Accounts).filter(Accounts.email == user.email).first()

    elif user.role == RoleEnum.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin registration is not allowed")

    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Account already exists")
    
    new_account = Accounts(
        username=user.username if user.role == RoleEnum.student else None,
        email=user.email if user.role == RoleEnum.teacher else None,
        hashed_password=hash_password(user.password),
        role=user.role
    )

    db.add(new_account)
    db.commit()
    db.refresh(new_account)

    return new_account

@router.post("/account/login", response_model=TokenResponse)
def account_login(user: AccountLogin, response: Response, db: Session = Depends(get_db)):

    if not user.username and not user.email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email is required"
        )
    
    if user.username and user.email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Use only username or email"
        )

    if user.username:
        db_account = db.query(Accounts).filter(Accounts.username == user.username).first()
    else:
        db_account = db.query(Accounts).filter(Accounts.email == user.email).first()

    if not db_account:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    if not verify_password(user.password, db_account.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    access_token = create_access_token(
        data={
            "sub": str(db_account.id),
            "username": db_account.username,
            "email": db_account.email,
            "role": db_account.role
        }
    )

    refresh_token = create_refresh_token(
        data={
            "sub": str(db_account.id)
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
