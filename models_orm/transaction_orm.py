from sqlalchemy import Column, Integer, Float, Enum, ForeignKey
from sqlalchemy.orm import relationship
import enum
from database.database import Base

class TransactionType(enum.Enum):
    deposit = "deposit"
    analysis = "analysis"

class TransactionORM(Base):
    __tablename__ = "transactions"

    transaction_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    amount = Column(Float, nullable=False)
    type = Column(Enum(TransactionType), nullable=False)

    user = relationship("UserORM", back_populates="transactions")
