# worker.py
import json
import pika
from sqlalchemy.orm import Session
from database.database import SessionLocal
from services.task_service import create_prediction

RABBITMQ_HOST = "rabbitmq"
QUEUE_NAME = "task_queue"

def process_task(ch, method, properties, body):
    task_data = json.loads(body)
    print(f"[Worker] Processing task {task_data['task_id']}")

    # Работа с БД
    db: Session = SessionLocal()
    create_prediction(db, task_data)
    db.close()

    ch.basic_ack(delivery_tag=method.delivery_tag)
    print(f"[Worker] Task {task_data['task_id']} done")

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



