# DAY 22 — HOW THE WEB WORKS (NON-NEGOTIABLE)

> **Goal:** Understand exactly what happens when a browser, mobile app, or frontend talks to a backend API.
>
> **Week:** W4 — How the Web Works + Git + Advanced Python
>
> **Status:** ✅

---

# WHY THIS DAY IS IMPORTANT

Many beginners learn Python, FastAPI, Django, and databases without truly understanding HTTP.

Then they memorize code like:

```python
@app.get("/users")
def get_users():
    return {"users": []}
```

But they don't understand:

- Who called this endpoint?
- How did the request reach the server?
- What is GET exactly?
- What is a response and how is it structured?
- Why does FastAPI return 422 when I send wrong data?
- Why do we need headers?
- Why does authentication even work?
- What is CORS and why does everyone hate it?

Today you will learn the **foundation that every backend framework is built on.**

Skip this and you will always be guessing.

Understand this and FastAPI, Django, Node.js all make sense.

---

# SECTION 1 — THE BIG PICTURE

## THE INTERNET IS JUST COMPUTERS TALKING

Most people think Instagram, YouTube, Amazon are just "websites."

Technically they are:

```
Frontend (What you see)
+
Backend (Logic and processing)
+
Database (Data storage)
+
HTTP Communication (The glue between all of them)
```

When you click **LIKE** on Instagram:

```
Your phone doesn't magically increase likes.
Your phone sends a REQUEST to Instagram's server.
Instagram's server processes it.
Instagram's server sends back a RESPONSE.
Instagram shows you the updated like count.
```

**This entire cycle takes under 200ms on a good network.**

Every time. Billions of times per day.

---

## THE FULL JOURNEY OF A REQUEST

```
Browser / Mobile App / React App
             │
             │  1. HTTP Request (GET /posts)
             ▼
        Backend Server (FastAPI / Django / Node)
             │
             │  2. Database Query (SELECT * FROM posts)
             ▼
          Database (PostgreSQL / MySQL / MongoDB)
             │
             │  3. Returns Data
             ▼
        Backend Server
             │
             │  4. HTTP Response (200 OK + JSON data)
             ▼
Browser / Mobile App / React App
             │
             │  5. Renders the page / updates UI
             ▼
          User sees result
```

**This entire flow is what backend developers build and maintain.**

---

# SECTION 2 — THE WEB STACK EXPLAINED

## WHAT IS A PROTOCOL?

A **protocol** is an agreed set of rules for communication.

Think of it like this:

```
English = Protocol for humans
HTTP    = Protocol for web clients and servers
```

Without a shared protocol:

```
Client says:  "Give me users"
Server says:  "What? I only speak XML-1998-format"
```

Chaos.

HTTP standardizes everything.

---

## WHAT IS HTTP?

**HTTP = HyperText Transfer Protocol**

HTTP defines:

- How requests are structured
- How responses are structured
- What methods mean (GET, POST, etc.)
- What status codes mean (200, 404, etc.)

HTTP was created by **Tim Berners-Lee** in **1991**.

Current version used widely: **HTTP/1.1** and **HTTP/2**

**HTTP/3** is the newest version using a different transport protocol called **QUIC** instead of TCP.

---

## HTTP vs HTTPS

| Feature | HTTP | HTTPS |
|---|---|---|
| Full Form | HyperText Transfer Protocol | HyperText Transfer Protocol **Secure** |
| Encryption | None. Plain text. | Yes. Uses SSL/TLS. |
| Port | 80 | 443 |
| Used for | Old/internal systems | All modern websites |
| Data visible to attacker? | Yes | No |
| Certificate required? | No | Yes |

**You must always use HTTPS in production.**

HTTP sends passwords, tokens, and data in plain text. Anyone on the same WiFi can see it.

HTTPS encrypts everything using **TLS (Transport Layer Security)**.

---

## WHAT IS TLS/SSL?

**TLS = Transport Layer Security**
**SSL = Secure Sockets Layer** (older, now deprecated, but the term stuck)

TLS creates an **encrypted tunnel** between client and server.

```
Client                          Server
  │                               │
  │  ──── ClientHello ──────────► │
  │  ◄─── ServerHello + Cert ──── │
  │  ──── Key Exchange ─────────► │
  │  ◄─── Finished ────────────── │
  │                               │
  │  ══ Encrypted Communication ══│
```

This is called the **TLS Handshake**.

All of this happens in milliseconds before your HTTP request is even sent.

---

## WHAT IS DNS?

**DNS = Domain Name System**

Computers work with IP addresses:

```
142.250.195.78
```

Humans remember names:

```
google.com
```

DNS converts one to the other.

```
You type:    google.com
DNS says:    That's 142.250.195.78
Browser connects to that IP
```

DNS is like the **phonebook of the internet**.

### DNS Resolution Steps

```
1. Your browser checks its own cache
2. Operating system checks its own cache
3. Router cache is checked
4. ISP's DNS server is queried
5. Root DNS servers consulted (if needed)
6. Authoritative DNS server returns IP
7. Browser connects to that IP
```

**This is why "changing DNS settings propagates in 24-48 hours."** Caches take time to update.

---

## WHAT ACTUALLY HAPPENS WHEN YOU TYPE `google.com`?

This is a **classic interview question** at big tech companies.

Full answer:

```
Step 1: Browser checks if URL has protocol
        → Adds https:// if missing

Step 2: DNS Resolution
        → google.com → 142.250.195.78

Step 3: TCP Connection Established
        → Three-way handshake (SYN, SYN-ACK, ACK)

Step 4: TLS Handshake (for HTTPS)
        → Encryption established

Step 5: HTTP Request Sent
        → GET / HTTP/1.1
        → Host: google.com

Step 6: Google's Server processes request
        → Load balancer routes to correct server
        → Server generates response

Step 7: HTTP Response Received
        → 200 OK
        → HTML content

Step 8: Browser parses HTML
        → Discovers CSS, JS, image files
        → Sends additional requests for each

Step 9: Page renders completely
```

**This happens every time you open any website.**

---

# SECTION 3 — CLIENT SERVER ARCHITECTURE

## CLIENT

A client is anything that **requests data.**

Examples:

```
Chrome Browser
Firefox Browser
Safari Browser
Mobile App (iOS / Android)
React Frontend Application
Flutter App
Postman (API Testing Tool)
Python requests library
curl command
```

A client **initiates** communication.

A client **does not wait** to be called. It calls the server.

---

## SERVER

A server is anything that **receives requests and sends responses.**

Examples:

```
FastAPI Application
Django Application
Flask Application
Node.js with Express
Spring Boot (Java)
Ruby on Rails
```

A server **listens** for incoming connections.

A server **processes** requests.

A server **returns** responses.

---

## IMPORTANT: ONE SERVER CAN SERVE MILLIONS OF CLIENTS

Instagram's backend serves **500 million+ users** per day.

Not 500 million servers.

One (highly scaled) backend system.

This is achieved through:

```
Load Balancers
Multiple Server Instances
Caching (Redis)
CDNs (Content Delivery Networks)
Database Replication
```

As a backend developer, **you will build the server side.**

---

# SECTION 4 — HTTP REQUEST IN DEPTH

## ANATOMY OF AN HTTP REQUEST

Every HTTP request has:

```
1. Method        → What action to perform
2. URL / Path    → Which resource
3. HTTP Version  → Protocol version
4. Headers       → Metadata about the request
5. Body          → Actual data (optional, mainly for POST/PUT/PATCH)
```

Raw HTTP Request Example:

```http
POST /users HTTP/1.1
Host: api.example.com
Content-Type: application/json
Authorization: Bearer eyJhbGciOiJIUzI1NiJ9...
Accept: application/json
User-Agent: Mozilla/5.0

{
  "name": "Adyaprana",
  "email": "adya@example.com",
  "age": 23
}
```

Breaking this down:

```
POST                    → Method
/users                  → URL Path
HTTP/1.1                → Version

Host: api.example.com   → Which server to hit
Content-Type: ...       → I'm sending JSON
Authorization: Bearer   → My auth token
Accept: ...             → I want JSON back
User-Agent: ...         → I'm a browser

{ "name": ... }         → The actual data (Body)
```

---

## ANATOMY OF AN HTTP RESPONSE

Every HTTP response has:

```
1. HTTP Version    → Protocol version
2. Status Code     → Result of the request
3. Status Message  → Text description of status
4. Headers         → Metadata about the response
5. Body            → Returned data (optional)
```

Raw HTTP Response Example:

```http
HTTP/1.1 201 Created
Content-Type: application/json
Date: Wed, 17 Jun 2026 10:30:00 GMT
X-Request-ID: abc123xyz

{
  "id": 42,
  "name": "Adyaprana",
  "email": "adya@example.com",
  "created_at": "2026-06-17T10:30:00Z"
}
```

---

# SECTION 5 — HTTP METHODS (DEEP DIVE)

## THE FIVE CORE METHODS

```
GET      → Read
POST     → Create
PUT      → Replace
PATCH    → Update (partial)
DELETE   → Delete
```

This is called **CRUD**:

```
C → Create  → POST
R → Read    → GET
U → Update  → PUT / PATCH
D → Delete  → DELETE
```

Every API you build will use these.

---

## GET — READ DATA

**Purpose:** Retrieve data from server. Never modify anything.

```http
GET /users HTTP/1.1
Host: api.example.com
```

Key properties:

- Has **no request body** (in practice)
- **Safe** — should not change server state
- **Idempotent** — calling it 100 times has same result as calling once
- Responses can be **cached**

Examples:

```http
GET /users               → Get all users
GET /users/42            → Get user with ID 42
GET /products?page=1     → Get first page of products
GET /search?q=python     → Search for "python"
```

FastAPI Example:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/users")
def get_all_users():
    return [
        {"id": 1, "name": "Adyaprana"},
        {"id": 2, "name": "Ravi"}
    ]

@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"id": user_id, "name": "Adyaprana"}
```

---

## POST — CREATE DATA

**Purpose:** Create a new resource on the server.

```http
POST /users HTTP/1.1
Content-Type: application/json

{
  "name": "Adyaprana",
  "email": "adya@example.com"
}
```

Key properties:

- **Has request body** with data
- **Not idempotent** — calling it 3 times creates 3 users
- **Not safe** — modifies server state
- Typically returns **201 Created**

Examples:

```http
POST /users         → Create new user
POST /orders        → Place new order
POST /login         → Login (creates session/token)
POST /register      → Register new account
POST /payments      → Process payment
```

FastAPI Example:

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class UserCreate(BaseModel):
    name: str
    email: str

@app.post("/users", status_code=201)
def create_user(user: UserCreate):
    # In real app: save to database
    return {
        "id": 42,
        "name": user.name,
        "email": user.email
    }
```

---

## PUT — REPLACE ENTIRE RESOURCE

**Purpose:** Replace an existing resource completely.

```http
PUT /users/42 HTTP/1.1
Content-Type: application/json

{
  "name": "Adya",
  "email": "adya@new.com",
  "city": "Mumbai"
}
```

Before:

```json
{
  "id": 42,
  "name": "Adyaprana",
  "email": "old@email.com",
  "city": "Bangalore"
}
```

After PUT:

```json
{
  "id": 42,
  "name": "Adya",
  "email": "adya@new.com",
  "city": "Mumbai"
}
```

**Every field gets replaced.** If you forget to include `city`, it gets deleted.

Key properties:

- **Idempotent** — calling 100 times has same result
- Always sends the **complete** resource
- Returns **200 OK**

---

## PATCH — UPDATE PARTIAL RESOURCE

**Purpose:** Update only specific fields of an existing resource.

```http
PATCH /users/42 HTTP/1.1
Content-Type: application/json

{
  "city": "Mumbai"
}
```

Before:

```json
{
  "id": 42,
  "name": "Adyaprana",
  "email": "adya@email.com",
  "city": "Bangalore"
}
```

After PATCH:

```json
{
  "id": 42,
  "name": "Adyaprana",
  "email": "adya@email.com",
  "city": "Mumbai"
}
```

Only `city` changed. Everything else stays.

**Use PATCH for most update operations. Use PUT only when replacing the whole object.**

---

## DELETE — REMOVE RESOURCE

**Purpose:** Delete a resource from the server.

```http
DELETE /users/42 HTTP/1.1
```

Key properties:

- Usually **no request body**
- Returns **204 No Content** (success with no body) or **200 OK**
- **Idempotent** — deleting the same thing twice is fine (second time: 404)

Examples:

```http
DELETE /users/42           → Delete user 42
DELETE /posts/10           → Delete post 10
DELETE /comments/5         → Delete comment 5
```

---

## PUT VS PATCH — THE INTERVIEW TRAP

This question will be asked in almost every backend interview.

| Scenario | Use |
|---|---|
| Update user's entire profile | PUT |
| Update only user's city | PATCH |
| Update only user's profile picture | PATCH |
| Replace entire product object | PUT |
| Change order status from pending to shipped | PATCH |

**Rule:** If you're sending the **complete** object → PUT. If you're sending **only what changed** → PATCH.

---

## IDEMPOTENCY — IMPORTANT CONCEPT

**Idempotent** means: making the same request multiple times gives the same result.

```
GET /users/1      → Always returns same user (idempotent)
PUT /users/1      → Always results in same state (idempotent)
DELETE /users/1   → After first call it's gone. Second call: 404 (idempotent)
POST /users       → Every call creates a NEW user (NOT idempotent)
```

Why does this matter?

**Network failures.** If a request fails halfway, do you retry it?

- GET → Always safe to retry
- PUT → Safe to retry
- DELETE → Safe to retry
- POST → **Dangerous to retry** (could create duplicates)

Modern systems use **idempotency keys** for POST requests to prevent this.

---

# SECTION 6 — HTTP STATUS CODES (COMPLETE GUIDE)

## STATUS CODE FAMILIES

```
1xx  →  Informational   (Request received, continuing process)
2xx  →  Success         (Request was received, understood, and accepted)
3xx  →  Redirection     (Further action needed to complete request)
4xx  →  Client Error    (Request contains bad syntax or cannot be fulfilled)
5xx  →  Server Error    (Server failed to fulfil a valid request)
```

**Interview favorite: "What do 4xx and 5xx mean?"**

```
4xx = YOUR fault (client sent wrong data)
5xx = SERVER's fault (backend crashed)
```

---

## 2XX — SUCCESS CODES

### 200 OK

The most common success response.

```
GET /users         → 200 OK + list of users
PATCH /users/1     → 200 OK + updated user
DELETE /users/1    → 200 OK + deleted confirmation
```

---

### 201 Created

A new resource was successfully created.

```
POST /users        → 201 Created + new user object
POST /orders       → 201 Created + new order
```

Always return 201 (not 200) after POST that creates something. It communicates intent clearly.

---

### 204 No Content

Request successful but no data to return.

```
DELETE /users/1    → 204 No Content (deleted, nothing to show)
```

Note: **204 means success.** It's not an error. Just empty response.

---

### 202 Accepted

Request received but processing is not yet complete.

Used for **asynchronous operations.**

```
POST /reports/generate   → 202 Accepted
                         → "Your report is being generated. Check back later."
```

---

## 3XX — REDIRECT CODES

### 301 Moved Permanently

Resource has moved to a new URL forever.

```
http://oldsite.com  →  301  →  https://newsite.com
```

---

### 302 Found (Temporary Redirect)

Resource temporarily moved.

---

### 304 Not Modified

Used with caching. "You already have the latest version."

---

## 4XX — CLIENT ERROR CODES

### 400 Bad Request

Client sent something the server cannot understand.

```json
{
  "age": "not-a-number"
}
```

Server expected integer. Got string. Bad Request.

---

### 401 Unauthorized

Not authenticated. No valid credentials provided.

```
GET /profile
Authorization: (missing)

Response: 401 Unauthorized
```

Think: **"Who are you? Please log in."**

---

### 403 Forbidden

Authenticated but not authorized. You logged in but don't have permission.

```
Normal user trying to delete someone else's post.
Response: 403 Forbidden
```

Think: **"I know who you are. You're just not allowed."**

---

### 401 vs 403 — CRITICAL DIFFERENCE

| Code | Meaning | Example |
|---|---|---|
| 401 | Not logged in at all | No token provided |
| 403 | Logged in but no permission | Student accessing admin panel |

**Always confused in interviews. Memorize this.**

---

### 404 Not Found

Requested resource does not exist.

```
GET /users/99999
→ 404 Not Found
```

---

### 405 Method Not Allowed

You used the wrong HTTP method.

```
POST /users/42       (but the route only allows GET)
→ 405 Method Not Allowed
```

---

### 409 Conflict

Request conflicts with current state of server.

```
POST /users
{
  "email": "already@exists.com"
}
→ 409 Conflict  (email already registered)
```

Common use cases:

- Duplicate email registration
- Version conflict (someone else updated the record first)

---

### 422 Unprocessable Entity

**Very common in FastAPI.**

Request is syntactically correct (valid JSON) but semantically wrong (wrong field types).

```python
from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int    # expects integer
```

Request:

```json
{
  "name": "Adyaprana",
  "age": "twenty-three"
}
```

FastAPI automatically returns:

```json
{
  "detail": [
    {
      "type": "int_parsing",
      "loc": ["body", "age"],
      "msg": "Input should be a valid integer",
      "input": "twenty-three"
    }
  ]
}
```

Status code: **422**

---

### 429 Too Many Requests

Client is sending too many requests. Rate limited.

```
Sending 1000 API calls per second.
Response: 429 Too Many Requests
Retry-After: 60
```

Important for:

- Public APIs (free tier limits)
- DDoS protection
- Fair usage policies

---

## 5XX — SERVER ERROR CODES

### 500 Internal Server Error

Something went wrong on the server. Generic server crash.

```python
@app.get("/divide")
def divide():
    result = 10 / 0   # ZeroDivisionError
    return result

# Response: 500 Internal Server Error
```

---

### 502 Bad Gateway

Server (acting as proxy) got invalid response from upstream server.

---

### 503 Service Unavailable

Server is down for maintenance or overloaded.

---

### 504 Gateway Timeout

Server didn't get a response in time from upstream service.

---

## STATUS CODE CHEAT SHEET

```
✅ 200  → Success
✅ 201  → Created
✅ 204  → No Content (deleted)
✅ 202  → Accepted (async task)

🔄 301  → Moved Permanently
🔄 304  → Not Modified (cached)

❌ 400  → Bad Request (invalid data)
❌ 401  → Unauthorized (not logged in)
❌ 403  → Forbidden (no permission)
❌ 404  → Not Found
❌ 405  → Method Not Allowed
❌ 409  → Conflict (duplicate)
❌ 422  → Unprocessable Entity (FastAPI validation)
❌ 429  → Too Many Requests (rate limited)

💥 500  → Internal Server Error (backend bug)
💥 502  → Bad Gateway
💥 503  → Service Unavailable
💥 504  → Gateway Timeout
```

---

# SECTION 7 — HEADERS (COMPLETE GUIDE)

## WHAT ARE HEADERS?

Headers are **key-value pairs** that carry metadata about the request or response.

Think of it as the **label on a package** before you open it.

```
Package Label (Headers):
  Sender: Adyaprana
  Contents: JSON
  Auth Token: Bearer xyz

Package Contents (Body):
  { "name": "Adyaprana" }
```

---

## REQUEST HEADERS

### Authorization

The most important header for backend developers.

```http
Authorization: Bearer eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjM0In0.abc
```

Types:

```
Basic Auth:   Authorization: Basic dXNlcjpwYXNz
Bearer Token: Authorization: Bearer <JWT_TOKEN>
API Key:      X-API-Key: my-secret-key-123
```

---

### Content-Type

Tells server what format the body is in.

```http
Content-Type: application/json       → JSON data
Content-Type: application/xml        → XML data
Content-Type: multipart/form-data    → File upload
Content-Type: application/x-www-form-urlencoded → HTML form
```

If you forget this, many servers reject your request.

---

### Accept

Tells server what format the client wants in response.

```http
Accept: application/json    → I want JSON back
Accept: text/html           → I want HTML back
Accept: */*                 → I accept anything
```

---

### User-Agent

Identifies what type of client is making the request.

```http
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64) Chrome/120.0
User-Agent: python-requests/2.31.0
User-Agent: PostmanRuntime/7.36.0
```

Servers use this for analytics, bot detection, and mobile optimization.

---

### Host

Which server to contact.

```http
Host: api.example.com
```

Required in HTTP/1.1. Without it: 400 Bad Request.

---

## RESPONSE HEADERS

### Content-Type

Tells client what format the response body is in.

```http
Content-Type: application/json
Content-Type: text/html; charset=UTF-8
Content-Type: image/png
```

---

### Content-Length

Size of response body in bytes.

```http
Content-Length: 1234
```

---

### Cache-Control

Controls caching behavior.

```http
Cache-Control: max-age=3600        → Cache for 1 hour
Cache-Control: no-cache            → Don't cache
Cache-Control: no-store            → Don't store at all
```

---

### Set-Cookie

Server sets a cookie in the browser.

```http
Set-Cookie: session_id=abc123; HttpOnly; Secure; Path=/
```

---

### X-Request-ID

Custom header. Unique ID for request tracing.

```http
X-Request-ID: 550e8400-e29b-41d4-a716-446655440000
```

Used for debugging in distributed systems.

---

## CUSTOM HEADERS

Any header starting with `X-` is custom.

```http
X-API-Version: 2.0
X-Rate-Limit: 1000
X-Request-ID: unique-id-here
```

Companies create their own headers for tracking and versioning.

---

# SECTION 8 — REQUEST BODY

## WHAT IS THE REQUEST BODY?

The body is the **actual data** you send to the server.

```
Headers = Envelope + Label
Body    = The Letter Inside
```

---

## WHEN IS BODY USED?

```
GET     → Usually NO body
POST    → YES, body with new data
PUT     → YES, body with complete object
PATCH   → YES, body with fields to update
DELETE  → Usually NO body
```

---

## JSON BODY (MOST COMMON)

```http
POST /users HTTP/1.1
Content-Type: application/json

{
  "name": "Adyaprana",
  "email": "adya@example.com",
  "age": 23,
  "city": "Bangalore"
}
```

---

## FORM DATA BODY

HTML forms use this format:

```http
POST /login HTTP/1.1
Content-Type: application/x-www-form-urlencoded

username=adyaprana&password=secret123
```

---

## MULTIPART BODY (FILE UPLOAD)

Used for uploading files:

```http
POST /upload HTTP/1.1
Content-Type: multipart/form-data; boundary=----WebKitBoundary

------WebKitBoundary
Content-Disposition: form-data; name="file"; filename="resume.pdf"
Content-Type: application/pdf

[binary file data here]
------WebKitBoundary--
```

FastAPI handles all these automatically.

---

# SECTION 9 — URL PARAMETERS

## TWO TYPES OF PARAMETERS

```
Path Parameters   → Part of the URL path
Query Parameters  → After the ? in the URL
```

---

## PATH PARAMETERS

Used to **identify a specific resource.**

```http
GET /users/42
GET /products/laptop-model-x
GET /posts/100/comments/5
```

FastAPI:

```python
@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id}

@app.get("/posts/{post_id}/comments/{comment_id}")
def get_comment(post_id: int, comment_id: int):
    return {"post": post_id, "comment": comment_id}
```

---

## QUERY PARAMETERS

Used to **filter, sort, paginate, or search.**

```http
GET /products?category=laptop
GET /users?page=2&limit=10
GET /search?q=python+developer&location=bangalore
GET /posts?sort=created_at&order=desc
```

FastAPI:

```python
@app.get("/products")
def get_products(
    category: str = None,
    page: int = 1,
    limit: int = 10,
    sort: str = "name"
):
    return {
        "category": category,
        "page": page,
        "limit": limit,
        "sort": sort
    }
```

Call it as:

```
GET /products?category=laptop&page=2&limit=5
```

---

## PATH PARAMS VS QUERY PARAMS — WHEN TO USE WHICH

| Scenario | Use | Example |
|---|---|---|
| Get specific user by ID | Path Param | `/users/42` |
| Get all users on page 2 | Query Param | `/users?page=2` |
| Get specific blog post | Path Param | `/posts/100` |
| Filter posts by category | Query Param | `/posts?category=python` |
| Delete a specific comment | Path Param | `/comments/5` |
| Search products | Query Param | `/products?search=laptop` |

**Rule of thumb:**

- Path param = resource identity (which specific thing)
- Query param = filtering/options (how to get it)

---

# SECTION 10 — COOKIES

## WHAT ARE COOKIES?

Cookies are **small pieces of data** stored in the browser, sent with every request to the server.

```
Browser             Server
   │                  │
   │  GET /dashboard  │
   │ ──────────────► │
   │                  │
   │  200 OK          │
   │  Set-Cookie:     │
   │  session=abc123  │
   │ ◄────────────── │
   │                  │
   │  GET /profile    │   Next request
   │  Cookie: session │   Browser automatically sends cookie
   │  =abc123         │
   │ ──────────────► │
```

---

## WHAT ARE COOKIES USED FOR?

```
1. Session Management     → Remember logged-in users
2. Personalization        → Theme, language, preferences
3. Tracking               → Analytics, ad targeting
4. Shopping Cart          → Items before login
```

---

## COOKIE SECURITY FLAGS

```http
Set-Cookie: session=abc123; HttpOnly; Secure; SameSite=Strict; Path=/; Expires=...
```

| Flag | Meaning |
|---|---|
| HttpOnly | JavaScript cannot read this cookie (XSS protection) |
| Secure | Only send cookie over HTTPS |
| SameSite=Strict | Don't send cookie in cross-site requests (CSRF protection) |
| Expires | When cookie expires |
| Path | Which paths this cookie applies to |

---

# SECTION 11 — JWT (JSON WEB TOKENS)

## WHAT IS JWT?

JWT = **JSON Web Token**

Modern way to authenticate API users **without server-side sessions.**

```
Traditional Session:
   Server stores session in database/memory
   Client sends session ID
   Server looks it up every request  ← SLOW for distributed systems

JWT:
   Server generates a signed token
   Client stores token (localStorage or cookie)
   Client sends token with every request
   Server verifies signature  ← NO database lookup needed
```

---

## JWT STRUCTURE

A JWT looks like:

```
eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI0MiIsIm5hbWUiOiJBZHlhIn0.abc123
```

Three parts separated by dots:

```
HEADER.PAYLOAD.SIGNATURE
```

Decoded:

```json
Header:
{
  "alg": "HS256",
  "typ": "JWT"
}

Payload:
{
  "sub": "42",
  "name": "Adyaprana",
  "exp": 1751234567
}

Signature:
HMACSHA256(base64(header) + "." + base64(payload), secret_key)
```

---

## HOW JWT AUTH WORKS

```
Step 1: User logs in
POST /login
{ "email": "adya@example.com", "password": "secret" }

Step 2: Server verifies credentials
→ Correct! Generates JWT token.

Step 3: Server returns token
{ "token": "eyJhbGci..." }

Step 4: Client stores token
localStorage.setItem("token", "eyJhbGci...")

Step 5: Every future request includes token
GET /profile
Authorization: Bearer eyJhbGci...

Step 6: Server verifies token signature
→ Valid! Returns profile data.
```

---

## JWT SECURITY NOTES

```
DO:
✅ Set expiry time (exp claim)
✅ Use HTTPS only
✅ Store in HttpOnly cookie (better than localStorage)
✅ Implement token refresh mechanism

DON'T:
❌ Store sensitive data in payload (it's base64, not encrypted)
❌ Use very long expiry times (1 year tokens = security risk)
❌ Store in localStorage (vulnerable to XSS attacks)
```

---

# SECTION 12 — CORS

## WHAT IS CORS?

**CORS = Cross-Origin Resource Sharing**

One of the most frustrating errors for beginners.

The error message you'll see:

```
Access to fetch at 'http://localhost:8000/users' from origin
'http://localhost:3000' has been blocked by CORS policy.
```

---

## WHY DOES CORS EXIST?

**Same-Origin Policy:**

Browsers have a security rule: JavaScript can only make requests to the **same origin** as the page.

```
Same Origin:
http://example.com:3000   → http://example.com:3000  ✅

Different Origins (BLOCKED by default):
http://localhost:3000     → http://localhost:8000     ❌ (different port)
http://frontend.com       → http://api.backend.com   ❌ (different domain)
https://app.com           → http://app.com            ❌ (different protocol)
```

---

## HOW TO FIX CORS IN FASTAPI

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://yourfrontend.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)
```

For development only (never in production):

```python
allow_origins=["*"]   # Allows all origins — INSECURE in production
```

---

## CORS PREFLIGHT REQUEST

Before the actual request, browser sends a **preflight** OPTIONS request:

```http
OPTIONS /users HTTP/1.1
Origin: http://localhost:3000
Access-Control-Request-Method: POST
Access-Control-Request-Headers: Content-Type, Authorization
```

Server responds:

```http
HTTP/1.1 200 OK
Access-Control-Allow-Origin: http://localhost:3000
Access-Control-Allow-Methods: GET, POST, PUT, DELETE
Access-Control-Allow-Headers: Content-Type, Authorization
```

If the server doesn't respond correctly → CORS error.

---

# SECTION 13 — REST API PRINCIPLES

## WHAT IS REST?

**REST = Representational State Transfer**

An architectural style for building APIs.

Not a protocol. Not a technology. A **set of principles.**

---

## THE 6 REST PRINCIPLES

### 1. Uniform Interface

Use consistent URLs and methods.

```
Users resource:
GET    /users          → Get all users
POST   /users          → Create user
GET    /users/{id}     → Get specific user
PUT    /users/{id}     → Replace user
PATCH  /users/{id}     → Update user
DELETE /users/{id}     → Delete user
```

This pattern is the same for every resource.

---

### 2. Stateless

Every request must contain all information needed to process it.

Server stores NO session state.

```
BAD (stateful):
Request 1: POST /login → Server remembers you're logged in
Request 2: GET /profile → Works because server remembers

GOOD (stateless):
Every request: GET /profile + Authorization: Bearer TOKEN
Server doesn't remember anything. Token proves identity every time.
```

---

### 3. Client-Server Separation

Frontend and backend are independent.

```
Frontend (React) can change without touching backend.
Backend (FastAPI) can change without touching frontend.
They only communicate via defined API contract.
```

---

### 4. Cacheable

Responses should indicate if they can be cached.

```http
Cache-Control: max-age=3600    → Cache for 1 hour
Cache-Control: no-store        → Never cache
```

---

### 5. Layered System

Client doesn't need to know if it's talking to the real server or a load balancer or a cache layer.

---

### 6. Code on Demand (Optional)

Server can send executable code to client. Rarely used.

---

## REST URL DESIGN BEST PRACTICES

**Use nouns, not verbs:**

```
✅  GET /users           (noun)
❌  GET /getUsers        (verb)

✅  POST /orders         (noun)
❌  POST /createOrder    (verb)

✅  DELETE /posts/5      (noun)
❌  DELETE /deletePost/5 (verb)
```

**Use plural nouns:**

```
✅  /users
❌  /user

✅  /products
❌  /product
```

**Nested resources:**

```
GET  /users/42/orders          → All orders of user 42
GET  /users/42/orders/7        → Order 7 of user 42
POST /posts/10/comments        → Add comment to post 10
```

---

# SECTION 14 — PRACTICAL CODE EXAMPLES

## EXAMPLE 1 — BASIC GET REQUEST (Python)

```python
import requests

response = requests.get("https://jsonplaceholder.typicode.com/users")

print("Status Code:", response.status_code)
print("Headers:", dict(response.headers))
print("Body:", response.json())

# Output:
# Status Code: 200
# Headers: {'Content-Type': 'application/json', ...}
# Body: [{'id': 1, 'name': 'Leanne Graham', ...}]
```

---

## EXAMPLE 2 — POST WITH HEADERS

```python
import requests

headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer my-token-here"
}

data = {
    "name": "Adyaprana",
    "email": "adya@example.com"
}

response = requests.post(
    "https://jsonplaceholder.typicode.com/users",
    json=data,
    headers=headers
)

print(response.status_code)   # 201
print(response.json())        # {'id': 11, 'name': 'Adyaprana', ...}
```

---

## EXAMPLE 3 — QUERY PARAMETERS

```python
import requests

params = {
    "userId": 1,
    "page": 1,
    "limit": 5
}

response = requests.get(
    "https://jsonplaceholder.typicode.com/posts",
    params=params
)

# Actual URL sent: /posts?userId=1&page=1&limit=5
print(response.url)
print(response.json())
```

---

## EXAMPLE 4 — COMPLETE FASTAPI CRUD API

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI()

# In-memory database (replace with PostgreSQL in real app)
users_db = {}
next_id = 1

class UserCreate(BaseModel):
    name: str
    email: str
    city: Optional[str] = None

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    city: Optional[str] = None

# GET all users
@app.get("/users")
def get_users():
    return list(users_db.values())

# GET specific user
@app.get("/users/{user_id}")
def get_user(user_id: int):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    return users_db[user_id]

# POST create user
@app.post("/users", status_code=201)
def create_user(user: UserCreate):
    global next_id
    new_user = {"id": next_id, **user.dict()}
    users_db[next_id] = new_user
    next_id += 1
    return new_user

# PATCH update user
@app.patch("/users/{user_id}")
def update_user(user_id: int, user: UserUpdate):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    stored_user = users_db[user_id]
    update_data = user.dict(exclude_unset=True)   # Only sent fields
    stored_user.update(update_data)
    return stored_user

# DELETE user
@app.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: int):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    del users_db[user_id]
    return None
```

---

# SECTION 15 — TOOLS EVERY BACKEND DEVELOPER NEEDS

## POSTMAN

The most widely used API testing tool.

What you can do:

```
✅ Send GET, POST, PUT, PATCH, DELETE requests
✅ Set headers (including Authorization)
✅ Add request body (JSON)
✅ View status codes and responses
✅ Save collections of requests
✅ Create environments (dev, staging, production URLs)
✅ Write automated tests for APIs
✅ Generate API documentation
```

Download: https://postman.com

**Every backend developer uses Postman. Learn it on Day 22.**

---

## HOPPSCOTCH

Open-source, web-based alternative to Postman.

No installation required.

Use at: https://hoppscotch.io

Useful when:

```
You're on a new computer
You can't install software
You want a quick test
```

---

## REQRES

A fake REST API for learning and testing.

URL: https://reqres.in

Available endpoints:

```
GET    /api/users          → List users
GET    /api/users/2        → Single user
POST   /api/users          → Create user
PUT    /api/users/2        → Update user
PATCH  /api/users/2        → Partial update
DELETE /api/users/2        → Delete user
POST   /api/login          → Login
POST   /api/register       → Register
```

**Practice all HTTP methods here before building your own API.**

---

## CURL

Command-line tool to make HTTP requests.

```bash
# GET request
curl https://reqres.in/api/users

# POST request
curl -X POST https://reqres.in/api/users \
     -H "Content-Type: application/json" \
     -d '{"name": "Adyaprana", "job": "Developer"}'

# With auth token
curl https://api.example.com/profile \
     -H "Authorization: Bearer my-token"

# Verbose (shows headers)
curl -v https://example.com
```

Knowing curl = looking professional in interviews and DevOps environments.

---

## HTTP CAT / HTTP STATUS DOGS

Fun way to memorize status codes.

```
https://http.cat/404     → Shows a cat photo for 404
https://http.dog/500     → Shows a dog photo for 500
```

Genuinely helpful for memory.

---

# SECTION 16 — ADDITIONAL CONCEPTS

## RATE LIMITING

Restricts how many requests a client can make in a time period.

```
Free tier: 100 requests/hour
Pro tier: 10,000 requests/hour
```

When exceeded: **429 Too Many Requests**

Response includes:

```http
HTTP/1.1 429 Too Many Requests
Retry-After: 3600
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1751234567
```

---

## API VERSIONING

APIs change over time. Old clients must still work.

```
/api/v1/users    ← Old version still works
/api/v2/users    ← New version with different response
```

Common versioning methods:

```
URL versioning:      /api/v1/users         (most common, most visible)
Header versioning:   Accept: application/vnd.api+json; version=1
Query param:         /users?version=1
```

---

## PAGINATION

Never return millions of records at once.

```
GET /users?page=1&limit=10    → First 10 users
GET /users?page=2&limit=10    → Next 10 users
```

Response with pagination metadata:

```json
{
  "data": [...],
  "pagination": {
    "page": 1,
    "limit": 10,
    "total": 500,
    "total_pages": 50,
    "next": "/users?page=2&limit=10",
    "prev": null
  }
}
```

---

## WEBHOOKS

**Reverse of API calls.**

Normal API:

```
Client calls Server when it needs data
```

Webhook:

```
Server calls Client when something happens
```

Example: Razorpay payment webhook

```
User pays on Razorpay
Razorpay server sends POST request to YOUR server
YOUR server receives: "Payment successful for order 42"
Your server updates order status
```

You don't poll Razorpay every second. They call you.

---

## HTTP/2 ADVANTAGES OVER HTTP/1.1

```
HTTP/1.1:
One request at a time per connection
Browser opens 6-8 parallel connections to workaround this

HTTP/2:
Multiplexing: Multiple requests on same connection
Header compression (HPACK)
Server Push: Server can send resources before client asks
Binary protocol (not text like HTTP/1.1)
```

FastAPI with uvicorn supports HTTP/2 automatically.

---

# SECTION 17 — INTERVIEW QUESTIONS (EXTENDED)

## BASIC LEVEL

### Q1. What is HTTP?

HTTP (HyperText Transfer Protocol) is a stateless, application-layer protocol that defines how messages are formatted and transmitted between web clients and servers. It is the foundation of data communication on the World Wide Web. HTTP uses a request-response model where the client sends a request and the server sends back a response.

---

### Q2. What is the difference between HTTP and HTTPS?

HTTP sends data in plain text over the network. Any attacker performing a man-in-the-middle attack can read usernames, passwords, and tokens in plain text.

HTTPS adds a security layer using TLS (Transport Layer Security). All data is encrypted before transmission. Even if intercepted, it appears as unreadable encrypted bytes.

In production, always use HTTPS. Modern browsers mark HTTP sites as "Not Secure."

---

### Q3. What is DNS and why is it needed?

DNS (Domain Name System) is a distributed database that maps human-readable domain names to machine-readable IP addresses.

Humans remember `google.com`. Computers communicate via IP addresses like `142.250.195.78`.

DNS acts as the phonebook of the internet, resolving this translation. Without DNS, you would need to memorize IP addresses for every website.

---

### Q4. Explain Client-Server Architecture.

Client-Server Architecture is a distributed application structure where:

- **Client** is any application that requests services or data.
- **Server** is any application that provides services or data in response.

Communication happens over a network using protocols like HTTP. The client initiates requests. The server processes them and returns responses. This is the foundation of every web application and API.

---

### Q5. What are the five main HTTP methods?

- **GET** — Retrieve data. No body. Safe and idempotent.
- **POST** — Create a new resource. Has body. Not idempotent.
- **PUT** — Replace an existing resource completely. Has body. Idempotent.
- **PATCH** — Update part of an existing resource. Has body.
- **DELETE** — Remove a resource. No body. Idempotent.

---

## INTERMEDIATE LEVEL

### Q6. What does idempotent mean? Which methods are idempotent?

An operation is idempotent if performing it multiple times produces the same result as performing it once.

Idempotent methods: GET, PUT, DELETE

Non-idempotent methods: POST (each call creates a new resource)

This matters for retry logic. If a network request fails, you can safely retry idempotent operations but must be careful with POST.

---

### Q7. Difference between 401 and 403?

**401 Unauthorized** — The client has NOT provided authentication credentials. The server doesn't know who the client is. The client should provide valid credentials (like a JWT token).

**403 Forbidden** — The client IS authenticated (server knows who they are), but they don't have permission to access the requested resource.

Example:
- 401 → You're not logged in. Please log in.
- 403 → You're logged in as a regular user. You can't access the admin panel.

---

### Q8. What is a path parameter vs a query parameter?

**Path Parameter** is embedded in the URL path itself. It identifies a specific resource.

```
GET /users/42      ← 42 is the path parameter (identifies user 42)
```

**Query Parameter** comes after the `?` symbol. It filters, sorts, or paginates resources.

```
GET /users?page=2&limit=10    ← page and limit are query params
```

Rule: Use path params to identify WHICH resource. Use query params for HOW to get it.

---

### Q9. What is the purpose of the Content-Type header?

Content-Type tells the receiver what format the body data is in.

In requests: "I am sending JSON/XML/form-data to you."
In responses: "I am returning JSON/HTML/image to you."

If Content-Type is missing or wrong, servers may reject the request or parse the body incorrectly.

Common values:
- `application/json` — JSON data
- `multipart/form-data` — File upload
- `text/html` — HTML content

---

### Q10. What is CORS and why does it occur?

CORS (Cross-Origin Resource Sharing) is a browser security mechanism that restricts web pages from making requests to a different origin than the page was served from.

It occurs because browsers enforce the Same-Origin Policy. A React app on `localhost:3000` cannot freely call a FastAPI backend on `localhost:8000` because different ports mean different origins.

The server must explicitly allow cross-origin requests by sending the appropriate `Access-Control-Allow-Origin` headers in its response.

CORS only applies to browser-based requests. Postman and server-to-server requests are not affected by CORS.

---

### Q11. What is a stateless protocol? Why is HTTP stateless?

A stateless protocol means each request is completely independent. The server does not store any memory of previous requests.

HTTP is stateless by design. After responding to a request, the server immediately forgets that request ever happened.

This makes HTTP:
- Scalable (any server can handle any request)
- Simple (no session state to maintain)

But also means authentication must be handled separately using tokens, cookies, or sessions.

---

## ADVANCED LEVEL

### Q12. What happens when you type a URL in the browser? (Full Answer)

1. Browser checks if URL has a protocol. If not, adds `https://`.
2. Browser parses the URL into parts: scheme, domain, path, query.
3. Browser checks DNS cache (browser → OS → router → ISP DNS).
4. DNS resolves domain to IP address.
5. Browser establishes TCP connection (SYN → SYN-ACK → ACK).
6. If HTTPS: TLS Handshake occurs (exchange certificates, establish encryption).
7. Browser sends HTTP GET request with headers.
8. Server (possibly via load balancer) receives and processes request.
9. Server queries database if needed.
10. Server sends HTTP response with status code, headers, and body.
11. Browser parses HTML and discovers CSS, JS, images.
12. Browser sends additional requests for each discovered asset.
13. Browser renders the complete page.

---

### Q13. What is JWT? How does it work?

JWT (JSON Web Token) is a compact, URL-safe token format used for securely transmitting authentication information between client and server.

Structure: `HEADER.PAYLOAD.SIGNATURE`

**Header** contains algorithm type.
**Payload** contains claims (user ID, expiry, roles).
**Signature** is a cryptographic hash of header + payload using a secret key.

How it works:
1. User logs in with credentials.
2. Server validates credentials and creates JWT signed with secret key.
3. Client receives JWT and stores it.
4. Client sends JWT with every request in `Authorization: Bearer TOKEN` header.
5. Server verifies signature (no database lookup needed).
6. If valid, server processes request. If expired or tampered, returns 401.

JWT payload is base64-encoded, not encrypted. Never store sensitive data in it.

---

### Q14. Explain the difference between cookies and JWT for authentication.

| Feature | Cookies | JWT |
|---|---|---|
| Storage | Browser automatically stores and sends | Developer manages storage |
| Cross-domain | Limited by SameSite policy | Works across domains |
| CSRF risk | Yes (auto-sent by browser) | No (must be manually sent) |
| XSS risk | If not HttpOnly | Yes (if in localStorage) |
| Stateful/Stateless | Can be either | Stateless |
| Best for | Traditional web apps | SPAs, mobile apps, microservices |

---

### Q15. What is rate limiting and how is it implemented?

Rate limiting restricts the number of API requests a client can make in a given time window.

Purpose:
- Prevent API abuse and DDoS attacks
- Ensure fair usage
- Protect server resources

Common strategies:
- **Fixed window**: 100 requests per hour. Counter resets every hour.
- **Sliding window**: 100 requests per any rolling 60-minute period.
- **Token bucket**: Tokens added at fixed rate. Each request consumes a token.

Implementation in FastAPI uses libraries like `slowapi`:

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.get("/users")
@limiter.limit("100/hour")
def get_users(request: Request):
    return []
```

Response when exceeded:

```http
429 Too Many Requests
Retry-After: 3600
```

---

### Q16. What is the difference between authentication and authorization?

**Authentication** answers: **WHO are you?**

```
You provide:
  Email: adya@example.com
  Password: secret123

System verifies your identity.
Result: "You are Adyaprana."
```

**Authorization** answers: **WHAT are you allowed to do?**

```
You are Adyaprana (authenticated).
Can Adyaprana delete other users? NO.
Can Adyaprana access admin panel? NO.
Can Adyaprana view their own profile? YES.
```

In HTTP terms:
- No authentication at all → 401 Unauthorized
- Authenticated but no permission → 403 Forbidden

---

### Q17. What is a webhook? How is it different from an API call?

**Regular API Call (Polling):**

```
Your server → asks Razorpay every 5 seconds → "Did the payment happen?"
Razorpay → "No. No. No. No. Yes!"
```

Wasteful. 99% of requests are empty.

**Webhook (Event-driven):**

```
Razorpay → calls YOUR server → "Payment just happened! Here's the data."
```

You register a URL with Razorpay.
Razorpay sends a POST request to your URL when events happen.
Your server processes it once, immediately.

Webhooks are used by: Razorpay, Stripe, GitHub, Slack, SendGrid, Twilio.

---

### Q18. What is API versioning and why is it important?

API versioning allows you to make breaking changes to your API without breaking existing clients.

Without versioning:

```
Your app returns: {"name": "Adyaprana"}
You change it to: {"full_name": "Adyaprana"}

Every existing client breaks immediately.
Mobile apps that can't auto-update break permanently.
```

With versioning:

```
/api/v1/users → Still returns {"name": "Adyaprana"}
/api/v2/users → Returns {"full_name": "Adyaprana"}

Old clients use v1. New clients use v2.
Both work. Nobody breaks.
```

---

### Q19. Explain the TCP Three-Way Handshake.

Before any HTTP communication, a TCP connection must be established.

```
Client                    Server
  │                          │
  │ ──── SYN ─────────────► │   "I want to connect"
  │                          │
  │ ◄─── SYN-ACK ─────────  │   "OK, I'm ready"
  │                          │
  │ ──── ACK ─────────────► │   "Great, let's go"
  │                          │
  │ ══ Connection Open ══════│
  │ ══ HTTP Request Now ═════│
```

SYN = Synchronize
ACK = Acknowledge

This happens before every HTTP/1.1 connection.

HTTP/2 and HTTP/3 reduce this overhead with connection reuse and faster handshakes.

---

### Q20. What are the differences between HTTP/1.1, HTTP/2, and HTTP/3?

| Feature | HTTP/1.1 | HTTP/2 | HTTP/3 |
|---|---|---|---|
| Year | 1997 | 2015 | 2022 |
| Transport | TCP | TCP | QUIC (UDP-based) |
| Multiplexing | No | Yes | Yes |
| Header Compression | No | HPACK | QPACK |
| Server Push | No | Yes | Yes |
| Connection per Request | Multiple connections | Single connection | Single connection |
| Head-of-Line Blocking | Yes | Partially | No |

HTTP/2 is the current standard for most modern web applications.

FastAPI + uvicorn supports HTTP/2 out of the box.

---

# SECTION 18 — COMMON MISTAKES BEGINNERS MAKE

```
1. Using GET for creating data
   Wrong:  GET /createUser?name=adya
   Right:  POST /users + JSON body

2. Putting sensitive data in query params
   Wrong:  GET /login?password=secret
   Right:  POST /login + JSON body

3. Ignoring status codes
   Wrong:  Always returning 200 even on errors
   Right:  Return 201 for creation, 404 for not found, 422 for validation

4. Not setting Content-Type header
   Wrong:  Sending JSON without Content-Type: application/json
   Right:  Always set Content-Type when sending body

5. Confusing 401 and 403
   401 = Not logged in
   403 = Logged in, no permission

6. CORS in production
   Wrong:  allow_origins=["*"] in production
   Right:  Specify exact frontend origins only

7. Not versioning APIs
   Wrong:  /users (changes break old clients)
   Right:  /v1/users

8. Returning 500 for client errors
   Wrong:  500 for invalid input
   Right:  400 for bad syntax, 422 for validation failure

9. Storing JWT in localStorage
   Better:  HttpOnly cookie (protects from XSS)

10. No pagination
    Wrong:  Returning all 1 million records at once
    Right:  GET /users?page=1&limit=20
```

---

# DAY 22 ASSIGNMENTS

✅ Explain client-server architecture from scratch without notes

✅ Explain the DNS resolution process step by step

✅ Explain what happens when you type a URL — all steps

✅ Memorize all 5 HTTP methods and their purpose

✅ Memorize status codes: 200, 201, 204, 400, 401, 403, 404, 409, 422, 429, 500

✅ Install Postman and explore the interface

✅ Use Postman to hit all endpoints on ReqRes API (GET, POST, PUT, PATCH, DELETE)

✅ Create your own HTTP cheat sheet by hand

✅ Explain the difference between PUT and PATCH with an example

✅ Explain CORS — what it is, why it happens, how to fix it

✅ Explain JWT — what it is, how the auth flow works

✅ Write a complete CRUD API in FastAPI using the template from Section 14

✅ Test your FastAPI API with Postman

---

# DAY 22 BACKEND DEVELOPER CHECKPOINT

If you can explain without notes:

**Core Web Concepts:**
✅ Client and Server
✅ DNS
✅ HTTP
✅ HTTPS and TLS
✅ Request-Response Cycle
✅ TCP Three-Way Handshake

**HTTP Request:**
✅ Methods (GET, POST, PUT, PATCH, DELETE)
✅ Headers (Authorization, Content-Type, User-Agent)
✅ Body
✅ Path Parameters
✅ Query Parameters

**HTTP Response:**
✅ Status Code families (2xx, 3xx, 4xx, 5xx)
✅ Key status codes (200, 201, 204, 400, 401, 403, 404, 409, 422, 429, 500)

**Authentication:**
✅ Cookies
✅ JWT tokens
✅ How Bearer token auth works
✅ Difference between authentication and authorization

**Security:**
✅ CORS — what it is, why it happens, how to fix
✅ HTTPS — why it's mandatory
✅ HttpOnly cookies

**Advanced:**
✅ REST principles
✅ Idempotency
✅ Rate Limiting
✅ API Versioning
✅ Pagination
✅ Webhooks
✅ HTTP/1.1 vs HTTP/2 vs HTTP/3

**Tools:**
✅ Postman
✅ Hoppscotch
✅ ReqRes
✅ curl

---

Then you understand more about HTTP than most beginners who are already building APIs.

Tomorrow when you write:

```python
@app.post("/users", status_code=201)
def create_user(user: UserCreate):
    return new_user
```

You won't just know the syntax.

You'll know:

```
POST means the client is creating a new resource.
status_code=201 means "Created" — the correct code for this.
UserCreate is validated by Pydantic — wrong types = 422.
The response goes back over HTTP as JSON.
The client could be a browser, Postman, a React app, or a mobile app.
All of this happens over HTTPS in production.
If the client is on a different domain, CORS applies.
If authentication is needed, JWT in the Authorization header handles it.
```

**That's the difference between a developer who copies code and one who understands what they're building.**

---

*Day 22 Complete.* ✅
