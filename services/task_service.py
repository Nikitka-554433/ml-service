from sqlalchemy.orm import Session
from models_orm.task_orm import TaskORM, TaskStatus
from models.ml_model import MLModel

def create_task(db: Session, user_id: int, model_id: int, text: str):
    task = TaskORM(user_id=user_id, model_id=model_id, text=text)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def update_task_status(db: Session, task_id: int, status: TaskStatus, result=None):
    task = db.query(TaskORM).filter(TaskORM.task_id == task_id).first()
    if task:
        task.status = status
        if result is not None:
            task.result = result
        db.commit()
        db.refresh(task)
    return task

def get_task(db: Session, task_id: int):
    return db.query(TaskORM).filter(TaskORM.task_id == task_id).first()

def get_user_tasks(db: Session, user_id: int):
    return db.query(TaskORM).filter(TaskORM.user_id == user_id).all()

ml_model = MLModel()  # экземпляр модели

def create_prediction(db: Session, task_data: dict):
    """
    Запускает ML-модель на тексте задачи и сохраняет результат в БД.
    """
    task_id = task_data["task_id"]
    text = task_data["text"]

    # предсказание от модели
    prediction = ml_model.predict(text)

    #Обновляем задачу в БД с результатом
    update_task_status(db, task_id, TaskStatus.COMPLETED, result=prediction)

    return prediction

