from database.database import Base, engine, SessionLocal
from models_orm import user_orm, task_orm, transaction_orm, ml_model_orm
from services.user_service import create_user
from models_orm.user_orm import UserRole
from models_orm.ml_model_orm import MLModelORM

print("Creating tables…")
Base.metadata.create_all(bind=engine)

db = SessionLocal()

# Users
admin = create_user(db, "admin", "admin@example.com", "admin123", role=UserRole.admin)
demo = create_user(db, "demo", "demo@example.com", "demo123")

# ML models
sentiment = MLModelORM(model_name="sentiment", cost_per_request=2.0)
toxicity = MLModelORM(model_name="toxicity", cost_per_request=1.5)

db.add_all([sentiment, toxicity])
db.commit()

db.close()
print("Init completed.")
