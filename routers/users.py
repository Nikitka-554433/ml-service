# users.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import get_db
from services.user_service import create_user, get_user, list_users
from schemas.user import UserCreate, UserRead

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserRead)
def register_user(data: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, data.username, data.email, data.password)


@router.get("/{user_id}", response_model=UserRead)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(404, "User not found")
    return user


@router.get("/", response_model=list[UserRead])
def list_all_users(db: Session = Depends(get_db)):
    return list_users(db)
