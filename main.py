# main.py
from fastapi import FastAPI

from routers.auth import router as auth_router
from routers.balance import router as balance_router
from routers.tasks import router as tasks_router
from routers.users import router as users_router

app = FastAPI(title="ML-Service API", version="1.0")


@app.get("/")
def root():
    return {"message": "ML Service API is running"}


app.include_router(auth_router)
app.include_router(balance_router)
app.include_router(tasks_router)
app.include_router(users_router)
