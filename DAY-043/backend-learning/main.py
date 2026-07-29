from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def home():
    return {"message": "Welcome to my first FastAPI application!"}

@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id}

@app.get("/items")
def get_items(skip: int = 0, limit: int = 10):
    return {
        "skip": skip,
        "limit": limit
    }