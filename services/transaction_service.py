from database.database import SessionLocal
from models_orm.transaction_orm import TransactionORM
from datetime import datetime

db = SessionLocal()

def create_transaction(user_id, amount, t_type):
    tx = TransactionORM(user_id=user_id, amount=amount, type=t_type, timestamp=datetime.utcnow())
    db.add(tx)
    db.commit()
    db.refresh(tx)
    return tx

def get_transactions(user_id):
    return db.query(TransactionORM).filter(TransactionORM.user_id == user_id).all()
