# balance.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from services.user_service import get_user
from services.transaction_service import create_transaction, get_user_transactions
from models_orm.transaction_orm import TransactionType
from database.database import get_db
from auth_utils import get_current_user

router = APIRouter(prefix="/balance", tags=["balance"])

@router.post("/deposit")
def deposit(amount: float, db: Session = Depends(get_db), user=Depends(get_current_user)):
    user.balance += amount
    create_transaction(db, user.user_id, amount, TransactionType.deposit)
    db.commit()
    return {"balance": user.balance}

@router.get("/history")
def history(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return get_user_transactions(db, user.user_id)
