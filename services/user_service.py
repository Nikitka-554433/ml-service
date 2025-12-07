from sqlalchemy.orm import Session
from models_orm.user_orm import UserORM, UserRole
from passlib.hash import bcrypt

def create_user(db: Session, username: str, email: str, password: str, role=UserRole.user):
    hashed = bcrypt.hash(password)
    user = UserORM(username=username, email=email, password_hash=hashed, role=role)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user(db: Session, user_id: int):
    return db.query(UserORM).filter(UserORM.user_id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(UserORM).filter(UserORM.username == username).first()

def list_users(db: Session):
    return db.query(UserORM).all()
