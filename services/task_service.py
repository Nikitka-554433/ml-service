from sqlalchemy.orm import Session
from models_orm.task_orm import TaskORM, TaskStatus
from models_orm.ml_model_orm import MLModelORM
from services.balance_service import charge_for_task
from models.ml_model import MLModel

ml_model = MLModel()


def create_task_and_predict(
    db: Session,
    user_id: int,
    model_id: int,
    text: str
) -> TaskORM:
    # Проверяем модель
    model = db.query(MLModelORM).filter(
        MLModelORM.model_id == model_id
    ).first()
    if not model:
        raise ValueError("ML model not found")

    # Считаем стоимость
    price = max(1, len(text) * model.cost_per_request)

    # Списываем деньги
    if not charge_for_task(db, user_id, price):
        raise ValueError("Not enough balance")

    # Создаём задачу
    task = TaskORM(
        user_id=user_id,
        model_id=model_id,
        text=text,
        status=TaskStatus.in_progress
    )
    db.add(task)
    db.commit()
    db.refresh(task)

    # ML prediction
    result = ml_model.predict(text)

    # Сохраняем результат
    task.status = TaskStatus.completed
    task.result = result
    db.commit()
    db.refresh(task)

    return task


def get_user_tasks(db: Session, user_id: int):
    return db.query(TaskORM).filter(TaskORM.user_id == user_id).all()

