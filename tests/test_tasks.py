import json
import pytest
from services.task_service import get_task, TaskStatus

def test_create_task_endpoint(client, db):
    # Тестовая задача через API
    response = client.post(
        "/tasks/create",
        json={"user_id": 1, "model_id": 1, "text": "Hello world"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "task_id" in data

    # Задача в базе
    task = get_task(db, data["task_id"])
    assert task is not None
    assert task.status == TaskStatus.PENDING
