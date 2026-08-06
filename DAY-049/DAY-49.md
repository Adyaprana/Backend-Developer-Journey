# DAY 49 — Rest + Review: URL Shortener Architecture + LeetCode Prefix Sum + HashMap

> **Phase:** 02 — FastAPI Backend (Days 43–90)
>
> **Week:** W7 — FastAPI Core (Days 43–49) — Final Day of Week 7
>
> **Today:** Rest + Review FastAPI basics + URL Shortener deep architecture design + LeetCode #560
>
> **LeetCode:** #560 Subarray Sum Equals K ✅ (43ms · Accepted 93/93)
>
> **Status:** ✅ Day 49 Complete — Week 7 reviewed, URL Shortener architecture fully designed, Prefix Sum + HashMap pattern mastered

---

# 🎯 What Day 49 Is About

```
Rest + Review FastAPI basics

  ✅ Review the 7-day FastAPI journey (Days 43-49)
  ✅ URL Shortener Architecture — Why Layered Design?
  ✅ Folder structure designed (deeper than Day 48 planning)
  ✅ Layer responsibilities explained
  ✅ LeetCode #560 — Subarray Sum Equals K (Brute Force + Prefix Sum + HashMap)

  Build day — no new tutorials. Consolidate what was learned.
```

---

# SECTION 1 — WEEK 7 REVIEW: WHAT WAS BUILT (DAYS 43–49)

## The Complete Journey

```
Day 43: FastAPI Setup + First Endpoint
  → pip install fastapi uvicorn
  → @app.get("/") — first working API
  → uvicorn main:app --reload
  → Path parameters: /users/{user_id}
  → Query parameters: /items?skip=0&limit=10
  → Swagger UI at /docs

Day 44: Pydantic Models — Request/Response Validation
  → from pydantic import BaseModel
  → UserCreate (input), UserResponse (output — hides password)
  → Field(min_length=3), Optional[int], EmailStr
  → HTTP 422 for validation failures
  → response_model filters output automatically

Day 45: FastAPI + PostgreSQL + SQLAlchemy
  → database.py: engine, SessionLocal, Base, get_db()
  → models.py: SQLAlchemy ORM User class
  → schemas.py: Pydantic input/output
  → crud.py: create, read, update, delete operations
  → main.py: Depends(get_db) — Dependency Injection
  → Base.metadata.create_all(engine) on startup

Day 46: JWT Authentication — Login System
  → bcrypt password hashing
  → JWT: header.payload.signature structure
  → create_access_token(), decode_access_token()
  → OAuth2PasswordBearer (extracts token — not authenticator)
  → get_current_user() dependency
  → Protected routes with Depends(get_current_user)

Day 47: Error Handling, Middleware, CORS
  → HTTPException with status codes
  → Custom exception classes + handlers
  → Middleware: runs before/after every request
  → CORSMiddleware: allows frontend to call the API
  → logging.basicConfig — never use print() in production

Day 48: URL Shortener — Project Planning
  → shortened_urls table schema designed
  → 3 endpoints: POST /shorten, GET /{code}, GET /stats/{code}
  → Short code generation strategy (secrets module)
  → 307 vs 301 redirect decision

Day 49 (Today): Rest + Review + Architecture + LeetCode #560
```

## What You Can Now Build From Scratch

```
✅ A FastAPI server with multiple endpoints
✅ Pydantic request/response validation
✅ Connection to PostgreSQL with SQLAlchemy
✅ Full CRUD operations
✅ JWT authentication with bcrypt passwords
✅ Protected routes
✅ Custom error handling
✅ Middleware (logging, timing, CORS)
✅ Production-ready project structure
```

**After 7 days, you can build the backend of most standard web applications.**

---

# SECTION 2 — URL SHORTENER ARCHITECTURE: THINK BEFORE YOU CODE

## Why Architecture Matters

Imagine building a house. Would you start placing bricks immediately? No.

You would first decide:
- Number of floors
- Rooms
- Plumbing locations
- Electrical wiring routes
- Foundation type

**Software is exactly the same.**

If you start coding immediately:

```
main.py       → 300 lines
helpers.py    → "I'll put some stuff here"
utils.py      → "More random helpers"
crud.py       → "Database stuff"
new_crud.py   → "Fixed version of crud.py"
crud_final.py → "Actually this one"
```

Everything becomes tangled. Nobody knows what belongs where. Adding a new feature breaks two existing ones.

Professional software avoids this by defining architecture first.

---

## What Architecture Defines

```
Architecture answers four questions:

1. WHERE should code live?
   "All database operations go in repositories/"
   "All business rules go in services/"

2. WHO is responsible for what?
   "The router is responsible for HTTP, nothing else"
   "The service is responsible for business logic, nothing else"

3. HOW do parts communicate?
   "Router calls Service. Service calls Repository. Repository calls Database."
   "Repository never calls Router. Database never calls Service."

4. WHAT depends on what?
   "Service depends on Repository"
   "Router depends on Service"
   "Nothing depends on Router"
```

---

## Choosing the Right Architecture

```
Architecture           Best For                        Complexity
─────────────────────────────────────────────────────────────────
MVC                    Small web apps                  ⭐
Layered Architecture   APIs & business applications    ⭐⭐
Clean Architecture     Large enterprise systems        ⭐⭐⭐⭐
Hexagonal Architecture Highly scalable services        ⭐⭐⭐⭐⭐
Microservices          Very large organizations        ⭐⭐⭐⭐⭐
```

**Why Not Clean Architecture for Version 1?**

Many tutorials say: "Always use Clean Architecture."

In reality:

```
Full Clean Architecture for a URL shortener:
  → Entities, Use Cases, Interface Adapters, Framework layer
  → 15+ files before writing a single endpoint
  → Abstract interfaces everywhere
  → Dependency injection containers
  → Enormous boilerplate

For Version 1 of a URL shortener with 3 endpoints:
  → This is unnecessary complexity
  → Slower development
  → Harder to debug
  → Intimidating for everyone reading the code
```

**Our choice: Layered Architecture with clean boundaries.**

This gives most of the benefits while keeping the project approachable. As the project grows (authentication, Redis, analytics, Docker), the architecture can evolve toward more complexity if needed.

---

## Our Architecture

```
         Client
            │
            │ HTTP Request
            ▼
      FastAPI Router
            │
            │ Calls
            ▼
      Service Layer
            │
            │ Calls
            ▼
    Repository Layer
            │
            │ Queries
            ▼
   PostgreSQL Database
```

**One direction only. No layer skips another. No layer reaches backward.**

---

# SECTION 3 — LAYER RESPONSIBILITIES

## Layer 1: Router Layer

**What it handles:** HTTP concerns only.

```python
# Router knows:
#   → HTTP methods (GET, POST)
#   → URL paths (/shorten, /{short_code})
#   → Request body (Pydantic schema validation)
#   → Response format (Pydantic response_model)
#   → Status codes (201, 404, 307)
#   → Dependency injection (Depends(get_db))

# Router does NOT know:
#   → How short codes are generated
#   → Whether a short code already exists
#   → How to increment click counts
#   → SQL or database operations
```

**What the router should look like:**

```python
@router.post("/shorten", response_model=URLResponse, status_code=201)
def shorten_url(url: URLCreate, db: Session = Depends(get_db)):
    result = url_service.create_short_url(db, url.original_url)
    return result

# Three lines. No business logic. No SQL.
# Router receives → delegates → returns.
```

---

## Layer 2: Service Layer

**What it handles:** Business logic — the heart of the application.

```python
# Service knows:
#   → Business rules
#   → "Check if this URL was already shortened"
#   → "Generate a short code using secrets module"
#   → "Retry if short code collision occurs"
#   → "Increment click count on every redirect"

# Service does NOT know:
#   → HTTP status codes
#   → Request/response formats
#   → SQL syntax
#   → Table names
```

**Why does the service layer exist?**

```
Without service layer:
  Router calls Repository directly.
  Business logic scattered in router functions.
  "Check if already shortened" is in one router.
  "Collision retry logic" is in another.
  Testing requires mocking the database.
  Adding a new rule means finding all places to update.

With service layer:
  ALL business rules in one place.
  Router never decides anything.
  Repository never decides anything.
  Testing: mock the repository, test only business logic.
  Adding a new rule: one place to change.
```

---

## Layer 3: Repository Layer

**What it handles:** Data access only.

```python
# Repository knows:
#   → How to INSERT a new URL
#   → How to SELECT by short_code
#   → How to UPDATE click count
#   → SQLAlchemy syntax

# Repository does NOT know:
#   → Business rules
#   → HTTP status codes
#   → Short code generation
#   → Whether the URL already exists (that's service logic)
```

**Repository is a TRANSLATOR:**

```
Service wants:   "Give me the URL with code 'aB92Kx'"
Repository does: SELECT * FROM shortened_urls WHERE short_code = 'aB92Kx';
Repository gives: ShortenedURL Python object back to Service
```

---

## Layer 4: Database Layer (PostgreSQL)

**What it handles:** Persistent storage.

```
Stores data permanently.
Enforces constraints (UNIQUE on short_code, NOT NULL).
For Version 1: PostgreSQL via SQLAlchemy.
Future: could add Redis for caching, still using same Repository interface.
```

---

## The One Rule To Memorize

```
ROUTERS never contain database queries.
REPOSITORIES never contain business logic.
SERVICES never handle HTTP directly.
UTILITIES never contain domain-specific logic.

If you're unsure where something belongs:
  Does it know about HTTP? → Router
  Does it implement a business rule? → Service
  Does it talk to the database? → Repository
  Is it small and reusable across domains? → Utils
```

---

# SECTION 4 — DETAILED FOLDER STRUCTURE

```
url_shortener_api/
│
├── app/
│   │
│   ├── routers/
│   │   └── urls.py            ← API endpoints: POST /shorten, GET /{code}, GET /stats/{code}
│   │
│   ├── services/
│   │   └── url_service.py     ← Business logic: generate codes, handle collisions
│   │
│   ├── repositories/
│   │   └── url_repository.py  ← Database operations: create, read, update
│   │
│   ├── models/
│   │   └── url_model.py       ← SQLAlchemy ORM: class ShortenedURL(Base)
│   │
│   ├── schemas/
│   │   └── url_schema.py      ← Pydantic: URLCreate, URLResponse, URLStats
│   │
│   ├── database/
│   │   └── db.py              ← engine, SessionLocal, Base, get_db()
│   │
│   ├── core/
│   │   └── config.py          ← Settings: DATABASE_URL, BASE_DOMAIN, CODE_LENGTH
│   │
│   └── utils/
│       └── code_generator.py  ← secrets.choice() short code generation
│
├── tests/
│   └── test_urls.py           ← Unit and integration tests (future)
│
├── requirements.txt
├── .env                        ← DATABASE_URL, SECRET_KEY (never commit this)
├── .gitignore                  ← includes .env, __pycache__, .venv
└── README.md
```

---

## Folder Responsibilities Table

```
Folder          │ File              │ What Lives Here
────────────────┼───────────────────┼─────────────────────────────────────
routers/        │ urls.py           │ @router.post, @router.get — HTTP only
services/       │ url_service.py    │ create_short_url(), handle_redirect()
repositories/   │ url_repository.py │ create_url(), get_by_code(), add_click()
models/         │ url_model.py      │ class ShortenedURL(Base)
schemas/        │ url_schema.py     │ URLCreate, URLResponse, URLStats
database/       │ db.py             │ engine, SessionLocal, Base, get_db()
core/           │ config.py         │ DATABASE_URL, BASE_DOMAIN, CODE_LENGTH
utils/          │ code_generator.py │ generate_short_code() — secrets.choice()
tests/          │ test_urls.py      │ pytest unit and integration tests
```

---

## Why Separate models/ and schemas/?

This is one of the most common beginner confusions:

```
models/ (SQLAlchemy models = database tables):

class ShortenedURL(Base):
    __tablename__ = "shortened_urls"
    id           = Column(Integer, primary_key=True)
    original_url = Column(Text)
    short_code   = Column(String(10))
    clicks       = Column(Integer, default=0)
    created_at   = Column(DateTime)

→ This IS the database.
→ SQLAlchemy maps this Python class to a PostgreSQL table.
→ Changing this changes the database schema.


schemas/ (Pydantic models = API data shape):

class URLCreate(BaseModel):
    original_url: HttpUrl      ← what client sends

class URLResponse(BaseModel):
    short_code: str
    short_url: str             ← constructed in service
    clicks: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

→ This is the API contract.
→ Pydantic validates and serializes data.
→ Changing this changes what clients send/receive.
→ Changing this does NOT change the database.


Why keep them separate?
  Change the API (add a new field to response)
    → Change schemas/ only. Database unchanged.

  Change the database (add an index)
    → Change models/ only. API unchanged.

  If they were the same class: changing one always changes the other.
  Bugs appear in unexpected places.
  Keeping them separate = keeping concerns separate.
```

---

## core/config.py — Centralized Configuration

```python
# app/core/config.py

import os
from dotenv import load_dotenv

load_dotenv()  # reads .env file

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:postgres123@localhost:5432/url_shortener")
    BASE_DOMAIN: str = os.getenv("BASE_DOMAIN", "http://localhost:8000")
    CODE_LENGTH: int = 6

settings = Settings()
```

```
Why core/config.py?

Before core/config.py:
  In main.py:       DATABASE_URL = "postgresql://..."
  In database.py:   engine = create_engine("postgresql://...")
  In service:       domain = "http://localhost:8000"
  In tests:         domain = "http://localhost:8000"  ← different copy

  Change the domain? Must find every file and update.
  Easy to miss one. Bugs appear only in production.

After core/config.py:
  All configuration in ONE place.
  Change BASE_DOMAIN once → all files use the new value.
  Production uses environment variables (.env file).
  Never hardcode credentials.
```

---

## utils/code_generator.py — Pure Utility

```python
# app/utils/code_generator.py

import secrets
import string


def generate_short_code(length: int = 6) -> str:
    """
    Generate a cryptographically secure, URL-safe short code.

    Characters: a-z + A-Z + 0-9 = 62 possible characters
    Length 6:   62^6 = 56,800,235,584 possible codes (56 billion)
    """
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))


# Why secrets.choice() not random.choice()?
#
# random.choice uses a pseudo-random generator.
# Output can be predicted if the seed is known.
# Example: if attacker knows the time your server started,
# they can calculate codes that will be generated.
#
# secrets.choice uses OS-level cryptographic randomness.
# Output is unpredictable.
# Short codes are public — anyone can see "aB92Kx".
# But they should NOT be able to guess the NEXT one.
```

---

## Request Flow — Detailed (All 3 Endpoints)

**POST /shorten (Create Short URL):**

```
Client → POST /shorten {"original_url": "https://amazon.in/..."}
              │
              ▼
Pydantic URLCreate validates (HttpUrl checks format)
              │
              ▼
routers/urls.py calls url_service.create_short_url(db, original_url)
              │
              ▼
services/url_service.py:
  1. code = generate_short_code()      → "aB92Kx"
  2. Check if code exists (collision)  → retry if yes
  3. url_repository.create(db, original_url, code)
              │
              ▼
repositories/url_repository.py:
  INSERT INTO shortened_urls (original_url, short_code)
  VALUES ('https://amazon.in/...', 'aB92Kx')
  RETURNING *
              │
              ▼
ShortenedURL object returned → service → router
              │
              ▼
Pydantic URLResponse builds short_url = BASE_DOMAIN + "/" + short_code
              │
              ▼
Client receives 201 Created:
{
  "short_code": "aB92Kx",
  "short_url": "http://localhost:8000/aB92Kx",
  "clicks": 0,
  "created_at": "2026-07-11T09:00:00"
}
```

**GET /{short_code} (Redirect):**

```
Browser → GET /aB92Kx
              │
              ▼
routers/urls.py calls url_service.handle_redirect(db, "aB92Kx")
              │
              ▼
services/url_service.py:
  1. url_repository.get_by_code(db, "aB92Kx")
  2. If not found → raise HTTPException(404)
  3. url_repository.increment_clicks(db, url)
              │
              ▼
repositories/url_repository.py:
  SELECT * FROM shortened_urls WHERE short_code = 'aB92Kx';
  UPDATE shortened_urls SET clicks = clicks + 1 WHERE id = 1;
              │
              ▼
ShortenedURL.original_url = "https://amazon.in/..."
              │
              ▼
Router returns RedirectResponse(url=original_url, status_code=307)
              │
              ▼
Browser follows Location header → navigates to Amazon
```

**GET /stats/{short_code}:**

```
Client → GET /stats/aB92Kx
              │
              ▼
url_repository.get_by_code(db, "aB92Kx")
              │
              ▼
SELECT * FROM shortened_urls WHERE short_code = 'aB92Kx';
              │
              ▼
Pydantic URLStats filters response
              │
              ▼
Client receives 200:
{
  "original_url": "https://amazon.in/...",
  "short_code": "aB92Kx",
  "clicks": 142,
  "created_at": "2026-07-11T09:00:00"
}
```

---

# SECTION 5 — ARCHITECTURE PRINCIPLES (RULES TO FOLLOW)

```
Principle 1: One Responsibility Per Layer
  Router: HTTP only.
  Service: Business rules only.
  Repository: Database only.
  Utils: Small, generic helpers.

Principle 2: Dependency Direction
  Router → Service → Repository → Database
  Never backwards. Never skip levels.
  Repository cannot call Router. Service cannot query database directly.

Principle 3: Business Logic Lives in Service
  "Check if short code already exists" → Service
  "Retry on collision" → Service
  "Validate URL format beyond Pydantic" → Service
  Never in Router. Never in Repository.

Principle 4: Configuration Centralized
  All DATABASE_URL, BASE_DOMAIN, CODE_LENGTH in core/config.py
  Never hardcoded. Never duplicated.
  Read from environment variables in production.

Principle 5: Schemas and Models Are Separate
  models/ = database tables (SQLAlchemy)
  schemas/ = API data shapes (Pydantic)
  Changing one should not require changing the other.

Principle 6: Testability
  Each layer can be tested independently.
  Service tests: mock the repository.
  Repository tests: use a test database.
  Router tests: mock the service.
  No test needs to touch all three layers simultaneously.
```

---

# SECTION 6 — INTERVIEW QUESTIONS (ARCHITECTURE)

## Q1. What is Layered Architecture?

Layered Architecture organizes code into layers where each layer has exactly one responsibility. Common layers: Presentation (Router), Business Logic (Service), Data Access (Repository), Database. Each layer only communicates with the layer directly below it. This makes code easier to maintain, test, and extend.

## Q2. Why should routers not contain business logic?

If business logic lives in routers, the same logic must be duplicated across multiple endpoints. Testing requires sending HTTP requests instead of calling functions. When the logic changes, every endpoint must be updated. The service layer centralizes business logic, making it testable without HTTP and changeable in one place.

## Q3. What is the difference between a Model and a Schema?

A model (SQLAlchemy) represents a database table — it defines how data is stored. A schema (Pydantic) represents the API data contract — it defines how data is validated and serialized for the client. They are intentionally separate so database changes don't break the API, and API changes don't require database migrations.

## Q4. Why use a Repository Layer instead of writing SQL directly in services?

The repository layer is the only place that knows about the database. If you need to switch from PostgreSQL to MongoDB, only the repository changes. If you use raw SQL throughout the service, every service function must be rewritten. The repository provides a stable interface ("give me the URL with this code") regardless of the storage backend.

## Q5. Why should configuration be centralized?

If DATABASE_URL is hardcoded in multiple files, changing it requires finding every occurrence. Missing one causes subtle bugs. Centralized config (core/config.py) means one change propagates everywhere. It also separates configuration from code, allowing environment-specific values (dev vs production) without modifying code.

## Q6. How does this architecture improve testing?

Each layer can be mocked independently. To test the service layer, inject a mock repository that returns test data — no real database needed. To test the repository, use a test database — no service needed. Each layer is small enough to test in isolation. Without layering, all tests require a running database and HTTP server.

---

# SECTION 7 — LEETCODE #560: SUBARRAY SUM EQUALS K

## Problem

Given array `nums` and integer `k`, return the total number of **continuous subarrays** whose sum equals exactly `k`.

```
nums = [1,1,1],  k = 2  →  Output: 2
nums = [1,2,3],  k = 3  →  Output: 2
```

---

## What Is a Subarray?

```
Subarray = CONTINUOUS portion of the array.
Subset   = Any elements (can skip).

nums = [1, 2, 3]

Valid subarrays:
  [1], [2], [3], [1,2], [2,3], [1,2,3]

Invalid subarray:
  [1,3]  ← skips element 2. This is a subset, NOT a subarray.
```

---

## The Problem Asks for COUNT, Not Existence

```
Not: "Does any subarray sum to k?"
Not: "Find ONE subarray summing to k."
Yes: "Count ALL subarrays summing to k."

For nums = [1,2,3], k = 3:
  [1,2] → sum = 3  ✅
  [3]   → sum = 3  ✅
  Answer: 2
```

---

## Approach 1 — Brute Force O(n²)

```python
class Solution(object):
    def subarraySum(self, nums, k):
        count = 0
        for start in range(len(nums)):
            current_sum = 0
            for i in range(start, len(nums)):
                current_sum += nums[i]
                if current_sum == k:
                    count += 1
        return count
```

**How it works:**

```
Pick every possible start index.
From that start, expand towards the right.
Keep a running sum.
Every time running_sum == k → count it.

For nums = [1,1,1], k = 2:

Start = 0:
  current_sum = 0
  Add 1 → 1  (not equal)
  Add 1 → 2  ✅ count = 1
  Add 1 → 3  (not equal)

Start = 1:
  current_sum = 0
  Add 1 → 1  (not equal)
  Add 1 → 2  ✅ count = 2

Start = 2:
  current_sum = 0
  Add 1 → 1  (not equal)

Answer: 2 ✅
```

**Why it's too slow:**

```
n = 20,000 (constraint maximum)
Outer loop: 20,000 iterations
Inner loop: up to 20,000 iterations per outer iteration

20,000 × 20,000 = 400,000,000 operations

Python cannot execute 400 million operations within the time limit.
Algorithm is CORRECT but too SLOW.
```

---

## The Key Insight: Prefix Sum

Connect to what you already learned:

```
Day 43: Basics
Day 44: Pydantic
...

LeetCode journey:
  #1480 Running Sum  → learned: accumulate running total
  #303  Range Sum    → learned: prefix[right] - prefix[left-1] = range sum
  #560  This problem → extends: need = prefix_sum - k
```

**The mathematical observation:**

```
If prefix_sum(0, i) = current cumulative sum
And prefix_sum(0, j) = some earlier cumulative sum

Then:
  subarray sum from j+1 to i
  = prefix_sum(0, i) - prefix_sum(0, j)

We want:
  prefix_sum(0, i) - prefix_sum(0, j) = k

Rearranging:
  prefix_sum(0, j) = prefix_sum(0, i) - k

In code:
  need = prefix_sum - k
  "Have I seen this value as a prefix sum before?"
```

**Example:**

```
nums = [1, 2, 3], k = 3

Prefix sums: 1, 3, 6

At index 2 (prefix_sum = 6):
  need = 6 - 3 = 3
  Have I seen prefix_sum = 3 before? YES (at index 1)
  → Subarray from index 2 to 2 = [3] sums to 3 ✅

At index 1 (prefix_sum = 3):
  need = 3 - 3 = 0
  Have I seen prefix_sum = 0 before? YES (the HashMap starts with {0:1})
  → Subarray from index 0 to 1 = [1,2] sums to 3 ✅

Total: 2
```

---

## Approach 2 — Prefix Sum + HashMap O(n) ✅ Submitted

```python
class Solution(object):
    def subarraySum(self, nums, k):
        prefix_sum = 0
        count = 0
        HashMap = {0: 1}     # ← CRITICAL: initialize with {0: 1}

        for i in range(len(nums)):
            prefix_sum += nums[i]        # Step 1: update running prefix sum
            need = prefix_sum - k        # Step 2: what prefix sum do we need?

            if need in HashMap:          # Step 3: have we seen it before?
                count += HashMap[need]   # Step 4: add its frequency to count

            HashMap[prefix_sum] = HashMap.get(prefix_sum, 0) + 1  # Step 5: store current

        return count
```

---

## The Three Critical Questions (And Answers)

### Why `HashMap = {0: 1}` (Not Empty)?

```
nums = [2], k = 2

prefix_sum = 2
need = 2 - 2 = 0
Is 0 in HashMap? 

Without {0:1}: No → count stays 0 → Answer: 0 (WRONG!)
With {0:1}:    Yes → count += 1   → Answer: 1 (CORRECT!)

Explanation:
  {0:1} represents: "Before we started, the prefix sum was 0.
                     This 'virtual starting point' allows subarrays
                     that start at index 0 to be counted."

Without {0:1}: every subarray starting at index 0 is missed.
```

### Why Store `prefix_sum`, Not `nums[i]`?

```
We never ask: "Have we seen this NUMBER before?"
We ask:       "Have we seen this PREFIX SUM before?"

nums = [1,1,1], k = 2

At index 2:
  prefix_sum = 3
  need = 3 - 2 = 1
  "Have we seen prefix_sum = 1?"  → YES (at index 0)

If we stored nums[i] instead:
  "Have we seen number = 1?"  → YES (at index 0)
  But this would match for wrong reasons.
  Number 1 at index 0 doesn't mean a subarray ends there that sums to k.

Always store PREFIX SUMS in the HashMap. Never the raw numbers.
```

### Why Store FREQUENCY (Not True/False)?

```
nums = [0,0,0], k = 0

All prefix sums are 0, 0, 0, 0 (starting with the initial 0)
HashMap after all elements: {0: 4}

At index 2 (prefix_sum = 0):
  need = 0 - 0 = 0
  HashMap[0] = 3 (three previous prefix sums of 0 existed)
  count += 3

If we stored True/False:
  HashMap[0] = True → count += 1 only
  We'd miss subarrays [0], [0,0] → count would be wrong

Frequency (how many times we've seen this prefix sum)
tells us how many VALID SUBARRAYS end at the current index.
```

---

## Complete Dry Run — nums = [1,1,1], k = 2

```
Initial state:
  prefix_sum = 0
  count = 0
  HashMap = {0: 1}

─────────────────────────────────────
Index 0: nums[0] = 1
  prefix_sum = 0 + 1 = 1
  need = 1 - 2 = -1
  -1 in HashMap? NO
  Store prefix_sum: HashMap = {0:1, 1:1}

─────────────────────────────────────
Index 1: nums[1] = 1
  prefix_sum = 1 + 1 = 2
  need = 2 - 2 = 0
  0 in HashMap? YES, frequency = 1
  count += 1 → count = 1
  Store prefix_sum: HashMap = {0:1, 1:1, 2:1}

─────────────────────────────────────
Index 2: nums[2] = 1
  prefix_sum = 2 + 1 = 3
  need = 3 - 2 = 1
  1 in HashMap? YES, frequency = 1
  count += 1 → count = 2
  Store prefix_sum: HashMap = {0:1, 1:1, 2:1, 3:1}

─────────────────────────────────────
Return count = 2 ✅
```

---

## Dry Run With Duplicates — nums = [0,0,0], k = 0

```
Initial state:
  HashMap = {0: 1}

Index 0: nums[0] = 0
  prefix_sum = 0
  need = 0 - 0 = 0
  0 in HashMap? YES, frequency = 1
  count = 1
  HashMap[0] = 1 + 1 = 2 → {0: 2}

Index 1: nums[1] = 0
  prefix_sum = 0
  need = 0
  0 in HashMap? YES, frequency = 2
  count = 3
  HashMap[0] = 2 + 1 = 3 → {0: 3}

Index 2: nums[2] = 0
  prefix_sum = 0
  need = 0
  0 in HashMap? YES, frequency = 3
  count = 6
  HashMap[0] = 3 + 1 = 4 → {0: 4}

Return count = 6 ✅

Why 6? All subarrays of [0,0,0] sum to 0:
[0], [0], [0], [0,0], [0,0], [0,0,0] = 6 subarrays
```

---

## Common Mistakes

```
Mistake 1: Missing initialization
  HashMap = {}  ← WRONG
  HashMap = {0:1}  ← CORRECT
  Without {0:1}: subarrays starting at index 0 are never counted.

Mistake 2: Storing nums[i] instead of prefix_sum
  HashMap[nums[i]] = ...  ← WRONG
  HashMap[prefix_sum] = ...  ← CORRECT
  We look for PREFIX SUMS, not individual numbers.

Mistake 3: Always adding 1 to count
  count += 1  ← WRONG (only correct if all prefix sums are unique)
  count += HashMap[need]  ← CORRECT
  Need can appear multiple times. Each appearance = one valid subarray.

Mistake 4: Overwriting frequency
  HashMap[prefix_sum] = 1  ← WRONG (erases previous occurrences)
  HashMap[prefix_sum] = HashMap.get(prefix_sum, 0) + 1  ← CORRECT
  HashMap.get(prefix_sum, 0): "get current value, or 0 if not present, then add 1"
```

---

## The Complete Pattern (Memorize This)

```
Prefix Sum + HashMap Pattern:

Problem type: "Count subarrays whose sum equals k"

Algorithm:
  Initialize: prefix_sum = 0, count = 0, HashMap = {0: 1}
  
  For each element:
    prefix_sum += nums[i]           → update running sum
    need = prefix_sum - k           → what earlier prefix sum would work?
    if need in HashMap:
        count += HashMap[need]      → add all times we've seen that prefix sum
    HashMap[prefix_sum] += 1       → record this prefix sum

  Return count

Why it works:
  If prefix_sum(i) - prefix_sum(j) = k
  Then subarray from j+1 to i sums to k
  We look for prefix_sum(j) = prefix_sum(i) - k using HashMap in O(1)

Complexity:
  Time:  O(n) — one pass through the array
  Space: O(n) — HashMap stores up to n prefix sums
```

---

## Complexity Comparison

```
Approach         Time    Space   Notes
──────────────────────────────────────────
Brute Force      O(n²)   O(1)   Correct but TLE on n=20,000
Prefix + HashMap O(n)    O(n)   Optimal for interviews
```

**Result:** ✅ Accepted | 93/93 test cases | Runtime: 43ms

---

## Interview Questions for This Problem

```
Q: What is the difference between a subarray and a subset?
A: A subarray must be continuous (no skipping). A subset can skip elements.

Q: Why does the brute force solution get Time Limit Exceeded?
A: O(n²) with n=20,000 → 400 million operations. Too slow for Python.

Q: Why do we initialize HashMap = {0: 1}?
A: Without it, subarrays starting from index 0 are never counted.
   The {0:1} represents the "virtual" prefix sum before processing begins.

Q: Why do we store prefix_sum in the HashMap, not nums[i]?
A: We search for a previous PREFIX SUM, not a previous NUMBER.
   The formula: subarray_sum = current_prefix - previous_prefix

Q: Why do we store frequency, not True/False?
A: The same prefix sum can appear multiple times.
   Each occurrence represents one valid subarray.
   Storing frequency counts all valid subarrays correctly.

Q: What is the relationship between #303 and #560?
A: Both use Prefix Sum.
   #303: find the sum between two indices using prefix[right] - prefix[left-1]
   #560: count subarrays summing to k using need = prefix - k, stored in HashMap.
```

---

# SECTION 8 — THE WEEK 7 MENTAL MODEL

## FastAPI Layered Diagram (Complete)

```
HTTP Request
      │
      ▼
Uvicorn (ASGI server)
      │
      ▼
CORS Middleware (checks Origin header)
      │
      ▼
Custom Middleware (logging, timing)
      │
      ▼
FastAPI Router (URL pattern matching)
      │
      ▼
Dependencies (Depends(get_db), Depends(get_current_user))
      │
      ▼
Pydantic Validation (request body, path/query params)
      │
      ├── FAILS → 422 Unprocessable Entity
      │
      ▼ (PASSES)
Endpoint Function
      │
      ▼
CRUD / Service Logic
      │
      ▼
SQLAlchemy ORM
      │
      ▼
psycopg2 driver
      │
      ▼
PostgreSQL
      │
      ▼ (result travels back up)
Pydantic Response Model (filters output, removes password etc.)
      │
      ▼
Custom Exception Handler (if exception was raised)
      │
      ▼
Middleware (logs response, calculates duration)
      │
      ▼
HTTP Response → Client
```

**This diagram represents everything learned in Week 7. Every layer has a clear role. No layer does another's job.**

---

# SECTION 9 — IMPORTANT THINGS TO KNOW

```
 1. Architecture is designed before code is written.
    The right structure prevents months of messy refactoring later.

 2. Layered Architecture: Router → Service → Repository → Database.
    One direction. No skipping. No reversing.

 3. Router handles HTTP only. No SQL. No business rules.

 4. Service handles business rules only. No SQL. No HTTP status codes.

 5. Repository handles database only. No business rules. No HTTP.

 6. Models (SQLAlchemy) and Schemas (Pydantic) serve different purposes.
    Separating them allows each to change independently.

 7. core/config.py centralizes all configuration.
    Never hardcode DATABASE_URL or domain in multiple files.

 8. secrets.choice() for short code generation — cryptographically secure.
    random.choice() is predictable — not suitable for public codes.

 9. 307 Temporary Redirect: browser asks server every visit → click counting works.
    301 Permanent Redirect: browser caches → click counting is impossible.

10. Prefix Sum + HashMap is one of the most important array interview patterns.
    Appears in #560, #209, #523, #1248, and dozens of other problems.

11. HashMap = {0:1} initialization is required for prefix sum problems.
    Without it: subarrays starting at index 0 are never counted.

12. Store PREFIX SUMS in the HashMap, not array elements.
    The formula: subarray_sum = current_prefix - previous_prefix.

13. Store FREQUENCY (how many times seen), not boolean.
    The same prefix sum can appear multiple times.
    Each occurrence represents one valid subarray.

14. count += HashMap[need] not count += 1.
    One prefix sum frequency can account for many valid subarrays.

15. Complexity: O(n²) brute → O(n) with Prefix Sum + HashMap.
    This improvement is standard for all "count subarrays" interview problems.
```

---

# REVISION SHEET

```
═══════════════════════════════════════════════════════════
DAY 49 — WEEK 7 FINAL REVISION
═══════════════════════════════════════════════════════════

WEEK 7 SUMMARY:
  Day 43: FastAPI setup, path/query params, Swagger
  Day 44: Pydantic models, validation, response filtering
  Day 45: PostgreSQL + SQLAlchemy, full CRUD, Depends(get_db)
  Day 46: JWT auth, bcrypt, OAuth2PasswordBearer, protected routes
  Day 47: HTTPException, custom exceptions, CORS, middleware, logging
  Day 48: URL Shortener planning, schema design, 307 vs 301
  Day 49: Architecture deep dive, LeetCode #560

URL SHORTENER ARCHITECTURE:
  Client → Router → Service → Repository → PostgreSQL
  One direction only. Never backwards. Never skip.

  Router:     HTTP only (request/response, status codes)
  Service:    Business logic (generate code, handle collision)
  Repository: Database only (SELECT, INSERT, UPDATE)
  Utils:      Small helpers (code generator)
  Config:     All settings in one place

FOLDER STRUCTURE:
  app/routers/, app/services/, app/repositories/
  app/models/, app/schemas/, app/database/, app/core/, app/utils/
  tests/, requirements.txt, .env, README.md

LEET CODE #560 PATTERN:
  Initialize: HashMap = {0:1}, prefix_sum = 0, count = 0
  For each num:
    prefix_sum += num
    need = prefix_sum - k
    if need in HashMap: count += HashMap[need]
    HashMap[prefix_sum] = HashMap.get(prefix_sum, 0) + 1
  Return count

THREE CRITICAL QUESTIONS:
  Why {0:1}?       → Count subarrays starting at index 0
  Why prefix_sum?  → We look for prefix sums, not raw numbers
  Why frequency?   → Same prefix sum = multiple valid subarrays

COMPLEXITY:
  Brute: O(n²) time, O(1) space → TLE on n=20,000
  Optimal: O(n) time, O(n) space → Accepted
```

---

## LeetCode Solved This Day

| Problem | Difficulty | Topic | Status | Runtime |
|---------|-----------|-------|--------|---------|
| #560 Subarray Sum Equals K | Medium | Prefix Sum + HashMap | ✅ Accepted 93/93 | 43ms |

---

*Day 49 Complete. Week 7 finished. URL Shortener architecture fully designed. Prefix Sum + HashMap pattern mastered. Week 8 starts with implementation.* ✅
