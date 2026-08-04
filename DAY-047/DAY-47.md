cat > /mnt/user-data/outputs/DAY-47.md << 'ENDOFFILE'
# DAY 47 — Error Handling, Middleware, CORS & Logging in FastAPI

> **Phase:** 02 — FastAPI Backend (Days 43–90)
>
> **Week:** W7 — FastAPI Core (Days 43–49)
>
> **Goal:** Make an API production-ready — handle failures gracefully, observe every request, secure cross-origin access, and understand the middleware pipeline.
>
> **Status:** ✅ Day 47 Complete — HTTPException, custom exception handlers, CORS, middleware, and logging all working

---

# 🎯 Learning Roadmap

```
Error Handling in APIs + Middleware + CORS

  ✅ HTTPException — raise custom errors with status codes
  ✅ Custom exception handlers
  ✅ CORS middleware (required for frontend to talk to your API)
  ✅ Request/response middleware
  ✅ Logging in FastAPI

  ▶ fastapi.tiangolo.com/tutorial/handling-errors/
```

## Day 47 Checklist

- [ ] Explain why a crashed server returning 500 is bad engineering
- [ ] Explain the difference between `raise` and `return` for errors
- [ ] List 6 common HTTP status codes and when to use each
- [ ] Write a `HTTPException(status_code=404, detail="...")` from memory
- [ ] Create a custom exception class and its handler
- [ ] Explain what middleware is with the airport analogy
- [ ] Write a request timing middleware from memory
- [ ] Explain what CORS is and WHY browsers enforce it
- [ ] Add `CORSMiddleware` to a FastAPI app
- [ ] Explain why `allow_origins=["*"]` is dangerous in production
- [ ] Explain why `logger.info()` is better than `print()` in production
- [ ] Draw the complete request lifecycle (all layers)

---

# SECTION 1 — THINK LIKE A BACKEND ENGINEER

## The Problem

Before writing any code today, ask this question:

```
Your API has this endpoint:

@app.get("/users/{user_id}")
def get_user(user_id: int):
    user = db.get(User, user_id)
    return user

Someone requests: GET /users/999
But user 999 doesn't exist.

What should happen?
```

**Option A:** Internal Server Error (500) — the application crashes

**Option B:** Return `None` — client receives `null`

**Option C:** 404 Not Found `{"detail": "User not found"}`

---

```
Option A is wrong:
  "Something went wrong" tells the frontend nothing.
  They don't know if it's their fault or yours.
  They can't fix anything.

Option B is wrong:
  Client receives null and doesn't know why.
  Was the user deleted? Never existed? Wrong ID format?
  Frontend breaks silently.

Option C is correct:
  404 = resource doesn't exist.
  {"detail": "User not found"} = exactly what happened.
  Frontend can show "User not found" message to the user.
  Professional. Clear. REST-compliant.
```

**A backend engineer doesn't only write code. A backend engineer communicates clearly with API consumers.**

---

## What "Production-Ready" Means

Until Day 46, your API could receive requests, validate data, talk to PostgreSQL, and authenticate users.

But it was missing:

```
❌ Meaningful error responses (not just 500)
❌ Custom error formats
❌ Request logging (how do you debug production issues?)
❌ Cross-origin security (frontend can't talk to it)
❌ Request timing (how fast is each endpoint?)
```

Today's topics fix all of these.

---

# SECTION 2 — THE COMPLETE CODE

## main.py (Everything Changes Here Only)

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
# Logging Setup
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
# Custom Middleware (Request Logging + Timing)
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
# Endpoints
# =====================================================

@app.get("/")
def home():
    return {
        "message": "Welcome to Backend Developer Journey!"
    }


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

**Run:**

```bash
python -m uvicorn main:app --reload
```

---

# SECTION 3 — HTTPLEXCEPTION

## What is HTTPException?

FastAPI's built-in exception class for returning proper HTTP errors.

```python
from fastapi import HTTPException

raise HTTPException(
    status_code=404,
    detail="User not found"
)
```

**What the client receives:**

```json
{
  "detail": "User not found"
}
```

HTTP Status: 404

---

## Why `raise` Instead of `return`?

This is one of the most important distinctions in FastAPI:

```python
# WRONG — using return for errors
def get_user(user_id: int):
    if user_id != 1:
        return {"error": "not found"}   # ← HTTP status is still 200!
    return {"id": 1, "name": "Adya"}

# Client receives: 200 OK {"error": "not found"}
# Client thinks: success! (because 200 means success)
# Client is confused: why is there an error in a success response?
```

```python
# CORRECT — using raise for errors
def get_user(user_id: int):
    if user_id != 1:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": 1, "name": "Adya"}

# Client receives: 404 Not Found {"detail": "User not found"}
# Client knows: this resource doesn't exist.
# Frontend can show appropriate message to the user.
```

**How `raise` works internally:**

```
Function running
        │
        │ raise HTTPException(status_code=404)
        ▼
Execution STOPS immediately
        │
        ▼
FastAPI catches the exception
        │
        ▼
FastAPI builds HTTP 404 response
        │
        ▼
{"detail": "User not found"} → Client

Your code after the raise NEVER runs.
This is why it's called an "exception" — it interrupts normal flow.
```

---

## Common HTTP Status Codes (Memorize These)

```
400 Bad Request
  → Client sent invalid data.
  → Example: missing required field, wrong format.
  → Who's at fault: the CLIENT.

401 Unauthorized
  → Not authenticated. Token missing or invalid.
  → Example: accessing protected route without logging in.
  → "I don't know who you are."

403 Forbidden
  → Authenticated but not permitted.
  → Example: regular user trying to access admin panel.
  → "I know who you are, but you can't do this."

404 Not Found
  → Resource doesn't exist.
  → Example: GET /users/999 but user 999 was deleted.
  → "That thing you're looking for doesn't exist here."

409 Conflict
  → Request conflicts with current state.
  → Example: trying to register with an email already taken.
  → "This would create a conflict."

422 Unprocessable Entity
  → Pydantic validation failed.
  → FastAPI sends this automatically.
  → "The request format is valid JSON but fails schema rules."

500 Internal Server Error
  → Unexpected crash. Your code threw an unhandled exception.
  → Clients should NOT see this in production.
  → "We broke something. Not your fault."
```

**The mental model:**

```
4xx errors → Client's fault (wrong request)
5xx errors → Server's fault (your code failed)
2xx errors → Success
3xx errors → Redirect
```

---

## HTTPException in Practice

```python
# Login — wrong credentials
raise HTTPException(
    status_code=401,
    detail="Incorrect email or password",
    headers={"WWW-Authenticate": "Bearer"}   # standard for 401
)

# Protected route — no token
raise HTTPException(
    status_code=401,
    detail="Not authenticated"
)

# Admin only route — non-admin user
raise HTTPException(
    status_code=403,
    detail="You don't have permission to perform this action"
)

# Resource not found
raise HTTPException(
    status_code=404,
    detail="User not found"
)

# Duplicate email
raise HTTPException(
    status_code=409,
    detail="Email already registered"
)

# Invalid request (custom logic validation)
raise HTTPException(
    status_code=400,
    detail="Age must be greater than 0"
)
```

---

# SECTION 4 — CUSTOM EXCEPTION HANDLERS

## The Problem With HTTPException Everywhere

Suppose your API has 50 endpoints and 30 of them can throw "User not found":

```python
# Endpoint 1:
raise HTTPException(status_code=404, detail="User not found")

# Endpoint 2:
raise HTTPException(status_code=404, detail="User not found")

# Endpoint 3:
raise HTTPException(status_code=404, detail="User not found")

# ... 27 more times
```

**What if the response format needs to change?** You update 30 places. Easy to miss one.

**What if you want a different format?** Default HTTPException returns `{"detail": "..."}`. What if you want `{"success": false, "message": "..."}`?

---

## The Solution: Custom Exception + Handler

```python
# Step 1: Define your own exception class
class UserNotFoundException(Exception):
    pass
```

```python
# Step 2: Register a handler with FastAPI
@app.exception_handler(UserNotFoundException)
async def user_not_found_handler(
    request: Request,
    exc: UserNotFoundException
):
    return JSONResponse(
        status_code=404,
        content={
            "success": False,           # custom format!
            "message": "User not found."
        }
    )
```

```python
# Step 3: Raise it anywhere
@app.get("/users/{user_id}")
def get_user(user_id: int):
    if user_id != 1:
        raise UserNotFoundException()   # clean, semantic, reusable
    return {"id": 1, "name": "Adyaprana"}
```

**What the client receives:**

```json
{
  "success": false,
  "message": "User not found."
}
```

HTTP Status: 404

---

## What Each Part Does

**`class UserNotFoundException(Exception): pass`**

```python
class UserNotFoundException(Exception):
    pass

# Inherits from Exception (Python's base exception class).
# "pass" means: no extra logic, just define the type.
# The class itself is just a label — a new exception TYPE.

# Can be extended later:
class UserNotFoundException(Exception):
    def __init__(self, user_id: int):
        self.user_id = user_id
        super().__init__(f"User {user_id} not found")
```

**`@app.exception_handler(UserNotFoundException)`**

```python
@app.exception_handler(UserNotFoundException)

# Tells FastAPI: "When UserNotFoundException is raised ANYWHERE in the app,
# call this function instead of returning a generic 500."
# Works globally — catches the exception from any endpoint, any router.
```

**`async def user_not_found_handler(request, exc)`**

```python
async def user_not_found_handler(
    request: Request,     # the incoming HTTP request
    exc: UserNotFoundException  # the exception that was raised
):
    return JSONResponse(
        status_code=404,
        content={"success": False, "message": "User not found."}
    )

# Must be async (FastAPI requirement for exception handlers).
# request: full info about the incoming request (URL, headers, method).
# exc: the exception object (you can read exc.user_id if defined).
# JSONResponse: manually creates a JSON HTTP response.
```

**`JSONResponse`**

```python
from fastapi.responses import JSONResponse

return JSONResponse(
    status_code=404,
    content={"success": False, "message": "User not found."}
)

# Why JSONResponse instead of just return a dict?
# Exception handlers must return a Response object explicitly.
# FastAPI's automatic dict → JSON conversion doesn't apply here.
# JSONResponse: "Build an HTTP 404 response with this JSON body."
```

---

## HTTPException vs Custom Exception — When to Use Which

```
Use HTTPException when:
  → Single endpoint, one-off error
  → No custom response format needed
  → Default {"detail": "..."} format is fine

  raise HTTPException(status_code=404, detail="Product not found")

Use Custom Exception when:
  → Same error raised in many places
  → Custom response format needed (success/message instead of detail)
  → You want semantic, readable raise statements
  → You want centralized response format control

  raise UserNotFoundException()
  raise ProductNotFoundException()
  raise InsufficientStockException()
```

---

## Complete Custom Exception Pattern

```python
# Define exceptions for your domain
class ItemNotFoundException(Exception):
    pass

class InsufficientStockException(Exception):
    def __init__(self, product_id: int, requested: int, available: int):
        self.product_id = product_id
        self.requested = requested
        self.available = available

# Register handlers
@app.exception_handler(ItemNotFoundException)
async def item_not_found_handler(request: Request, exc: ItemNotFoundException):
    return JSONResponse(
        status_code=404,
        content={"success": False, "error": "Item not found"}
    )

@app.exception_handler(InsufficientStockException)
async def insufficient_stock_handler(request: Request, exc: InsufficientStockException):
    return JSONResponse(
        status_code=409,
        content={
            "success": False,
            "error": "Insufficient stock",
            "product_id": exc.product_id,
            "requested": exc.requested,
            "available": exc.available
        }
    )

# Use them cleanly in endpoints
@app.post("/orders")
def create_order(product_id: int, quantity: int):
    product = get_product(product_id)
    if product is None:
        raise ItemNotFoundException()
    if product.stock < quantity:
        raise InsufficientStockException(product_id, quantity, product.stock)
    # process order...
```

---

# SECTION 5 — MIDDLEWARE

## What is Middleware?

Middleware is code that runs before and after EVERY request.

**The airport security analogy:**

```
Everyone entering the airport must pass through security.
It doesn't matter if you're going to Gate A or Gate Z.
It doesn't matter if you bought a business or economy ticket.
Everyone goes through the same checkpoint.

Middleware works the same way.
Every HTTP request passes through middleware.
It doesn't matter which endpoint is being called.
```

**Request lifecycle with middleware:**

```
Browser
   │
   ▼
Middleware starts (before endpoint)
   │
   ▼
Endpoint runs
   │
   ▼
Middleware resumes (after endpoint)
   │
   ▼
Response returns to browser
```

**Without middleware:**

```
Request → Endpoint → Response
```

**With middleware:**

```
Request → [Middleware starts] → Endpoint → [Middleware resumes] → Response
```

---

## The Log Requests Middleware (Complete Explanation)

```python
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
```

**`@app.middleware("http")`**

```python
@app.middleware("http")

# Registers this function as HTTP middleware.
# "http" means: run for every HTTP request (not WebSocket, etc.)
# Every incoming request will pass through this function.
```

**`async def log_requests(request: Request, call_next)`**

```python
async def log_requests(request: Request, call_next):

# Must be async — middleware in FastAPI is always async.
# request: the full HTTP request object.
#   request.method      → "GET", "POST", etc.
#   request.url.path    → "/users/5"
#   request.headers     → all headers
#   request.client.host → client IP address
#   request.body()      → request body (async)

# call_next: a function that continues execution.
# Calling call_next(request) passes the request to the next step
# (either the next middleware or the actual endpoint).
```

**`start_time = time.time()`**

```python
start_time = time.time()

# Records the current time in seconds (float).
# Example: 1782000000.123456
# We'll calculate how long the request took by comparing to this.
```

**`logger.info(f"Incoming Request...")`**

```python
logger.info(f"Incoming Request -> {request.method} {request.url.path}")

# Logs before the endpoint runs.
# Console output: "2026-07-11 09:10:00 | INFO | Incoming Request -> GET /users/5"
```

**`response = await call_next(request)` — THE MOST IMPORTANT LINE**

```python
response = await call_next(request)

# This is where the actual endpoint executes.
# Execution pauses here while the endpoint runs.
# When the endpoint finishes, execution resumes here.
# response = the HTTP response from the endpoint.

# If you DON'T call call_next(request):
# → The endpoint NEVER executes
# → Client receives no response (or middleware blocks it)
# → Effectively a middleware that blocks all requests

# Timeline:
# log_requests starts → call_next() called → endpoint runs
# → endpoint returns → call_next() returns → log_requests resumes
```

**`process_time = time.time() - start_time`**

```python
process_time = time.time() - start_time

# Total time = end_time - start_time
# Example: 1782000000.137 - 1782000000.123 = 0.014 seconds = 14ms
```

**`return response`**

```python
return response

# Returns the endpoint's response to the client.
# Without this, the client never receives anything.
```

---

## What Middleware Sees

```python
async def log_requests(request: Request, call_next):
    # === BEFORE endpoint runs ===
    print(request.method)         # GET, POST, PUT, DELETE
    print(request.url.path)       # /users/5
    print(request.url.query)      # skip=0&limit=10
    print(request.headers)        # all HTTP headers
    print(request.client.host)    # IP address: 127.0.0.1

    response = await call_next(request)

    # === AFTER endpoint runs ===
    print(response.status_code)   # 200, 404, 401, etc.
    # Note: response body is a stream, harder to read

    return response
```

---

## Real-World Middleware Use Cases

```
Authentication Middleware:
  → Check Authorization header before endpoint runs
  → If invalid: return 401 immediately
  → If valid: let request through

Rate Limiting:
  → Count requests per IP per minute
  → If too many: return 429 Too Many Requests
  → If ok: let request through

Request ID (for distributed tracing):
  → Generate unique ID per request
  → Add X-Request-ID to response headers
  → Log every message with the same ID (so logs can be traced)

Compression:
  → If client supports gzip: compress response body
  → Reduces bandwidth

Security Headers:
  → Add X-Content-Type-Options: nosniff
  → Add X-Frame-Options: DENY
  → Standard security best practices

CORS (Cross-Origin Resource Sharing):
  → Handled by CORSMiddleware (next section)
```

---

## Multiple Middleware — Execution Order

```python
# If you have multiple middleware, they execute like an onion:
#
# Request:
#   Middleware 1 starts
#     Middleware 2 starts
#       Middleware 3 starts
#         Endpoint runs
#       Middleware 3 finishes
#     Middleware 2 finishes
#   Middleware 1 finishes
#
# ORDER: LIFO (Last In, First Out)
# Last middleware registered is the outermost layer.
# First middleware registered is the innermost (closest to endpoint).
```

---

# SECTION 6 — CORS

## What is CORS?

**Cross-Origin Resource Sharing.**

Before explaining how to enable it, you must understand WHY it exists.

---

## The Problem CORS Solves

**Origin = Protocol + Domain + Port**

```
http://localhost:3000   → Origin A  (React frontend)
http://localhost:8000   → Origin B  (FastAPI backend)

Same machine, different ports → DIFFERENT ORIGINS
```

```
The evil website attack scenario (without CORS):

You log into your bank: https://mybank.com
Your session cookie is stored in the browser.

You visit a malicious site: https://evil.com

evil.com's JavaScript runs:
  fetch("https://api.mybank.com/transfer", {
      method: "POST",
      body: {"amount": 100000, "to": "hacker_account"}
  })

Your browser sends this request WITH your bank's session cookie.
The bank API sees: valid session → transfer executed.
Your money is gone.
```

**CORS prevents this:**

```
Browser checks: "Is api.mybank.com on evil.com's allowed list?"
api.mybank.com responds: "I only allow requests from https://mybank.com"
Browser blocks the request.
Your money is safe.
```

**CRITICAL UNDERSTANDING:**

```
CORS is NOT enforced by the server.
CORS is enforced by the BROWSER.

If you use curl, Postman, or any server-to-server call:
  CORS doesn't apply.
  No restrictions.

Only browsers enforce CORS.
Only browser-based JavaScript is restricted.
```

---

## How CORSMiddleware Works

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**`allow_origins=["http://localhost:3000"]`**

```python
allow_origins=["http://localhost:3000"]

# Tells the browser: "Only requests from localhost:3000 are allowed."
# Browser checks the Origin header of the request.
# If origin matches: request is allowed.
# If origin doesn't match: browser blocks it (server still runs, browser ignores response).

# Development: allow_origins=["http://localhost:3000"]
# Production:  allow_origins=["https://myapp.com", "https://www.myapp.com"]
# DANGEROUS:   allow_origins=["*"]  → allows ANY website to call your API
```

**`allow_credentials=True`**

```python
allow_credentials=True

# Allows requests that include cookies and Authorization headers.
# Required for:
#   → JWT token in Authorization header
#   → Session cookies
#   → Any authenticated request

# When allow_credentials=True:
#   allow_origins must be specific URLs (not *)
#   allow_origins=["*"] + allow_credentials=True = CORS error!
```

**`allow_methods=["*"]`**

```python
allow_methods=["*"]

# Allows all HTTP methods: GET, POST, PUT, PATCH, DELETE, OPTIONS, etc.
# More restrictive: ["GET", "POST"]  → only read and create operations
```

**`allow_headers=["*"]`**

```python
allow_headers=["*"]

# Allows all request headers.
# If restricted: ["Content-Type", "Authorization"] → only these headers allowed.
```

---

## What CORS Actually Looks Like (Browser Network Tab)

**Preflight request (OPTIONS):**

```
Browser → OPTIONS /users HTTP/1.1
          Origin: http://localhost:3000
          Access-Control-Request-Method: POST
          Access-Control-Request-Headers: Authorization, Content-Type

FastAPI → HTTP 200 OK
           Access-Control-Allow-Origin: http://localhost:3000
           Access-Control-Allow-Methods: GET, POST, PUT, DELETE
           Access-Control-Allow-Headers: Authorization, Content-Type

Browser: "Origin is allowed, methods are allowed, headers are allowed."
Browser → sends the actual POST request.
```

**If CORS is NOT configured:**

```
Browser → GET /users HTTP/1.1
          Origin: http://localhost:3000

FastAPI → HTTP 200 OK
           (no CORS headers in response)

Browser: "No Access-Control-Allow-Origin header. BLOCKING."
Developer sees: "CORS error" in browser console.
Your API returned 200 but the browser blocked the response.
```

---

## Production CORS Configuration

```python
import os

# Development
ALLOWED_ORIGINS_DEV = ["http://localhost:3000", "http://localhost:5173"]

# Production
ALLOWED_ORIGINS_PROD = [
    "https://myapp.com",
    "https://www.myapp.com",
    "https://api.myapp.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS_PROD if os.getenv("ENV") == "production"
                  else ALLOWED_ORIGINS_DEV,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["Authorization", "Content-Type", "Accept"],
)
```

---

# SECTION 7 — LOGGING

## Why Logging Matters

**Without logs:**

```
Production server crashes at 2 AM.
Error: "500 Internal Server Error"
You wake up. Server is down. Customers are angry.
You look at the code.
No idea what happened.
No timeline.
No context.
You're debugging blind.
```

**With logs:**

```
2026-07-11 02:14:33 | INFO  | Incoming Request -> POST /orders
2026-07-11 02:14:33 | INFO  | User authenticated: adya@gmail.com
2026-07-11 02:14:33 | ERROR | Database connection timeout after 30s
2026-07-11 02:14:33 | ERROR | Failed to insert order: connection refused
2026-07-11 02:14:33 | INFO  | Completed -> 500 (30.0021s)

Now you know:
  → Request came in at 02:14:33
  → It was a POST /orders request
  → User was authenticated (not an auth issue)
  → Database timed out (database server is down!)
  → 30 seconds wasted waiting for DB
  → The problem: your database server went offline

Diagnosis: 2 minutes instead of 2 hours.
```

---

## Python Logging Module

```python
import logging

# Step 1: Configure the root logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

# Step 2: Create a named logger for this module
logger = logging.getLogger(__name__)

# Step 3: Use it
logger.debug("Low-level debug info")     # only shown at DEBUG level
logger.info("User created successfully") # general information
logger.warning("High memory usage")      # something to watch
logger.error("Database connection failed")  # an error occurred
logger.critical("Server is down!")       # critical system failure
```

---

## Logging Levels

```
LEVEL       SEVERITY    USE WHEN
──────────────────────────────────────────────────────────────
DEBUG       Lowest      Detailed diagnostic info (dev only)
INFO        Normal      Normal operation: requests, user actions
WARNING     Medium      Something unexpected but recoverable
ERROR       High        A specific operation failed
CRITICAL    Highest     The entire application may crash

logging.basicConfig(level=logging.INFO)
→ Shows: INFO, WARNING, ERROR, CRITICAL
→ Hides: DEBUG (too verbose for most situations)
```

---

## Log Format

```python
format="%(asctime)s | %(levelname)s | %(message)s"

# %(asctime)s   → Timestamp: "2026-07-11 09:10:33,456"
# %(levelname)s → Level: "INFO", "ERROR", "WARNING"
# %(message)s   → Your message: "Incoming Request -> GET /users/5"

# Output: "2026-07-11 09:10:33,456 | INFO | Incoming Request -> GET /users/5"
```

---

## Why `logger.info()` Instead of `print()`

```
print() problems in production:
  ❌ No timestamp (when did this happen?)
  ❌ No log level (is this info, warning, or error?)
  ❌ No filtering (can't show only errors, must see everything)
  ❌ No file output (can't save logs to disk)
  ❌ No centralized collection (can't send to Datadog, CloudWatch, etc.)

logger.info() advantages:
  ✅ Automatic timestamp
  ✅ Log level attached (INFO, ERROR, etc.)
  ✅ Configurable: hide DEBUG in production, show everything in dev
  ✅ Can write to files: logging.FileHandler("app.log")
  ✅ Can send to monitoring systems: Datadog, Grafana, CloudWatch
  ✅ Multiple loggers per module (track which file generated the log)

Rule: Never use print() in production FastAPI code.
      Use logger.info() or logger.error() instead.
```

---

## Logging in the Middleware

```python
@app.middleware("http")
async def log_requests(request: Request, call_next):

    start_time = time.time()

    # Log BEFORE endpoint runs
    logger.info(f"Incoming Request -> {request.method} {request.url.path}")

    response = await call_next(request)   # endpoint runs here

    process_time = time.time() - start_time

    # Log AFTER endpoint runs (we now know the status code and duration)
    logger.info(
        f"Completed -> {response.status_code} ({process_time:.4f}s)"
    )

    return response
```

**Console output for each request:**

```
2026-07-11 09:10:00,123 | INFO | Incoming Request -> GET /users/1
2026-07-11 09:10:00,137 | INFO | Completed -> 200 (0.0140s)

2026-07-11 09:10:05,234 | INFO | Incoming Request -> GET /users/999
2026-07-11 09:10:05,241 | INFO | Completed -> 404 (0.0070s)

2026-07-11 09:10:10,100 | INFO | Incoming Request -> POST /orders
2026-07-11 09:10:10,150 | INFO | Completed -> 201 (0.0500s)
```

**What you can see from logs:**

```
GET /users/1 → 200 in 14ms    (fast, success)
GET /users/999 → 404 in 7ms   (fast, user doesn't exist)
POST /orders → 201 in 50ms    (database write, expected to be slower)
```

---

# SECTION 8 — OUTPUTS (ALL TEST CASES)

## Home Endpoint

```
GET /
```

```json
{
  "message": "Welcome to Backend Developer Journey!"
}
```

---

## Product Found

```
GET /products/1
```

```json
{
  "id": 1,
  "name": "Laptop",
  "price": 50000
}
```

---

## Product Not Found (HTTPException)

```
GET /products/5
```

```json
{
  "detail": "Product not found."
}
```

HTTP Status: 404

Note: `{"detail": ...}` is the default HTTPException format.

---

## User Found

```
GET /users/1
```

```json
{
  "id": 1,
  "name": "Adyaprana"
}
```

---

## User Not Found (Custom Exception Handler)

```
GET /users/5
```

```json
{
  "success": false,
  "message": "User not found."
}
```

HTTP Status: 404

Note: `{"success": false, "message": ...}` is the CUSTOM format from our handler.

---

## Console Logs

```
2026-07-11 09:10:00,100 | INFO | Incoming Request -> GET /
2026-07-11 09:10:00,102 | INFO | Completed -> 200 (0.0021s)

2026-07-11 09:10:05,200 | INFO | Incoming Request -> GET /users/5
2026-07-11 09:10:05,203 | INFO | Completed -> 404 (0.0017s)

2026-07-11 09:10:10,300 | INFO | Incoming Request -> GET /products/1
2026-07-11 09:10:10,304 | INFO | Completed -> 200 (0.0040s)
```

---

# SECTION 9 — COMPLETE REQUEST LIFECYCLE

## The Full Picture (Every Layer)

```
Client (Browser / Postman / Mobile App)
                │
                │ HTTP Request
                ▼
         Uvicorn (ASGI server)
         Parses TCP + HTTP
                │
                ▼
     CORSMiddleware
     Checks Origin header
     If allowed → adds CORS headers to response
     If not allowed → browser will block
                │
                ▼
     log_requests Middleware (START)
     start_time = time.time()
     logger.info("Incoming Request → GET /users/5")
                │
                ▼ call_next(request)
     FastAPI Router
     Matches: GET /users/{user_id} → get_user()
                │
                ▼
     Dependency Injection
     Depends(get_db) → session
     Depends(get_current_user) → verify JWT (if protected)
                │
                ▼
     Pydantic Validation
     user_id must be int
                │
                ▼
     get_user() endpoint runs
                │
       ┌────────┴─────────┐
       │ if user_id != 1  │
       │ raise            │
       │ UserNotFound()   │
       └────────┬─────────┘
                │
                ▼
     @app.exception_handler catches it
     Returns JSONResponse(404, {"success": False, ...})
                │
                ▼
     log_requests Middleware (RESUME)
     process_time calculated
     logger.info("Completed → 404 (0.0017s)")
     return response
                │
                ▼
         Uvicorn wraps in HTTP response
                │
                ▼
     Client receives:
     HTTP/1.1 404 Not Found
     {"success": false, "message": "User not found."}
```

---

# SECTION 10 — PROJECT STRUCTURE (DAY 47)

```
backend-learning/
│
├── main.py          ← ALL DAY 47 CHANGES HERE
│                      (CORS, Middleware, Logging, Custom Exceptions)
│
├── database.py      ← unchanged
├── models.py        ← unchanged
├── schemas.py       ← unchanged
├── crud.py          ← unchanged
├── security.py      ← unchanged
│
└── routers/
    ├── auth.py      ← unchanged
    └── users.py     ← unchanged
```

**One of the important lessons of Day 47:**

The entire middleware/error/CORS/logging layer was added by modifying ONLY `main.py`. The business logic, CRUD operations, and security are completely unaffected. This is the benefit of layered architecture.

---

# SECTION 11 — REAL WORLD USAGE

## HTTPException

```
Used in every production API:
  → Login APIs (Stripe, Razorpay, Twilio)
  → Banking APIs (check balance, transfer)
  → E-commerce APIs (order items, check stock)
  → Admin APIs (restricted endpoints)
```

## Middleware

```
Used in every production application:
  → Authentication: verify JWT before any endpoint
  → Logging: log every request to CloudWatch/Datadog
  → Timing: monitor slow endpoints (>500ms → alert)
  → Rate Limiting: block users making too many requests
  → Request ID: assign unique ID to trace logs
  → Security Headers: prevent XSS, clickjacking
```

## CORS

```
Required whenever frontend and backend are separate:
  → React + FastAPI
  → Angular + FastAPI
  → Vue + FastAPI
  → Mobile App (React Native, Flutter) + FastAPI
  → Any SPA (Single Page Application) + any backend
```

## Logging

```
Non-negotiable in production:
  → Production monitoring (Datadog, New Relic)
  → Bug investigation ("what happened before the crash?")
  → Performance analysis ("which endpoints are slow?")
  → Audit logs ("who changed what at when?")
  → Security alerts ("multiple failed logins from this IP")
```

---

# SECTION 12 — INTERVIEW QUESTIONS

## Q1. What is HTTPException?

FastAPI's built-in exception class for returning proper HTTP error responses. Instead of crashing with 500, you `raise HTTPException(status_code=404, detail="User not found")` to return a meaningful 404 response. FastAPI catches the exception and converts it to a proper HTTP response automatically.

## Q2. Why do we use `raise` instead of `return` for errors?

`raise` immediately stops function execution and passes control to FastAPI's exception handling mechanism, which sets the correct HTTP status code. `return {"error": "..."}` would still return HTTP 200 (success), misleading the client. Proper HTTP status codes are essential for REST APIs.

## Q3. What is Middleware?

Middleware is code that executes before and after every HTTP request. It wraps the entire request-response cycle. Common uses: logging, authentication, CORS, timing, rate limiting, compression, and security headers. FastAPI middleware receives the request, can process it, calls `call_next(request)` to execute the endpoint, and processes the response before returning.

## Q4. What happens if you don't call `await call_next(request)` in middleware?

The endpoint never executes. The middleware effectively blocks the request. The client either receives no response or receives whatever the middleware returns instead. This is used intentionally in authentication middleware: if the token is invalid, don't call `call_next` — return 401 immediately.

## Q5. What is CORS and why do browsers enforce it?

CORS (Cross-Origin Resource Sharing) is a browser security mechanism that prevents malicious websites from making unauthorized requests to other domains using the user's session credentials. An origin is defined as protocol + domain + port. Browsers block cross-origin requests unless the server explicitly allows them via CORS headers. CORS is enforced by browsers only — `curl`, Postman, and server-to-server calls are not restricted.

## Q6. Why is `allow_origins=["*"]` dangerous in production?

It allows any website on the internet to make requests to your API using the user's cookies and credentials. This reopens the cross-origin attack vector that CORS is designed to prevent. In production, always list specific trusted origins: `["https://myapp.com"]`.

## Q7. Why is `logger.info()` better than `print()` for production?

`print()` has no timestamp, no level (info/error/warning), no filtering, no file output, and no integration with monitoring systems. `logging.info()` provides timestamps, log levels, filtering by severity, file output, and integration with monitoring platforms like Datadog, CloudWatch, and Grafana. Professional backend applications always use structured logging.

## Q8. What is the difference between HTTPException and a custom exception handler?

`HTTPException` is FastAPI's built-in exception that returns `{"detail": "..."}`. It's good for simple, one-off errors. Custom exceptions (like `UserNotFoundException`) allow you to define your own response format (e.g., `{"success": false, "message": "..."}`), reuse the same error across many endpoints, and centralize error handling in one handler function.

## Q9. Explain the complete FastAPI request lifecycle.

Client → Uvicorn (parses TCP/HTTP) → CORS Middleware (checks Origin) → Custom Middleware (logs start, records time) → FastAPI Router (matches URL pattern) → Dependency Injection (injects db session, current user) → Pydantic Validation (validates request body/params) → Endpoint function runs → Database operations → Response built → Middleware resumes (logs status + duration) → Uvicorn sends HTTP response → Client.

## Q10. What does `logging.getLogger(__name__)` do?

`__name__` is Python's built-in variable containing the current module name (e.g., `main`, `routers.auth`). `getLogger(__name__)` creates a logger named after the current file. This lets you see which file generated each log message in complex applications, making debugging much easier.

---

# SECTION 13 — IMPORTANT THINGS TO KNOW

```
 1. Always use HTTPException for expected API errors.
    Never let unexpected exceptions reach the client as 500.

 2. raise stops execution immediately.
    return does NOT stop execution (code after return still runs... until it hits return).

 3. 4xx = client error. 5xx = server error.
    Good APIs minimize 500 errors in production.

 4. Custom exceptions are reusable across the entire application.
    One exception class + one handler = centralized error format.

 5. JSONResponse is required in exception handlers.
    FastAPI's automatic dict → JSON doesn't work in handlers.

 6. @app.exception_handler() catches globally — from any endpoint, any router.

 7. Middleware runs for EVERY request, no exceptions.
    Heavy middleware logic can slow down the entire API.

 8. call_next(request) MUST be awaited — it's async.
    await call_next(request) runs the endpoint and returns the response.

 9. If call_next() is not called, the endpoint never runs.
    Use this intentionally (e.g., authentication middleware returns 401).

10. CORS is enforced by BROWSERS ONLY.
    curl, Postman, server-to-server calls ignore CORS completely.

11. allow_origins=["*"] means "any website can call my API."
    In production, always specify exact allowed origins.

12. allow_credentials=True requires specific origins (not ["*"]).
    Using ["*"] + credentials=True causes CORS errors.

13. Never use print() in production FastAPI code.
    Use logger.info(), logger.error(), logger.warning().

14. Log levels: DEBUG < INFO < WARNING < ERROR < CRITICAL.
    basicConfig(level=INFO) shows INFO and above, hides DEBUG.

15. Middleware order matters.
    Last add_middleware() registered = outermost layer = runs first.
    First add_middleware() registered = innermost layer = closest to endpoint.
```

---

# REVISION SHEET

```
═══════════════════════════════════════════════════════════
FASTAPI DAY 47 — PRODUCTION PATTERNS REVISION
═══════════════════════════════════════════════════════════

HTTPEXCEPTION:
  from fastapi import HTTPException
  raise HTTPException(status_code=404, detail="Not found")
  Use raise (not return) — stops execution, sets HTTP status.

STATUS CODES:
  400 Bad Request      → Client sent invalid data
  401 Unauthorized     → Not authenticated
  403 Forbidden        → Authenticated but not permitted
  404 Not Found        → Resource doesn't exist
  409 Conflict         → Duplicate email, concurrent update
  422 Validation Error → Pydantic failed (auto)
  500 Server Error     → Your code crashed (avoid in production)

CUSTOM EXCEPTION:
  class MyException(Exception): pass
  @app.exception_handler(MyException)
  async def handler(request, exc):
      return JSONResponse(status_code=404, content={...})
  raise MyException()  → handler runs automatically

MIDDLEWARE:
  @app.middleware("http")
  async def my_middleware(request: Request, call_next):
      # BEFORE endpoint
      response = await call_next(request)  ← MUST call this!
      # AFTER endpoint
      return response

CORS:
  app.add_middleware(CORSMiddleware,
      allow_origins=["http://localhost:3000"],
      allow_credentials=True,
      allow_methods=["*"],
      allow_headers=["*"],
  )
  CORS = browsers only. curl/Postman not affected.
  Production: specific origins, NOT ["*"]

LOGGING:
  import logging
  logging.basicConfig(level=logging.INFO,
      format="%(asctime)s | %(levelname)s | %(message)s")
  logger = logging.getLogger(__name__)
  logger.info("message")   → INFO
  logger.error("message")  → ERROR
  Never use print() in production.

COMPLETE LIFECYCLE:
  Client → Uvicorn → CORS → Middleware → Router →
  Dependencies → Pydantic → Endpoint → DB →
  Exception Handler (if raised) → Middleware → Client
```

---

*Day 47 Complete. API is production-ready: graceful error handling, request logging, cross-origin security, and a clear request lifecycle mental model.* ✅
