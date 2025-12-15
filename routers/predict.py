from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.database import get_db
from schemas.task import TaskCreate, TaskRead
from services.task_service import create_task
import json
import pika

router = APIRouter()

RABBITMQ_HOST = "rabbitmq"
QUEUE_NAME = "task_queue"

@router.post("/create", response_model=TaskRead)
def create_task_endpoint(task: TaskCreate, db: Session = Depends(get_db)):
    db_task = create_task(db, task.user_id, task.model_id, task.text)
    
    # Отправляем задачу в очередь RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME, durable=True)
    channel.basic_publish(
        exchange="",
        routing_key=QUEUE_NAME,
        body=json.dumps({"task_id": db_task.task_id, "text": task.text}),
        properties=pika.BasicProperties(delivery_mode=2)
    )
    connection.close()

    return db_task

@router.post("/predict", response_model=TaskRead)
def predict(task: TaskCreate, db: Session = Depends(get_db)):
    """
    Создаём задачу и сразу запускаем предсказание через воркер.
    """
    db_task = create_task(db, task.user_id, task.model_id, task.text)

    # Отправляем задачу в RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME, durable=True)
    channel.basic_publish(
        exchange="",
        routing_key=QUEUE_NAME,
        body=json.dumps({"task_id": db_task.task_id, "text": task.text}),
        properties=pika.BasicProperties(delivery_mode=2)
    )
    connection.close()

    return db_task

