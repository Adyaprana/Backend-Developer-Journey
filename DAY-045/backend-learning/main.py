from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import Base, engine, get_db

app = FastAPI()

# Create all database tables
Base.metadata.create_all(bind=engine)


@app.get("/")
def home():
    return {
        "message": "FastAPI + PostgreSQL working!"
    }


@app.post(
    "/users",
    response_model=schemas.UserResponse,
)
def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db),
):
    return crud.create_user(db, user)


@app.get(
    "/users",
    response_model=list[schemas.UserResponse],
)
def get_users(
    db: Session = Depends(get_db),
):
    return crud.get_users(db)


@app.get(
    "/users/{user_id}",
    response_model=schemas.UserResponse,
)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
):
    user = crud.get_user(db, user_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return user


@app.put(
    "/users/{user_id}",
    response_model=schemas.UserResponse,
)
def update_user(
    user_id: int,
    user: schemas.UserUpdate,
    db: Session = Depends(get_db),
):
    updated_user = crud.update_user(
        db,
        user_id,
        user,
    )

    if updated_user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return updated_user


@app.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
):
    deleted_user = crud.delete_user(
        db,
        user_id,
    )

    if deleted_user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return {
        "message": "User deleted successfully"
    }