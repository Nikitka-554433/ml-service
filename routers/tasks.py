from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import get_db
from schemas.task import TaskCreate, TaskRead
from services.task_service import create_task_and_predict

router = APIRouter()

@router.post("/create", response_model=TaskRead)
def create_task_endpoint(
    task: TaskCreate,
    db: Session = Depends(get_db)
):
    try:

        return create_task_and_predict(
            db=db,
            user_id=1,
            model_id=task.model_id,
            text=task.text
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

