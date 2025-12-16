from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from services.user_service import create_user, list_users
from database.database import get_db
from schemas.user import UserCreate, UserRead
from typing import List

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserRead)
def create_user_api(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user.username, user.email, user.password, user.role)

@router.get("/", response_model=List[UserRead])
def get_users_api(db: Session = Depends(get_db)):
    return list_users(db)
