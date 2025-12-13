from fastapi import APIRouter, HTTPException, Depends
from schemas.auth import AuthRequest, AuthResponse
from sqlalchemy.orm import Session
from services.user_service import get_user_by_username
from database.database import get_db
from passlib.hash import bcrypt
from jose import jwt
import datetime

SECRET_KEY = "supersecretkey"

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login", response_model=AuthResponse)
def login(auth: AuthRequest, db: Session = Depends(get_db)):
    user = get_user_by_username(db, auth.username)
    if not user or not bcrypt.verify(auth.password, user.password_hash):
        raise HTTPException(401, "Invalid credentials")
    payload = {
        "sub": user.user_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return AuthResponse(access_token=token)
