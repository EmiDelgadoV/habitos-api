from fastapi import FastAPI
from app.database import engine
from app import models
from app.routers import auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Hábitos API",
    description="API para gestionar hábitos diarios",
    version="1.0.0"
)

app.include_router(auth.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}