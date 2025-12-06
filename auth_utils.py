# auth_utils.py
import jwt
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database.database import get_db
from models_orm.user_orm import UserORM
import os

SECRET = os.getenv("JWT_SECRET", "secret123")
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def create_token(user_id: int):
    return jwt.encode({"user_id": user_id}, SECRET, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        data = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        user = db.query(UserORM).filter(UserORM.user_id == data["user_id"]).first()
        if not user:
            raise HTTPException(401, "Invalid token")
        return user
    except:
        raise HTTPException(401, "Invalid token")
