from database.database import Base, engine
from sqlalchemy.orm import Session

from models_orm.user_orm import UserORM, UserRole
from models_orm.ml_model_orm import MLModelORM
from passlib.hash import bcrypt

print("Creating tables...")
Base.metadata.create_all(bind=engine)

session = Session(bind=engine)

# Пользователи
admin = UserORM(
    username="admin",
    email="admin@example.com",
    password_hash=bcrypt.hash("adminpass"),
    balance=1000.0,
    role=UserRole.admin
)

demo = UserORM(
    username="demo",
    email="demo@example.com",
    password_hash=bcrypt.hash("demo123"),
    balance=200.0,
    role=UserRole.user
)

session.add(admin)
session.add(demo)

# ML-модели
sentiment = MLModelORM(model_name="sentiment", cost_per_request=2.0)
toxicity = MLModelORM(model_name="toxicity", cost_per_request=1.5)

session.add_all([sentiment, toxicity])
session.commit()
session.close()

