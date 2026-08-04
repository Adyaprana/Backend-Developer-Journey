# Day 47 — Error Handling, Middleware, CORS & Logging in FastAPI

> **Backend Developer Journey**  
> **Phase 02 — FastAPI Backend**  
> **Day 47 / 420**

---

# Today's Goal

Today I learned one of the most important backend engineering topics.

Until now my API could:

- Receive requests
- Validate data
- Connect to PostgreSQL
- Authenticate users

Today I learned how to make an API production-ready by understanding:

- HTTP Exceptions
- Custom Exception Handlers
- Middleware
- CORS
- Logging
- Complete Request Lifecycle

---

# Final Project Structure

```text
app/

│

├── main.py
├── database.py
├── models.py
├── schemas.py
├── crud.py
└── auth.py
```

Only **main.py** changes today.

---

# Complete Code

```python
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
# Run Server
# =====================================================

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )
```

---

# Understanding Every Line of Code

---

# Imports

```python
from fastapi import FastAPI, HTTPException, Request
```

## Why?

Import required FastAPI classes.

---

### FastAPI

```python
FastAPI
```

Creates the web application.

Without this

there is no backend.

---

### HTTPException

Used for returning HTTP errors.

Instead of

```
Program crashed.
```

we return

```
404 User Not Found
```

or

```
401 Unauthorized
```

---

### Request

Represents the incoming HTTP request.

Contains information like

- URL
- Headers
- Cookies
- Body
- Query Parameters
- Client IP

Middleware uses this object heavily.

---

```python
from fastapi.responses import JSONResponse
```

Allows us to manually create a JSON response.

Normally FastAPI converts dictionaries automatically.

But custom exception handlers need explicit JSON responses.

---

```python
from fastapi.middleware.cors import CORSMiddleware
```

Imports FastAPI's built-in CORS middleware.

Used when frontend and backend are running on different origins.

---

```python
import logging
```

Python's built-in logging module.

Used instead of print() in production.

---

```python
import time
```

Used to calculate how long a request took.

---

# Creating the Application

```python
app = FastAPI(
    title="Backend Developer Journey API",
    version="1.0.0"
)
```

Creates the FastAPI application.

title and version automatically appear inside Swagger UI.

---

# Logging Configuration

```python
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
```

Configure the logger.

---

## level=logging.INFO

Only INFO level and above are shown.

Levels

```
DEBUG

INFO

WARNING

ERROR

CRITICAL
```

---

## format

```
%(asctime)s
```

Current timestamp

```
%(levelname)s
```

INFO

ERROR

WARNING

```
%(message)s
```

Actual log message.

---

```python
logger = logging.getLogger(__name__)
```

Creates a logger object.

Instead of

```python
print(...)
```

we use

```python
logger.info(...)
```

Professional projects never use print() for application logs.

---

# CORS Middleware

```python
app.add_middleware(
```

Adds middleware to FastAPI.

Middleware runs before every endpoint.

---

```python
CORSMiddleware
```

Specifically adds CORS protection.

---

```python
allow_origins=[
    "http://localhost:3000"
]
```

Only React running on localhost:3000 is allowed.

---

```python
allow_credentials=True
```

Allows cookies and Authorization headers.

Needed for authentication.

---

```python
allow_methods=["*"]
```

Allow every HTTP method.

GET

POST

PUT

DELETE

PATCH

etc.

---

```python
allow_headers=["*"]
```

Allow every request header.

Authorization

Content-Type

Accept

etc.

---

# Middleware

```python
@app.middleware("http")
```

Register a middleware.

Every HTTP request passes through it.

---

```python
async def log_requests(...)
```

Middleware function.

---

```python
request
```

Incoming HTTP request.

---

```python
call_next
```

Calls the next step.

Usually

the endpoint.

Think of it as

```
Continue execution.
```

---

```python
start_time = time.time()
```

Record start time.

---

```python
logger.info(...)
```

Logs incoming request.

Example

```
GET /users/1
```

---

```python
response = await call_next(request)
```

Pass request to endpoint.

Without this

endpoint never executes.

This is the most important line in middleware.

---

```python
process_time
```

Calculate total execution time.

---

```python
return response
```

Return endpoint response back to client.

---

# Custom Exception

```python
class UserNotFoundException(Exception):
```

Our own exception.

Instead of repeatedly writing

```python
raise HTTPException(...)
```

we create meaningful exception classes.

---

```python
pass
```

No extra logic.

Only defines a new exception type.

---

# Exception Handler

```python
@app.exception_handler(...)
```

Registers a handler.

Whenever

```
UserNotFoundException
```

is raised

FastAPI calls this function.

---

```python
JSONResponse(...)
```

Creates manual JSON response.

---

```python
status_code=404
```

HTTP Status

---

```python
content={...}
```

JSON body returned to client.

---

# Home Endpoint

```python
@app.get("/")
```

GET request.

---

```python
def home():
```

Function executed when someone visits

```
/
```

---

```python
return {...}
```

Dictionary

↓

FastAPI

↓

JSON

↓

Browser

---

# HTTPException Example

```python
raise HTTPException(...)
```

Immediately stops function execution.

Returns

```
404
```

instead of crashing.

---

# Why raise?

Because exceptions interrupt execution immediately.

```
Function

↓

raise

↓

Stop

↓

Return Error
```

---

# Custom Exception Example

```python
raise UserNotFoundException()
```

Instead of directly returning JSON

FastAPI automatically calls our custom handler.

---

# Running Server

```python
if __name__ == "__main__":
```

Runs only when main.py is executed directly.

---

```python
uvicorn.run(...)
```

Starts the ASGI server.

---

# HTTPException

## What is HTTPException?

FastAPI's built-in exception.

Used for expected API failures.

Examples

- User not found
- Product not found
- Invalid credentials
- Forbidden access

---

## Why not use Exception?

Bad

```python
raise Exception("User missing")
```

Result

```
500 Internal Server Error
```

Good

```python
raise HTTPException(
    status_code=404,
    detail="User not found"
)
```

Result

```
404
```

Cleaner.

Professional.

REST compliant.

---

# Built-in Exception vs Custom Exception

## Built-in

```
HTTPException
```

Use when

single endpoint

simple error

---

## Custom Exception

```
UserNotFoundException
```

Use when

same error appears

across many endpoints

Cleaner

Reusable

Easy to maintain

---

# Middleware

Middleware wraps every request.

```
Browser

↓

Middleware

↓

Endpoint

↓

Middleware

↓

Browser
```

Everything passes through middleware.

---

Middleware is commonly used for

- Authentication
- Logging
- Timing
- Compression
- Rate Limiting
- Security
- CORS

---

# CORS

## What is CORS?

Cross-Origin Resource Sharing.

---

Origin means

```
Protocol

+

Domain

+

Port
```

Example

```
http://localhost:3000
```

is different from

```
http://localhost:8000
```

Different port

↓

Different Origin

---

Browser blocks request.

Not FastAPI.

Browser.

---

We tell browser

```
I trust localhost:3000
```

using

CORSMiddleware.

---

# Logging

Without logs

```
Server crashed.
```

No idea why.

---

With logs

```
09:10 Request Started

09:10 GET /users/1

09:10 SQL Query

09:10 Response 200

09:10 Finished
```

Easy debugging.

Production systems depend heavily on logging.

---

# Complete Request Lifecycle

```
Client

↓

HTTP Request

↓

Uvicorn

↓

CORS Middleware

↓

Logging Middleware

↓

FastAPI Router

↓

Pydantic Validation

↓

Endpoint

↓

Database

↓

Endpoint

↓

Logging Middleware

↓

Response

↓

Client
```

This is the complete lifecycle of every request.

---

# Request Flow of This Project

```
Browser

↓

GET /users/5

↓

Uvicorn

↓

CORS

↓

Logging

↓

Router

↓

Endpoint

↓

raise UserNotFoundException

↓

Exception Handler

↓

JSONResponse

↓

Logging

↓

Browser
```

---

# Output

## Home

```
GET /
```

```json
{
    "message":"Welcome to Backend Developer Journey!"
}
```

---

## Product

```
GET /products/1
```

```json
{
    "id":1,
    "name":"Laptop",
    "price":50000
}
```

---

## Product Not Found

```
GET /products/5
```

```json
{
    "detail":"Product not found."
}
```

Status

```
404
```

---

## User

```
GET /users/1
```

```json
{
    "id":1,
    "name":"Adyaprana"
}
```

---

## User Not Found

```
GET /users/5
```

```json
{
    "success":false,
    "message":"User not found."
}
```

---

# Console Logs

```
Incoming Request -> GET /

Completed -> 200 (0.0021s)

Incoming Request -> GET /users/5

Completed -> 404 (0.0017s)
```

---

# Real World Uses

HTTPException

- Login APIs
- Payment APIs
- Banking APIs
- Admin APIs

Middleware

- Authentication
- JWT Verification
- Logging
- Timing
- Rate Limiting
- Request ID
- Security

CORS

- React + FastAPI
- Angular + FastAPI
- Vue + FastAPI
- Mobile Apps

Logging

- Production Monitoring
- Bug Investigation
- Performance Analysis
- Audit Logs

---

# Interview Questions

## Beginner

### Q1 What is HTTPException?

**Answer**

HTTPException is FastAPI's built-in exception class used to return proper HTTP status codes and JSON error responses instead of crashing the application.

---

### Q2 Why use raise instead of return?

**Answer**

Because exceptions immediately stop execution and allow FastAPI to generate the correct HTTP error response.

---

### Q3 What is Middleware?

**Answer**

Middleware is code that executes before and after every request. It is commonly used for logging, authentication, CORS, timing, and security.

---

### Q4 What is CORS?

**Answer**

CORS (Cross-Origin Resource Sharing) is a browser security mechanism that controls which origins are allowed to access a backend API.

---

### Q5 Why does FastAPI need CORSMiddleware?

**Answer**

To explicitly allow trusted frontend applications from different origins to access the backend.

---

### Q6 Why is logging better than print()?

**Answer**

Logging supports log levels, timestamps, formatting, files, and centralized monitoring, making it suitable for production systems.

---

## Intermediate

### Q7 Explain the request lifecycle in FastAPI.

### Q8 Difference between HTTPException and custom exceptions?

### Q9 Explain request middleware.

### Q10 Explain response middleware.

### Q11 Why is CORS enforced by browsers instead of servers?

### Q12 What happens if `call_next(request)` is not called?

**Answer**

The request never reaches the endpoint, and the middleware effectively blocks further processing.

---

## Senior-Level

### Q13 How would you implement centralized exception handling?

### Q14 How would you add request IDs for distributed tracing?

### Q15 How would you structure logging in a microservice architecture?

### Q16 How would you secure CORS in production?

---

# Key Takeaways

- Learned production-ready API error handling.
- Understood why `HTTPException` is preferred for expected API errors.
- Built reusable custom exception handlers.
- Understood how middleware wraps every request and response.
- Learned why browsers enforce CORS and how FastAPI configures it safely.
- Replaced `print()` with structured logging.
- Understood the complete FastAPI request lifecycle from client to response.

---

# Day 47 Complete ✅

Today I moved beyond writing functional APIs and learned the production concerns that every backend service must address: handling failures gracefully, observing requests through logging, securing cross-origin access, and understanding the middleware pipeline that every request travels through.