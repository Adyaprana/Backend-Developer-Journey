from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel, EmailStr, Field

app = FastAPI()


class UserCreate(BaseModel):
    name: str = Field(min_length=3, max_length=50)
    email: EmailStr
    age: Optional[int] = Field(default=None, gt=0)
    country: str = "India"


@app.post("/users")
def create_user(user: UserCreate):
    return {
        "message": "User created successfully!",
        "user": user,
    }