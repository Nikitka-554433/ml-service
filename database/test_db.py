from services.user_service import create_user, add_balance, deduct_balance, get_balance
from services.transaction_service import get_transactions
from services.task_service import create_task, get_user_tasks

def run_tests():
    print("Starting tests...")

    # 1. Создание пользователя
    u = create_user("testuser", "testuser@test.com", balance=10)
    assert u.user_id is not None
    print("User created:", u.username)

    # 2. Пополнение баланса
    add_balance(u.user_id, 100)
    assert get_balance(u.user_id) == 110
    print("Balance after top-up:", get_balance(u.user_id))

    # 3. Списание баланса
    deduct_balance(u.user_id, 50)
    assert get_balance(u.user_id) == 60
    print("Balance after deduction:", get_balance(u.user_id))

    # 4. Проверка транзакций
    txs = get_transactions(u.user_id)
    assert len(txs) >= 2
    print("Transactions count:", len(txs))

    # 5. Создание задачи анализа
    from models_orm.ml_model_orm import MLModelORM
    from database.database import SessionLocal
    session = SessionLocal()
    model = session.query(MLModelORM).first()
    task = create_task(u.user_id, model.model_id, "Test analysis text")
    tasks = get_user_tasks(u.user_id)
    assert len(tasks) >= 1
    print("Tasks count:", len(tasks))

    print("All tests passed successfully!")

if __name__ == "__main__":
    run_tests()
