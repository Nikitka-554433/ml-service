# tasks.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from services.task_service import create_task, get_task, get_user_tasks
from services.transaction_service import create_transaction
from services.user_service import get_user
from models_orm.transaction_orm import TransactionType
from schemas.task import TaskCreate, TaskRead
from auth_utils import get_current_user
from database.database import get_db

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("/create", response_model=TaskRead)
def make_task(
    data: TaskCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    # Проверка баланса
    model_cost = db.execute(
        "SELECT cost_per_request FROM ml_models WHERE model_id=:id",
        {"id": data.model_id}
    ).fetchone()[0]

    if user.balance < model_cost:
        raise HTTPException(400, "Insufficient funds")

    # списание баланса
    user.balance -= model_cost
    create_transaction(db, user.user_id, -model_cost, TransactionType.analysis)

    db.commit()

    return create_task(db, user.user_id, data.model_id, data.text)

@router.get("/{task_id}", response_model=TaskRead)
def read_task(task_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    task = get_task(db, task_id)
    if not task or task.user_id != user.user_id:
        raise HTTPException(404, "Task not found")
    return task
