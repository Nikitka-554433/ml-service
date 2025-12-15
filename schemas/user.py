from pydantic import BaseModel, EmailStr
from models_orm.user_orm import UserRole

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: UserRole = UserRole.user

class UserRead(BaseModel):
    user_id: int
    username: str
    email: EmailStr
    balance: float
    role: UserRole

    class Config:
        orm_mode = True
