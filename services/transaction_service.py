from database.database import SessionLocal
from models_orm.transaction_orm import TransactionORM, TransactionType
from datetime import datetime

def add_transaction(db, user_id: int, amount: float, type: TransactionType):
    transaction = TransactionORM(user_id=user_id, amount=amount, type=type, created_at=datetime.utcnow())
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction

def get_user_transactions(db, user_id: int):
    return db.query(TransactionORM).filter(TransactionORM.user_id == user_id).all()

def create_transaction(db, user_id: int, amount: float, type: TransactionType):
    # Пример логики для создания транзакции
    return add_transaction(db, user_id, amount, type)


