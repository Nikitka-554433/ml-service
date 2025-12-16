from sqlalchemy.orm import Session
from models_orm.user_orm import UserORM
from models_orm.transaction_orm import TransactionORM, TransactionType

def deposit(db: Session, user_id: int, amount: float):
    """
    Пополнение баланса пользователя.
    """
    user = db.query(UserORM).filter(UserORM.user_id == user_id).first()
    if not user:
        return None
    
    # Увеличиваем баланс
    user.balance += amount
    
    # Создаём транзакцию
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
    """
    Списание средств за выполнение задачи.
    Возвращает True, если списание прошло успешно, иначе False.
    """
    user = db.query(UserORM).filter(UserORM.user_id == user_id).first()
    if not user:
        return False
    
    if user.balance < price:
        return False  # недостаточно средств

    # Списание
    user.balance -= price
    tx = TransactionORM(
        user_id=user_id,
        amount=-price,
        type=TransactionType.analysis
    )

    db.add(tx)
    db.commit()
    return True
