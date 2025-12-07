from sqlalchemy import Column, Integer, String, Enum, ForeignKey, JSON
from sqlalchemy.orm import relationship
import enum
from database.database import Base

class TaskStatus(enum.Enum):
    created = "created"
    in_progress = "in_progress"
    completed = "completed"
    failed = "failed"

class TaskORM(Base):
    __tablename__ = "tasks"

    task_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    model_id = Column(Integer, ForeignKey("ml_models.model_id"))
    text = Column(String, nullable=False)
    status = Column(Enum(TaskStatus), default=TaskStatus.created)
    result = Column(JSON, nullable=True)

    user = relationship("UserORM", back_populates="tasks")
    model = relationship("MLModelORM", back_populates="tasks")


