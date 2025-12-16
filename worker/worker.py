import pika
import json
import time
from sqlalchemy.orm import Session
from database.database import SessionLocal
from services.task_service import update_task_status
from models_orm.task_orm import TaskStatus
from models.ml_model import TextAnalyzerModel


RABBITMQ_HOST = "rabbitmq"
QUEUE_NAME = "ml_tasks"

def simulate_prediction(text: str):
    model = TextAnalyzerModel(model_name="text_analyzer", cost_per_request=0)
    return model.analyze(text)

def process_task(ch, method, properties, body):
    print(" [*] Received", body)

    payload = json.loads(body)
    task_id = payload["task_id"]
    text = payload["text"]

    db: Session = SessionLocal()

    try:
        update_task_status(db, task_id, TaskStatus.in_progress)

        result = simulate_prediction(text)

        update_task_status(db, task_id, TaskStatus.completed, result=result)

    except Exception as ex:
        print("[ERROR]:", ex)
        update_task_status(db, task_id, TaskStatus.failed)

    finally:
        db.close()

    ch.basic_ack(delivery_tag=method.delivery_tag)


def start_worker():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST)
    )
    channel = connection.channel()

    channel.queue_declare(queue=QUEUE_NAME, durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=process_task)

    print(" [*] Worker started. Waiting for tasks…")
    channel.start_consuming()


if __name__ == "__main__":
    start_worker()
