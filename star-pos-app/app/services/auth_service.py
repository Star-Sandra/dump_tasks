from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.core.security import create_access_token, verify_password
from app.repositories.user import get_user_by_email


def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User account is inactive")
    return user


def login(db: Session, email: str, password: str) -> str:
    user = authenticate_user(db, email, password)
    return create_access_token(subject=str(user.id), role=user.role.value)
