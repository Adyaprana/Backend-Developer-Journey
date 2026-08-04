from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

import logging
import time

app = FastAPI(
    title="Backend Developer Journey API",
    version="1.0.0"
)

# =====================================================
# Logging
# =====================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)


# =====================================================
# CORS Middleware
# =====================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =====================================================
# Custom Middleware
# =====================================================

@app.middleware("http")
async def log_requests(request: Request, call_next):

    start_time = time.time()

    logger.info(f"Incoming Request -> {request.method} {request.url.path}")

    response = await call_next(request)

    process_time = time.time() - start_time

    logger.info(
        f"Completed -> {response.status_code} ({process_time:.4f}s)"
    )

    return response


# =====================================================
# Custom Exception
# =====================================================

class UserNotFoundException(Exception):
    pass


@app.exception_handler(UserNotFoundException)
async def user_not_found_handler(
    request: Request,
    exc: UserNotFoundException
):
    return JSONResponse(
        status_code=404,
        content={
            "success": False,
            "message": "User not found."
        }
    )


# =====================================================
# Home
# =====================================================

@app.get("/")
def home():
    return {
        "message": "Welcome to Backend Developer Journey!"
    }


# =====================================================
# HTTPException Example
# =====================================================

@app.get("/products/{product_id}")
def get_product(product_id: int):

    if product_id != 1:

        raise HTTPException(
            status_code=404,
            detail="Product not found."
        )

    return {
        "id": 1,
        "name": "Laptop",
        "price": 50000
    }


# =====================================================
# Custom Exception Example
# =====================================================

@app.get("/users/{user_id}")
def get_user(user_id: int):

    if user_id != 1:
        raise UserNotFoundException()

    return {
        "id": 1,
        "name": "Adyaprana"
    }

# =====================================================
# For running the app using uvicorn
# =====================================================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)












# from fastapi import FastAPI

# import models  # noqa: F401 — ensure models are registered with Base
# from database import Base, engine, ensure_schema
# from routers import auth, users

# app = FastAPI(
#     title="Backend Learning API",
#     description="FastAPI + PostgreSQL with JWT authentication",
# )

# ensure_schema()
# Base.metadata.create_all(bind=engine)

# app.include_router(auth.router)
# app.include_router(users.router)


# @app.get("/")
# def home():
#     return {
#         "message": "FastAPI + PostgreSQL working!",
#         "docs": "/docs",
#         "steps": [
#             "POST /register with name, email, password",
#             "Click Authorize in /docs — email goes in username, then password",
#             "Call protected /users routes",
#         ],
#     }
