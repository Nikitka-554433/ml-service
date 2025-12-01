from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, JSON, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum as PyEnum

from database import Base

class TaskStatus(PyEnum):
    created = "created"
    completed = "completed"
    failed = "failed"

class AnalysisTaskORM(Base):
    __tablename__ = "analysis_tasks"

    task_id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    model_id = Column(Integer, ForeignKey("ml_models.model_id"), nullable=False)

    text = Column(String, nullable=False)
    status = Column(Enum(TaskStatus), default=TaskStatus.created)

    result = Column(JSON, nullable=True)

    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("UserORM", back_populates="tasks")
    model = relationship("MLModelORM", back_populates="tasks")

