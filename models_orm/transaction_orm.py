from sqlalchemy import Column, Integer, Float, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship
import enum
from database.database import Base
from datetime import datetime

class TransactionType(enum.Enum):
    deposit = "deposit"
    analysis = "analysis"


class TransactionORM(Base):
    __tablename__ = "transactions"

    transaction_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    amount = Column(Float, nullable=False)
    type = Column(Enum(TransactionType), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("UserORM", back_populates="transactions")
