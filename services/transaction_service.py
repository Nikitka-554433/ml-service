from database.database import SessionLocal
from models_orm.transaction_orm import Transaction, TransactionType
from datetime import datetime

def add_transaction(db, user_id: int, amount: float, type: TransactionType):
    transaction = Transaction(user_id=user_id, amount=amount, type=type, created_at=datetime.utcnow())
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction

def charge_user(db, user_id: int, amount: float):
    from services.user_service import get_user_by_id, update_user_balance

    user = get_user_by_id(db, user_id)
    if user.balance < amount:
        raise Exception("Insufficient balance")
    user.balance -= amount
    update_user_balance(db, user)
    add_transaction(db, user_id, -amount, TransactionType.debit)

