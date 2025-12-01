# task.py
from pydantic import BaseModel
from typing import Optional
from enum import Enum


class TaskStatus(str, Enum):
    created = "created"
    completed = "completed"
    failed = "failed"


class TaskCreate(BaseModel):
    model_id: int
    text: str


class TaskRead(BaseModel):
    task_id: int
    user_id: int
    model_id: int
    text: str
    status: TaskStatus
    result: Optional[dict] = None

    class Config:
        orm_mode = True
