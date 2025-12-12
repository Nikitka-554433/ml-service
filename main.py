from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from routers import tasks, auth, users, transactions, web
from database.database import get_db

app = FastAPI(title="ML Service API")

# Подключаем API роутеры
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
app.include_router(transactions.router, prefix="/transactions", tags=["transactions"])

# Веб-интерфейс
app.include_router(web.router, tags=["web"])

# Статика и шаблоны
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/")
def root():
    return {"message": "ML Service is running"}

@app.get("/dashboard")
def dashboard(request: Request, user_id: int = 1, db: Session = Depends(get_db)):
    from services.user_service import get_user_by_id
    from services.task_service import get_user_tasks
    from services.transaction_service import get_user_transactions

    user = get_user_by_id(db, user_id)
    tasks_list = get_user_tasks(db, user.user_id)
    transactions_list = get_user_transactions(db, user.user_id)
    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "user": user, "tasks": tasks_list, "transactions": transactions_list}
    )

