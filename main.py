from fastapi import FastAPI
from routers import tasks

app = FastAPI(title="ML Service API")

# Подключаем роутеры
app.include_router(tasks.router)

@app.get("/")
def root():
    return {"message": "ML Service is running"}

