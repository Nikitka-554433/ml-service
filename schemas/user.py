# user.py
from pydantic import BaseModel, EmailStr
from enum import Enum
from typing import Optional

class UserRole(str, Enum):
    user = "user"
    admin = "admin"

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserRead(BaseModel):
    user_id: int
    username: str
    email: EmailStr
    balance: float
    role: UserRole

    class Config:
        orm_mode = True
