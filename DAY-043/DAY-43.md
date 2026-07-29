# DAY 43 — FastAPI: Setup, First Endpoint, Path & Query Parameters + LeetCode Prefix Sum

> **Phase:** 02 — FastAPI Backend (Days 43–90)
>
> **Week:** W7 — FastAPI Core (Days 43–49)
>
> **Goal:** Start FastAPI. By end of the week you can build a working API with 5+ endpoints.
>
> **LeetCode:** #303 Range Sum Query - Immutable ✅ (7ms · Beats 53.12%)
>
> **Status:** ✅ Day 43 Complete — First FastAPI server running, endpoints responding

---

# 🎯 Learning Roadmap

```
FastAPI Setup + First Endpoint

  ✅ pip install fastapi uvicorn
  ✅ Create main.py, write first @app.get("/") endpoint
  ✅ Run with: uvicorn main:app --reload
  ✅ Open Swagger UI at localhost:8000/docs — understand auto-documentation
  ✅ Path parameters: @app.get("/users/{user_id}")
  ✅ Query parameters: @app.get("/items?skip=0&limit=10")

  ▶ fastapi.tiangolo.com/tutorial — START HERE ⭐
  ▶ Hitesh Choudhary FastAPI playlist (Hindi)
```

## Day 43 Checklist

- [ ] Explain what a web framework is from memory
- [ ] Explain the request lifecycle: Browser → Uvicorn → FastAPI → function → JSON
- [ ] Explain the difference between Uvicorn and FastAPI
- [ ] Write the `@app.get("/")` endpoint from memory
- [ ] Run the server with the correct command
- [ ] Open Swagger UI and explain what it shows
- [ ] Write a path parameter endpoint with type validation
- [ ] Write a query parameter endpoint with default values
- [ ] Explain the difference between path and query parameters with real examples
- [ ] Solve LeetCode #303 using Prefix Sum

---

# SECTION 1 — BEFORE FASTAPI: WHY WEB FRAMEWORKS EXIST

## What Happens When You Run a Normal Python Script

```python
print("Hello World")
```

```
Run: python main.py
Output: Hello World
Program ends.
```

Now consider Google. Millions of users open it every second. Can Google's backend do:

```python
print("Hello User 1")
exit()
```

No. A backend server must:

```
1. Stay alive forever (never exit)
2. Listen for incoming connections
3. Accept TCP connections
4. Parse HTTP requests
5. Route to the right handler
6. Build HTTP responses
7. Send them back
8. Go back to waiting
```

Without a framework, you would write all of this yourself. That's thousands of lines before writing a single business rule.

**This is why web frameworks exist.**

---

## The Full Request Journey

```
Browser
   │
   │ DNS Lookup: example.com → 172.217.1.1
   ▼
IP Address
   │
   │ TCP Handshake (SYN → SYN-ACK → ACK)
   ▼
TCP Connection Open
   │
   │ HTTP Request:
   │ GET /users/5 HTTP/1.1
   │ Host: example.com
   │ Accept: application/json
   ▼
Uvicorn (the server — listens on port 8000)
   │
   │ Parses HTTP, speaks ASGI
   ▼
FastAPI (the framework — knows routes)
   │
   │ Matches: GET /users/{user_id} → get_user()
   ▼
Your Python Function
   │
   │ return {"user_id": 5}
   ▼
FastAPI (converts dict → JSON automatically)
   │
   │ HTTP Response:
   │ 200 OK
   │ Content-Type: application/json
   │ {"user_id": 5}
   ▼
Browser receives JSON
```

**This single diagram explains the entire backend request lifecycle.** Every backend developer should have this memorized.

---

# SECTION 2 — WHY FASTAPI EXISTS

## What Python Had Before FastAPI

```
Flask:   Simple, flexible, but no type safety, no async, no auto-docs
Django:  Full-featured, but heavy, ORM-coupled, complex for APIs
Pyramid: Flexible but low adoption
Bottle:  Tiny but limited
```

## What FastAPI Adds

```
FastAPI was built because Python lacked a framework that was simultaneously:

1. Fast          → One of the fastest Python frameworks (ASGI + async)
2. Asynchronous  → async/await support from the ground up
3. Type-safe     → Uses Python type hints for validation
4. Self-documenting → Generates Swagger UI automatically
5. Editor-friendly → Full autocomplete in VS Code/Pycharm
```

FastAPI achieves this by building heavily on:

- **Python type hints** (PEP 484)
- **Pydantic** (for data validation)
- **Starlette** (the ASGI framework underneath)
- **ASGI** (the async server interface)

---

# SECTION 3 — ASGI AND UVICORN

## What is ASGI?

Before FastAPI, Python web frameworks used WSGI (Web Server Gateway Interface). WSGI is synchronous — one request at a time.

ASGI (Asynchronous Server Gateway Interface) is the modern replacement. It supports:

```
Synchronous requests  → handled normally
Async requests        → handled concurrently
WebSockets            → long-lived connections
Background tasks      → run after response sent
```

The request path with ASGI:

```
Client
  │
  │ HTTP request
  ▼
Uvicorn (ASGI server — handles networking)
  │
  │ ASGI interface
  ▼
FastAPI (ASGI application — handles routing)
  │
  ▼
Your function
```

## Uvicorn vs FastAPI — The Key Distinction

```
Uvicorn:                          FastAPI:
─────────────────────────────     ─────────────────────────────
Knows networking                  Knows routing
Knows ports                       Knows validation
Knows sockets                     Knows documentation
Knows HTTP                        Knows request parsing
Runs forever                      Calls your functions
Handles connections               Returns responses

Browser → Uvicorn → FastAPI → Your Code

FastAPI never opens Port 8000. Uvicorn does.
FastAPI never accepts TCP connections. Uvicorn does.
FastAPI never speaks raw HTTP. Uvicorn does.
```

**Analogy:**

```
Restaurant: Customer → Door → Waiter → Chef

Uvicorn  = The building + door (accepts customers)
FastAPI  = The waiter (routes to correct chef)
Your fn  = The chef (prepares the response)
```

This distinction matters when you deploy to production. You configure Uvicorn, not FastAPI, for workers, ports, and SSL.

---

# SECTION 4 — INSTALLATION

## Setup

```bash
# Create virtual environment
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate

# Install FastAPI and Uvicorn
pip install fastapi uvicorn

# Verify
pip show fastapi
pip show uvicorn
```

## Project Structure (Day 43)

```
backend-learning/
│
├── main.py
└── .venv/
```

Keep it simple. We'll organize properly when we understand the basics.

---

# SECTION 5 — YOUR FIRST FASTAPI APP

## main.py — Complete File

```python
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
```

---

## Line-by-Line Explanation

### Line 1: Import FastAPI

```python
from fastapi import FastAPI
```

```
We import the FastAPI class from the fastapi package.
This is exactly like:
  from pathlib import Path
  from datetime import datetime

FastAPI is just a Python class. You create an instance of it.
```

### Line 2: Create the Application

```python
app = FastAPI()
```

```
This creates your application object.
This single object stores:
  → Routes: GET /users → get_users function
  → Documentation: the Swagger UI at /docs
  → Middleware: code that runs before/after every request
  → Configuration: debug mode, title, version
  → Event handlers: startup/shutdown code

Everything in your API revolves around this one app instance.
```

### Line 3: The Route Decorator

```python
@app.get("/")
```

```
This is a DECORATOR.

Decorators in Python are functions that modify other functions.
Here, @app.get("/") does something specific:

It tells FastAPI:
  "When someone sends a GET request to '/', call the function below."

The function is NOT called here.
The decorator only REGISTERS it with the application.

FastAPI stores this internally as:
  route_table = {
      "GET /": home,
      "GET /users/{user_id}": get_user,
      "GET /items": get_items,
  }
```

### Line 4: Your Handler Function

```python
def home():
    return {"message": "Welcome to my first FastAPI application!"}
```

```
This is a completely normal Python function.

When a GET request arrives at "/", FastAPI:
  1. Finds home() in its route table
  2. Calls it
  3. Takes the return value (a Python dict)
  4. Converts it to JSON
  5. Wraps it in an HTTP 200 response
  6. Sends it back to the browser

You write: {"message": "Hello"}
Client receives: {"message": "Hello"}    (as JSON)

This automatic dict → JSON conversion is one of FastAPI's core conveniences.
You never write: json.dumps({"message": "Hello"})
FastAPI handles it.
```

---

## Run the Server

```bash
python -m uvicorn main:app --reload
```

**Breaking this command down:**

```
uvicorn      → start the Uvicorn ASGI server
main         → the filename (main.py without .py extension)
:app         → the variable name inside main.py (our app = FastAPI() instance)
--reload     → development mode:
               save main.py → server automatically restarts
               no need to Ctrl+C and re-run
```

**Output you see:**

```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345]
INFO:     Started server process [12346]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**Why `python -m uvicorn` and not just `uvicorn`?**

```
uvicorn main:app --reload      → works if uvicorn is on PATH
python -m uvicorn main:app --reload → always works (runs uvicorn as a module)

If the first doesn't work, the second always will.
Use: python -m uvicorn main:app --reload
```

---

## What Happens Internally

```
Browser → http://127.0.0.1:8000/

Step 1: Browser opens TCP connection to 127.0.0.1 port 8000
Step 2: Sends HTTP GET / HTTP/1.1
Step 3: Uvicorn receives the request, parses HTTP
Step 4: Passes to FastAPI via ASGI
Step 5: FastAPI looks up route: GET / → home()
Step 6: home() runs → returns {"message": "..."}
Step 7: FastAPI serializes dict to JSON
Step 8: Uvicorn wraps in HTTP response (200 OK)
Step 9: Browser receives: {"message": "Welcome to my first FastAPI application!"}
```

---

# SECTION 6 — SWAGGER UI: AUTOMATIC DOCUMENTATION

## Open the Docs

```
http://127.0.0.1:8000/docs
```

You'll see an interactive documentation page. **You wrote zero documentation.** FastAPI generated it automatically.

## What Swagger UI Shows

```
GET /                       → home endpoint
GET /users/{user_id}        → get_user with parameter info
GET /items                  → get_items with query params and defaults
```

For each endpoint:

```
Method:      GET / POST / PUT / DELETE
URL:         /users/{user_id}
Parameters:  user_id (integer, required, path)
Response:    200 OK {"user_id": integer}
Try it:      Execute button — test directly from browser
```

## Why Swagger Is Valuable

```
1. No separate documentation tool needed
2. Always in sync with your code (can't be outdated)
3. Frontend developers can test endpoints without Postman
4. Shows exact request/response formats
5. Automatically includes validation rules
6. When you add a new endpoint, it appears instantly
```

## How FastAPI Knows What to Document

```python
@app.get("/users/{user_id}")
def get_user(user_id: int):          # ← type hint tells FastAPI: integer
    return {"user_id": user_id}
```

```
From this one function, FastAPI knows:
  HTTP method:  GET
  URL pattern:  /users/{user_id}
  Parameter:    user_id
  Type:         int (integer)
  Required:     yes (it's in the path, must be provided)
  Response:     {"user_id": ...}

Everything comes from Python type hints.
No configuration files. No comments. No YAML.
```

---

# SECTION 7 — PATH PARAMETERS

## The Concept

Imagine you're building Instagram. Someone opens:

```
https://instagram.com/adyaprana
```

How does Instagram know whose profile to show?

It extracts `adyaprana` from the URL. That value **identifies a specific resource**.

That's exactly what a **Path Parameter** is.

## Syntax

```python
@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id}
```

```
{user_id} in the URL pattern — curly braces mark the parameter slot.

FastAPI automatically:
  1. Extracts whatever value is at that position in the URL
  2. Stores it in the variable named user_id
  3. Converts it to the declared type (int)
  4. Validates it
  5. Passes it to your function
```

## Testing Path Parameters

```
Visit: http://127.0.0.1:8000/users/5
FastAPI: user_id = 5
Returns: {"user_id": 5}

Visit: http://127.0.0.1:8000/users/100
FastAPI: user_id = 100
Returns: {"user_id": 100}

Visit: http://127.0.0.1:8000/users/999
FastAPI: user_id = 999
Returns: {"user_id": 999}
```

## Type Validation — Automatic Error Handling

```
Visit: http://127.0.0.1:8000/users/hello

You wrote: user_id: int
"hello" cannot be converted to int.
FastAPI automatically returns:

{
    "detail": [
        {
            "type": "int_parsing",
            "loc": ["path", "user_id"],
            "msg": "Input should be a valid integer",
            "input": "hello"
        }
    ]
}

HTTP Status: 422 Unprocessable Entity

You never wrote:
  try: user_id = int(user_id)
  except: return {"error": "invalid"}

FastAPI does this validation for you.
This is why Python type hints + FastAPI = less code, safer code.
```

## How Path Parameter Matching Works Internally

```python
# FastAPI stores routes in a routing table.
# When a request arrives for: GET /users/42

# FastAPI iterates over its routes:
#   GET /               → no match
#   GET /users/{user_id} → match! user_id = "42"
#   GET /items           → no match

# FastAPI then:
#   user_id = int("42")  → 42 (succeeds)
#   get_user(user_id=42)
#   Return {"user_id": 42}
```

---

# SECTION 8 — QUERY PARAMETERS

## The Concept

Imagine Amazon. You don't always want ALL products. Sometimes:

```
Only 10 products
Page 2
Sorted by price
Category: laptops
```

The RESOURCE is still `/products`. You're just changing HOW you fetch it.

Query parameters go AFTER `?` in the URL, separated by `&`:

```
/products?category=laptop&page=2&sort=price&limit=10
```

## Syntax

```python
@app.get("/items")
def get_items(skip: int = 0, limit: int = 10):
    return {
        "skip": skip,
        "limit": limit
    }
```

```
No curly braces in the URL pattern.
Function parameters WITH default values → query parameters.
Function parameters WITHOUT default values (in a non-path route) → required query params.
```

## Testing Query Parameters

```
Visit: http://127.0.0.1:8000/items
FastAPI: skip=0 (default), limit=10 (default)
Returns: {"skip": 0, "limit": 10}

Visit: http://127.0.0.1:8000/items?skip=20
FastAPI: skip=20, limit=10 (default)
Returns: {"skip": 20, "limit": 10}

Visit: http://127.0.0.1:8000/items?skip=50&limit=5
FastAPI: skip=50, limit=5
Returns: {"skip": 50, "limit": 5}
```

## How FastAPI Parses Query Parameters

```
When you type: /items?skip=40&limit=5

FastAPI parses:
  Query string: skip=40&limit=5
  Split on &:   ["skip=40", "limit=5"]
  Split on =:   skip=40, limit=5
  Convert types: skip=int("40")=40, limit=int("5")=5
  Call: get_items(skip=40, limit=5)

You don't write this parsing.
FastAPI does it all automatically from your type hints.
```

## Pagination — The Real Use Case

```python
@app.get("/users")
def get_users(page: int = 1, limit: int = 20):
    skip = (page - 1) * limit
    # SELECT * FROM users LIMIT 20 OFFSET 0   (page 1)
    # SELECT * FROM users LIMIT 20 OFFSET 20  (page 2)
    # SELECT * FROM users LIMIT 20 OFFSET 40  (page 3)
    return {"page": page, "limit": limit, "skip": skip}

# GET /users          → page 1, 20 per page
# GET /users?page=2   → page 2, 20 per page
# GET /users?page=3&limit=50 → page 3, 50 per page
```

---

# SECTION 9 — PATH vs QUERY PARAMETERS

## Comparison Table

```
┌────────────────────────────────┬────────────────────────────────┐
│       Path Parameter           │       Query Parameter          │
├────────────────────────────────┼────────────────────────────────┤
│ Identifies a specific resource │ Modifies how data is returned  │
│ Required (must be in URL)      │ Usually optional (has default) │
│ Written inside {}              │ Written after ?                │
│ /users/{user_id}               │ /users?limit=10                │
│ /products/{product_id}         │ /products?sort=price&page=2   │
│ Order matters (position)       │ Order doesn't matter           │
│ GET /users/5 (user 5)          │ GET /users?role=admin          │
└────────────────────────────────┴────────────────────────────────┘
```

## Real-World Examples

```
GitHub API:
  GET /users/octocat            → path param: identifies user "octocat"
  GET /users?since=100&per_page=30 → query params: pagination

YouTube:
  GET /results?search_query=fastapi → query param: modifies search
  GET /watch?v=dQw4w9WgXcQ          → query param: identifies video

Amazon:
  GET /products?category=laptop&page=2 → query params
  GET /products/B0CX9NMFR2             → path param: identifies product

LeetCode:
  GET /problems/two-sum  → path param: identifies problem
  GET /problems?difficulty=easy → query param: filters results

Your Future API:
  GET /users/42            → get user 42 (path)
  GET /users?city=Blore    → filter users by city (query)
  GET /users/42/orders     → orders for user 42 (path)
  GET /users/42/orders?status=pending → filter (both!)
```

---

# SECTION 10 — COMPLETE main.py WITH EXPLANATION

```python
from fastapi import FastAPI

# Create the FastAPI application instance
app = FastAPI()


# Root endpoint — "home page" of your API
@app.get("/")
def home():
    return {"message": "Welcome to my first FastAPI application!"}


# Path parameter endpoint
# {user_id} in the path is extracted and type-validated
@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id}


# Query parameter endpoint
# Parameters with defaults = optional query params
@app.get("/items")
def get_items(skip: int = 0, limit: int = 10):
    return {
        "skip": skip,
        "limit": limit
    }
```

**Run:**

```bash
python -m uvicorn main:app --reload
```

**Test URLs:**

```
http://127.0.0.1:8000/             → {"message": "Welcome..."}
http://127.0.0.1:8000/docs         → Swagger UI
http://127.0.0.1:8000/users/7      → {"user_id": 7}
http://127.0.0.1:8000/users/100    → {"user_id": 100}
http://127.0.0.1:8000/users/abc    → 422 validation error
http://127.0.0.1:8000/items        → {"skip": 0, "limit": 10}
http://127.0.0.1:8000/items?skip=20 → {"skip": 20, "limit": 10}
http://127.0.0.1:8000/items?skip=50&limit=5 → {"skip": 50, "limit": 5}
```

---

# SECTION 11 — PHASE 2 OVERVIEW (Days 43–90)

## What Phase 2 Is

```
Phase 01 (Days 1–42):   Python Fundamentals + SQL + SQLAlchemy + GuessWise
Phase 02 (Days 43–90):  FastAPI Backend

Goal: "Build your first complete backend API from scratch.
       Every line — you write it. By day 90, you have Project 1 deployed live."

Duration: Days 43–90 · Months 2–3 · 3–4 hrs/day
```

## The Big Picture

```
Every skill from Phase 1 was preparing for this:

Python         → You write all FastAPI logic in Python
OOP            → FastAPI uses class-based patterns
Type hints     → FastAPI is built entirely on type hints
SQLAlchemy     → Connect FastAPI to the database
PostgreSQL     → The database your API reads/writes
HTTP methods   → GET, POST, PUT, DELETE (you know all of them)
JSON           → Every API response is JSON
Architecture   → GuessWise taught you layered design
Repository     → You'll use this pattern in every FastAPI project
```

---

# SECTION 12 — KEY CONCEPTS LEARNED TODAY

## Web Framework

```
A web framework handles:
  → Listening on a port
  → Accepting TCP connections
  → Parsing HTTP requests
  → Routing URLs to functions
  → Serializing responses
  → Generating documentation

Without it: you write thousands of lines before business logic.
With FastAPI: 5 lines and your server is running.
```

## ASGI

```
Asynchronous Server Gateway Interface.
The standard interface between ASGI servers (Uvicorn) and applications (FastAPI).
Supports: HTTP, WebSockets, async code.
Replaced WSGI for modern Python web development.
```

## The Decorator Pattern in FastAPI

```python
@app.get("/")          # ← This registers the route
def home():            # ← This is the handler function
    return {...}

# @app.get("/") is equivalent to:
# app.add_route("/", home, methods=["GET"])
# Just cleaner syntax.
```

## Automatic JSON Serialization

```python
# You return a Python dict:
return {"user_id": 5, "name": "Adya"}

# FastAPI automatically:
# 1. Serializes: json.dumps({"user_id": 5, "name": "Adya"})
# 2. Sets Content-Type: application/json header
# 3. Sets HTTP status 200
# You never write any of this.
```

## Type Hint = Validation + Documentation + Autocomplete

```python
def get_user(user_id: int):
#                    ↑
#                 One type hint does THREE things:
#   1. Validates: rejects non-integer user_id (422 error)
#   2. Documents: Swagger shows "integer" type in docs
#   3. Autocomplete: VS Code knows user_id is int
```

---

# SECTION 13 — INTERVIEW QUESTIONS

## Q1. What is FastAPI?

FastAPI is a modern Python web framework for building APIs. It is built on ASGI (specifically on Starlette) and uses Python type hints extensively for automatic request validation, serialization, and documentation generation. It is one of the fastest Python frameworks available and natively supports async/await.

## Q2. What is the difference between FastAPI and Uvicorn?

Uvicorn is the ASGI web server — it handles the networking layer: opening ports, accepting TCP connections, parsing HTTP, and speaking ASGI. FastAPI is the application framework — it handles routing, validation, serialization, and calling your functions. FastAPI never opens a port. Uvicorn never routes a URL. You always need both: `uvicorn main:app --reload`.

## Q3. What is a path parameter vs query parameter?

A path parameter identifies a specific resource by being part of the URL path: `/users/{user_id}`. It is required. A query parameter modifies how data is returned and appears after `?` in the URL: `/items?skip=0&limit=10`. It is usually optional with defaults. Path: "give me THIS thing." Query: "give me things, but filtered THIS way."

## Q4. How does FastAPI validate path parameters automatically?

Through Python type hints. `user_id: int` tells FastAPI to convert and validate the URL segment as an integer. If `/users/hello` is requested, FastAPI returns 422 Unprocessable Entity without you writing any try/except block. The validation happens before your function is called.

## Q5. What is Swagger UI and how does FastAPI generate it?

Swagger UI is an interactive API documentation interface available at `/docs`. FastAPI generates it automatically by inspecting your route decorators (`@app.get`, etc.) and function type hints. Every route, parameter type, default value, and response appears in the docs without any manual documentation work. It stays in sync with your code automatically.

## Q6. What does `--reload` do in the uvicorn command?

`--reload` enables development mode. When you save your Python file, Uvicorn automatically detects the change and restarts the server. You don't need to stop and restart manually. It should only be used in development, not in production (it adds overhead for watching file changes).

## Q7. Why does FastAPI use Python type hints so heavily?

Type hints provide three things simultaneously: validation (FastAPI rejects invalid inputs before your code runs), serialization (FastAPI knows how to convert your return type to JSON), and documentation (FastAPI reads types to generate accurate Swagger docs). One type hint does the work of what traditionally required three separate pieces of code.

---

# SECTION 14 — LEETCODE #303: RANGE SUM QUERY - IMMUTABLE

## Problem

Given an integer array `nums`, answer multiple `sumRange(left, right)` queries returning the sum of elements between index `left` and `right` inclusive. The array never changes.

```
nums = [-2, 0, 3, -5, 2, -1]

sumRange(0, 2) → -2+0+3   = 1
sumRange(2, 5) → 3-5+2-1  = -1
sumRange(0, 5) → -2+0+3-5+2-1 = -3
```

## Why Brute Force Fails

```
Brute force: for each query, loop from left to right and sum.
Time: O(n) per query.
If 10,000 queries on 10,000 elements: 10,000 × 10,000 = 100,000,000 operations.

The problem says: "sumRange() can be called at most 10⁴ times."
Brute force: 10⁴ × 10⁴ = 10⁸ operations → too slow.
```

## The Insight: Preprocessing

```
The array NEVER CHANGES.

Instead of recalculating for every query,
compute something ONCE in __init__() that makes every future query O(1).

That "something" is the Prefix Sum array.
```

## Prefix Sum Array

```
nums:    [-2,  0,  3, -5,  2, -1]
index:     0   1   2   3   4   5

prefix:  [-2, -2,  1, -4, -2, -3]

prefix[i] = sum of nums[0] through nums[i]

prefix[0] = -2
prefix[1] = -2 + 0   = -2
prefix[2] = -2 + 0 + 3 = 1
prefix[3] = -2 + 0 + 3 - 5 = -4
prefix[4] = -2 + 0 + 3 - 5 + 2 = -2
prefix[5] = -2 + 0 + 3 - 5 + 2 - 1 = -3
```

## The Formula

```
Case 1: left == 0
  sumRange(0, right) = prefix[right]
  (sum from beginning to right — already stored)

Case 2: left > 0
  sumRange(left, right) = prefix[right] - prefix[left-1]
  
  Why? prefix[right] = sum of nums[0..right]
       prefix[left-1] = sum of nums[0..left-1]
       Subtracting removes the "before left" portion.
       Result: sum of nums[left..right]
```

**Example:**

```
sumRange(2, 5):
  prefix[5] = -3  (sum of all elements)
  prefix[1] = -2  (sum of elements before index 2)
  Answer = -3 - (-2) = -3 + 2 = -1 ✅
```

## The Complete Solution

```python
class NumArray(object):

    def __init__(self, nums):
        self.prefix = []
        running_sum = 0

        for i in range(len(nums)):
            running_sum += nums[i]          # Add current element
            self.prefix.append(running_sum) # Store cumulative sum

        # After __init__ with nums = [-2, 0, 3, -5, 2, -1]:
        # self.prefix = [-2, -2, 1, -4, -2, -3]

    def sumRange(self, left, right):
        if left == 0:
            return self.prefix[right]       # No subtraction needed
        else:
            return self.prefix[right] - self.prefix[left - 1]

# Usage:
obj = NumArray([-2, 0, 3, -5, 2, -1])
obj.sumRange(0, 2)   # 1
obj.sumRange(2, 5)   # -1
obj.sumRange(0, 5)   # -3
```

## Dry Run — Building Prefix Sum

```
nums = [-2, 0, 3, -5, 2, -1]

Initially: running_sum = 0, prefix = []

i=0: running_sum = 0 + (-2) = -2    prefix = [-2]
i=1: running_sum = -2 + 0  = -2    prefix = [-2, -2]
i=2: running_sum = -2 + 3  =  1    prefix = [-2, -2, 1]
i=3: running_sum =  1 + (-5) = -4  prefix = [-2, -2, 1, -4]
i=4: running_sum = -4 + 2  = -2    prefix = [-2, -2, 1, -4, -2]
i=5: running_sum = -2 + (-1) = -3  prefix = [-2, -2, 1, -4, -2, -3]
```

## Why `__init__` is the Right Place for Preprocessing

```
__init__ runs EXACTLY ONCE when the object is created.
sumRange() can run thousands of times.

Build the prefix array once (O(n)).
Answer every future query instantly (O(1)).

This is the time/space tradeoff:
  Spend O(n) space on the prefix array.
  Save O(n) time on every single query.

For 10,000 queries: saves nearly 10,000 × n operations.
```

## Complexity

```
__init__():  O(n) time,  O(n) space
sumRange():  O(1) time,  O(1) extra space

Total (k queries): O(n + k) instead of O(n × k)
```

## Complexity Comparison

```
Approach         Build      Query      For 10k queries on 10k elements
─────────────────────────────────────────────────────────────────────
Brute Force      O(1)       O(n)       10⁸ operations → slow
Prefix Sum       O(n)       O(1)       10⁴ operations → fast
```

**Result:** ✅ Accepted | 15/15 test cases | Runtime: 7ms | Beats 53.12%

## The Prefix Sum Pattern Family

```
This pattern appears in many important problems:

Problem                         Pattern Used
──────────────────────────────────────────────────────
#1480 Running Sum of 1d Array   Accumulate running sum
#724  Find Pivot Index           Left/right running sums
#303  Range Sum Query (this)     Prefix sum for O(1) queries
#560  Subarray Sum Equals K      Prefix sum + hash map
#238  Product of Array Except Self  Left/right prefix products
#304  Range Sum Query 2D         2D prefix sum

Core idea: "Don't recalculate. Precompute and reuse."
```

---

# SECTION 15 — IMPORTANT THINGS TO KNOW

```
 1. FastAPI doesn't open ports. Uvicorn does.
    FastAPI is the application. Uvicorn is the server.

 2. uvicorn main:app — "main" is the filename, "app" is the variable.
    If you name your file server.py and your instance api = FastAPI(),
    the command becomes: uvicorn server:api --reload

 3. --reload is for development only.
    Production: uvicorn main:app --workers 4 (no --reload)

 4. @app.get("/") is a decorator that registers the route.
    It does NOT call the function immediately.

 5. Return a Python dict → FastAPI converts it to JSON automatically.
    No need to call json.dumps() manually.

 6. Path parameters: {variable_name} in the URL.
    Function must have a parameter with the SAME name.

 7. Query parameters: function parameters with default values.
    No curly braces in the URL needed.

 8. Type hints provide THREE things simultaneously:
    Validation, Serialization, Documentation.

 9. Swagger UI (/docs) is generated automatically from type hints.
    ReDoc (/redoc) is another auto-generated docs format.

10. HTTP 422 Unprocessable Entity = validation failed.
    FastAPI returns this automatically for type mismatches.

11. ASGI replaced WSGI for modern Python web development.
    ASGI supports async, WebSockets, and long-lived connections.

12. Path parameter order matters.
    GET /users/me and GET /users/{user_id} could conflict.
    FastAPI routes match top-to-bottom — define specific routes BEFORE generic ones.

13. Query parameters with no default value are REQUIRED query params.
    query_param: str → required
    query_param: str = "default" → optional with default

14. FastAPI is built on Starlette (ASGI routing) and Pydantic (validation).
    Learning these two libraries explains 80% of FastAPI's behavior.

15. The auto-generated OpenAPI spec is available at:
    http://127.0.0.1:8000/openapi.json
    Every major API tooling understands this format.
```

---

# REVISION SHEET

```
═══════════════════════════════════════════════════════════
FASTAPI DAY 43 — ONE-PAGE REVISION
═══════════════════════════════════════════════════════════

INSTALL:
  pip install fastapi uvicorn

MINIMAL APP:
  from fastapi import FastAPI
  app = FastAPI()
  @app.get("/")
  def home():
      return {"message": "Hello"}

RUN:
  python -m uvicorn main:app --reload

SWAGGER:
  http://127.0.0.1:8000/docs

PATH PARAMETER:
  @app.get("/users/{user_id}")
  def get_user(user_id: int):
      return {"user_id": user_id}
  Test: /users/42  → {"user_id": 42}
  Test: /users/abc → 422 (validation error)

QUERY PARAMETER:
  @app.get("/items")
  def get_items(skip: int = 0, limit: int = 10):
      return {"skip": skip, "limit": limit}
  Test: /items              → skip=0, limit=10 (defaults)
  Test: /items?skip=20      → skip=20, limit=10
  Test: /items?skip=5&limit=5 → skip=5, limit=5

PATH vs QUERY:
  Path  → identifies a resource → /users/{user_id}
  Query → modifies the request  → /users?limit=10

REQUEST LIFECYCLE:
  Browser → Uvicorn → FastAPI → Your function → dict → JSON → Browser

FASTAPI = application (routing, validation, docs)
UVICORN = server (ports, TCP, HTTP, ASGI)

TYPE HINTS:
  : int → validates, documents, autocompletes (all three at once)

PREFIX SUM (#303):
  Build prefix array once in __init__: O(n)
  Answer each query in sumRange():     O(1)
  Formula: prefix[right] - prefix[left-1]   (when left > 0)
           prefix[right]                    (when left == 0)
```

---

## LeetCode Solved This Day

| Problem | Difficulty | Topic | Status | Runtime |
|---------|-----------|-------|--------|---------|
| #303 Range Sum Query - Immutable | Easy | Prefix Sum, Preprocessing, O(1) query | ✅ Accepted 15/15 | 7ms |

---

*Day 43 Complete. First FastAPI server running. Phase 2 has begun.* ✅