from fastapi import FastAPI

app = FastAPI(
    title="Hábitos API",
    description="API para gestionar hábitos diarios",
    version="1.0.0"
)

@app.get("/health")
def health_check():
    return {"status": "ok"}