from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.dependencies import get_db
from core.config import settings
from auth.account_auth import hash_password, verify_password, create_access_token
from models.accounts import Accounts
from schemas.accounts_schema import StudentRegister, TeacherRegister, AccountResponse

router = APIRouter(prefix="/auth", tags=["Auth"])

