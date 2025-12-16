from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas.transaction import TransactionCreate, TransactionRead
from services.transaction_service import create_transaction, get_user_transactions
from database.database import get_db
from typing import List

router = APIRouter(prefix="/transactions", tags=["Transactions"])

@router.post("/", response_model=TransactionRead)
def create_transaction_api(tx: TransactionCreate, db: Session = Depends(get_db)):
    return create_transaction(db, tx.user_id, tx.amount, tx.type)

@router.get("/{user_id}", response_model=List[TransactionRead])
def get_user_transactions_api(user_id: int, db: Session = Depends(get_db)):
    return get_user_transactions(db, user_id)
