from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from database import Base


class TransactionORM(Base):
    __tablename__ = "transactions"

    transaction_id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.user_id"))
    amount = Column(Float, nullable=False)
    type = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("UserORM", back_populates="transactions")
