from pydantic import BaseModel
from typing import Optional, Dict
from models_orm.task_orm import TaskStatus

class TaskCreate(BaseModel):
    model_id: int
    text: str

class TaskRead(BaseModel):
    task_id: int
    user_id: int
    model_id: int
    text: str
    status: TaskStatus
    result: Optional[Dict] = None

    class Config:
        orm_mode = True
