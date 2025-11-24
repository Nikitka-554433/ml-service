from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from datetime import datetime

from database import Base


class AnalysisTaskORM(Base):
    __tablename__ = "analysis_tasks"

    task_id = Column(Integer, primary_key=True, index=True)
    
    user_id = Column(Integer, ForeignKey("users.user_id"))
    model_id = Column(Integer, ForeignKey("ml_models.model_id"))

    text = Column(String, nullable=False)
    status = Column(String, default="created")
    result = Column(JSON, nullable=True)

    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("UserORM", back_populates="tasks")
    model = relationship("MLModelORM", back_populates="tasks")
