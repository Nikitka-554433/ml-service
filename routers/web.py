from fastapi import APIRouter, Request, Form, Depends, Response
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from services.user_service import create_user, get_user_by_username, verify_password, create_access_token
from database.database import get_db
from services.task_service import get_user_tasks
from fastapi.responses import RedirectResponse
from jose import jwt, JWTError
from services.balance_service import deposit
from services.transaction_service import get_user_transactions
from services.task_service import create_task_and_predict
from services.balance_service import charge_for_task
from models_orm.user_orm import UserORM

templates = Jinja2Templates(directory="templates")
router = APIRouter()

SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"

def get_current_user_dep(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    if not token:
        return None
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        return db.query(UserORM).filter(UserORM.user_id == user_id).first()
    except JWTError:
        return None

@router.get("/register")
def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@router.post("/register")
def register_user(request: Request, username: str = Form(...), email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    if get_user_by_username(db, username):
        return templates.TemplateResponse("register.html", {"request": request, "error": "Пользователь уже существует"})
    user = create_user(db, username, email, password)
    response = RedirectResponse("/login", status_code=302)
    return response

@router.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
def login_user(request: Request, response: Response, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = get_user_by_username(db, username)
    if not user or not verify_password(password, user.password_hash):
        return templates.TemplateResponse("login.html", {"request": request, "error": "Неверный логин или пароль"})
    token = create_access_token({"sub": user.user_id})
    response = RedirectResponse("/dashboard", status_code=302)
    response.set_cookie(key="access_token", value=token, httponly=True)
    return response

@router.get("/logout")
def logout_user():
    response = RedirectResponse("/login", status_code=302)
    response.delete_cookie("access_token")
    return response

@router.get("/dashboard")
def dashboard(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if not user:
        return RedirectResponse("/login")
    tasks_list = get_user_tasks(db, user.user_id)
    return templates.TemplateResponse("dashboard.html", {"request": request, "user": user, "tasks": tasks_list})

# Пополнение
@router.post("/deposit")
def deposit_money(request: Request, amount: float = Form(...), db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if not user:
        return RedirectResponse("/login")

    deposit(db, user.user_id, amount)
    return RedirectResponse("/dashboard")

# Создание задачи через WEB
@router.get("/create_task")
def create_task_page(request: Request):
    return templates.TemplateResponse("create_task.html", {"request": request})

@router.post("/create_task")
def create_task_web(
    request: Request,
    db: Session = Depends(get_db),
    model_id: int = Form(...),
    text: str = Form(...)
):
    user = get_current_user(request, db)
    if not user:
        return RedirectResponse("/login")

    price = max(1, len(text) * 0.01)  
    if not charge_for_task(db, user.user_id, price):
        return templates.TemplateResponse("create_task.html", {
            "request": request,
            "error": "Недостаточно средств!"
        })

    task = create_task_and_predict(
    db=db,
    user_id=user.user_id,
    model_id=model_id,
    text=text
)
    return RedirectResponse("/dashboard")

# История транзакций
@router.get("/transactions")
def view_transactions(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if not user:
        return RedirectResponse("/login")

    txs = get_user_transactions(db, user.user_id)
    return templates.TemplateResponse("transactions.html", {
        "request": request,
        "transactions": txs
    })


