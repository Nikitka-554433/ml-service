# main.py
from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from routers import tasks, auth, users, transactions, web
from database.database import get_db, Base, engine

app = FastAPI(title="ML Service API")

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

# API роутеры
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
app.include_router(transactions.router, prefix="/transactions", tags=["transactions"])

# Веб
app.include_router(web.router, tags=["web"])

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/")
def root():
    return {"message": "ML Service is running"}
