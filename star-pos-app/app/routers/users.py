from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.security import get_current_user, require_admin
from database import get_db
from app.repositories import user as user_repo
from app.schemas.user import Token, UserCreate, UserOut, UserUpdate
from app.services.auth_service import login

router = APIRouter(prefix="/users", tags=["Employee Management"])


@router.post("/login", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Login with email (as 'username') + password. Returns a JWT bearer token."""
    return Token(access_token=login(db, email=form_data.username, password=form_data.password))


@router.post("", response_model=UserOut, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_admin)])
def register_staff(user_in: UserCreate, db: Session = Depends(get_db)):
    """Admin-only: register a new staff account (admin, manager, or cashier)."""
    if user_repo.get_user_by_email(db, user_in.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    return user_repo.create_user(db, user_in)


@router.get("", response_model=list[UserOut], dependencies=[Depends(require_admin)])
def list_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return user_repo.list_users(db, skip=skip, limit=limit)


@router.get("/current", response_model=UserOut)
def get_current_user_profile(current_user=Depends(get_current_user)):
    return current_user


@router.patch("/{user_id}", response_model=UserOut, dependencies=[Depends(require_admin)])
def update_user(user_id: int, user_in: UserUpdate, db: Session = Depends(get_db)):
    user = user_repo.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user_repo.update_user(db, user, user_in)
