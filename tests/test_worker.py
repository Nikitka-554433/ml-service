import pytest
from services.task_service import create_task, get_task, TaskStatus, create_prediction
from database.database import SessionLocal

def test_worker_process_task():
    db = SessionLocal()
    # создание тестовой задачи
    task = create_task(db, user_id=1, model_id=1, text="Test text")
    
    # имитация тела RabbitMQ
    task_data = {"task_id": task.task_id, "text": task.text}
    
    # вызов воркера напрямую
    prediction = create_prediction(db, task_data)
    
    # результат
    updated_task = get_task(db, task.task_id)
    assert updated_task.status == TaskStatus.COMPLETED
    assert updated_task.result == prediction

    db.close()
