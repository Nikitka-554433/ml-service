import time
import json
import pika
from sqlalchemy.orm import Session
from database.database import SessionLocal
from services.task_service import update_task_result, get_task_by_id
from models.ml_model import MLModel

# Подключение к RabbitMQ
RABBITMQ_HOST = "rabbitmq"
QUEUE_NAME = "task_queue"

ml_model = MLModel()  # глобальный экземпляр модели

def process_task(ch, method, properties, body):
    task_data = json.loads(body)
    task_id = task_data["task_id"]
    text = task_data["text"]

    print(f"[Worker] Processing task {task_id}")

    result = ml_model.predict(text)

    # Сохраняем результат в БД
    db: Session = SessionLocal()
    update_task_result(db, task_id, result)
    db.close()

    ch.basic_ack(delivery_tag=method.delivery_tag)
    print(f"[Worker] Task {task_id} done")

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME, durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=process_task)
    print("[Worker] Waiting for tasks...")
    channel.start_consuming()

if __name__ == "__main__":
    main()


