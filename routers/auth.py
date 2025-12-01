# auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas.auth import AuthRequest, AuthResponse
from schemas.user import UserCreate, UserRead
from services.user_service import create_user, get_user
from database.database import get_db
from passlib.hash import bcrypt

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserRead)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(get_user).filter_by(username=user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")
    return create_user(db, user.username, user.email, user.password)

@router.post("/login", response_model=AuthResponse)
def login(auth: AuthRequest, db: Session = Depends(get_db)):
    user = db.query(get_user).filter_by(username=auth.username).first()
    if not user or not bcrypt.verify(auth.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    # Тут можно добавить генерацию JWT токена, для примера сделаем фиктивный
    token = "fake-jwt-token-for-" + user.username
    return AuthResponse(access_token=token)
