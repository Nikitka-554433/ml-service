# tasks.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import get_db
from services.task_service import (
    create_task, get_task, update_task_status, get_user_tasks
)
from schemas.task import TaskCreate, TaskRead, TaskStatus

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/create/{user_id}", response_model=TaskRead)
def make_task(user_id: int, data: TaskCreate, db: Session = Depends(get_db)):
    return create_task(db, user_id, data.model_id, data.text)


@router.put("/{task_id}/complete", response_model=TaskRead)
def complete_task(task_id: int, db: Session = Depends(get_db)):
    task = update_task_status(db, task_id, TaskStatus.completed)
    if not task:
        raise HTTPException(404, "Task not found")
    return task


@router.get("/{task_id}", response_model=TaskRead)
def read_task(task_id: int, db: Session = Depends(get_db)):
    task = get_task(db, task_id)
    if not task:
        raise HTTPException(404, "Task not found")
    return task


@router.get("/user/{user_id}", response_model=list[TaskRead])
def user_tasks(user_id: int, db: Session = Depends(get_db)):
    return get_user_tasks(db, user_id)
