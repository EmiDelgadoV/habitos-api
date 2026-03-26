from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from app.database import engine
from app import models
from app.routers import auth, habits

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Hábitos API",
    description="API para gestionar hábitos diarios",
    version="1.0.0"
)

app.include_router(auth.router)
app.include_router(habits.router)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def serve_frontend():
    return FileResponse("static/index.html")

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content={"detail": "Error interno del servidor"}
    )

@app.get("/health")
def health_check() -> dict:
    return {"status": "ok"}