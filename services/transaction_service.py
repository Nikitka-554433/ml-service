from sqlalchemy.orm import Session
from models_orm.transaction_orm import TransactionORM, TransactionType

def create_transaction(db: Session, user_id: int, amount: float, tx_type: TransactionType):
    tx = TransactionORM(user_id=user_id, amount=amount, type=tx_type)
    db.add(tx)
    db.commit()
    db.refresh(tx)
    return tx

def get_user_transactions(db: Session, user_id: int):
    return db.query(TransactionORM).filter(TransactionORM.user_id == user_id).all()
