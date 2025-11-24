from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from database import Base


class UserORM(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    balance = Column(Float, default=0.0)
    role = Column(String, default="user")

    tasks = relationship("AnalysisTaskORM", back_populates="user")
    transactions = relationship("TransactionORM", back_populates="user")
