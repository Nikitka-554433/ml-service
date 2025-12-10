from fastapi import FastAPI, Request, Form, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from passlib.hash import bcrypt

# Импорт роутеров API
from routers import tasks, auth, users, transactions, web
from database.database import get_db
from services.user_service import get_user_by_username
from services.task_service import get_user_tasks
from services.transaction_service import get_user_transactions
from routers import web

app = FastAPI(title="ML Service API")

# REST API роутеры
app.include_router(tasks.router)
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(transactions.router)
app.include_router(web.router)


# Роутер веб-интерфейса
app.include_router(web.router)

# Статические файлы и шаблоны
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Корневой маршрут
@app.get("/")
def root():
    return {"message": "ML Service is running"}

# Пример dashboard
@app.get("/dashboard")
def dashboard(request: Request, user_id: int = 1, db: Session = Depends(get_db)):
    user = get_user_by_username(db, username="demo")  # для теста
    tasks_list = get_user_tasks(db, user.user_id)
    transactions_list = get_user_transactions(db, user.user_id)
    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "user": user, "tasks": tasks_list, "transactions": transactions_list}
    )
