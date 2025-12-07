from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from database.database import Base

class MLModelORM(Base):
    __tablename__ = "ml_models"

    model_id = Column(Integer, primary_key=True)
    model_name = Column(String, unique=True)
    cost_per_request = Column(Float, nullable=False)

    tasks = relationship("TaskORM", back_populates="model")
