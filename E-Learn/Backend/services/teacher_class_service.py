from fastapi import HTTPException, Request, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from models.accounts import Accounts
from models.teacher_class import TeacherClass
from schemas.teacher_class_schema import TeacherClassCreate, TeacherClassUpdate
from utils.enum import RoleEnum


def _ensure_teacher(current_user: Accounts):
    if current_user.role != RoleEnum.teacher:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Teacher only")


def list_teacher_classes(request: Request, db: Session, current_user: Accounts):
    _ensure_teacher(current_user)

    return (
        db.query(TeacherClass)
        .filter(TeacherClass.teacher_id == current_user.id)
        .order_by(TeacherClass.created_at.desc())
        .all()
    )


def create_teacher_class(request: Request, teacher_class: TeacherClassCreate, db: Session, current_user: Accounts):
    _ensure_teacher(current_user)

    new_teacher_class = TeacherClass(
        teacher_id=current_user.id,
        grade_level=teacher_class.grade_level.strip(),
        section=teacher_class.section.strip(),
    )

    db.add(new_teacher_class)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Class already exists for this teacher"
        )

    db.refresh(new_teacher_class)

    return new_teacher_class


def get_teacher_class(request: Request, class_id: int, db: Session, current_user: Accounts):
    _ensure_teacher(current_user)

    teacher_class = (
        db.query(TeacherClass)
        .filter(TeacherClass.id == class_id, TeacherClass.teacher_id == current_user.id)
        .first()
    )

    if not teacher_class:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Class not found")

    return teacher_class


def update_teacher_class(request: Request, class_id: int, update: TeacherClassUpdate, db: Session, current_user: Accounts):
    teacher_class = get_teacher_class(
        request=request,
        class_id=class_id,
        db=db,
        current_user=current_user
    )

    update_data = update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(teacher_class, key, value.strip() if isinstance(value, str) else value)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Class already exists for this teacher"
        )

    db.refresh(teacher_class)

    return teacher_class


def delete_teacher_class(request: Request, class_id: int, db: Session, current_user: Accounts):
    teacher_class = get_teacher_class(
        request=request,
        class_id=class_id,
        db=db,
        current_user=current_user
    )

    db.delete(teacher_class)
    db.commit()

    return {"detail": "Class deleted successfully"}
