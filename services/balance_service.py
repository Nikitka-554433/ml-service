from sqlalchemy.orm import Session
from models_orm.user_orm import UserORM
from models_orm.transaction_orm import TransactionORM, TransactionType

def deposit(db: Session, user_id: int, amount: float):
    user = db.query(UserORM).filter(UserORM.user_id == user_id).first()
    if not user:
        return None
    
    user.balance += amount
    tx = TransactionORM(
        user_id=user_id,
        amount=amount,
        type=TransactionType.deposit
    )
    
    db.add(tx)
    db.commit()
    db.refresh(user)
    return user

def charge_for_task(db: Session, user_id: int, price: float) -> bool:
    user = db.query(UserORM).filter(UserORM.user_id == user_id).first()
    if not user:
        return False
    
    if user.balance < price:
        return False

    user.balance -= price
    tx = TransactionORM(
        user_id=user_id,
        amount=-price,
        type=TransactionType.analysis
    )

    db.add(tx)
    db.commit()
    return True
