# transaction.py
from pydantic import BaseModel
from enum import Enum


class TransactionType(str, Enum):
    deposit = "deposit"
    analysis = "analysis"


class TransactionRead(BaseModel):
    transaction_id: int
    user_id: int
    amount: float
    type: TransactionType

    class Config:
        orm_mode = True
