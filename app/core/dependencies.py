from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories import user_repository
from database import get_db

DbSession = Annotated[Session, Depends(get_db)]

DEV_USER_EMAIL = "dev@example.com"


def get_current_user(db: DbSession) -> User:
    """TEMPORARY: returns the seeded dev user. Replaced by JWT auth later."""
    user = user_repository.get_by_email(db, DEV_USER_EMAIL)
    if user is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Dev user not seeded")
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]