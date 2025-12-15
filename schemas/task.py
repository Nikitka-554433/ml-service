from pydantic import BaseModel
from typing import Optional, Dict
from models_orm.task_orm import TaskStatus
from pydantic import validator

class TaskCreate(BaseModel):
    model_id: int
    text: str

    @validator("text")
    def text_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Text cannot be empty")
        return v

class TaskRead(BaseModel):
    task_id: int
    user_id: int
    model_id: int
    text: str
    status: TaskStatus
    result: Optional[Dict] = None

    class Config:
        orm_mode = True
