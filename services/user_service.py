from sqlalchemy.orm import Session
from passlib.hash import bcrypt

from models_orm.user_orm import UserORM, UserRole
from models_orm.transaction_orm import TransactionType
from services.transaction_service import create_transaction

def create_user(db: Session, username: str, email: str, password: str, balance=0.0, role=UserRole.user):
    hashed = bcrypt.hash(password)

    user = UserORM(
        username=username,
        email=email,
        password_hash=hashed,
        balance=balance,
        role=role
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user(db: Session, user_id: int):
    return db.query(UserORM).filter(UserORM.user_id == user_id).first()

def add_balance(db: Session, user_id: int, amount: float):
    user = get_user(db, user_id)
    if not user:
        return None

    user.balance += amount
    db.commit()
    db.refresh(user)

    create_transaction(db, user_id, amount, TransactionType.deposit)
    return user

def deduct_balance(db: Session, user_id: int, amount: float):
    user = get_user(db, user_id)
    if not user or user.balance < amount:
        return None

    user.balance -= amount
    db.commit()
    db.refresh(user)

    create_transaction(db, user_id, amount, TransactionType.analysis)
    return user

def get_balance(db: Session, user_id: int):
    user = get_user(db, user_id)
    return user.balance if user else None

