from fastapi import FastAPI
from .database import Base, engine
from .models import User, Category, Task  # noqa: F401

app = FastAPI(title="TODO App API", version="0.1.0")

Base.metadata.create_all(bind=engine)


@app.get("/api/health")
async def health_check():
    return {"status": "ok"}
