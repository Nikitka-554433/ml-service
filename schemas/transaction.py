from pydantic import BaseModel
from models_orm.transaction_orm import TransactionType

class TransactionCreate(BaseModel):
    user_id: int
    amount: float
    type: TransactionType

class TransactionRead(BaseModel):
    transaction_id: int
    user_id: int
    amount: float
    type: TransactionType

    class Config:
        orm_mode = True
