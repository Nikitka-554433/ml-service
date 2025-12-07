# balance.py
from pydantic import BaseModel

class BalanceUpdate(BaseModel):
    amount: float

class BalanceRead(BaseModel):
    balance: float