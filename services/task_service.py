from database.database import SessionLocal
from models_orm.task_orm import AnalysisTaskORM
from datetime import datetime

db = SessionLocal()

def create_task(user_id, model_id, text):
    task = AnalysisTaskORM(
        user_id=user_id,
        model_id=model_id,
        text=text,
        status="created",
        timestamp=datetime.utcnow()
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def update_task_status(task_id, status, result=None):
    task = db.query(AnalysisTaskORM).filter(AnalysisTaskORM.task_id == task_id).first()
    if task:
        task.status = status
        task.result = result
        db.commit()
        db.refresh(task)
        return task
    return None

def get_user_tasks(user_id):
    return db.query(AnalysisTaskORM).filter(AnalysisTaskORM.user_id == user_id).all()
