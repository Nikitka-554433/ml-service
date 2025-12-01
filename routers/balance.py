# balance.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import get_db
from services.user_service import get_user
from services.transaction_service import create_transaction, get_user_transactions
from models_orm.transaction_orm import TransactionType

router = APIRouter(prefix="/balance", tags=["balance"])


@router.post("/deposit/{user_id}")
def deposit(user_id: int, amount: float, db: Session = Depends(get_db)):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(404, "User not found")

    user.balance += amount
    create_transaction(db, user_id, amount, TransactionType.deposit)

    db.commit()
    return {"message": "Balance updated", "balance": user.balance}


@router.get("/history/{user_id}")
def transaction_history(user_id: int, db: Session = Depends(get_db)):
    return get_user_transactions(db, user_id)
