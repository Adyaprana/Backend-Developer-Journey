from fastapi import FastAPI

import models  # noqa: F401 — ensure models are registered with Base
from database import Base, engine, ensure_schema
from routers import auth, users

app = FastAPI(
    title="Backend Learning API",
    description="FastAPI + PostgreSQL with JWT authentication",
)

ensure_schema()
Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(users.router)


@app.get("/")
def home():
    return {
        "message": "FastAPI + PostgreSQL working!",
        "docs": "/docs",
        "steps": [
            "POST /register with name, email, password",
            "Click Authorize in /docs — email goes in username, then password",
            "Call protected /users routes",
        ],
    }
