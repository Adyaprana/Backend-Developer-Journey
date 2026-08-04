# 🗓️ DAY 47 — Error Handling + Middleware + CORS + Logging

# Before We Start...
# Let's think like backend engineers.

# Imagine your API has this endpoint:
# @app.get("/users/{user_id}")
# def get_user(user_id: int):
#     user = db.get(User, user_id)
#     return user

# Now someone requests: GET /users/999
# But user 999 doesn't exist.
# What should happen?
# Option 1: Internal Server Error -> ❌ Wrong.
# Option 2: Return None -> ❌ Wrong.
# Option 3: 404 Not Found -> ✅ Correct.
# A backend engineer doesn't only write code.
# A backend engineer communicates clearly with API consumers.






# Chapter 1 — What is Error Handling?
# Every backend has failures.

# Examples:
# User not found
# Invalid password
# Duplicate email
# Missing token
# Permission denied
# Database offline
# Invalid request body
# A good API never crashes. Instead, it returns meaningful HTTP responses.

# Bad Backend:
# Client -> GET/users/999 -> 500 Internal Server Error -> "Something went wrong."
# The client learns nothing.

# Good Backend:
# Client -> GET /users/999 -> 404 Not Found -> {"detail": "User not found"}
# Now the frontend knows exactly what happened.






# Chapter 2 — HTTPException
# FastAPI provides a built-in way to return HTTP errors.

# from fastapi import HTTPException
# Suppose:
# @app.get("/users/{user_id}")
# def get_user(user_id: int):
#     if user_id != 1:
#         raise HTTPException(
#             status_code=404,
#             detail="User not found"
#         )
#     return {
#         "id": 1,
#         "name": "Adyaprana"
#     }
# Notice something important.

# We don't return an error.
# We raise it.
# Why -> Because an exception immediately stops execution.

# What Happens Internally?
# Client -> GET/users/5 -> FastAPI -> Endpoint -> raise HTTPException -> FastAPI catches it -> JSON Response -> 404
# Your application never crashes.

# Common Status Codes You'll Use

# | Status Code | Meaning               | Example                     |
# | ----------- | --------------------- | --------------------------- |
# | 400         | Bad Request           | Invalid client request      |
# | 401         | Unauthorized          | Missing or invalid token    |
# | 403         | Forbidden             | Logged in but no permission |
# | 404         | Not Found             | User doesn't exist          |
# | 409         | Conflict              | Email already registered    |
# | 422         | Validation Error      | Pydantic validation failed  |
# | 500         | Internal Server Error | Unexpected server error     |
# These become second nature as you build APIs.






# Chapter 3 — Custom Exception Handlers

# Suppose your whole application uses: raise UserNotFoundException() 
# instead of repeating: raise HTTPException(...)
# everywhere. You can define your own exception.
class UserNotFoundException(Exception):
    pass
# Then tell FastAPI how to respond:
# @app.exception_handler(UserNotFoundException)
# async def user_not_found_handler(request, exc):
    # return JSONResponse(
        # status_code=404,
        # content={
            # "message": "User not found"
        # }
    # )

# Now every time this exception is raised,
# FastAPI automatically converts it into a proper HTTP response.






# Chapter 4 — Middleware
# This is one of the most important backend concepts.

# Imagine airport security. Everyone entering the airport must pass security first.
# Likewise, every HTTP request passes through middleware.

# Without middleware:
# Request -> Endpoint -> Response

# With middleware:
# Request -> Middleware -> Endpoint -> Middleware -> Response

# Middleware surrounds every request.
# What Can Middleware Do Almost anything.
# Examples: Authentication, Logging, Timing requests, Compression, CORS, Rate limiting, Security headers

# Every large backend uses middleware extensively.
# Example
# @app.middleware("http")
# async def log_requests(request, call_next):
#     print("Request started")
#     response = await call_next(request)
#     print("Request finished")
#     return response

# Let's understand this.
# Request Arrives GET /users -> Middleware starts -> Print: Request started -> Endpoint executes -> Middleware resumes -> Print: Request finished -> Return response

# Notice: call_next(request)
# means: "Continue to the next step in the pipeline."






# Chapter 5 — CORS

# Let's understand why CORS exists, not just how to enable it.
# Suppose your frontend is running here: http://localhost:3000
# Your backend is here: http://localhost:8000

# Different ports mean different origins.
# The browser sees: Origin A -> Origin B -> ⚠ Different Origin

# By default,the browser blocks the request.
# Not FastAPI. The browser.
# Why -> Imagine any website could silently call your banking API using your logged-in session.
# CORS is a browser security mechanism to prevent that kind of attack.
# How FastAPI Solves It by provides CORS middleware.

# from fastapi.middleware.cors import CORSMiddleware
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=[
#         "http://localhost:3000"
#     ],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
# Now the browser knows:
# This backend explicitly allows requests from localhost:3000.

# Important Production Note
# During development, you'll often see: allow_origins=["*"]
# This allows any origin. Convenient for testing.
# But in production, it's safer to list only the trusted frontend domains that should access your API.






# Chapter 6 — Logging
# Imagine your production server crashes.

# Without logs: Server crashed.
# Good luck debugging.

# With logs:
# 09:10 Request Started
# 09:10 GET /users/15
# 09:10 Database Connected
# 09:10 Response 200
# 09:10 Finished in 14ms
# Now you know exactly what happened.

# Logging is one of the first tools you'll use when diagnosing issues in production.

# FastAPI Logging
# You can start with Python's standard logging module.

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("User created successfully")

# Later you'll move to structured logging, but this is the right starting point.
# The Complete Request Lifecycle

# The mental model should look like this:
# Client -> Request -> CORS Middleware -> Logging Middleware -> Authentication Middleware (later) -> FastAPI Router -> Pydantic Validation -> Endpoint -> Database -> Response -> Logging Middleware -> Client

# Every request travels through this pipeline.
# Real Industry Practice

# In a production FastAPI application, we commonly have:
# Request
#   ↓
# Middleware
#     ├── Logging
#     ├── CORS
#     ├── Security Headers
#     ├── Authentication
#     └── Rate Limiting
#   ↓
# Router
#   ↓
# Service Layer
#   ↓
# Repository Layer
#   ↓
# Database
# This layered pipeline keeps responsibilities separate and makes applications easier to maintain.