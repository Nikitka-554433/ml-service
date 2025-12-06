# auth.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.auth import AuthRequest, AuthResponse
from schemas.user import UserCreate, UserRead
from services.user_service import create_user, get_user_by_username
from passlib.hash import bcrypt
from database.database import get_db
from auth_utils import create_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserRead)
def register(data: UserCreate, db: Session = Depends(get_db)):
    existing = get_user_by_username(db, data.username)
    if existing:
        raise HTTPException(400, "Username already taken")

    return create_user(
        db,
        username=data.username,
        email=data.email,
        password=data.password,
    )

@router.post("/login", response_model=AuthResponse)
def login(auth: AuthRequest, db: Session = Depends(get_db)):
    user = get_user_by_username(db, auth.username)
    if not user or not bcrypt.verify(auth.password, user.password_hash):
        raise HTTPException(401, "Invalid credentials")

    token = create_token(user.user_id)
    return AuthResponse(access_token=token)
