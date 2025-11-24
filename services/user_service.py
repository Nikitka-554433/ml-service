from database.database import SessionLocal
from models_orm.user_orm import UserORM
from models_orm.transaction_orm import TransactionORM

db = SessionLocal()

def create_user(username, email, balance=0.0, role="user"):
    user = UserORM(username=username, email=email, balance=balance, role=role)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user(user_id):
    return db.query(UserORM).filter(UserORM.user_id == user_id).first()

def add_balance(user_id, amount):
    user = get_user(user_id)
    if user:
        user.balance += amount
        db.commit()
        db.refresh(user)
        # Создать транзакцию
        from services.transaction_service import create_transaction
        create_transaction(user_id, amount, "deposit")
        return user
    return None

def deduct_balance(user_id, amount):
    user = get_user(user_id)
    if user and user.balance >= amount:
        user.balance -= amount
        db.commit()
        db.refresh(user)
        # Создать транзакцию
        from services.transaction_service import create_transaction
        create_transaction(user_id, amount, "analyze")
        return True
    return False

def get_balance(user_id):
    user = get_user(user_id)
    return user.balance if user else None
