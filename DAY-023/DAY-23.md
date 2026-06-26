# DAY 23 — REST API CONCEPTS (NON-NEGOTIABLE)

> **Goal:** Understand what an API is, what REST means, how JSON works, and how to actually call real APIs.
>
> **Week:** W4 — How the Web Works + Git + Advanced Python
>
> **Status:** ✅

---

# WHY THIS DAY IS IMPORTANT

You will spend your entire backend career building APIs.

Not understanding what an API is, what REST means, and how JSON works is like a chef not knowing what cooking is.

Most beginners jump straight into FastAPI and start writing routes.

But they don't understand:

- What exactly is an API?
- Why is it called REST?
- Who decided these rules?
- Why does JSON look exactly like a Python dictionary?
- What makes an API "RESTful" vs just an endpoint?
- What is HATEOAS?
- What is the difference between REST and GraphQL?
- What is OpenAPI and Swagger?
- Why do companies like Stripe and Razorpay have API documentation?

Today you will understand all of this from the ground up.

---

# SECTION 1 — WHAT IS AN API?

## THE SIMPLEST EXPLANATION

**API = Application Programming Interface**

The word "interface" is the key.

An interface is a point where two things **meet and interact.**

Examples of interfaces:

```
TV Remote      = Interface between you and TV
Steering Wheel = Interface between you and car
Menu at restaurant = Interface between you and kitchen
```

An **API** is the interface between two software systems.

---

## THE RESTAURANT ANALOGY (DEEP VERSION)

Imagine a restaurant.

```
You (Customer)
    │
    │ "I want Butter Chicken"
    ▼
Waiter (API)
    │
    │ Carries your order to kitchen
    ▼
Kitchen (Backend + Database)
    │
    │ Prepares food
    ▼
Waiter (API)
    │
    │ Brings food back to you
    ▼
You (Customer)
    │
    │ Receives food
```

Notice:

- You **never go into the kitchen** yourself.
- You don't need to know **how the food is made.**
- You just use the **menu (API documentation)** to order.
- The waiter **carries your request** and **returns the result.**

This is exactly how APIs work.

---

## REAL WORLD API EXAMPLES

**Weather App on your phone:**

```
Your phone (client)
    │
    │ API call: GET /weather?city=Bangalore
    ▼
OpenWeatherMap servers
    │
    │ Returns: {"temp": 28, "humidity": 65}
    ▼
Your phone displays the weather
```

Your phone doesn't store weather data. It **asks** OpenWeatherMap via API.

---

**Paytm Payment:**

```
Your app
    │
    │ API call: POST /payments
    │ Body: {amount: 500, to: "merchant_id"}
    ▼
Paytm API servers
    │
    │ Processes payment
    │ Calls bank APIs internally
    │
    │ Returns: {"status": "success", "transaction_id": "TXN123"}
    ▼
Your app shows "Payment Successful"
```

---

**Login with Google:**

```
Your app
    │
    │ "User wants to login with Google"
    ▼
Google OAuth API
    │
    │ Verifies Google account
    │
    │ Returns: {"email": "adya@gmail.com", "name": "Adyaprana"}
    ▼
Your app logs the user in
```

---

## TYPES OF APIs

```
1. REST API        → Most common. Uses HTTP. JSON responses.
2. GraphQL API     → Query language for APIs. One endpoint. You choose what data you get.
3. SOAP API        → Old. Uses XML. Still in banking/enterprise.
4. gRPC API        → Fast. Uses Protocol Buffers. For microservices.
5. WebSocket API   → Real-time. Two-way connection. Chat apps.
```

**As a Python backend developer, you will primarily build REST APIs.**

You will encounter GraphQL and gRPC as you grow.

---

## PUBLIC API vs PRIVATE API vs PARTNER API

```
Public API:
  Open to everyone.
  Examples: OpenWeatherMap, JSONPlaceholder, GitHub API
  May require API key for rate limiting.

Private API:
  Internal use only.
  Example: Your company's internal services talking to each other.
  Not exposed to the internet.

Partner API:
  Shared with specific business partners.
  Example: Razorpay gives payment API to merchants.
  Requires agreement and authentication.
```

---

# SECTION 2 — WHAT IS REST?

## THE FORMAL DEFINITION

**REST = Representational State Transfer**

Created by **Roy Fielding** in his PhD dissertation in **2000**.

Roy Fielding was one of the primary authors of the HTTP specification itself.

He looked at what made the web scalable and defined a set of principles.

He called this architectural style **REST.**

---

## WHAT "REPRESENTATIONAL STATE TRANSFER" MEANS

Break it down:

**Resource** — Any data object with an identity.

```
A User is a resource.
A Product is a resource.
An Order is a resource.
A Post is a resource.
```

**Representation** — How the resource is sent to the client.

```
The server has a User in the database.
When it sends the User to the client, it sends a REPRESENTATION.
Usually JSON.
Sometimes XML.
The actual database record never leaves the server.
```

**State Transfer** — The server transfers the current state of the resource to the client.

```
GET /users/42
→ Server reads user 42's current state from database
→ Creates a JSON representation of that state
→ Transfers it to the client
```

So **REST = Transfer the current representation of a resource's state.**

---

## REST IS NOT A STANDARD

This confuses many people.

REST is not:

```
❌ A protocol (like HTTP or TCP)
❌ A framework
❌ A specification with strict rules
```

REST is:

```
✅ An architectural style
✅ A set of design principles
✅ A way of thinking about APIs
```

Two developers can build REST APIs and disagree on implementation details. That's fine.

What matters is following the core constraints.

---

# SECTION 3 — THE 6 REST CONSTRAINTS (DEEP DIVE)

Roy Fielding defined 6 constraints. If your API follows these, it is RESTful.

---

## CONSTRAINT 1: CLIENT-SERVER SEPARATION

**Rule:** The client and server are completely independent.

Client handles:

```
User interface
User experience
Presentation logic
```

Server handles:

```
Business logic
Data storage
Security
Authentication
```

**Why this matters:**

```
You can completely rebuild your React frontend without touching FastAPI.
You can completely rewrite your FastAPI backend without touching React.
You can have multiple clients (web, iOS, Android) using the same backend.
```

Bad practice (violates this):

```
Server generates HTML and sends it (like old PHP apps)
Frontend talks directly to database
```

Good practice:

```
React → API Call → FastAPI → Database
Flutter App → Same API Call → Same FastAPI → Same Database
```

---

## CONSTRAINT 2: STATELESS

**Rule:** Every request from client to server must contain ALL information needed to understand and process the request.

The server must NOT store any client context between requests.

```
Stateful (BAD):
Request 1: POST /login  → Server remembers "Adyaprana is logged in"
Request 2: GET /profile → Server uses remembered state → Returns profile

Stateless (GOOD):
Request 1: POST /login  → Server returns JWT token
Request 2: GET /profile + Token → Server verifies token → Returns profile
```

**Why stateless?**

```
Scalability:
  Any server in a cluster can handle any request.
  Request 1 can hit Server A.
  Request 2 can hit Server B.
  Both work because all state is in the request itself.

If stateful:
  Request 2 MUST hit Server A (where session is stored)
  This breaks horizontal scaling
```

**Common interview trap:**

```
"Does stateless mean no database?"

Answer: NO.
Stateless means the SERVER doesn't remember client context between requests.
The DATABASE stores data. That's different.
The server accesses database fresh for every request.
```

---

## CONSTRAINT 3: CACHEABLE

**Rule:** Responses must define themselves as either cacheable or non-cacheable.

If cacheable, the client (or intermediate caches) can reuse that response for future equivalent requests.

```
Cache-Control: max-age=3600       → Cache for 1 hour
Cache-Control: no-store           → Never cache
ETag: "abc123"                     → Version identifier for caching
```

**Examples:**

```
GET /logo.png             → Cache for 1 year (rarely changes)
GET /products             → Cache for 5 minutes
GET /users/42/balance     → No cache (changes frequently)
POST /orders              → No cache (creates new data)
```

**Benefits:**

```
Reduces server load
Faster response for client
Less bandwidth usage
```

**CDN (Content Delivery Network)** is built entirely on this concept.

---

## CONSTRAINT 4: UNIFORM INTERFACE

This is the **most important and defining constraint of REST.**

It has 4 sub-constraints:

### 4a. Resource Identification in Requests

Resources are identified by URLs.

```
/users/42        → Identifies user with ID 42
/products/iphone → Identifies iPhone product
/orders/ORD-001  → Identifies order ORD-001
```

The URL is the resource's address. It never changes regardless of what representation is returned.

---

### 4b. Resource Manipulation Through Representations

When a client holds a representation of a resource, it has enough information to modify or delete the resource.

```
GET /users/42
→ Returns: {"id": 42, "name": "Adyaprana", "city": "Bangalore"}

Client wants to update city:
PATCH /users/42
Body: {"city": "Mumbai"}

Client wants to delete:
DELETE /users/42
```

The representation contains everything needed to manipulate the resource.

---

### 4c. Self-Descriptive Messages

Each message includes enough information to describe how to process it.

```http
POST /users HTTP/1.1
Content-Type: application/json     ← How to parse the body
Accept: application/json           ← What format to return

{"name": "Adyaprana"}
```

The server knows exactly how to parse the body because `Content-Type` says so.

---

### 4d. HATEOAS

**HATEOAS = Hypermedia As The Engine Of Application State**

This is the most advanced REST concept.

The API response includes links to related actions the client can take.

Example WITHOUT HATEOAS:

```json
{
  "id": 42,
  "name": "Adyaprana",
  "order_count": 3
}
```

Client must know separately: "To get orders, call GET /users/42/orders"

Example WITH HATEOAS:

```json
{
  "id": 42,
  "name": "Adyaprana",
  "order_count": 3,
  "_links": {
    "self": {"href": "/users/42"},
    "orders": {"href": "/users/42/orders"},
    "update": {"href": "/users/42", "method": "PATCH"},
    "delete": {"href": "/users/42", "method": "DELETE"}
  }
}
```

The response tells the client exactly what it can do next.

Most real-world REST APIs don't fully implement HATEOAS. It's a Level 3 concept (Richardson Maturity Model).

---

## CONSTRAINT 5: LAYERED SYSTEM

**Rule:** A client cannot tell whether it is connected directly to the end server or to an intermediary.

The client just calls the API. It doesn't know:

```
Is this the actual FastAPI server?
Is this a load balancer?
Is this a CDN?
Is this an API gateway?
Is this a caching layer?
Is this a security proxy?
```

Example architecture the client has no idea about:

```
Client
  │
  ▼
Cloudflare (CDN + DDoS protection)
  │
  ▼
AWS API Gateway (Rate limiting, authentication)
  │
  ▼
Load Balancer (Distributes to multiple servers)
  │
  ▼
FastAPI Server 1  or  FastAPI Server 2  or  FastAPI Server 3
  │
  ▼
PostgreSQL Database
```

Client sees only one URL: `api.yourapp.com`

This is the power of layered architecture.

---

## CONSTRAINT 6: CODE ON DEMAND (OPTIONAL)

**Rule:** Servers can optionally send executable code to clients.

Example: Server sends JavaScript that the browser executes.

This is the only **optional** REST constraint.

Rarely discussed. Rarely used in modern APIs.

---

## THE RICHARDSON MATURITY MODEL

Leonard Richardson created a model to measure how "RESTful" an API is.

```
Level 0 — The Swamp of POX
  Single URL, all operations via POST
  Example: POST /api {"action": "getUser", "id": 42}
  This is NOT REST at all.

Level 1 — Resources
  Multiple URLs for different resources
  Example: POST /users, POST /products
  Still using POST for everything.

Level 2 — HTTP Verbs
  Using correct HTTP methods (GET, POST, PUT, PATCH, DELETE)
  Most "REST" APIs are actually Level 2.
  Example: GET /users/42, DELETE /users/42

Level 3 — Hypermedia Controls (HATEOAS)
  Responses include links to related actions
  True REST according to Roy Fielding
  Very few APIs implement this fully
```

**Most real-world production APIs are Level 2.**

When someone says "RESTful API," they usually mean Level 2.

---

# SECTION 4 — JSON (COMPLETE GUIDE)

## WHAT IS JSON?

**JSON = JavaScript Object Notation**

Invented by **Douglas Crockford** around 2001.

Why it became the standard:

```
Lightweight (small file size)
Human-readable (you can read it without tools)
Machine-parseable (easy to parse in any language)
Language-independent (Python, JavaScript, Java all support it)
```

Before JSON, XML was used. JSON replaced it for most web APIs.

---

## JSON DATA TYPES

JSON supports exactly **6 data types:**

```
1. String    → "hello"
2. Number    → 42 or 3.14
3. Boolean   → true or false (lowercase in JSON)
4. Null      → null
5. Object    → {"key": "value"}
6. Array     → [1, 2, 3]
```

**Critical: JSON booleans are lowercase.**

```json
true    ← JSON (correct)
false   ← JSON (correct)
True    ← Python (NOT valid JSON)
False   ← Python (NOT valid JSON)
```

This trips up every Python developer at some point.

---

## JSON OBJECT

Uses curly braces `{}`.

Contains key-value pairs.

Keys must ALWAYS be strings (double quotes).

```json
{
  "name": "Adyaprana",
  "age": 23,
  "is_active": true,
  "score": 9.5,
  "nickname": null
}
```

---

## JSON ARRAY

Uses square brackets `[]`.

Contains ordered list of values.

```json
[
  "Python",
  "FastAPI",
  "PostgreSQL",
  "Redis",
  "Docker"
]
```

Array of objects (very common in APIs):

```json
[
  {"id": 1, "name": "Adyaprana"},
  {"id": 2, "name": "Ravi"},
  {"id": 3, "name": "Priya"}
]
```

This is what `GET /users` typically returns.

---

## NESTED JSON

JSON inside JSON. Extremely common.

```json
{
  "user": {
    "id": 42,
    "name": "Adyaprana",
    "address": {
      "street": "MG Road",
      "city": "Bangalore",
      "state": "Karnataka",
      "pincode": "560001"
    },
    "skills": ["Python", "FastAPI", "PostgreSQL"],
    "social": {
      "github": "github.com/Adyaprana",
      "linkedin": "linkedin.com/in/adyaprana21"
    }
  }
}
```

Python access pattern:

```python
data["user"]["address"]["city"]      # "Bangalore"
data["user"]["skills"][0]            # "Python"
data["user"]["social"]["github"]     # "github.com/Adyaprana"
```

---

## JSON vs PYTHON DICTIONARY — THE COMPARISON

This is why Python developers love working with JSON.

| JSON | Python |
|---|---|
| `"string"` | `"string"` |
| `42` | `42` |
| `3.14` | `3.14` |
| `true` | `True` |
| `false` | `False` |
| `null` | `None` |
| `{"key": "value"}` | `{"key": "value"}` |
| `[1, 2, 3]` | `[1, 2, 3]` |

**Differences:**

```
JSON booleans:   true / false    (lowercase)
Python booleans: True / False    (uppercase)

JSON null:       null
Python null:     None

JSON keys:       Must be strings ("name": ...)
Python keys:     Can be anything (42: ..., True: ...)
```

---

## WORKING WITH JSON IN PYTHON

### Parsing JSON string to Python dict

```python
import json

json_string = '{"name": "Adyaprana", "age": 23}'
data = json.loads(json_string)

print(data["name"])   # Adyaprana
print(type(data))     # <class 'dict'>
```

---

### Converting Python dict to JSON string

```python
import json

data = {
    "name": "Adyaprana",
    "age": 23,
    "active": True,   # Python True → JSON true
    "score": None     # Python None → JSON null
}

json_string = json.dumps(data)
print(json_string)
# {"name": "Adyaprana", "age": 23, "active": true, "score": null}
```

---

### Pretty printing JSON

```python
import json

data = {"users": [{"id": 1, "name": "Adya"}, {"id": 2, "name": "Ravi"}]}

print(json.dumps(data, indent=2))
# {
#   "users": [
#     {
#       "id": 1,
#       "name": "Adya"
#     },
#     {
#       "id": 2,
#       "name": "Ravi"
#     }
#   ]
# }
```

---

### Reading JSON from file

```python
import json

with open("data.json", "r") as f:
    data = json.load(f)

print(data)
```

---

### Writing JSON to file

```python
import json

data = {"name": "Adyaprana", "role": "Backend Developer"}

with open("output.json", "w") as f:
    json.dump(data, f, indent=2)
```

---

## JSON IN FASTAPI

FastAPI automatically handles JSON conversion.

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    name: str
    age: int
    active: bool = True

@app.post("/users")
def create_user(user: User):
    # FastAPI automatically:
    # 1. Parses incoming JSON body
    # 2. Validates it against User model
    # 3. Converts response dict to JSON
    return {
        "id": 42,
        "name": user.name,
        "age": user.age,
        "active": user.active
    }
```

Send:

```json
{
  "name": "Adyaprana",
  "age": 23
}
```

Receive:

```json
{
  "id": 42,
  "name": "Adyaprana",
  "age": 23,
  "active": true
}
```

---

# SECTION 5 — REST API DESIGN PATTERNS

## RESOURCE NAMING CONVENTIONS

```
Use nouns, not verbs:

✅  /users
❌  /getUsers

✅  /orders
❌  /createOrder

✅  /posts/42/comments
❌  /getCommentsForPost42
```

---

## PLURAL vs SINGULAR

Always use **plural** for collection endpoints.

```
✅  /users         (collection)
✅  /users/42      (single item)
❌  /user          (inconsistent)
❌  /user/42       (inconsistent)
```

---

## NESTED RESOURCES

When one resource belongs to another:

```
GET  /users/42/orders          → All orders of user 42
GET  /users/42/orders/7        → Specific order 7 of user 42
POST /users/42/orders          → Create order for user 42
DELETE /users/42/orders/7      → Delete order 7 of user 42

GET  /posts/10/comments        → All comments on post 10
POST /posts/10/comments        → Add comment to post 10
DELETE /posts/10/comments/5    → Delete comment 5 on post 10
```

---

## STANDARD CRUD PATTERN

For any resource, the standard REST pattern is:

```
GET    /resources           → List all resources
POST   /resources           → Create new resource
GET    /resources/{id}      → Get specific resource
PUT    /resources/{id}      → Replace resource
PATCH  /resources/{id}      → Update resource
DELETE /resources/{id}      → Delete resource
```

Example for `products`:

```
GET    /products            → List all products
POST   /products            → Create product
GET    /products/42         → Get product 42
PUT    /products/42         → Replace product 42
PATCH  /products/42         → Update product 42
DELETE /products/42         → Delete product 42
```

---

## API RESPONSE STANDARDS

### Consistent success response

```json
{
  "success": true,
  "data": {
    "id": 42,
    "name": "Adyaprana"
  },
  "message": "User created successfully"
}
```

---

### Consistent error response

```json
{
  "success": false,
  "error": {
    "code": "USER_NOT_FOUND",
    "message": "User with id 999 does not exist"
  }
}
```

---

### List response with pagination

```json
{
  "success": true,
  "data": [
    {"id": 1, "name": "Adyaprana"},
    {"id": 2, "name": "Ravi"}
  ],
  "pagination": {
    "page": 1,
    "limit": 10,
    "total": 500,
    "total_pages": 50
  }
}
```

---

# SECTION 6 — API DOCUMENTATION

## WHY API DOCUMENTATION MATTERS

When you build a REST API, other developers need to use it.

They need to know:

```
What endpoints exist?
What HTTP method to use?
What parameters to send?
What body format?
What response format?
What status codes to expect?
What authentication is needed?
```

API documentation answers all of this.

---

## OPENAPI SPECIFICATION

**OpenAPI** (formerly Swagger) is the standard for documenting REST APIs.

It's a JSON/YAML file that describes your entire API.

FastAPI **automatically generates** OpenAPI documentation.

When you run FastAPI:

```
http://localhost:8000/docs       → Swagger UI (interactive documentation)
http://localhost:8000/redoc      → ReDoc (clean documentation)
http://localhost:8000/openapi.json → Raw OpenAPI spec
```

Example of auto-generated docs:

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="My Backend API",
    description="API for managing users and orders",
    version="1.0.0"
)

class User(BaseModel):
    name: str
    email: str

@app.post("/users", summary="Create a new user", tags=["Users"])
def create_user(user: User):
    """
    Create a new user account.
    
    - **name**: Full name of the user
    - **email**: Valid email address
    """
    return {"id": 1, **user.dict()}
```

FastAPI generates complete interactive documentation automatically.

---

## REAL API DOCUMENTATION EXAMPLES

Study these as a backend developer:

```
Stripe API:    https://stripe.com/docs/api
GitHub API:    https://docs.github.com/en/rest
Razorpay API:  https://razorpay.com/docs/api
Twitter API:   https://developer.twitter.com/en/docs
OpenWeather:   https://openweathermap.org/api
```

Every professional API has documentation like this.

Your portfolio projects should too.

---

# SECTION 7 — REST vs OTHER API STYLES

## REST vs GraphQL

| Feature | REST | GraphQL |
|---|---|---|
| Created by | Roy Fielding (2000) | Facebook (2015) |
| Endpoints | Multiple (one per resource) | Single endpoint (`/graphql`) |
| Data fetching | Server decides what to return | Client decides what to get |
| Over-fetching | Common (get more data than needed) | Never (get exactly what you ask for) |
| Under-fetching | Common (multiple requests needed) | Never (one request for all data) |
| Learning curve | Easy | Medium |
| Tooling | Mature | Growing |
| Best for | Simple CRUD APIs | Complex data relationships |

**REST Example:**

```http
GET /users/42
→ Returns ALL user fields (even ones you don't need)

GET /users/42/posts
→ Second request needed for posts
```

**GraphQL Example:**

```graphql
query {
  user(id: 42) {
    name
    email
    posts {
      title
      createdAt
    }
  }
}
```

One request. Exactly the fields you asked for.

---

## REST vs gRPC

| Feature | REST | gRPC |
|---|---|---|
| Created by | Roy Fielding (2000) | Google (2015) |
| Protocol | HTTP | HTTP/2 |
| Data format | JSON | Protocol Buffers (binary) |
| Speed | Slower (JSON parsing) | Very fast (binary) |
| Human-readable | Yes | No (binary) |
| Best for | Public APIs | Internal microservices |

**gRPC** is used when two backend services need to communicate with very high performance.

Not for public APIs. Not for frontend-backend communication.

---

## REST vs WebSocket

| Feature | REST | WebSocket |
|---|---|---|
| Communication | Request-Response | Full-duplex (both directions) |
| Connection | New connection per request | Persistent connection |
| Real-time | No | Yes |
| Best for | CRUD operations | Chat, live updates, gaming |

**WebSocket Example:**

```
WhatsApp Web:
  You send a message: WebSocket sends to server.
  Server pushes message to receiver: WebSocket pushes to browser.
  No polling needed.
```

---

# SECTION 8 — PRACTICAL CODE (BEYOND YOUR FILES)

## WORKING WITH THE JSONPLACEHOLDER API

JSONPlaceholder: `https://jsonplaceholder.typicode.com`

A fake REST API for testing. Supports all HTTP methods.

Available resources:

```
/posts      (100 posts)
/comments   (500 comments)
/albums     (100 albums)
/photos     (5000 photos)
/todos      (200 todos)
/users      (10 users)
```

---

## COMPLETE PYTHON SCRIPT — ALL METHODS

```python
import requests
import json

BASE_URL = "https://jsonplaceholder.typicode.com"

# ─────────────────────────────────────────
# GET — Fetch all posts
# ─────────────────────────────────────────
response = requests.get(f"{BASE_URL}/posts")
posts = response.json()
print(f"Total posts: {len(posts)}")
print(f"First post title: {posts[0]['title']}")
print()

# ─────────────────────────────────────────
# GET — Fetch single post
# ─────────────────────────────────────────
response = requests.get(f"{BASE_URL}/posts/1")
post = response.json()
print(f"Post ID: {post['id']}")
print(f"Title: {post['title']}")
print()

# ─────────────────────────────────────────
# GET — Fetch with query params (filter)
# ─────────────────────────────────────────
response = requests.get(f"{BASE_URL}/posts", params={"userId": 1})
user_posts = response.json()
print(f"Posts by user 1: {len(user_posts)}")
print()

# ─────────────────────────────────────────
# POST — Create new resource
# ─────────────────────────────────────────
new_post = {
    "title": "Learning REST APIs",
    "body": "Day 23 of Backend Developer Journey",
    "userId": 1
}
response = requests.post(f"{BASE_URL}/posts", json=new_post)
created = response.json()
print(f"Status: {response.status_code}")     # 201
print(f"Created ID: {created['id']}")        # 101
print()

# ─────────────────────────────────────────
# PUT — Replace entire resource
# ─────────────────────────────────────────
update_data = {
    "id": 1,
    "title": "Updated Title",
    "body": "Updated body content",
    "userId": 1
}
response = requests.put(f"{BASE_URL}/posts/1", json=update_data)
print(f"PUT Status: {response.status_code}")   # 200
print(f"Updated: {response.json()['title']}")
print()

# ─────────────────────────────────────────
# PATCH — Update partial resource
# ─────────────────────────────────────────
partial_update = {"title": "Only Title Changed"}
response = requests.patch(f"{BASE_URL}/posts/1", json=partial_update)
print(f"PATCH Status: {response.status_code}")   # 200
print(f"Patched title: {response.json()['title']}")
print()

# ─────────────────────────────────────────
# DELETE — Remove resource
# ─────────────────────────────────────────
response = requests.delete(f"{BASE_URL}/posts/1")
print(f"DELETE Status: {response.status_code}")   # 200
print(f"Response: {response.json()}")             # {}
```

---

## PARSING NESTED JSON RESPONSES

```python
import requests

# Get user with full nested data
response = requests.get("https://jsonplaceholder.typicode.com/users/1")
user = response.json()

# Access nested data
name = user["name"]
email = user["email"]
city = user["address"]["city"]
zipcode = user["address"]["zipcode"]
lat = user["address"]["geo"]["lat"]
lng = user["address"]["geo"]["lng"]
company = user["company"]["name"]

print(f"Name: {name}")
print(f"Email: {email}")
print(f"City: {city}")
print(f"Location: {lat}, {lng}")
print(f"Company: {company}")

# Safe access (avoid KeyError)
username = user.get("username", "Not provided")
website = user.get("website", "Not provided")
print(f"Username: {username}")
```

---

## HANDLING API ERRORS PROPERLY

```python
import requests

def get_user(user_id: int):
    try:
        response = requests.get(
            f"https://jsonplaceholder.typicode.com/users/{user_id}",
            timeout=5   # Wait max 5 seconds
        )

        # Check if request was successful
        response.raise_for_status()   # Raises exception for 4xx/5xx

        return response.json()

    except requests.exceptions.Timeout:
        print("Request timed out")
        return None

    except requests.exceptions.ConnectionError:
        print("Could not connect to server")
        return None

    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e.response.status_code}")
        if e.response.status_code == 404:
            print("User not found")
        elif e.response.status_code == 401:
            print("Unauthorized — check your API key")
        elif e.response.status_code == 500:
            print("Server error — try again later")
        return None

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

# Usage
user = get_user(1)
if user:
    print(f"Found: {user['name']}")

user = get_user(9999)  # Non-existent user
if not user:
    print("User not found")
```

---

## USING HEADERS WITH REQUESTS

```python
import requests

# API key authentication
headers = {
    "Authorization": "Bearer YOUR_JWT_TOKEN",
    "Content-Type": "application/json",
    "Accept": "application/json",
    "X-API-Version": "2.0"
}

response = requests.get(
    "https://api.example.com/profile",
    headers=headers
)

print(response.status_code)
print(response.json())
```

---

## BUILDING A MINI API CLIENT CLASS

```python
import requests

class JSONPlaceholderClient:
    """A simple client for the JSONPlaceholder API"""

    BASE_URL = "https://jsonplaceholder.typicode.com"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json"
        })

    def get_all_posts(self):
        response = self.session.get(f"{self.BASE_URL}/posts")
        response.raise_for_status()
        return response.json()

    def get_post(self, post_id: int):
        response = self.session.get(f"{self.BASE_URL}/posts/{post_id}")
        response.raise_for_status()
        return response.json()

    def get_user_posts(self, user_id: int):
        response = self.session.get(
            f"{self.BASE_URL}/posts",
            params={"userId": user_id}
        )
        response.raise_for_status()
        return response.json()

    def create_post(self, title: str, body: str, user_id: int):
        payload = {"title": title, "body": body, "userId": user_id}
        response = self.session.post(f"{self.BASE_URL}/posts", json=payload)
        response.raise_for_status()
        return response.json()

    def update_post(self, post_id: int, title: str):
        payload = {"title": title}
        response = self.session.patch(
            f"{self.BASE_URL}/posts/{post_id}",
            json=payload
        )
        response.raise_for_status()
        return response.json()

    def delete_post(self, post_id: int):
        response = self.session.delete(f"{self.BASE_URL}/posts/{post_id}")
        response.raise_for_status()
        return True


# Usage
client = JSONPlaceholderClient()

# Get all posts
posts = client.get_all_posts()
print(f"Total posts: {len(posts)}")

# Get posts by user
user_posts = client.get_user_posts(1)
print(f"User 1 has {len(user_posts)} posts")

# Create a post
new_post = client.create_post(
    title="Day 23 - REST APIs",
    body="Learning REST API concepts today",
    user_id=1
)
print(f"Created post with ID: {new_post['id']}")
```

---

## USING REQRES API (WITH REAL AUTH)

ReqRes supports real authentication simulation.

```python
import requests

BASE = "https://reqres.in/api"

# ─────────────────────────────────────────
# REGISTER
# ─────────────────────────────────────────
register_payload = {
    "email": "eve.holt@reqres.in",
    "password": "pistol"
}
response = requests.post(f"{BASE}/register", json=register_payload)
print("Register:", response.status_code)
print(response.json())
# {"id": 4, "token": "QpwL5tpe83ilfN2"}

# ─────────────────────────────────────────
# LOGIN
# ─────────────────────────────────────────
login_payload = {
    "email": "eve.holt@reqres.in",
    "password": "cityslicka"
}
response = requests.post(f"{BASE}/login", json=login_payload)
print("\nLogin:", response.status_code)
data = response.json()
token = data["token"]
print(f"Token received: {token}")

# ─────────────────────────────────────────
# GET USERS (no auth needed on reqres)
# ─────────────────────────────────────────
response = requests.get(f"{BASE}/users?page=2")
users = response.json()
print(f"\nPage: {users['page']}")
print(f"Total users: {users['total']}")
for user in users["data"]:
    print(f"  {user['first_name']} {user['last_name']} — {user['email']}")

# ─────────────────────────────────────────
# DELAYED RESPONSE (Simulates slow API)
# ─────────────────────────────────────────
response = requests.get(f"{BASE}/users?delay=3")
print(f"\nDelayed response: {response.status_code}")
```

---

# SECTION 9 — API AUTHENTICATION METHODS

## 1. API KEY

Simplest form of authentication.

```http
GET /data HTTP/1.1
X-API-Key: sk_live_abc123xyz
```

Or in query params (less secure):

```http
GET /data?api_key=sk_live_abc123xyz
```

Used by: OpenWeatherMap, Google Maps, SendGrid.

---

## 2. BASIC AUTH

Username and password encoded in Base64.

```http
GET /data HTTP/1.1
Authorization: Basic YWRtaW46cGFzc3dvcmQ=
```

`YWRtaW46cGFzc3dvcmQ=` is Base64 of `admin:password`

**Never use over HTTP. Only HTTPS.**

---

## 3. BEARER TOKEN (JWT)

Most common in modern APIs.

```http
GET /profile HTTP/1.1
Authorization: Bearer eyJhbGciOiJIUzI1NiJ9...
```

---

## 4. OAUTH 2.0

For "Login with Google/GitHub/Facebook."

Complex but powerful.

```
Step 1: User clicks "Login with Google"
Step 2: App redirects to Google
Step 3: User logs in on Google
Step 4: Google redirects back with auth code
Step 5: App exchanges code for access token
Step 6: App uses access token to call Google APIs
```

FastAPI has OAuth2PasswordBearer built in.

---

## 5. HMAC SIGNATURES

Used by payment APIs (Razorpay, Stripe).

```
Client:
  Creates HMAC signature of request body using secret key
  Sends signature in header

Server:
  Recreates HMAC using same secret key
  Compares with received signature
  If match → request is authentic
```

This prevents man-in-the-middle tampering.

---

# SECTION 10 — POSTMAN COMPLETE GUIDE

## WHAT IS POSTMAN?

Postman is the world's most popular API testing tool.

Used by:

```
Backend developers — to test their own APIs
Frontend developers — to explore backend APIs
QA engineers — to write automated API tests
DevOps — to monitor API health
```

---

## POSTMAN KEY FEATURES

### Collections

Organize related API requests into groups.

```
My FastAPI Project
├── Auth
│   ├── POST /login
│   ├── POST /register
│   └── POST /logout
├── Users
│   ├── GET /users
│   ├── POST /users
│   ├── GET /users/:id
│   ├── PATCH /users/:id
│   └── DELETE /users/:id
└── Products
    ├── GET /products
    └── POST /products
```

---

### Environments

Switch between development, staging, production URLs easily.

```
Development:  base_url = http://localhost:8000
Staging:      base_url = https://staging.yourapi.com
Production:   base_url = https://api.yourapi.com
```

Your requests use `{{base_url}}/users` and Postman fills in the right URL.

---

### Variables

Store reusable values.

```
{{base_url}}     → http://localhost:8000
{{token}}        → eyJhbGci...
{{user_id}}      → 42
```

In Tests tab (after login):

```javascript
// Automatically save token after login
const data = pm.response.json();
pm.environment.set("token", data.token);
```

---

### Tests in Postman

Write automated tests for your APIs.

```javascript
// Test: Status code is 200
pm.test("Status 200", () => {
    pm.response.to.have.status(200);
});

// Test: Response has name field
pm.test("Has name", () => {
    const data = pm.response.json();
    pm.expect(data.name).to.not.be.empty;
});

// Test: Response time under 500ms
pm.test("Fast response", () => {
    pm.expect(pm.response.responseTime).to.be.below(500);
});
```

---

## THUNDER CLIENT (VS CODE)

A lightweight Postman alternative inside VS Code.

Install: VS Code Extensions → Thunder Client

Advantages:

```
No browser/separate app needed
Works inside your editor
Sync with Git (requests stored as JSON files)
Lightweight
```

Good for quick testing while coding.

---

# SECTION 11 — REAL-WORLD API DESIGN EXAMPLE

## BUILDING A BLOG API — COMPLETE DESIGN

```
Resources:
  Users    /users
  Posts    /posts
  Comments /comments
  Tags     /tags

Authentication:
  POST /auth/register    → Register
  POST /auth/login       → Login → Returns JWT
  POST /auth/logout      → Logout

Users:
  GET  /users             → List users (admin only)
  GET  /users/me          → My profile
  PATCH /users/me         → Update my profile
  DELETE /users/me        → Delete my account

Posts:
  GET  /posts             → All published posts (public)
  GET  /posts?author=42   → Posts by user 42
  GET  /posts?tag=python  → Posts tagged "python"
  POST /posts             → Create post (auth required)
  GET  /posts/{id}        → Get specific post (public)
  PATCH /posts/{id}       → Update post (author only)
  DELETE /posts/{id}      → Delete post (author or admin)

Comments:
  GET  /posts/{id}/comments        → Comments on a post
  POST /posts/{id}/comments        → Add comment (auth required)
  PATCH /posts/{id}/comments/{cid} → Edit comment (author only)
  DELETE /posts/{id}/comments/{cid}→ Delete comment

Tags:
  GET /tags               → All tags
  GET /tags/{name}/posts  → Posts with this tag
```

---

## FASTAPI IMPLEMENTATION

```python
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI(title="Blog API", version="1.0.0")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


# ── Models ──────────────────────────────────────────────────────────

class PostCreate(BaseModel):
    title: str
    body: str
    tags: List[str] = []

class PostUpdate(BaseModel):
    title: Optional[str] = None
    body: Optional[str] = None
    tags: Optional[List[str]] = None

class CommentCreate(BaseModel):
    content: str


# ── Fake DB ─────────────────────────────────────────────────────────

posts_db = {
    1: {"id": 1, "title": "First Post", "body": "Hello World", "author_id": 1, "tags": ["python"]},
    2: {"id": 2, "title": "REST APIs", "body": "Learning REST", "author_id": 1, "tags": ["api", "rest"]},
}
comments_db = {}
next_post_id = 3
next_comment_id = 1


# ── Helpers ──────────────────────────────────────────────────────────

def get_current_user(token: str = Depends(oauth2_scheme)):
    # In real app: decode JWT, get user from DB
    return {"id": 1, "name": "Adyaprana"}


# ── Posts ────────────────────────────────────────────────────────────

@app.get("/posts", tags=["Posts"])
def list_posts(author: Optional[int] = None, tag: Optional[str] = None):
    posts = list(posts_db.values())
    if author:
        posts = [p for p in posts if p["author_id"] == author]
    if tag:
        posts = [p for p in posts if tag in p["tags"]]
    return {"data": posts, "total": len(posts)}


@app.post("/posts", status_code=201, tags=["Posts"])
def create_post(post: PostCreate, current_user = Depends(get_current_user)):
    global next_post_id
    new_post = {
        "id": next_post_id,
        "title": post.title,
        "body": post.body,
        "tags": post.tags,
        "author_id": current_user["id"]
    }
    posts_db[next_post_id] = new_post
    next_post_id += 1
    return new_post


@app.get("/posts/{post_id}", tags=["Posts"])
def get_post(post_id: int):
    if post_id not in posts_db:
        raise HTTPException(status_code=404, detail="Post not found")
    return posts_db[post_id]


@app.patch("/posts/{post_id}", tags=["Posts"])
def update_post(post_id: int, post: PostUpdate, current_user = Depends(get_current_user)):
    if post_id not in posts_db:
        raise HTTPException(status_code=404, detail="Post not found")
    stored = posts_db[post_id]
    if stored["author_id"] != current_user["id"]:
        raise HTTPException(status_code=403, detail="Not your post")
    update_data = post.dict(exclude_unset=True)
    stored.update(update_data)
    return stored


@app.delete("/posts/{post_id}", status_code=204, tags=["Posts"])
def delete_post(post_id: int, current_user = Depends(get_current_user)):
    if post_id not in posts_db:
        raise HTTPException(status_code=404, detail="Post not found")
    stored = posts_db[post_id]
    if stored["author_id"] != current_user["id"]:
        raise HTTPException(status_code=403, detail="Not your post")
    del posts_db[post_id]
    return None


# ── Comments ─────────────────────────────────────────────────────────

@app.get("/posts/{post_id}/comments", tags=["Comments"])
def list_comments(post_id: int):
    if post_id not in posts_db:
        raise HTTPException(status_code=404, detail="Post not found")
    post_comments = [c for c in comments_db.values() if c["post_id"] == post_id]
    return {"data": post_comments}


@app.post("/posts/{post_id}/comments", status_code=201, tags=["Comments"])
def add_comment(post_id: int, comment: CommentCreate, current_user = Depends(get_current_user)):
    global next_comment_id
    if post_id not in posts_db:
        raise HTTPException(status_code=404, detail="Post not found")
    new_comment = {
        "id": next_comment_id,
        "post_id": post_id,
        "content": comment.content,
        "author_id": current_user["id"]
    }
    comments_db[next_comment_id] = new_comment
    next_comment_id += 1
    return new_comment
```

---

# SECTION 12 — INTERVIEW QUESTIONS (EXTENDED)

## BASIC LEVEL

### Q1. What is an API? Give a real-world analogy.

An API (Application Programming Interface) is a set of rules and protocols that allows two software systems to communicate with each other.

The best real-world analogy is a restaurant waiter. When you're at a restaurant, you don't go into the kitchen to cook your own food. You tell the waiter what you want. The waiter carries your order to the kitchen, and brings the food back to you. You never need to know how the kitchen works.

In software:
- You (customer) are the client application (mobile app, browser)
- The waiter is the API
- The kitchen is the backend server and database

You tell the API what you want. The API fetches it from the backend. The API returns the result to you. You never need to know how the backend works internally.

---

### Q2. What is REST? Who created it?

REST (Representational State Transfer) is an architectural style for designing networked applications. It was created by Roy Fielding and described in his doctoral dissertation at UC Irvine in the year 2000.

REST is not a protocol or a standard — it is a set of design principles. APIs that follow these principles are called RESTful APIs.

The core idea is that resources (users, products, orders) are identified by URLs, and you interact with them using standard HTTP methods (GET, POST, PUT, PATCH, DELETE).

---

### Q3. List the 6 REST constraints.

1. **Client-Server Separation** — Client and server are independent. Each can evolve separately.
2. **Stateless** — Every request is self-contained. Server stores no client session state.
3. **Cacheable** — Responses indicate whether they can be cached.
4. **Uniform Interface** — Consistent URLs, methods, and response formats across all resources.
5. **Layered System** — Client doesn't know about load balancers, gateways, or other intermediaries.
6. **Code on Demand** (Optional) — Server can send executable code to client.

---

### Q4. What is JSON? Why is it the standard for APIs?

JSON (JavaScript Object Notation) is a lightweight, text-based data interchange format. It was created by Douglas Crockford and became the dominant format for web APIs.

Reasons for its popularity:

- **Human-readable** — You can read JSON without any tools
- **Lightweight** — Smaller than XML, less bandwidth
- **Easy to parse** — Every modern programming language has JSON parsing built in
- **Flexible** — Supports nested structures, arrays, and all basic data types
- **Language-independent** — Works with Python, JavaScript, Java, Go, Ruby, etc.

Before JSON, XML was the standard. JSON replaced it because it is simpler and smaller.

---

### Q5. What are the data types supported in JSON?

JSON supports exactly 6 data types:

1. **String** — `"Adyaprana"` (always double quotes)
2. **Number** — `42` or `3.14` (integer or float, no quotes)
3. **Boolean** — `true` or `false` (always lowercase)
4. **Null** — `null` (lowercase)
5. **Object** — `{"key": "value"}` (curly braces, key must be string)
6. **Array** — `[1, 2, 3]` (square brackets)

A common mistake: using Python's `True`/`False`/`None` in JSON. JSON requires `true`/`false`/`null`.

---

## INTERMEDIATE LEVEL

### Q6. Explain statelessness in REST. Why is it important?

Statelessness means that each HTTP request from client to server must contain all information necessary to understand and process the request. The server must not store any session information about the client.

Why it is important:

**Scalability:** In a stateless system, any server in a cluster can handle any request. If you have 10 servers and a client sends 3 requests, each request can go to a different server. This is impossible if sessions are stored server-side.

**Simplicity:** The server doesn't need to maintain session databases or worry about session expiry, garbage collection, or distributed session synchronization.

**Reliability:** If a server crashes, the client can simply retry on a different server. No session data is lost.

The tradeoff is that each request carries more data (like the auth token), but this is a small price to pay for massive scalability gains.

---

### Q7. What is the Uniform Interface constraint? Why is it the most important?

The Uniform Interface is the constraint that most defines REST. It means that all resources in a REST API are accessed and manipulated using the same set of conventions.

It has 4 sub-constraints:
- Resources identified by URLs
- Resources manipulated through their representations
- Self-descriptive messages
- HATEOAS (hypermedia as engine of application state)

It is the most important constraint because it provides a consistent, predictable contract between client and server. Any developer can look at a REST API and immediately know that:

- `GET /users` lists users
- `POST /users` creates a user
- `GET /users/42` gets user 42
- `DELETE /users/42` deletes user 42

They don't need to read documentation for every endpoint because the convention is uniform.

---

### Q8. What is HATEOAS?

HATEOAS stands for Hypermedia As The Engine Of Application State. It is the highest level of REST compliance (Level 3 of the Richardson Maturity Model).

In a HATEOAS API, responses include links to related actions the client can take next.

Without HATEOAS, a client must know all URLs in advance from external documentation.

With HATEOAS, the API response itself tells the client what it can do next:

```json
{
  "id": 42,
  "name": "Adyaprana",
  "balance": 5000,
  "_links": {
    "self": {"href": "/users/42"},
    "orders": {"href": "/users/42/orders"},
    "deposit": {"href": "/users/42/deposit", "method": "POST"},
    "withdraw": {"href": "/users/42/withdraw", "method": "POST"}
  }
}
```

The API guides the client through possible actions. This is how the web itself works — you follow links from page to page.

Most real-world REST APIs don't implement HATEOAS, but it is considered "true REST" by Roy Fielding.

---

### Q9. What is the Richardson Maturity Model?

The Richardson Maturity Model (created by Leonard Richardson) measures how RESTful an API is on a scale from 0 to 3.

**Level 0 — The Swamp of POX:**
Single endpoint, all operations done via POST with action names in the body.
```
POST /api
Body: {"action": "getUser", "id": 42}
```
Not REST at all.

**Level 1 — Resources:**
Multiple URLs for different resources, but still using POST for everything.
```
POST /users → get user
POST /users → create user
```
Inconsistent.

**Level 2 — HTTP Verbs:**
Using correct HTTP methods with proper URLs.
```
GET /users/42    → get user
DELETE /users/42 → delete user
```
This is what most "REST APIs" are in practice.

**Level 3 — HATEOAS:**
Responses include hypermedia links to related actions.
True REST according to Roy Fielding.

Most production APIs are Level 2.

---

### Q10. What is the difference between REST and GraphQL?

**REST:**
- Multiple endpoints, one per resource (`/users`, `/posts`, `/orders`)
- Server decides what data to return
- Can over-fetch (get more data than needed)
- Can under-fetch (need multiple requests for related data)
- Simple to implement and understand
- Best for simple CRUD applications

**GraphQL:**
- Single endpoint (`/graphql`)
- Client decides exactly what data to return
- Never over-fetches (you ask for exactly what you need)
- Never under-fetches (one request can get all related data)
- More complex to implement
- Best for complex applications with many related data types

Example of under-fetching in REST:

```
Need: User name + their latest 5 posts + post authors

REST requires:
  GET /users/42
  GET /users/42/posts?limit=5
  GET /users/1
  GET /users/3
  4 separate requests
```

GraphQL requires exactly 1 request for all of this.

---

## ADVANCED LEVEL

### Q11. What is the difference between API key, Basic Auth, JWT, and OAuth2?

**API Key:**
- A unique string issued to a developer
- Sent in a header or query parameter
- Simple but no user identity
- Good for: Server-to-server, public APIs, rate limiting
- Risk: If leaked, anyone can use your key

**Basic Auth:**
- Username and password encoded in Base64
- Sent with every request
- Only safe over HTTPS
- Good for: Simple internal APIs
- Risk: Password sent every request, even encoded

**JWT (JSON Web Token):**
- Token issued after login, contains claims about the user
- Server verifies signature, no database lookup needed
- Stateless by design
- Good for: Modern SPAs, mobile apps, microservices
- Risk: Token valid until expiry even if user logs out (use short expiry + refresh tokens)

**OAuth2:**
- Delegation protocol — "Login with Google/GitHub"
- User authorizes your app to access their data on another service
- Complex flow but powerful
- Good for: Social login, accessing third-party APIs on behalf of user
- Standard used by Google, GitHub, Facebook, Microsoft

---

### Q12. What is API versioning? What strategies exist?

API versioning allows you to make breaking changes to your API without breaking existing clients.

A breaking change is anything that changes the response format, removes fields, or changes behavior in a way that existing clients don't expect.

**URL Versioning (most common):**

```
/api/v1/users    ← Old clients still work
/api/v2/users    ← New clients use new format
```

Pros: Visible, simple, easy to understand
Cons: Pollutes URLs

**Header Versioning:**

```http
GET /users
Accept: application/vnd.myapi.v2+json
```

Pros: Cleaner URLs
Cons: Hidden in headers, harder to test in browser

**Query Parameter Versioning:**

```
GET /users?version=2
```

Pros: Easy to test
Cons: Version shouldn't be a filter parameter

**FastAPI example with versioning:**

```python
from fastapi import APIRouter

v1_router = APIRouter(prefix="/api/v1")
v2_router = APIRouter(prefix="/api/v2")

@v1_router.get("/users")
def get_users_v1():
    return [{"id": 1, "name": "Adyaprana"}]

@v2_router.get("/users")
def get_users_v2():
    return {
        "data": [{"id": 1, "full_name": "Adyaprana", "created_at": "2026-01-01"}],
        "pagination": {"page": 1, "total": 1}
    }
```

---

### Q13. What is OpenAPI and how does FastAPI use it?

OpenAPI (formerly Swagger) is a specification for describing REST APIs. It defines a standard, machine-readable format (JSON or YAML) that describes every endpoint, parameter, request body, and response in an API.

Benefits of OpenAPI:

- **Interactive documentation** — Swagger UI lets developers try API calls in the browser
- **Client generation** — Tools can auto-generate SDK code in any language
- **Validation** — Tools can validate requests against the spec
- **Collaboration** — Frontend and backend developers agree on the API contract before implementation

FastAPI automatically generates OpenAPI documentation from your Python code and type hints.

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="My API",
    version="1.0.0",
    description="Backend Developer Journey API"
)

class UserCreate(BaseModel):
    name: str
    email: str
    age: int

@app.post("/users",
    summary="Create user",
    description="Creates a new user account",
    response_description="The created user",
    tags=["Users"],
    status_code=201)
def create_user(user: UserCreate):
    return {"id": 1, **user.dict()}
```

Access at:
- `http://localhost:8000/docs` — Swagger UI
- `http://localhost:8000/redoc` — ReDoc
- `http://localhost:8000/openapi.json` — Raw spec

---

### Q14. What is idempotency in APIs? Why does it matter for payment APIs?

An operation is idempotent if performing it multiple times produces the same result as performing it once.

HTTP methods and idempotency:

```
GET     → Idempotent (always returns same data)
PUT     → Idempotent (always results in same state)
DELETE  → Idempotent (after first call: deleted. Second call: 404. State is same)
POST    → NOT idempotent (each call creates a new resource)
PATCH   → Usually NOT idempotent
```

**Why this matters for payment APIs:**

Consider this scenario:

```
User clicks "Pay ₹5000"
Your app sends POST /payments to Razorpay
Network fails — you don't know if it succeeded
```

What do you do?

- If you retry: Did the first payment go through? Could charge twice.
- If you don't retry: User might not have been charged.

**Solution: Idempotency Keys**

```python
headers = {
    "Idempotency-Key": "unique-uuid-for-this-payment-attempt"
}
response = requests.post("/payments", json=payload, headers=headers)
```

If you send the same idempotency key twice, the server returns the result of the first request without processing again.

Stripe, Razorpay, and all major payment APIs support idempotency keys.

---

### Q15. What are the best practices for designing a production REST API?

**1. Use correct HTTP methods and status codes**

```
POST → 201, not 200
DELETE → 204, not 200
Validation failure → 422, not 400
Not found → 404, not 500
```

**2. Consistent response structure**

```json
{
  "success": true,
  "data": {...},
  "message": "User created",
  "pagination": {...}
}
```

**3. Meaningful error messages**

```json
{
  "success": false,
  "error": {
    "code": "EMAIL_ALREADY_EXISTS",
    "message": "A user with this email already exists",
    "field": "email"
  }
}
```

**4. Versioning from day one**

```
/api/v1/users
```

**5. Pagination for list endpoints**

```
GET /users?page=1&limit=20
```

**6. Filtering and sorting**

```
GET /products?category=laptop&sort=price&order=asc
```

**7. Rate limiting**

```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1751234567
```

**8. HTTPS always**

**9. Request IDs for tracing**

```
X-Request-ID: 550e8400-e29b-41d4-a716-446655440000
```

**10. OpenAPI documentation**

---

# SECTION 13 — COMMON MISTAKES BEGINNERS MAKE

```
1. Putting verbs in URLs
   Wrong:  GET /getAllUsers
   Right:  GET /users

2. Using POST for everything
   Wrong:  POST /deleteUser
   Right:  DELETE /users/42

3. Not returning correct status codes
   Wrong:  return 200 for created resource
   Right:  return 201 for POST that creates

4. Returning inconsistent response format
   Wrong:  Sometimes {"user": ...} sometimes {"data": ...}
   Right:  Always {"data": ..., "success": bool}

5. Exposing database errors to clients
   Wrong:  {"error": "column 'emai' does not exist"} (typo exposed!)
   Right:  {"error": "Invalid request"}

6. No versioning from day one
   Wrong:  /users (breaking change breaks all clients)
   Right:  /v1/users

7. Returning all data without pagination
   Wrong:  GET /users returns all 1 million users
   Right:  GET /users?page=1&limit=20

8. Using singular for collection URLs
   Wrong:  /user, /product, /order
   Right:  /users, /products, /orders

9. Not documenting the API
   Wrong:  Only you know what your API does
   Right:  OpenAPI/Swagger docs, Postman collection

10. Ignoring security headers
    Wrong:  No CORS config, no rate limiting
    Right:  Proper CORS, rate limiting, input validation
```

---

# DAY 23 ASSIGNMENTS

✅ Explain what an API is to someone non-technical (use the restaurant analogy)

✅ Explain all 6 REST constraints from memory

✅ Explain why statelessness enables horizontal scaling

✅ Explain the Richardson Maturity Model levels 0 through 3

✅ Write all 6 JSON data types from memory with examples

✅ Explain the difference between Python `True` and JSON `true`

✅ Use Postman to hit JSONPlaceholder — GET posts, GET single user, POST new todo

✅ Use Python `requests` library to run GET, POST, PUT, PATCH, DELETE on JSONPlaceholder

✅ Use ReqRes to simulate register and login and extract JWT token

✅ Build the mini API client class from Section 8

✅ Explain HATEOAS — what it is and why most APIs don't implement it

✅ Explain the difference between REST and GraphQL

✅ Write a proper error handling wrapper around `requests.get()`

✅ Open FastAPI at `/docs` and explore auto-generated Swagger UI

---

# DAY 23 BACKEND DEVELOPER CHECKPOINT

If you can explain without notes:

**API Concepts:**
✅ What is an API (restaurant analogy)
✅ Public vs Private vs Partner API
✅ REST vs GraphQL vs gRPC vs WebSocket

**REST:**
✅ What REST stands for and who created it
✅ What "Representational State Transfer" actually means
✅ All 6 REST constraints
✅ The Richardson Maturity Model (Level 0 to Level 3)
✅ HATEOAS

**JSON:**
✅ All 6 JSON data types
✅ JSON Object vs JSON Array
✅ Nested JSON access pattern
✅ Python True vs JSON true
✅ json.loads() vs json.dumps() vs json.load() vs json.dump()

**API Design:**
✅ URL naming conventions (nouns not verbs, plural)
✅ Nested resource URLs
✅ Standard CRUD pattern
✅ Consistent response structure
✅ Proper error responses

**Authentication:**
✅ API Key
✅ Basic Auth
✅ Bearer Token / JWT
✅ OAuth2

**Tools:**
✅ Postman — Collections, Environments, Variables, Tests
✅ Thunder Client
✅ JSONPlaceholder
✅ ReqRes

**Advanced:**
✅ OpenAPI/Swagger
✅ API Versioning
✅ Idempotency and Idempotency Keys
✅ 15 production best practices

---

Tomorrow when you write your first real FastAPI endpoint, you won't just be typing code.

You'll know:

```
This route is a REST resource.
GET means read-only, safe, idempotent.
The JSON response is a representation of current database state.
The client is stateless — it carries its token in every request.
FastAPI is generating OpenAPI docs for this automatically.
The 201 status code tells the client a new resource was created.
The URL /users follows uniform interface conventions.
Any load balancer can route this request because it's stateless.
```

**That's the difference between someone who writes REST APIs and someone who understands REST APIs.**

---

*Day 23 Complete.* ✅