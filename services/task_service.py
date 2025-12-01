from sqlalchemy.orm import Session
from datetime import datetime
from models_orm.task_orm import AnalysisTaskORM, TaskStatus


def create_task(db: Session, user_id: int, model_id: int, text: str):
    task = AnalysisTaskORM(
        user_id=user_id,
        model_id=model_id,
        text=text,
        status=TaskStatus.created,
        timestamp=datetime.utcnow()
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def get_task(db: Session, task_id: int):
    return db.query(AnalysisTaskORM).filter(AnalysisTaskORM.task_id == task_id).first()


def get_user_tasks(db: Session, user_id: int):
    return db.query(AnalysisTaskORM).filter(
        AnalysisTaskORM.user_id == user_id
    ).all()


def update_task_status(db: Session, task_id: int, status: TaskStatus, result=None):
    task = get_task(db, task_id)
    if not task:
        return None

    task.status = status
    task.result = result

    db.commit()
    db.refresh(task)
    return task

