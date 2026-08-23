# DAY 55 — URL Shortener: Service Layer, Business Logic, Collision Safety + LeetCode Kadane's Algorithm

> **Phase:** 02 — FastAPI Backend (Days 43–90)
>
> **Week:** W8 — Project 1 Build (Days 50–56)
>
> **Project:** URL Shortener API v1.0 — Service Layer Complete
>
> **LeetCode:** #53 Maximum Subarray ✅ (44ms · Beats 86.10%) — Kadane's Algorithm
>
> **Status:** ✅ Day 55 Complete — URLService written with collision-safe short code generation, get_by_short_code added to Repository, architecture is now Router → Service → Repository → Database

---

# 🎯 What Day 55 Is About

```
URL Shortener — Service Layer (Business Logic)

  ✅ Why short code generation belongs in the Service (not Router, not Repository)
  ✅ Short code strategy: 62 characters, length 6, 56.8 billion combinations
  ✅ random.choice vs secrets.choice — when it matters
  ✅ The hidden collision bug — found BEFORE testing
  ✅ Two-layer protection: Application check + Database UNIQUE constraint
  ✅ Race conditions — why database constraint alone is not enough (and vice versa)
  ✅ URLRepository.get_by_short_code() — added to support collision checking
  ✅ while True loop — why it's correct here
  ✅ CODE_LENGTH constant — no magic numbers
  ✅ LeetCode #53 — Maximum Subarray (Brute Force → Kadane's O(n))
```

**Today's milestone:** The application now has a real brain. The Service layer generates a short code, checks uniqueness against the database, and delegates saving to the Repository. Business logic is properly isolated.

---

# SECTION 1 — THE FUNDAMENTAL QUESTION OF DAY 55

## Where Should Short Code Generation Live?

This is not a technical question. It is an architectural decision.

```
Three options:
  Option A → Router
  Option B → Repository
  Option C → Service

Answer: Service
```

---

## Why NOT the Router?

```python
# BAD — short code generation in the Router
@router.post("/shorten", response_model=URLResponse, status_code=201)
def shorten_url(url: URLCreate, db: Session = Depends(get_db)):
    short_code = "".join(random.choices(string.ascii_letters, k=6))
    db_url = ShortenedURL(original_url=str(url.original_url), short_code=short_code)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url
```

**Problems with this approach:**

```
The Router now does THREE things:
  1. Handles HTTP (its actual job)
  2. Generates short codes (business logic)
  3. Saves to database (data layer)

Consequences:
  → Want to add a CLI command that shortens URLs? Must duplicate code generation.
  → Want to change code length from 6 to 8? Must find and edit every router that creates URLs.
  → Want to test the generation logic? Must mock HTTP requests + database.
  → When something breaks: is it HTTP handling or code generation or database?

Three responsibilities = three reasons to break = three sets of bugs.
```

---

## Why NOT the Repository?

```python
# BAD — short code generation in the Repository
class URLRepository:
    def create(self, db: Session, original_url: str) -> ShortenedURL:
        short_code = "".join(random.choices(string.ascii_letters, k=6))
        db_url = ShortenedURL(original_url=original_url, short_code=short_code)
        db.add(db_url)
        db.commit()
        return db_url
```

**Problems with this approach:**

```
The Repository now mixes database operations with business rules.

Consequences:
  → Tomorrow: "Use Base58 instead of alphanumeric" → Edit the Repository.
  → Tomorrow: "Make code length configurable" → Edit the Repository.
  → Tomorrow: "Add premium users get 8-char codes" → Repository gets if/else for business rules.
  → Repository grows into a bloated class that does everything.

Single Responsibility: Repository should only answer:
  "Save this." / "Find this." / "Update this." / "Delete this."
```

---

## WHY the Service?

```
The Service is the BRAIN of the application.

It answers: "What should happen?"
  → Generate a code.
  → Check if it's unique.
  → Retry if not.
  → Create the model object.
  → Ask the Repository to save it.
  → Return the result.

It does NOT know:
  → HTTP methods or status codes (that's Router)
  → SQL syntax or session management (that's Repository)

"Where should short code generation live?"
→ In the layer that knows business rules.
→ That's the Service.
```

---

## The Business Rule That Belongs Here

```
"A short code must be 6 characters from [a-z A-Z 0-9] and must be unique."

This is a business rule. Not a database rule. Not an HTTP rule.

If the rule changes:
  "We now need 8 characters for premium users."
  → Edit URLService only.
  → Router unchanged.
  → Repository unchanged.
  → Database unchanged.
  → Tests for Router unchanged.

This is exactly what makes clean architecture maintainable.
```

---

# SECTION 2 — SHORT CODE DESIGN DECISIONS

## Character Set

```
Option A: lowercase only    → 26 characters → 26^6 = 308 million combinations
Option B: uppercase only    → 26 characters → 26^6 = 308 million combinations
Option C: digits only       → 10 characters → 10^6 = 1 million combinations
Option D: ALL of the above  → 62 characters → 62^6 = 56.8 BILLION combinations

Decision: Option D

In Python:
  import string
  string.ascii_letters → "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
  string.digits        → "0123456789"
  combined             → 62 characters total

Python gives us this string for free. No need to type all 62 characters.
```

## Code Length

```
Decision: 6 characters

Reasons:
  → Easy to type
  → Easy to share verbally ("the code is aB3xP7")
  → 62^6 = 56,800,235,584 ≈ 56.8 billion combinations
  → More than enough for Version 1

Comparison to real services:
  Bitly:   7 characters
  TinyURL: 8 characters
  Twitter t.co: 10 characters

6 is fine for development and early production.
If we ever need more: change CODE_LENGTH = 6 to CODE_LENGTH = 8.
One constant. One change.
```

---

# SECTION 3 — THE COLLISION BUG (FOUND BEFORE TESTING)

## What Is a Collision?

```
Scenario:
  User A shortens: https://google.com → code: "aB92Kx"
  User B shortens: https://github.com → random generates: "aB92Kx" again

Now the database has:
  original_url     | short_code
  ─────────────────────────────
  https://google.com | aB92Kx
  https://github.com | aB92Kx  ← COLLISION!

Someone visits: ourdomain.com/aB92Kx
Which URL should they see? Google? GitHub?
Impossible to answer. The data is corrupted.
```

## What Happens Without Collision Handling?

```
Our database has: unique=True on short_code

If we try to insert a duplicate:
  PostgreSQL: "ERROR: duplicate key value violates unique constraint"
  SQLAlchemy: sqlalchemy.exc.IntegrityError
  FastAPI: 500 Internal Server Error

The client sees:
  HTTP 500 Internal Server Error

No useful error message. Application crashed.
This is the bug: we didn't handle the case where random generation produces a duplicate.
```

## Why We Found It BEFORE Testing

```
This is called a Design Review — examining the code flow before running it.

The moment you see:
  short_code = generate_random_code()
  db.insert(short_code)

You ask: "What if that code already exists?"
If there's no check: you found a bug.

Finding bugs at design review time: free.
Finding bugs in production: expensive.

Design reviews are one of the most valuable skills in software engineering.
```

---

# SECTION 4 — THE TWO-LAYER PROTECTION STRATEGY

## Layer 1: Application-Level Check (Service)

```python
while True:
    short_code = self.generate_short_code()
    existing = self.repository.get_by_short_code(db, short_code)
    if existing is None:
        break  # found a unique code
# Save with confidence
```

```
This check:
  → Prevents 99.99% of duplicate attempts
  → Provides good user experience (no crash, just retry)
  → Keeps the Service in control of business logic
  → Is fast (collision probability is ~0 at low volume)
```

## Layer 2: Database-Level UNIQUE Constraint

```sql
short_code VARCHAR(10) UNIQUE NOT NULL
```

```
This constraint:
  → Guarantees correctness even if Layer 1 fails
  → Protects against race conditions (two simultaneous requests)
  → Cannot be bypassed by application bugs
  → Is enforced by PostgreSQL regardless of who writes the data
```

## The Race Condition (Why You Need Both)

```
Scenario: Two requests arrive at the same millisecond.

Request A: generates "aB92Kx"
Request B: generates "aB92Kx"

Request A: checks database → "aB92Kx" doesn't exist ✅
Request B: checks database → "aB92Kx" doesn't exist ✅

(Both checks complete before either insert happens)

Request A: inserts "aB92Kx" → SUCCESS
Request B: inserts "aB92Kx" → UNIQUE CONSTRAINT VIOLATION (Layer 2 saves us)

Without Layer 2: Both inserts succeed → corrupted data.
With Layer 2:    Second insert fails → one operation gets an error → handle gracefully.

Layer 1 (application check) prevents race conditions from happening often.
Layer 2 (database constraint) guarantees they can never corrupt data.
Both are required.
```

---

## The Username Analogy

```
When you sign up for Instagram:
  You type: "john123"
  Instagram checks: "Is this username taken?"
  If yes: Shows "Username already exists. Try another."
  If no: Proceeds to registration.

But even after that check:
  The database has: UNIQUE constraint on username.

Why both?
  Application check → good user experience (shows a friendly message)
  Database constraint → prevents two simultaneous registrations from taking the same name

Our URL shortener uses the same strategy:
  Application check → retry loop (generate another code)
  Database constraint → final safety net
```

---

# SECTION 5 — THE UPDATED URL REPOSITORY

## get_by_short_code() — New Method Added

```python
# app/repositories/url_repository.py (Updated)

from typing import Optional
from sqlalchemy.orm import Session

from app.models.shortened_url import ShortenedURL


class URLRepository:
    """
    Handles all database operations for shortened URLs.
    """

    def create(self, db: Session, url: ShortenedURL) -> ShortenedURL:
        """
        Save a new shortened URL to the database.
        """
        db.add(url)
        db.commit()
        db.refresh(url)
        return url

    def get_by_short_code(
        self,
        db: Session,
        short_code: str
    ) -> Optional[ShortenedURL]:
        """
        Find a shortened URL by its short code.

        Returns:
            ShortenedURL if found.
            None if the code doesn't exist in the database.
        """
        return (
            db.query(ShortenedURL)
            .filter(ShortenedURL.short_code == short_code)
            .first()
        )
```

---

## get_by_short_code() Explained

### Import: `from typing import Optional`

```python
from typing import Optional

# Optional[ShortenedURL] means the function can return:
#   → A ShortenedURL object (if found)
#   → None (if not found)

# This is the Python type hint for "might be None".
# Without Optional: caller doesn't know if None is possible.
# With Optional: clear documentation: "check if result is None before using it."
```

### The Query

```python
return (
    db.query(ShortenedURL)           # SELECT * FROM shortened_urls
    .filter(ShortenedURL.short_code == short_code)  # WHERE short_code = 'aB92Kx'
    .first()                         # LIMIT 1 → return one or None
)
```

```
db.query(ShortenedURL):
  Tells SQLAlchemy: "I'm working with the shortened_urls table."

.filter(ShortenedURL.short_code == short_code):
  Generates: WHERE short_code = 'aB92Kx'
  Note: SQLAlchemy uses Python's == operator for SQL equality.
  This is NOT comparing Python objects.
  SQLAlchemy intercepts == and generates SQL WHERE clause.

.first():
  → Returns the first matching row as a ShortenedURL object.
  → Returns None if no row matches.
  → Adds LIMIT 1 to the SQL (efficient — stops after finding one).

Why .first() and not .one_or_none()?
  .first()          → returns None if not found (we use this)
  .one_or_none()    → returns None if not found, raises if multiple found
  .one()            → raises if not found OR if multiple found

.first() is appropriate here:
  short_code is UNIQUE, so at most one row will match.
  If not found: None.
  If found: that one row.
```

### Repository's Responsibility

```
Repository answers exactly ONE question: "Does this code exist?"

It returns:
  ShortenedURL object → "Yes, this code exists. Here's the data."
  None               → "No, this code doesn't exist."

Repository does NOT decide:
  → "What do I do if it exists?" (that's Service's job)
  → "Generate another code" (that's Service's job)

It only reports the database state.
Single Responsibility Principle in action.
```

---

# SECTION 6 — THE SERVICE (THE COMPLETE FILE)

## app/services/url_service.py

```python
import random
import string

from sqlalchemy.orm import Session

from app.models.shortened_url import ShortenedURL
from app.repositories.url_repository import URLRepository


class URLService:
    """
    Handles business logic for URL shortening.

    Responsibilities:
      - Generate unique short codes
      - Ensure uniqueness via database check
      - Create ShortenedURL model objects
      - Delegate persistence to URLRepository

    Does NOT know about:
      - FastAPI or HTTP
      - SQL syntax or session management
      - Pydantic schemas or request validation
    """

    CODE_LENGTH = 6

    def __init__(self):
        self.repository = URLRepository()

    def generate_short_code(self) -> str:
        """
        Generate a random 6-character short code.

        Character set: a-z, A-Z, 0-9 (62 characters)
        Possible combinations: 62^6 ≈ 56.8 billion
        """
        characters = string.ascii_letters + string.digits

        return "".join(
            random.choice(characters)
            for _ in range(self.CODE_LENGTH)
        )

    def create_short_url(
        self,
        db: Session,
        original_url: str
    ) -> ShortenedURL:
        """
        Create and save a shortened URL with a guaranteed unique short code.

        Flow:
          1. Generate a random short code
          2. Check if it already exists in the database
          3. Repeat until a unique code is found
          4. Create ShortenedURL model object
          5. Delegate to Repository to save
          6. Return the saved object with database-generated values
        """
        while True:
            short_code = self.generate_short_code()

            existing_url = self.repository.get_by_short_code(
                db,
                short_code
            )

            if existing_url is None:
                break

        url = ShortenedURL(
            original_url=original_url,
            short_code=short_code
        )

        return self.repository.create(db, url)
```

---

## Every Design Decision Explained

### `import random` vs `secrets`

```python
import random

# We use random.choice() for generating short codes.
# The URL shortener's short codes are PUBLIC — they appear in shared links.
# They don't need to be cryptographically unpredictable.
# They just need to be:
#   1. Random enough to avoid collisions
#   2. Not sequential (so users can't guess other codes easily)

# For Version 1: random.choice() is acceptable.

# When to use secrets instead:
#   Generating authentication tokens → secrets (must be cryptographically unpredictable)
#   Generating password reset links → secrets (must be unpredictable)
#   Generating API keys → secrets (security-critical)
#   Generating short codes → random is fine (not security-critical)

# Future enhancement: switch to secrets.choice() for added security.
# In the submitted solution from the file: random.choice() was used.
# Both work. secrets is more secure for sensitive operations.
```

### `CODE_LENGTH = 6` — The "No Magic Numbers" Principle

```python
CODE_LENGTH = 6

# This is a CLASS CONSTANT — a value that belongs to the class,
# shared by all instances, never changes during runtime.

# Why not just write:
#   for _ in range(6)
#   "6" is called a "magic number"

# Problems with magic numbers:
#   → What does 6 mean? Length? Number of tries? Retries?
#   → If the requirement changes to 8: grep all files for "6"
#   → Easy to miss one occurrence → inconsistent behavior

# With CODE_LENGTH:
#   → self.generate_short_code() uses self.CODE_LENGTH
#   → If length changes: one line update
#   → Every usage automatically gets the new value
#   → self.CODE_LENGTH is self-documenting: "the length of short codes"

# Class constant vs instance variable:
#   CODE_LENGTH = 6       → class-level (shared by all URLService instances)
#   self.code_length = 6  → instance-level (each instance has its own copy)

# A constant that applies to all URL shortening operations:
# use a class constant. Simpler and clearer.
```

### `def __init__(self): self.repository = URLRepository()`

```python
def __init__(self):
    self.repository = URLRepository()

# Creates a URLRepository instance when URLService is created.
# The Service OWNS a Repository instance.
# This is called COMPOSITION: Service HAS a Repository.

# Benefits:
#   → self.repository.create(...) is clean — no new URLRepository() every call
#   → Future: inject a mock repository for testing

# Alternative (more testable):
#   def __init__(self, repository: URLRepository = None):
#       self.repository = repository or URLRepository()
# This allows injecting a mock: URLService(MockRepository())

# Version 1: simple instantiation.
# Future: dependency injection for testability.
```

### `generate_short_code()` — The Code Generator

```python
def generate_short_code(self) -> str:
    characters = string.ascii_letters + string.digits
    return "".join(
        random.choice(characters)
        for _ in range(self.CODE_LENGTH)
    )
```

**Step by step:**

```python
characters = string.ascii_letters + string.digits
# string.ascii_letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
# string.digits        = "0123456789"
# combined             = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
# Length: 62 characters
# Python provides these constants — no need to type all 62.

random.choice(characters)
# Picks ONE random character from the 62.
# Example: 'a', 'B', '3', 'X', 'p', '7'

for _ in range(self.CODE_LENGTH)
# Repeats 6 times (CODE_LENGTH = 6).
# The underscore _ means: "I don't need the loop variable."
# It's a Python convention for "unused loop variable."

"".join(...)
# Combines the 6 characters into a single string.
# Example: ['a','B','3','X','p','7'] → "aB3Xp7"

# The entire expression is a generator expression:
# (random.choice(characters) for _ in range(6))
# It generates 6 characters lazily, then join() collects them.
```

### `create_short_url()` — The Business Method

```python
def create_short_url(
    self,
    db: Session,
    original_url: str
) -> ShortenedURL:
```

**Why `original_url: str` and not `url: URLCreate`?**

```
The Service receives a plain str, not a Pydantic model.

Why?
  Pydantic's URLCreate belongs to the API/HTTP layer.
  The Service should not depend on FastAPI concepts.
  If we add a CLI tool later: CLI doesn't use Pydantic.
  Service still works because it only needs the URL string.

The conversion happens in the Router:
  url_data: URLCreate  → str(url_data.original_url) → Service

Service receives: plain Python string.
Service does NOT know where that string came from.
This is Loose Coupling.
```

### The `while True` Loop — Why It's Correct Here

```python
while True:
    short_code = self.generate_short_code()
    existing_url = self.repository.get_by_short_code(db, short_code)
    if existing_url is None:
        break
```

**Common reaction:** "While True looks dangerous — what if it never exits?"

**The reality:**

```
With 62 characters and length 6:
  62^6 = 56,800,235,584 possible codes (56.8 billion)

If the database has 1 million URLs:
  Collision probability per attempt = 1,000,000 / 56,800,235,584 ≈ 0.0000176%

With 100 million URLs:
  Collision probability per attempt ≈ 0.176%

The while True loop:
  In practice: exits after 1 iteration (essentially always)
  Worst case in production: maybe 2 iterations

Actual danger: essentially zero.
The loop terminates when a unique code is found.
Since 56.8 billion codes exist and the database will never fill that many,
a unique code is always available.

The while True pattern is standard for "retry until success" scenarios.
It's correct here.
```

**When would while True be dangerous?**

```
If the condition NEVER becomes True:
  → Infinite loop → server hangs → out of memory → crash

Here the condition WILL become True because:
  → Database can't have 56.8 billion entries (disk would overflow first)
  → A unique code is always available
  → Loop WILL terminate

Future protection (optional):
  max_attempts = 10
  for attempt in range(max_attempts):
      code = generate()
      if not exists(code): break
  else:
      raise RuntimeError("Could not generate unique code after 10 attempts")

For Version 1: simple while True is appropriate.
```

### After the Loop: Create and Save

```python
url = ShortenedURL(
    original_url=original_url,
    short_code=short_code
)

return self.repository.create(db, url)
```

```
url = ShortenedURL(original_url=..., short_code=...):
  Creates a SQLAlchemy model object.
  NOT saved to database yet.
  Just a Python object in memory.

Notice what we DON'T specify:
  id          → PostgreSQL SERIAL generates this
  clicks      → default=0 in the model
  created_at  → lambda: datetime.now(UTC) in the model

self.repository.create(db, url):
  Delegates to Repository:
    db.add(url)      → stage
    db.commit()      → save
    db.refresh(url)  → sync (get id, created_at from PostgreSQL)
  Returns the saved url with all values populated.

return: returns the ShortenedURL object to whoever called create_short_url().
```

---

# SECTION 7 — WHY EACH LAYER RECEIVES WHAT IT RECEIVES

## The Complete Type Flow

```
Client sends:           {"original_url": "https://google.com"}
Pydantic parses:        URLCreate(original_url=HttpUrl("https://google.com"))
Router receives:        url: URLCreate
Router passes to Service: str(url.original_url) = "https://google.com"
Service receives:       original_url: str
Service creates:        ShortenedURL(original_url="...", short_code="aB92Kx")
Service passes to Repository: url: ShortenedURL
Repository saves:       db.add(url) → PostgreSQL row
Repository returns:     ShortenedURL(id=1, original_url="...", short_code="aB92Kx", clicks=0, ...)
Service returns:        ShortenedURL object to Router
Router applies:         response_model=URLResponse (filter through Pydantic)
Client receives:        {"id": 1, "original_url": "...", "short_code": "aB92Kx", "short_url": "..."}
```

**Each layer speaks the language of its domain:**

```
HTTP layer (Router):   Pydantic schemas (URLCreate, URLResponse)
Business layer (Service): Plain Python types (str, ShortenedURL model)
Data layer (Repository):  SQLAlchemy models (ShortenedURL)
Database layer:           SQL rows
```

---

# SECTION 8 — PROJECT STRUCTURE (AFTER DAY 55)

```
url-shortener/
│
├── app/
│   ├── database/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   └── database.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   └── shortened_url.py
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── url.py
│   │
│   ├── repositories/
│   │   ├── __init__.py
│   │   └── url_repository.py    ← Updated: get_by_short_code() added
│   │
│   └── services/
│       ├── __init__.py
│       └── url_service.py       ← ✅ NEW today
│
├── main.py
├── .env
├── .gitignore
└── requirements.txt
```

**What's still missing:**

```
routers/url_router.py  ← POST /shorten, GET /{code}, GET /stats/{code}
(Day 56 — connecting everything through FastAPI endpoints)
```

---

# SECTION 9 — ARCHITECTURE REVIEW

## The Final Architecture (When Complete)

```
Client
  │
  │ POST /shorten {"original_url": "https://google.com"}
  ▼
URLCreate (Pydantic) — validates HttpUrl
  │
  ▼
URL Router
  │ str(url.original_url)
  ▼
URLService.create_short_url(db, original_url)
  │
  ├─ generate_short_code() → "aB92Kx"
  │
  ├─ URLRepository.get_by_short_code(db, "aB92Kx")
  │   → None (unique!) → exit loop
  │
  ├─ ShortenedURL(original_url="...", short_code="aB92Kx")
  │
  └─ URLRepository.create(db, url_object)
       │ db.add() → db.commit() → db.refresh()
       ▼
     PostgreSQL row: id=1, clicks=0, created_at=now()
       │
       ▼
     ShortenedURL(id=1, original_url="...", short_code="aB92Kx", clicks=0, created_at=...)
  │
  ▼
URL Router applies response_model=URLResponse
  │
  ▼
{"id": 1, "original_url": "...", "short_code": "aB92Kx", "short_url": "http://localhost:8000/aB92Kx"}
  │
  ▼
Client receives 201 Created
```

---

# SECTION 10 — INTERVIEW QUESTIONS

## Q1. What is the Service Layer?

The Service Layer contains business logic — the rules that define how the application behaves. In our URL shortener, the Service decides how to generate short codes, how to ensure uniqueness, and when to retry. It coordinates the Repository for data access but makes all business decisions itself. It doesn't know about HTTP or SQL — only the rules of the application.

## Q2. Why is short code generation in the Service and not the Repository?

Generating a short code is a business rule ("codes must be 6 characters, alphanumeric, unique"). Business rules belong in the Service. The Repository's responsibility is only database operations: save, retrieve, update, delete. Putting business logic in the Repository violates Single Responsibility Principle and makes the code harder to test and change.

## Q3. Why do we have both an application-level check AND a database UNIQUE constraint?

The application check (while True loop) handles 99.99% of cases and provides a good user experience (retry silently). But it cannot prevent race conditions — two requests could generate the same code simultaneously and both pass the check before either inserts. The database UNIQUE constraint is the final safety net that guarantees no duplicate can ever be stored, even under concurrent load. Professional systems always have both layers.

## Q4. What is a race condition?

A race condition occurs when two or more operations run concurrently and the outcome depends on the timing of execution. In our URL shortener: two requests could simultaneously generate the same code, both check the database (code doesn't exist), and both attempt to insert. Without the UNIQUE constraint, both would succeed and create corrupted duplicate data. With the constraint, the second insert fails with an integrity error.

## Q5. Why does the Service receive `original_url: str` instead of `url: URLCreate`?

The Service should not depend on Pydantic schemas (FastAPI's HTTP layer concept). If we add a CLI tool, a background job, or a batch import script, they would all call the Service with plain Python strings — not Pydantic objects. The Router converts URLCreate to str before passing to the Service, keeping the Service independent of the HTTP layer.

## Q6. Why use `CODE_LENGTH = 6` instead of the literal `6`?

Magic numbers (`6` written directly in code) make code harder to maintain. If the length needs to change, every occurrence of `6` must be found and updated. With `CODE_LENGTH = 6`, there is one source of truth. Change one constant, everything updates. The name also documents what the number means — "the length of short codes."

## Q7. Why is the `while True` loop safe here?

With 62 characters and length 6, there are 56.8 billion possible codes. The database will never contain close to that many entries. Collision probability is ~0.0000176% when 1 million URLs exist. The loop exits on the first iteration in almost every case. The `while True` pattern is standard for "retry until success" scenarios where the success condition is guaranteed to occur quickly.

---

# SECTION 11 — LEETCODE #53: MAXIMUM SUBARRAY

## Problem

Given integer array `nums`, find the contiguous subarray with the largest sum and return its sum.

```
nums = [-2,1,-3,4,-1,2,1,-5,4]  →  6  (subarray [4,-1,2,1])
nums = [1]                       →  1
nums = [5,4,-1,7,8]             →  23 (entire array)
```

---

## The Critical Word: "Contiguous"

```
Contiguous = elements must stay together. No skipping.

nums = [4, -1, 2, 1]

VALID subarrays:           INVALID "subarrays":
  [4]                        [4, 2]     ← skipped -1
  [4, -1]                    [4, 1]     ← skipped -1, 2
  [4, -1, 2]                 [-1, 1]    ← skipped 2
  [4, -1, 2, 1]

These are "subsets" — they are NOT subarrays.
This problem is asking about contiguous subarrays only.
```

---

## Why Prefix Sum Doesn't Work

```
My first instinct: keep a running sum and track the maximum.

Problem: prefix sum always starts from index 0.
The maximum subarray can start from ANY index.

Example: nums = [5, -10, 20]

Prefix sums:  5 → -5 → 15
Maximum prefix sum: 15

Correct answer: 20 (the subarray [20] starting at index 2)

Prefix sum completely misses subarrays that start after index 0.
Need a different approach.
```

---

## Brute Force — O(n²)

```python
class Solution(object):
    def maxSubArray(self, nums):
        maximum = nums[0]

        for start in range(len(nums)):
            current_sum = 0
            for end in range(start, len(nums)):
                current_sum += nums[end]
                if current_sum > maximum:
                    maximum = current_sum

        return maximum
```

**Why it's too slow:**

```
n = 100,000
Nested loops: 100,000 × 100,000 = 10,000,000,000 operations
TLE (Time Limit Exceeded)

But it works correctly. It checks every possible contiguous subarray.
Need to make it O(n).
```

---

## The Big Insight: When to Start Fresh

```
While extending a subarray, a natural question appears:

"Is it better to CONTINUE the current subarray, or START FRESH?"

Example:
  Current Sum = -5
  Current Number = 20

  Continue: -5 + 20 = 15
  Start Fresh: 20

  → 20 is better. Start fresh!

A negative running sum ONLY hurts future elements.
Carrying -5 forward reduces every future sum by 5.
Dropping it gives us a clean start.

This single observation leads to Kadane's Algorithm.
```

---

## Kadane's Algorithm — O(n) ✅

### The Decision at Every Element

```
For each number:
  CONTINUE: Current_Sum + nums[i]
  OR
  START FRESH: nums[i] alone

Pick whichever is larger.
Track the overall best answer seen so far.
```

### The Code (As Submitted)

```python
class Solution(object):
    def maxSubArray(self, nums):
        Current_Sum = nums[0]    # Start with first element
        ans = nums[0]            # Best answer starts as first element

        for i in range(1, len(nums)):    # Start from index 1 (already handled 0)

            if nums[i] > (Current_Sum + nums[i]):
                Current_Sum = nums[i]        # Start fresh (nums[i] alone is better)
            else:
                Current_Sum += nums[i]       # Continue the current subarray

            if ans < Current_Sum:
                ans = Current_Sum            # Update best if current is better

        return ans
```

### The Condition Explained

```python
if nums[i] > (Current_Sum + nums[i]):
    Current_Sum = nums[i]

# This checks: Is nums[i] alone better than continuing?
#
# Algebraic insight:
#   nums[i] > Current_Sum + nums[i]
#   ← subtract nums[i] from both sides →
#   0 > Current_Sum
#
# So this condition is equivalent to: if Current_Sum < 0: start fresh
#
# A negative current sum will always reduce any future number.
# A positive current sum will always improve any future number.
# The decision: keep if positive, drop if negative.

# Alternative (equivalent, simpler to read):
Current_Sum = max(nums[i], Current_Sum + nums[i])
```

---

## Complete Dry Run — nums = [-2,1,-3,4,-1,2,1,-5,4]

```
Initial: Current_Sum = -2, ans = -2

i=1: nums[1]=1
  Continue: -2 + 1 = -1
  Start Fresh: 1
  1 > -1 → Start Fresh → Current_Sum = 1
  ans = max(-2, 1) = 1

i=2: nums[2]=-3
  Continue: 1 + (-3) = -2
  Start Fresh: -3
  -2 > -3 → Continue → Current_Sum = -2
  ans = max(1, -2) = 1

i=3: nums[3]=4
  Continue: -2 + 4 = 2
  Start Fresh: 4
  4 > 2 → Start Fresh → Current_Sum = 4
  ans = max(1, 4) = 4

i=4: nums[4]=-1
  Continue: 4 + (-1) = 3
  Start Fresh: -1
  3 > -1 → Continue → Current_Sum = 3
  ans = max(4, 3) = 4

i=5: nums[5]=2
  Continue: 3 + 2 = 5
  Start Fresh: 2
  5 > 2 → Continue → Current_Sum = 5
  ans = max(4, 5) = 5

i=6: nums[6]=1
  Continue: 5 + 1 = 6
  Start Fresh: 1
  6 > 1 → Continue → Current_Sum = 6
  ans = max(5, 6) = 6

i=7: nums[7]=-5
  Continue: 6 + (-5) = 1
  Start Fresh: -5
  1 > -5 → Continue → Current_Sum = 1
  ans = max(6, 1) = 6

i=8: nums[8]=4
  Continue: 1 + 4 = 5
  Start Fresh: 4
  5 > 4 → Continue → Current_Sum = 5
  ans = max(6, 5) = 6

Return ans = 6 ✅

Subarray that gave this: [4, -1, 2, 1] (indices 3-6)
```

---

## The Dry Run Table

```
Num  Continue  Fresh   Current_Sum  ans
────────────────────────────────────────
-2   —         —          -2        -2    (initialization)
 1   -1        1           1         1    (fresh)
-3   -2       -3          -2         1    (continue: -2 > -3)
 4    2        4           4         4    (fresh)
-1    3       -1           3         4    (continue: 3 > -1)
 2    5        2           5         5    (continue)
 1    6        1           6         6    (continue)
-5    1       -5           1         6    (continue: 1 > -5)
 4    5        4           5         6    (continue)
```

---

## The Backpack Analogy

```
Your current sum is a BACKPACK.

When the backpack helps (positive sum):
  Keep carrying it. Adding future numbers to positive current = better.
  Current_Sum = 8, next = 2 → 10. Great. Keep going.

When the backpack becomes a burden (negative sum):
  Drop it. Starting fresh is always better.
  Current_Sum = -20, next = 5 → Continue: -15 vs Fresh: 5.
  Obviously 5 > -15. Drop the backpack.

Kadane's Algorithm: drop when burden, carry when helpful.
```

---

## Why `ans = nums[0]` (Not 0)

```python
ans = nums[0]  # ← CORRECT

# If ans = 0:
# nums = [-5, -3, -1]  ← all negative
# Answer should be: -1 (best option when all are negative)
# But with ans = 0: answer would be 0 (wrong — no element equals 0)

# Why?
# "At least one element must be included" (problem constraint)
# The answer can be negative (all elements negative)
# Initializing to 0 breaks the all-negative case

# Starting with ans = nums[0]:
# Even if nums[0] is the worst element, we have a valid baseline.
# Loop then correctly finds the actual maximum.
```

---

## Common Mistakes

```
Mistake 1: ans = 0
  Fails for all-negative arrays.
  Always initialize ans = nums[0].

Mistake 2: Returning Current_Sum instead of ans
  Current_Sum is the running total (changes every iteration).
  ans is the BEST value seen. Always return ans.

Mistake 3: Confusing prefix sum with Kadane's
  Prefix sum starts from index 0 always.
  Kadane can start a new subarray at ANY index.
  They solve different problems.

Mistake 4: Updating ans before the decision
  Always update Current_Sum first, THEN check if Current_Sum > ans.
  The decision (continue or fresh) changes Current_Sum.
  ans should reflect the latest Current_Sum.

Mistake 5: Skipping index 0
  Initializing Current_Sum and ans from nums[0], loop from index 1.
  Starting loop from 0 would process nums[0] twice.
```

---

## Kadane's Pattern Family

```
When you see:
  "Maximum/Minimum contiguous subarray sum"
  "Best subarray ending at each position"
  "Largest gain in a continuous sequence"

Think: Kadane's Algorithm.

Variations:
  #53  Maximum Subarray           → standard Kadane's
  #918 Maximum Sum Circular       → Kadane's + total - min_subarray
  #152 Maximum Product Subarray   → track both max and min (signs flip on negatives)
  2D Maximum Sum Rectangle        → Kadane's applied row by row

The core idea: make a greedy decision at each element.
Continue if helpful. Start fresh if burden.
```

---

## Complexity

```
Brute Force:   O(n²) time, O(1) space  → TLE
Kadane's:      O(n)  time, O(1) space  → Optimal

Why O(1) space?
  Only two variables: Current_Sum, ans
  No arrays. No extra memory. Perfect.
```

**Result:** ✅ Accepted | Runtime: 44ms | Beats 86.10%

---

# SECTION 12 — IMPORTANT THINGS TO KNOW

```
 1. Business logic belongs in the Service. Not the Router. Not the Repository.
    Change a business rule → edit Service only.

 2. Short code generation is a business rule:
    "6 characters, alphanumeric, unique."
    That's the Service's responsibility.

 3. Two-layer protection against collisions:
    Application check (while True loop): prevents most collisions, good UX.
    Database UNIQUE constraint: prevents ALL collisions, even in race conditions.
    Both are required in a production system.

 4. Race condition: two requests pass the application check simultaneously.
    Only the database constraint prevents corrupted data in this case.

 5. Repository answers exactly one question per method:
    get_by_short_code: "Does this code exist? Yes (return object) or No (return None)."
    It doesn't decide what to do next. That's the Service's job.

 6. Optional[ShortenedURL]: return type for get_by_short_code.
    Documents that the function can return None.
    Callers must check: if result is None: ...

 7. CODE_LENGTH = 6: class constant avoids magic numbers.
    Self-documenting. Single point of change.

 8. random.choice() is fine for non-security-critical random codes.
    secrets.choice() for authentication tokens, API keys, password resets.

 9. While True loop is correct when termination is guaranteed.
    With 56.8 billion codes, a unique one always exists.
    Collision probability: ~0.0000176% with 1 million entries.

10. Service receives plain str, not Pydantic URLCreate.
    Service should not depend on FastAPI/Pydantic concepts.
    Router converts URLCreate → str before calling Service.

11. Kadane's Algorithm: make a greedy choice at every element.
    Continue if Current_Sum > 0 (helps future elements).
    Start fresh if Current_Sum < 0 (hurts future elements).

12. Initialize ans = nums[0], not ans = 0.
    All-negative arrays require a negative answer.
    ans = 0 would incorrectly return 0 for all-negative input.

13. Kadane's is O(n) time, O(1) space.
    Brute force is O(n²) time, O(1) space.
    Same space. 1000x faster time.

14. db.query().filter().first() pattern:
    .query(Model) → SELECT * FROM table
    .filter(condition) → WHERE condition
    .first() → LIMIT 1, return one or None

15. Pattern recognition: "maximum/minimum contiguous subarray" → Kadane's.
    Just as "count subarrays equal to k" → prefix sum + HashMap.
```

---

# REVISION SHEET

```
═══════════════════════════════════════════════════════════
DAY 55 — SERVICE LAYER + KADANE'S REVISION
═══════════════════════════════════════════════════════════

ARCHITECTURE:
  Router → Service → Repository → Database
  Service: business logic (generate codes, check uniqueness)
  Repository: database operations (save, query)

SHORT CODE STRATEGY:
  Characters: string.ascii_letters + string.digits (62 chars)
  Length: CODE_LENGTH = 6
  Combinations: 62^6 = 56.8 billion

SERVICE FILE (url_service.py):
  class URLService:
      CODE_LENGTH = 6
      def __init__(self): self.repository = URLRepository()
      def generate_short_code(self) -> str:
          chars = string.ascii_letters + string.digits
          return "".join(random.choice(chars) for _ in range(self.CODE_LENGTH))
      def create_short_url(self, db, original_url) -> ShortenedURL:
          while True:
              code = self.generate_short_code()
              if self.repository.get_by_short_code(db, code) is None: break
          url = ShortenedURL(original_url=original_url, short_code=code)
          return self.repository.create(db, url)

COLLISION PROTECTION:
  App layer: while True loop (check then break)
  DB layer:  UNIQUE constraint (race condition safety net)

REPOSITORY UPDATE:
  def get_by_short_code(self, db, code) -> Optional[ShortenedURL]:
      return db.query(ShortenedURL).filter(ShortenedURL.short_code == code).first()

KADANE'S ALGORITHM:
  Current_Sum = ans = nums[0]
  for i in range(1, len(nums)):
      if nums[i] > Current_Sum + nums[i]:
          Current_Sum = nums[i]    # start fresh
      else:
          Current_Sum += nums[i]  # continue
      if ans < Current_Sum:
          ans = Current_Sum
  return ans
  Time O(n), Space O(1)

KEY RULES:
  ans = nums[0] not 0 (all-negative case)
  Kadane ≠ prefix sum (Kadane can start from any index)
  while True is safe here (56.8B codes available)
```

---

## LeetCode Solved This Day

| Problem | Difficulty | Topic | Status | Runtime |
|---------|-----------|-------|--------|---------|
| #53 Maximum Subarray | Medium | Kadane's Algorithm, Dynamic Programming | ✅ Accepted | 44ms, Beats 86.10% |

---

*Day 55 Complete. Service layer written with collision-safe code generation. Repository updated with get_by_short_code. Business logic is properly isolated. Router layer connects everything tomorrow.* ✅
