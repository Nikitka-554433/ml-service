from sqlalchemy import Column, Integer, String, Float, Enum
from sqlalchemy import Column, Integer, String, Float, Enum
from sqlalchemy.orm import relationship
import enum
from database.database import Base

class UserRole(enum.Enum):
    user = "user"
    admin = "admin"

class UserORM(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    balance = Column(Float, default=0.0)
    role = Column(Enum(UserRole), default=UserRole.user)

    tasks = relationship("TaskORM", back_populates="user")
    transactions = relationship("TransactionORM", back_populates="user")
