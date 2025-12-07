from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import pika
import json
from typing import List

from database.database import get_db
from services.task_service import create_task, get_task, get_user_tasks
from schemas.task import TaskCreate, TaskRead

# Создаём роутер в начале
router = APIRouter(prefix="/tasks", tags=["Tasks"])

# Конфигурация RabbitMQ
RABBITMQ_HOST = "rabbitmq"
QUEUE_NAME = "ml_tasks"

# Функция отправки сообщений в RabbitMQ
def publish_task_message(task_id: int, text: str, model_id: int, user_id: int):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST)
    )
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME, durable=True)

    payload = {
        "task_id": task_id,
        "text": text,
        "model_id": model_id,
        "user_id": user_id,
    }

    channel.basic_publish(
        exchange="",
        routing_key=QUEUE_NAME,
        body=json.dumps(payload),
        properties=pika.BasicProperties(delivery_mode=2)
    )
    connection.close()

# Создание задачи
@router.post("/", response_model=TaskRead)
def create_task_api(task_data: TaskCreate, db: Session = Depends(get_db), user_id: int = 1):
    task = create_task(db, user_id=user_id, model_id=task_data.model_id, text=task_data.text)
    publish_task_message(task.task_id, task.text, task.model_id, task.user_id)
    return task

# Получение одной задачи
@router.get("/{task_id}", response_model=TaskRead)
def get_task_api(task_id: int, db: Session = Depends(get_db)):
    task = get_task(db, task_id)
    if not task:
        raise HTTPException(404, "Task not found")
    return task

# Получение всех задач пользователя
@router.get("/", response_model=List[TaskRead])
def get_user_tasks_api(user_id: int = 1, db: Session = Depends(get_db)):
    tasks = get_user_tasks(db, user_id)
    return tasks


