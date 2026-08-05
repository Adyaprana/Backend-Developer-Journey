# DAY 48 — Project 1: URL Shortener API — Planning, Architecture & Design

> **Phase:** 02 — FastAPI Backend (Days 43–90)
>
> **Week:** W7 — FastAPI Core (Days 43–49)
>
> **Project:** URL Shortener API v1.0
>
> **Today:** Planning Only — No implementation code written
>
> **Status:** ✅ Day 48 Complete — Architecture finalized, schema designed, ready to build

---

# 🎯 What Day 48 Is About

```
START PROJECT 1 — URL Shortener API

  ✅ Plan schema: shortened_urls table (id, original_url, short_code, clicks, created_at)
  ✅ Endpoints: POST /shorten, GET /{short_code} (redirect), GET /stats/{short_code}
  ✅ Design folder structure: main.py, database.py, models.py, routers/urls.py
  ✅ Design the database schema and understand the data flow

  ⏳ Implementation: NOT today
  📌 Build day — no tutorials. Think like a backend engineer.
```

**What was NOT done today:**

```
❌ Setup project folder (next day)
❌ Write database models (next day)
❌ Connect PostgreSQL (next day)
❌ Write a single line of implementation code
```

Day 48 was entirely about **thinking** before building. Professional backend engineers plan before they code. Today was that planning session.

---

# SECTION 1 — THINK LIKE A BACKEND ENGINEER

## Before Any Code: Understand the Problem

The first question a backend engineer asks is never:

```
"What files do I need to create?"
```

It's always:

```
"What problem am I solving?"
"Who is affected by this problem?"
"What does solving it look like from the outside?"
```

---

## Step 1 — Understanding the Problem

Imagine someone gives you this URL:

```
https://www.amazon.in/Samsung-Galaxy-S24-Ultra-5G-Storage/dp/B0CT5DJ6XZ/
ref=sr_1_1?crid=3J7D8ZD4G2X4U&keywords=samsung+galaxy+s24&qid=1688000000
&sprefix=samsung+galaxy%2Caps%2C196&sr=8-1&th=1
```

This URL is:

```
❌ Ugly and unprofessional
❌ Impossible to share in a message or poster
❌ Hard to remember
❌ Easy to break if copied incorrectly
❌ Reveals platform and tracking parameters
```

Instead, we create:

```
https://our-domain.com/aB92Kx
```

When someone visits `GET /aB92Kx`, our backend:

```
1. Looks up "aB92Kx" in the database
2. Finds the original Amazon URL
3. Increases the click counter by 1
4. Returns HTTP 307 Redirect → user is sent to Amazon
```

**That's the entire business idea.** Simple from the user's perspective. Complex engineering underneath.

---

## What Our Backend Actually Does (Four Core Responsibilities)

Instead of jumping to APIs, think about what the service is responsible for:

**Responsibility 1: Store a long URL**

```
Input:  "https://amazon.in/very-long-url..."
Action: Save it in PostgreSQL with a unique short code
Output: "https://our-domain.com/aB92Kx"
```

**Responsibility 2: Generate a unique short code**

```
Input:  Any URL
Output: A unique, short, URL-safe code — e.g., "aB92Kx"

Requirements:
  → Unique: two different URLs must get different codes
  → Short: 6-8 characters is ideal
  → URL-safe: no spaces, special characters that break URLs
  → Fast to generate: not slow computation
```

**Responsibility 3: Redirect users**

```
Input:  GET /aB92Kx
Action: Find aB92Kx in database → get original URL → increment click count
Output: HTTP 307 Temporary Redirect to original URL

This is NOT a normal JSON response.
This is an HTTP redirect — browser follows it automatically.
```

**Responsibility 4: Show analytics**

```
Input:  GET /stats/aB92Kx
Output: {
    "original_url": "https://amazon.in/...",
    "short_code": "aB92Kx",
    "clicks": 142,
    "created_at": "2026-07-10T09:00:00"
}
```

---

# SECTION 2 — REQUIREMENTS

## Functional Requirements (What the system must do)

Functional requirements describe the exact behavior the system provides.

```
FR-1: URL Creation
  → Accept a valid long URL in the request body
  → Generate a unique 6-character short code
  → Store the mapping in PostgreSQL
  → Return the shortened URL string

FR-2: URL Redirection
  → Accept a short code in the path parameter
  → Look up the original URL from the database
  → Increment the click counter by 1
  → Return HTTP 307 Temporary Redirect to the original URL
  → If code not found: return 404

FR-3: URL Statistics
  → Accept a short code in the path parameter
  → Return: original URL, short code, total clicks, created_at timestamp
  → If code not found: return 404
```

**That is Version 1.** Three endpoints. Three responsibilities. Nothing more.

---

## Non-Functional Requirements (How the system should behave)

Non-functional requirements describe the quality of the system, not what it does.

```
NFR-1: Fast responses
  Why: Redirects must feel instant.
  A URL shortener is useless if it adds 3 seconds of delay.
  Target: < 100ms for redirect responses.

NFR-2: Reliable
  Why: Once a short URL is created, it should never return 404 unexpectedly.
  URLs must persist reliably in PostgreSQL.

NFR-3: Maintainable
  Why: Version 2 will add authentication, expiration, and Redis.
  If the code is written cleanly, adding features is easy.
  If the code is tangled, adding anything breaks everything.

NFR-4: Scalable architecture
  Why: The design should allow future extensions without rewrites.
  Service layer, repository layer — each can be changed independently.

NFR-5: Clean code
  Why: Self-documenting names, small functions, single responsibilities.
  Your future self and teammates must understand it without comments.

NFR-6: RESTful API
  Why: Industry conventions exist for a reason.
  POST /shorten to create. GET /{code} to redirect. GET /stats/{code} for data.
  REST makes the API predictable for frontend developers.
```

**The key insight:** Non-functional requirements don't add features. They determine the quality and longevity of the system.

---

## Who Are the Actors?

Version 1 has only one actor:

```
User:
  → Submits a long URL to shorten it
  → Shares the short URL with others
  → Opens a short URL to reach the original destination
  → Views statistics for their short URLs

No admin role.
No authenticated user role.
No API key holder.

Keeping actors simple keeps Version 1 buildable.
```

---

## User Stories

User stories describe requirements from the user's perspective, not the developer's.

```
Story 1:
  As a user, I want to submit a long URL and receive a short URL
  so that I can share it easily.

  Acceptance criteria:
  → POST /shorten with {"original_url": "..."} returns {"short_url": "..."}
  → The short code is unique
  → The URL is saved in the database

Story 2:
  As a user, I want anyone who opens my short URL to be automatically
  redirected to the original URL.

  Acceptance criteria:
  → GET /{short_code} returns HTTP 307 Redirect
  → The browser follows the redirect without user action
  → Click count increases by 1 on every visit
  → 404 if code doesn't exist

Story 3:
  As a user, I want to see how many times my short URL has been clicked.

  Acceptance criteria:
  → GET /stats/{short_code} returns original_url, short_code, clicks, created_at
  → 404 if code doesn't exist
```

User stories guide both development AND testing. A feature is complete when its acceptance criteria are all met.

---

## Version 1 Scope — What Is In and What Is Out

**Included in Version 1:**

```
✅ URL shortening
✅ Unique short code generation
✅ HTTP redirect to original URL
✅ Click counter (increments per visit)
✅ URL statistics endpoint
✅ PostgreSQL persistence
✅ FastAPI REST API
✅ Swagger documentation (auto-generated)
```

**Not included in Version 1:**

```
❌ User accounts
❌ JWT authentication (no login system)
❌ Custom aliases (user chooses their own short code)
❌ URL expiration (links work forever)
❌ QR code generation
❌ Redis caching (no performance optimization yet)
❌ Docker containerization
❌ CI/CD pipeline
❌ Rate limiting
❌ Analytics dashboard
❌ Bulk URL shortening
```

**Why exclude so much?**

```
Scope creep is the most common reason software projects fail.

Adding authentication before the core works means:
  → Two complex systems to debug simultaneously
  → More chances for bugs
  → Slower progress
  → Less confidence in what's working

Version 1 is complete and usable as described.
Version 2 adds authentication.
Version 3 adds Redis.
Each version builds confidently on a working foundation.

This is how professional engineers think.
```

---

# SECTION 3 — THE DATABASE SCHEMA

## The shortened_urls Table

```sql
CREATE TABLE shortened_urls (
    id           SERIAL        PRIMARY KEY,
    original_url TEXT          NOT NULL,
    short_code   VARCHAR(10)   UNIQUE NOT NULL,
    clicks       INTEGER       DEFAULT 0,
    created_at   TIMESTAMP     DEFAULT NOW()
);
```

**Every column explained:**

---

**`id SERIAL PRIMARY KEY`**

```
SERIAL    → PostgreSQL auto-generates: 1, 2, 3, 4...
            You never need to specify it manually.
PRIMARY KEY → Unique + NOT NULL.
             Every row has a unique integer identifier.

Why use id when short_code is also unique?
  → Integers are faster for database operations (smaller, indexed efficiently)
  → Joining tables (future) is cleaner with integer FKs
  → Short code format could change in the future
  → id is the stable internal identifier, short_code is the external one
```

---

**`original_url TEXT NOT NULL`**

```
TEXT      → Unlimited length. No VARCHAR(n) restriction.
             Amazon URLs can be 500+ characters.
             We never want to reject a URL because it's "too long".
NOT NULL  → A shortened URL must have an original. Cannot be empty.
             Every row MUST have an original URL.

Why not VARCHAR(255)?
  255 characters seems like a lot. But production URLs regularly exceed this.
  The safe choice for URLs: always TEXT.
```

---

**`short_code VARCHAR(10) UNIQUE NOT NULL`**

```
VARCHAR(10)  → Short codes are 6-8 characters. 10 gives a safety margin.
               "aB92Kx" = 6 chars. Fits easily.
UNIQUE       → No two URLs can have the same short code.
               The database enforces this. If we try to insert a duplicate,
               PostgreSQL raises an error immediately.
NOT NULL     → Every shortened URL must have a short code.

Why UNIQUE constraint on short_code?
  Correctness: if two URLs share a code, visiting that code is ambiguous.
  The database prevents this at the data level, not just the application level.
  Even if a bug in the code tries to insert a duplicate, PostgreSQL rejects it.
```

---

**`clicks INTEGER DEFAULT 0`**

```
INTEGER   → Whole number. Click counts are never fractional.
DEFAULT 0 → When a new URL is created, clicks start at 0.
             You don't need to specify it in the INSERT statement.
             PostgreSQL sets it automatically.

How it works:
  URL created:       clicks = 0
  First visit:       clicks = 1  (UPDATE SET clicks = clicks + 1)
  100th visit:       clicks = 100

Alternative: Count clicks by reading from a clicks table (more flexible for analytics).
Version 1: integer counter is simple and sufficient.
```

---

**`created_at TIMESTAMP DEFAULT NOW()`**

```
TIMESTAMP    → Stores date + time: "2026-07-10 09:30:15.123"
DEFAULT NOW() → PostgreSQL sets this to the current time automatically at insert.
                You never need to specify it manually.

Why store created_at?
  → Users can see when they created the short URL
  → Future: URL expiration based on creation time
  → Auditing and debugging
  → Sorting by newest first (ORDER BY created_at DESC)
```

---

## The Complete Table Visualization

```
shortened_urls table:
┌────┬──────────────────────────────────────┬────────────┬────────┬─────────────────────┐
│ id │ original_url                         │ short_code │ clicks │ created_at          │
├────┼──────────────────────────────────────┼────────────┼────────┼─────────────────────┤
│  1 │ https://amazon.in/very-long-url...   │ aB92Kx     │    142 │ 2026-07-10 09:30:15 │
│  2 │ https://youtube.com/watch?v=dQw4w... │ Yz31Pm     │     87 │ 2026-07-10 10:00:00 │
│  3 │ https://github.com/Adyaprana/...     │ Qr54Nt     │      3 │ 2026-07-10 11:15:30 │
└────┴──────────────────────────────────────┴────────────┴────────┴─────────────────────┘
```

---

## Index Strategy

```sql
-- Primary key on id (auto-created by PostgreSQL)
-- Unique index on short_code (auto-created by UNIQUE constraint)

-- For production, also consider:
CREATE INDEX idx_short_code ON shortened_urls(short_code);
-- Already covered by the UNIQUE constraint (UNIQUE creates an index automatically).
-- Nothing extra needed for Version 1.
```

---

## The SQLAlchemy Model (What Will Be Written in Day 49)

```python
# This is PLANNED today. Will be coded next day.

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime
from database import Base

class ShortenedURL(Base):
    __tablename__ = "shortened_urls"

    id           = Column(Integer, primary_key=True, index=True)
    original_url = Column(Text, nullable=False)
    short_code   = Column(String(10), unique=True, nullable=False, index=True)
    clicks       = Column(Integer, default=0)
    created_at   = Column(DateTime, default=datetime.utcnow)
```

---

# SECTION 4 — THE API ENDPOINTS

## Three Endpoints — Complete Design

```
POST   /shorten              → Create a short URL
GET    /{short_code}         → Redirect to original URL
GET    /stats/{short_code}   → Get click statistics
```

---

## Endpoint 1: POST /shorten

```
Method:  POST
URL:     /shorten
Purpose: Accept a long URL, generate a short code, store it, return shortened URL

Request Body (JSON):
{
  "original_url": "https://amazon.in/very-long-url..."
}

Success Response (201 Created):
{
  "id": 1,
  "original_url": "https://amazon.in/very-long-url...",
  "short_code": "aB92Kx",
  "short_url": "http://localhost:8000/aB92Kx",
  "clicks": 0,
  "created_at": "2026-07-10T09:30:15"
}

Error Responses:
  422 — URL is empty or not a valid URL format
  400 — URL already shortened (optional duplicate check)
```

**Why POST and not GET?**

```
GET  → Retrieves existing data. Safe, idempotent.
POST → Creates new data. Not safe, not idempotent.

Creating a short URL is a CREATE operation → POST.
Sending data in the request body (original_url) → POST.
Following REST conventions → POST /shorten.
```

---

## Endpoint 2: GET /{short_code}

```
Method:  GET
URL:     /{short_code}
Purpose: Look up the short code, increment click count, redirect to original URL

Path Parameter: short_code (string, e.g., "aB92Kx")

Success Response: HTTP 307 Temporary Redirect
  Location: https://amazon.in/very-long-url...
  (Browser automatically follows this)

Error Response:
  404 — short_code not found in database
```

**This is NOT a normal JSON endpoint:**

```
Normal API endpoint:
  GET /users/1 → HTTP 200 + {"id": 1, "name": "Adya"}
  Client receives data.

Redirect endpoint:
  GET /aB92Kx → HTTP 307 + Location: https://amazon.in/...
  Browser automatically navigates to the Location URL.
  Client never sees JSON. They're just sent somewhere else.

In FastAPI:
  from fastapi.responses import RedirectResponse

  @router.get("/{short_code}")
  def redirect(short_code: str):
      url = db lookup...
      return RedirectResponse(url=url.original_url, status_code=307)
```

**Why HTTP 307 (Temporary Redirect) and not 301 (Permanent)?**

```
301 Permanent Redirect:
  Browser caches the redirect.
  Second visit: browser uses cache, never asks server.
  We never see the click. Click count can't be incremented.
  Also: if we ever change or delete the short URL, browsers with
  cache still redirect. Cannot be corrected without clearing browser cache.

307 Temporary Redirect:
  Browser does NOT cache the redirect.
  Every visit: browser asks our server first.
  We can: increment click count, validate the URL still exists,
  apply rate limiting, gather analytics.
  We stay in control of every redirect.

For a URL shortener: always 307.
```

---

## Endpoint 3: GET /stats/{short_code}

```
Method:  GET
URL:     /stats/{short_code}
Purpose: Return analytics for a specific short URL

Path Parameter: short_code (string, e.g., "aB92Kx")

Success Response (200 OK):
{
  "id": 1,
  "original_url": "https://amazon.in/very-long-url...",
  "short_code": "aB92Kx",
  "clicks": 142,
  "created_at": "2026-07-10T09:30:15"
}

Error Response:
  404 — short_code not found
```

---

## URL Routing Conflict: `/{short_code}` vs `/stats/{short_code}`

```
Potential problem:
  /{short_code} matches EVERYTHING after /
  Including /stats, /docs, /openapi.json

  GET /stats/aB92Kx:
  Router tries to match /{short_code} first?
  short_code = "stats"? That would be wrong.

FastAPI solution:
  Register specific routes BEFORE generic ones.
  FastAPI routes match TOP-TO-BOTTOM.

  Correct order:
  @router.get("/stats/{short_code}")     ← registered first
  def get_stats(short_code: str): ...

  @router.get("/{short_code}")           ← registered second
  def redirect(short_code: str): ...

  When GET /stats/aB92Kx arrives:
  FastAPI checks /stats/{short_code} first → MATCH! Uses get_stats.
  Never reaches /{short_code}.

Rule: Always register specific routes before generic pattern routes.
```

---

# SECTION 5 — HIGH-LEVEL SYSTEM FLOW

## Create Short URL Flow

```
Client
   │
   │ POST /shorten
   │ {"original_url": "https://amazon.in/..."}
   ▼
FastAPI Router
   │
   ▼
Pydantic Schema validates original_url
   │ (422 if invalid URL format)
   ▼
Service Layer
   │ Generate unique short code:
   │   import secrets, string
   │   characters = string.ascii_letters + string.digits
   │   code = ''.join(secrets.choice(characters) for _ in range(6))
   │   → "aB92Kx"
   ▼
Repository Layer
   │ INSERT INTO shortened_urls (original_url, short_code)
   │ VALUES ('https://amazon.in/...', 'aB92Kx')
   │ RETURNING id, original_url, short_code, clicks, created_at;
   ▼
PostgreSQL stores permanently
   │
   ▼
Response built:
   {
     "short_code": "aB92Kx",
     "short_url": "http://localhost:8000/aB92Kx",
     ...
   }
   │
   ▼
Client receives 201 Created + response JSON
```

---

## Visit Short URL (Redirect) Flow

```
Browser
   │
   │ GET /aB92Kx
   ▼
FastAPI Router
   │ Matches /{short_code} with short_code = "aB92Kx"
   ▼
Service Layer
   │ Step 1: Look up "aB92Kx" in database
   ▼
Repository Layer
   │ SELECT * FROM shortened_urls WHERE short_code = 'aB92Kx';
   │ → Returns row with original_url
   ▼
Back to Service Layer
   │ Step 2: Increment click count
   │ UPDATE shortened_urls SET clicks = clicks + 1 WHERE short_code = 'aB92Kx';
   ▼
Return HTTP 307 Redirect
   │ Location: https://amazon.in/very-long-url...
   ▼
Browser receives 307
   │ Browser automatically follows Location header
   ▼
Browser navigates to Amazon
```

---

## Stats Request Flow

```
Client
   │
   │ GET /stats/aB92Kx
   ▼
FastAPI Router (matches /stats/{short_code} — registered before /{short_code})
   │
   ▼
Repository Layer
   │ SELECT * FROM shortened_urls WHERE short_code = 'aB92Kx';
   │ → Returns full row
   ▼
Pydantic Response Schema filters the result
   │
   ▼
JSON Response:
   {
     "original_url": "https://amazon.in/...",
     "short_code": "aB92Kx",
     "clicks": 142,
     "created_at": "2026-07-10T09:30:15"
   }
```

---

# SECTION 6 — PLANNED FOLDER STRUCTURE

This structure was designed today. Files will be created next day.

```
url-shortener/
│
├── main.py              ← FastAPI app + router registration + CORS + startup
├── database.py          ← Engine, SessionLocal, Base, get_db()
├── models.py            ← SQLAlchemy ORM model (ShortenedURL table)
├── schemas.py           ← Pydantic request/response schemas
├── crud.py              ← Database operations (create, get_by_code, increment_clicks)
├── utils.py             ← Short code generator (secrets.choice)
│
└── routers/
    └── urls.py          ← All 3 endpoints: POST /shorten, GET /{code}, GET /stats/{code}
```

---

## What Each File Will Do

**main.py:**

```python
# Creates app = FastAPI()
# Registers CORSMiddleware
# Calls Base.metadata.create_all(engine) on startup
# Includes urls.router
# Home endpoint /
```

**database.py:**

```python
# DATABASE_URL = "postgresql+psycopg2://..."
# engine = create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(...)
# Base = declarative_base()
# def get_db(): yield db (generator dependency)
```

**models.py:**

```python
# class ShortenedURL(Base):
#     __tablename__ = "shortened_urls"
#     id, original_url, short_code, clicks, created_at
```

**schemas.py:**

```python
# class URLCreate(BaseModel):
#     original_url: HttpUrl  # Pydantic validates URL format automatically
#
# class URLResponse(BaseModel):
#     id: int
#     original_url: str
#     short_code: str
#     short_url: str         # constructed: "domain/" + short_code
#     clicks: int
#     created_at: datetime
#     model_config = ConfigDict(from_attributes=True)
#
# class URLStats(BaseModel):
#     original_url: str
#     short_code: str
#     clicks: int
#     created_at: datetime
#     model_config = ConfigDict(from_attributes=True)
```

**crud.py:**

```python
# def create_url(db, original_url, short_code): ...
# def get_url_by_code(db, short_code): ...
# def increment_clicks(db, url): ...
```

**utils.py:**

```python
# import secrets, string
#
# def generate_short_code(length: int = 6) -> str:
#     characters = string.ascii_letters + string.digits
#     return ''.join(secrets.choice(characters) for _ in range(length))
#
# Generates: "aB92Kx", "Yz31Pm", "Qr54Nt"
# secrets module (NOT random!) — cryptographically secure randomness
```

**routers/urls.py:**

```python
# router = APIRouter()
#
# @router.post("/shorten", response_model=URLResponse, status_code=201)
# def shorten_url(url: URLCreate, db: Session = Depends(get_db)):
#     ...
#
# @router.get("/stats/{short_code}", response_model=URLStats)
# def get_stats(short_code: str, db: Session = Depends(get_db)):
#     ...
#
# @router.get("/{short_code}")   ← registered AFTER /stats/{short_code}
# def redirect_url(short_code: str, db: Session = Depends(get_db)):
#     ...
```

---

# SECTION 7 — SHORT CODE GENERATION

## Requirements for a Good Short Code

```
Uniqueness:    No two URLs can share a short code
Length:        6-8 characters (short enough to be convenient)
URL-safe:      Only letters and digits, no /, ?, #, &, =
Random:        Not sequential (sequential codes are predictable)
Fast:          Generated in microseconds, not milliseconds
```

## The Algorithm (Planned)

```python
import secrets
import string

def generate_short_code(length: int = 6) -> str:
    # Alphabet: a-z + A-Z + 0-9 = 62 characters
    characters = string.ascii_letters + string.digits

    # secrets.choice: cryptographically secure random pick
    # NOT random.choice (predictable, not suitable for codes)
    code = ''.join(secrets.choice(characters) for _ in range(length))
    return code

# Examples of generated codes:
# "aB92Kx", "Yz31Pm", "Qr54Nt", "mK78Ws", "eT45Nb"
```

**Why `secrets` module and not `random`?**

```python
# random module:
random.choice("abc123")
# Uses a pseudo-random number generator (PRNG).
# Output is predictable if you know the seed.
# NEVER use for security-related code generation.

# secrets module:
secrets.choice("abc123")
# Uses the operating system's cryptographic random source.
# Output is unpredictable and suitable for security tokens.
# Short codes are shared publicly, but unpredictable codes
# prevent people from guessing other users' URLs.
```

**Collision probability:**

```
62 characters, 6 positions:
62^6 = 56,800,235,584 possible codes (56 billion)

For 1 million short URLs:
Probability of collision ≈ 1/56,800 per generated code

Strategy for handling collision:
  Generate code → Check if it exists in database
  If exists: generate again (loop until unique)
  In practice: collisions are extremely rare
```

---

# SECTION 8 — WHY THIS PROJECT MATTERS FOR YOUR CAREER

## What You'll Demonstrate in Interviews

```
After building this project, you can say:

"I built a URL shortener API with FastAPI and PostgreSQL.
 It supports URL creation, HTTP redirect with click tracking,
 and a statistics endpoint. I designed the schema with a
 dedicated shortened_urls table, used SQLAlchemy ORM for
 data access, and followed layered architecture with
 separate router, service, and repository concerns."

This demonstrates:
  → FastAPI routing (path params, redirect, POST body)
  → PostgreSQL schema design (appropriate types, constraints, indexes)
  → SQLAlchemy ORM (models, sessions, queries)
  → HTTP protocol understanding (307 vs 301, redirect mechanics)
  → REST API design (correct verbs, endpoints, status codes)
  → Software engineering thinking (scope, requirements, design before code)
```

## Real Systems That Work This Way

```
Bitly:
  Same three operations (create, redirect, stats).
  At scale: billions of redirects per day.
  Adds: Redis caching, CDN, distributed short code generation.
  Our v1 is architecturally similar. Just smaller.

TinyURL:
  Pioneered the concept.
  Added: custom aliases, link expiration.
  Our v2 could add these.

Twitter's t.co:
  Every tweet link is automatically shortened to t.co/xxxxx.
  Same redirect pattern.
  Adds: malware scanning before redirect.

The engineering CONCEPTS are identical.
Scale differs. Architecture is the same.
```

---

# SECTION 9 — INTERVIEW QUESTIONS

## Q1. What is the difference between functional and non-functional requirements?

Functional requirements describe WHAT the system does — features the user directly experiences. "The system must create short URLs" is functional. Non-functional requirements describe HOW the system should behave — qualities like speed, reliability, maintainability. "Redirects must complete in under 100ms" is non-functional. Both are essential. Functional without non-functional produces slow, unreliable software.

## Q2. Why use HTTP 307 for redirects instead of 301?

HTTP 301 (Permanent Redirect) is cached by browsers. The second visit never reaches your server — the browser redirects locally. You can never increment the click count. If you delete the short URL, cached browsers still redirect until cache expires.

HTTP 307 (Temporary Redirect) is NOT cached. Every visit reaches your server. You can increment clicks, validate the URL still exists, and change the destination later. For a URL shortener where analytics matter, 307 is the only correct choice.

## Q3. Why do software teams define scope before implementation?

Scope definition prevents scope creep — the most common cause of delayed projects. If you start coding without clear scope, every new idea gets added. The project never finishes. Defining "Version 1 includes X, not Y" means: you build X completely, ship it, then add Y in version 2. Each version is complete and deliverable. Scope also helps estimate time and resources accurately.

## Q4. What is a URL shortener and how does it work internally?

A URL shortener accepts a long URL and generates a short, unique code. It stores the mapping (code → original URL) in a database. When someone visits the short URL, the server looks up the code, optionally increments a counter, and returns an HTTP redirect response pointing to the original URL. The browser follows the redirect automatically. The user never sees JSON — they just arrive at the original page.

## Q5. Why is a redirect endpoint different from a normal GET endpoint?

A normal GET endpoint returns data (JSON, HTML). A redirect endpoint returns an HTTP 307 response with a `Location` header. The browser automatically navigates to the `Location` URL without any user action. There is no JSON body in a redirect. The response code (307) tells the browser "go there instead."

## Q6. Why are user stories useful during software development?

User stories describe requirements from the user's perspective, not the technical perspective. "As a user, I want to see click statistics for my short URL" is more meaningful than "Build GET /stats endpoint." User stories keep the team focused on user value, serve as acceptance criteria for testing (a feature is done when the story's conditions are met), and prevent building features nobody needs.

## Q7. Why should Version 1 avoid features like authentication or Redis?

Adding complexity before the core works creates multiple unsolved problems simultaneously. Debugging becomes exponentially harder. Authentication has its own bugs. Redis has its own configuration. The core URL shortening might have bugs too. You can't isolate which layer is failing. Version 1 focused on core functionality (shorten, redirect, stats) builds confidence, delivers a usable product, and creates a stable foundation for Version 2 features.

## Q8. What is the purpose of the `clicks` column with `DEFAULT 0`?

`clicks` tracks how many times a short URL has been visited. `DEFAULT 0` means PostgreSQL sets it to zero when a new URL is created — you don't need to specify it in the INSERT statement. Every redirect increments it by 1 using `UPDATE SET clicks = clicks + 1`. It provides the basic analytics visible in the `/stats/{short_code}` endpoint.

---

# SECTION 10 — IMPORTANT THINGS TO KNOW

```
 1. Plan before you code. Architecture mistakes are expensive to fix later.
    30 minutes of planning saves hours of refactoring.

 2. Functional requirements = what the system does.
    Non-functional requirements = how well it does it.
    Both are required for professional software.

 3. User stories = requirements from the user's perspective.
    Used for both planning and acceptance testing.

 4. Scope definition = deciding what NOT to build.
    A focused v1 is better than an unfinished v2.

 5. HTTP 307 Temporary Redirect: browser asks server every time → click counting works.
    HTTP 301 Permanent Redirect: browser caches → click counting breaks.
    URL shorteners must use 307.

 6. The redirect endpoint (GET /{short_code}) returns no JSON.
    It returns an HTTP response with a Location header.
    Browsers follow Location automatically.

 7. Route order in FastAPI matters for pattern conflicts.
    /stats/{short_code} must be registered BEFORE /{short_code}.
    FastAPI matches routes top-to-bottom.

 8. Use TEXT for URLs, not VARCHAR(n).
    Production URLs easily exceed 255 characters.

 9. UNIQUE constraint on short_code prevents duplicates at the database level.
    Even if application code has a bug, the database is the last defense.

10. secrets.choice() is cryptographically secure.
    random.choice() is predictable and not suitable for generating codes.

11. 62^6 = 56 billion possible codes.
    Collision probability is very low, but must be handled (retry on duplicate).

12. The stats endpoint returns stored click count, not calculated.
    Incrementing on every redirect and reading on /stats is more efficient
    than counting redirect records.

13. SERIAL PRIMARY KEY auto-generates integers.
    You never need to specify id in INSERT statements.

14. default=datetime.utcnow (no parentheses) in SQLAlchemy.
    datetime.utcnow() evaluates at class definition time — all rows get the same timestamp.
    datetime.utcnow (no parens) is called fresh at INSERT time.

15. "Build day — no tutorials" means: solve problems yourself.
    Looking things up is fine. Copying solutions without understanding is not.
    Today was planning. Implementation starts next day.
```

---

# REVISION SHEET

```
═══════════════════════════════════════════════════════════
URL SHORTENER API — DAY 48 PLANNING REVISION
═══════════════════════════════════════════════════════════

THE PROBLEM:
  Long URL → Short code → Redirect to original

4 CORE RESPONSIBILITIES:
  1. Store long URL + generate short code
  2. Generate unique, URL-safe 6-char code
  3. Redirect visitors (307) + increment clicks
  4. Return statistics

DATABASE TABLE: shortened_urls
  id           SERIAL        PRIMARY KEY
  original_url TEXT          NOT NULL
  short_code   VARCHAR(10)   UNIQUE NOT NULL
  clicks       INTEGER       DEFAULT 0
  created_at   TIMESTAMP     DEFAULT NOW()

3 ENDPOINTS:
  POST   /shorten              → create + return short URL (201)
  GET    /stats/{short_code}   → statistics JSON (200 or 404)
  GET    /{short_code}         → 307 redirect (or 404)
  (register /stats BEFORE /{short_code} to avoid conflict!)

SHORT CODE GENERATION:
  import secrets, string
  chars = string.ascii_letters + string.digits  → 62 chars
  code = ''.join(secrets.choice(chars) for _ in range(6))
  62^6 = 56 billion combinations

HTTP REDIRECT:
  307 Temporary → NOT cached → browser asks every time → click count works
  301 Permanent → cached → click count BREAKS

FILES PLANNED (not yet created):
  main.py, database.py, models.py, schemas.py, crud.py, utils.py, routers/urls.py

VERSION 1 SCOPE:
  IN:  shorten, redirect, stats, PostgreSQL, FastAPI, Swagger
  OUT: auth, Redis, Docker, QR, expiry, custom aliases

KEY DECISIONS:
  TEXT (not VARCHAR) for original_url — URLs can be very long
  UNIQUE constraint on short_code — database enforces uniqueness
  307 (not 301) for redirect — analytics must work
  secrets.choice (not random.choice) — unpredictable codes
  DEFAULT 0 for clicks — no need to specify in INSERT
  DEFAULT NOW() for created_at — auto timestamp
```

---

*Day 48 Complete. Project 1 planned. Schema designed. Architecture finalized. Implementation starts next day.* ✅
