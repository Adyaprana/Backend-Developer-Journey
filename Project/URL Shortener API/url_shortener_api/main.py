from fastapi import FastAPI
from app.database.base import Base
from app.database.database import engine
from app.models.shortened_url import ShortenedURL

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="URL Shortener API",
    version="1.0.0",
    description="A URL Shortener API built with FastAPI and PostgreSQL."
)

@app.get("/")
def root():
    return {
        "message": "Welcome to URL Shortener API 🚀"
    }

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )