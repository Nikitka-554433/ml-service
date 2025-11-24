from database.database import Base, engine
from models_orm import user_orm, ml_model_orm, task_orm, transaction_orm
from services.user_service import create_user
from services.task_service import create_task

from sqlalchemy.orm import Session

print("Creating tables...")
Base.metadata.create_all(bind=engine)

# Инициализация демо-данных
session = Session(bind=engine)

# Пользователи
admin = create_user("admin", "admin@example.com", balance=1000.0, role="admin")
user1 = create_user("user1", "user1@example.com", balance=200.0)
user2 = create_user("user2", "user2@example.com", balance=50.0)

# ML-модели
from models_orm.ml_model_orm import MLModelORM

sentiment_model = MLModelORM(model_name="sentiment", cost_per_request=2.0)
toxicity_model = MLModelORM(model_name="toxicity", cost_per_request=1.5)

session.add_all([sentiment_model, toxicity_model])
session.commit()

# Простейшие задачи анализа
create_task(user1.user_id, sentiment_model.model_id, "This is a test text")
create_task(user2.user_id, toxicity_model.model_id, "This is another test")
