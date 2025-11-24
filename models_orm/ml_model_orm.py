from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from database import Base


class MLModelORM(Base):
    __tablename__ = "ml_models"

    model_id = Column(Integer, primary_key=True, index=True)
    model_name = Column(String, nullable=False)
    cost_per_request = Column(Float, nullable=False)

    tasks = relationship("AnalysisTaskORM", back_populates="model")
