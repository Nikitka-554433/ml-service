from database import Base, engine
import models_orm.user_orm
import models_orm.ml_model_orm
import models_orm.task_orm
import models_orm.transaction_orm

print("Creating tables...")
Base.metadata.create_all(bind=engine)
