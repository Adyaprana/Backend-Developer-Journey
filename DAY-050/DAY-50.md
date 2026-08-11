# DAY 50 — Project 1: URL Shortener — Database Design, API Contracts + LeetCode Prefix Sum % k

> **Phase:** 02 — FastAPI Backend (Days 43–90)
>
> **Week:** W8 — Project 1 Build (Days 50–56)
>
> **Project:** URL Shortener API v1.0 — Engineering-First Design Session
>
> **LeetCode:** #523 Continuous Subarray Sum ✅ (58ms · Accepted 103/103)
>
> **Status:** ✅ Day 50 Complete — Database schema fully engineered, API contracts defined, short code strategy chosen, ready to implement

---

# 🎯 What Day 50 Is About

```
URL Shortener API — Engineering First

  ✅ Ask the right question before designing the database
  ✅ Column-by-column schema design with reasoning
  ✅ Constraints: when and why (NOT NULL, UNIQUE, DEFAULT)
  ✅ Indexes: why short_code must be indexed
  ✅ API Contracts: define before coding
  ✅ Short code generation strategies compared
  ✅ LeetCode #523 Continuous Subarray Sum (Prefix Sum % k + HashMap)

  Build day — no tutorials. Think like an engineer.
```

---

# SECTION 1 — WHAT IS A DATABASE?

## The Beginner Answer vs The Engineer Answer

Most beginners answer: **"A database stores data."**

That isn't wrong. But engineers think differently.

```
Engineer's definition:
  A database stores the STATE of the application.

What is the state of our URL Shortener?
  "Which short code belongs to which original URL?"
  "How many times was each short URL clicked?"
  "When was each URL created?"

Everything else (responses, redirects, statistics) is derived from that state.
```

**Why this distinction matters:**

When you think of a database as "just storage," you make columns and tables that don't map to real needs. When you think of it as "the source of truth for application state," every column you add must answer: *"Does the application's state include this?"*

---

# SECTION 2 — WHAT INFORMATION DO WE ACTUALLY NEED?

## Think Before You Create Columns

Imagine a user submits: `https://www.google.com`

Before creating a table, ask: **"What do we need to remember forever?"**

```
Original URL?
  → Yes. Without it we cannot redirect. Core state.

Short Code?
  → Yes. Without it we cannot find the URL later. Core state.

ID?
  → This is actually an interesting question.
  → Could we use short_code as the primary key?
  → Technically yes. Many systems do.
  → Should we? (Answer in Section 3)

Click Count?
  → Yes. Without it /stats becomes impossible.
  → This IS part of the application state.
  → State changes every time someone visits the short URL.

Created At?
  → Yes. Useful for: analytics, sorting by newest, future expiration, auditing.
  → Clients don't send it — the server sets it automatically.

Password? Username? Category? Tags?
  → No. Version 1 has no authentication, no organization.
  → These belong in Version 2 or later.
  → Adding them now = unnecessary complexity.
```

**Version 1 Database Requirements:**

```
Five pieces of information and no more:
  id
  original_url
  short_code
  clicks
  created_at
```

---

# SECTION 3 — COLUMN-BY-COLUMN DESIGN

## Column 1: id

**The Question: Should we even have an ID?**

There are two common approaches:

```
Option A — Auto-Increment Integer ID
  Example: 1, 2, 3, 4, 5
  Advantages:
    → Fast for database operations (small, well-indexed)
    → Easy foreign key joins (if we add users table later)
    → Industry standard for most applications
    → Internal identifier — never exposed to users
  Disadvantages:
    → Users never see it (but that's fine — it's internal)

Option B — Use short_code as Primary Key
  Example: "aB92Kx" as primary key
  Advantages:
    → One fewer column
    → Simpler schema
  Disadvantages:
    → Changing short codes later is painful (cascades through all FKs)
    → Foreign key columns become larger (string vs integer)
    → Indexes are larger (strings are larger than integers)
    → Primary keys should be stable identifiers, not user-facing codes
```

**Engineering Decision: Use `id` as the internal primary key.**

```
Internal identifiers should stay internal.
Even if someday we change the short code algorithm (Base62 instead of random),
the database structure remains stable.
External users see the short code.
Internal systems use the id.
This is how production systems like Bitly, TinyURL, and most
large-scale URL shorteners are designed.
```

---

## Column 2: original_url

**The Question: What data type — VARCHAR, TEXT, or CHAR?**

```
CHAR(n):
  Fixed-length. Pads with spaces to fill n characters.
  "google.com" stored in CHAR(20) → "google.com          "
  Good for: fixed-format codes like postal codes, phone numbers.
  Bad for: URLs (variable length).
  Decision: Never for URLs.

VARCHAR(n):
  Variable length up to n characters.
  Efficient — stores only actual characters.
  Common mistake: VARCHAR(255)
  Problem: Many real URLs exceed 255 characters.
  Amazon product URL: 400+ characters
  Google search URL with parameters: 500+ characters
  Decision: Too risky for production.

TEXT:
  No length limit.
  PostgreSQL stores it identically to VARCHAR internally.
  No artificial ceiling.
  Good for: any free-form text of variable length.
  Decision: ✅ Use TEXT for URLs.
```

**Why TEXT over VARCHAR(255)?**

```
If we use VARCHAR(255) and a user tries to shorten this URL:
https://www.amazon.in/Samsung-Galaxy-S24-Ultra-5G-Storage/dp/B0CT5DJ6XZ/
ref=sr_1_1?crid=3J7D8ZD4G2X4U&keywords=samsung+galaxy+s24+ultra+256gb
&qid=1688000000&sprefix=samsung+galaxy%2Caps%2C196&sr=8-1&th=1

Length: 290 characters → rejected with a database error.

This is a real URL. It should work. Our schema shouldn't break it.
TEXT: No length limit. This URL is stored perfectly.
```

---

## Column 3: short_code

**The Star of the Project**

```
Example value: "Xa82Pq"

Requirements:
  → Unique: no two URLs can share a code
  → Indexed: lookups must be fast
  → Never NULL: a shortened URL must always have a code
  → Limited length: 6-10 characters is the standard

Data type: VARCHAR(10)
  Why not TEXT?
    → We WANT to enforce a maximum length here
    → Short codes should be short
    → VARCHAR(10) prevents accidentally storing 500-char codes

Constraints:
  → UNIQUE: database enforces no duplicates
  → NOT NULL: every URL needs a code
  → INDEX: created automatically by the UNIQUE constraint in PostgreSQL
```

---

## Column 4: clicks

**The Analytics Counter**

```
Data type: INTEGER

Reasoning:
  → Clicks are counted in whole numbers. Never 2.7 clicks.
  → INTEGER supports up to 2,147,483,647 values.
  → That's 2 billion clicks per URL. More than enough for Version 1.
  → For a viral URL at massive scale: BIGINT (8 bytes, 9 quintillion)

DEFAULT 0:
  → Every new URL starts with 0 clicks.
  → We never need to specify this in INSERT.
  → PostgreSQL sets it automatically.

Should clicks ever be negative?
  → No. Never. But we don't add a CHECK constraint in Version 1.
  → Future: CHECK (clicks >= 0) as a safety net.
```

---

## Column 5: created_at

**The Timestamp**

```
Data type: TIMESTAMP WITH TIME ZONE (or TIMESTAMPTZ)

Why WITH TIME ZONE?
  → Users exist in different timezones.
  → A timestamp without timezone is ambiguous.
  → "2026-07-10 09:00:00" — is that IST, UTC, or EST?
  → With timezone: "2026-07-10 09:00:00+05:30" — unambiguous.
  → Production APIs always use UTC timestamps.

DEFAULT NOW():
  → PostgreSQL automatically sets this to the current time at INSERT.
  → The client never sends created_at. The server records it.

Simple version: TIMESTAMP (without timezone)
  → Acceptable for Version 1 where all users are in one timezone.
  → We'll use this in our SQLAlchemy model with datetime.utcnow.
```

---

# SECTION 4 — COMPLETE SQL SCHEMA

```sql
-- The complete shortened_urls table
-- This represents all application state for Version 1.

CREATE TABLE shortened_urls (
    id           SERIAL        PRIMARY KEY,
    original_url TEXT          NOT NULL,
    short_code   VARCHAR(10)   UNIQUE NOT NULL,
    clicks       INTEGER       DEFAULT 0,
    created_at   TIMESTAMP     DEFAULT NOW()
);
```

**What PostgreSQL does automatically:**

```
SERIAL → Creates a sequence, generates 1, 2, 3... for every INSERT.
PRIMARY KEY → Creates an index on id. Enforces UNIQUE + NOT NULL.
UNIQUE → Creates an index on short_code. Enforces no duplicates.
DEFAULT 0 → Sets clicks to 0 if not specified.
DEFAULT NOW() → Sets created_at to current timestamp if not specified.
```

---

## SQLAlchemy Model (What We'll Write in Implementation)

```python
# models/url_model.py
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

# SECTION 5 — CONSTRAINTS: DATABASE-LEVEL RULES

## Why Constraints Matter

```
Scenario without constraints:
  Application bug: empty string sent as original_url.
  Without NOT NULL: "" gets saved to database.
  Redirect: GET /aB92Kx → redirect to ""
  Browser: navigates to nothing. Error.

Scenario with constraints:
  Application bug: empty string sent.
  WITH NOT NULL: database rejects it immediately.
  Error is caught at the boundary. Database stays clean.

Constraints are the last line of defense.
Even if your application code has a bug, the database rules stand.
```

## Constraints Applied to shortened_urls

```
PRIMARY KEY on id:
  → Guarantees every row is uniquely identifiable.
  → Automatically: UNIQUE + NOT NULL + INDEX.

NOT NULL on original_url:
  → A shortened URL without an original URL makes no sense.
  → Every row must have a destination.

UNIQUE on short_code:
  → No two rows can have the same short code.
  → Fundamental requirement: one code → one URL.
  → Database enforces this even if application code forgets.

NOT NULL on short_code:
  → Every shortened URL must have a code.
  → A row without a short code is unusable.

DEFAULT 0 on clicks:
  → No need to specify clicks on INSERT.
  → New URLs always start fresh.

DEFAULT NOW() on created_at:
  → No need to pass timestamp from client.
  → Server-side timestamp is more reliable.
```

---

# SECTION 6 — INDEXES: WHY SHORT_CODE MUST BE INDEXED

## The Problem Without an Index

```
Scenario: 10 million rows in shortened_urls.
User requests: GET /aB92Kx

Without index:
  PostgreSQL reads row 1: short_code = "Yz31Pm" → no match
  PostgreSQL reads row 2: short_code = "Qr54Nt" → no match
  PostgreSQL reads row 3: short_code = "mK78Ws" → no match
  ...continues through all 10 million rows...
  PostgreSQL reads row 4,827,392: short_code = "aB92Kx" → MATCH!

  This is called a Sequential Scan.
  Time: proportional to the number of rows.
  With 10M rows and a redirect every 10ms: catastrophically slow.

With index (B-tree):
  PostgreSQL navigates the tree in ~20 steps (log₂ of 10 million).
  Row found immediately.
  Time: nearly constant regardless of table size.
```

## What Creates the Index Automatically?

```
PRIMARY KEY     → creates an index on id automatically.
UNIQUE          → creates an index on short_code automatically.

We get the short_code index for free because of the UNIQUE constraint.
No separate CREATE INDEX needed.

For explicit control:
  CREATE INDEX idx_short_code ON shortened_urls(short_code);
  (Not needed since UNIQUE already creates it, but shows the intent clearly.)
```

---

# SECTION 7 — API CONTRACTS

## Define Before Coding — Always

An API Contract is a precise description of:

```
→ What the client sends
→ What the server returns
→ What happens when things go wrong
```

**Why define contracts before coding?**

```
Without contracts:
  Backend returns {"url": "..."} (uses key "url")
  Frontend expects {"short_url": "..."} (uses key "short_url")
  Frontend breaks. Arguments ensue.
  Hours wasted fixing field names.

With contracts:
  Both agree on {"short_url": "..."} before a single line is written.
  Backend implements it. Frontend implements it. They connect first try.
```

## Contract 1: POST /shorten

```
Method:  POST
URL:     /shorten
Purpose: Accept a long URL and return its shortened version.

Request Body:
{
  "url": "https://www.google.com"
}

Validation rules:
  → url must be present (NOT NULL)
  → url must be a valid URL format (Pydantic's HttpUrl validates this)
  → url length: no artificial limit (TEXT column in DB)

Success Response (201 Created):
{
  "original_url": "https://www.google.com",
  "short_code": "Xa82Pq",
  "short_url": "http://localhost:8000/Xa82Pq"
}

Error Responses:
  422 — url is missing or not a valid URL format (Pydantic auto-validates)
  500 — unexpected server error (should never reach client in production)
```

## Contract 2: GET /{short_code}

```
Method:  GET
URL:     /{short_code}
Purpose: Redirect user to the original URL and record the visit.

Path Parameter:
  short_code: string (e.g., "Xa82Pq")

Success Response:
  HTTP 307 Temporary Redirect
  Location: https://www.google.com
  (No JSON body. Browser follows Location header automatically.)

Error Responses:
  404 — {"detail": "Short URL not found"} if code doesn't exist in DB
```

**Important: This is NOT a normal JSON endpoint.**

```
Normal endpoint returns data.
Redirect endpoint returns navigation.

The client never sees JSON. The browser simply navigates.
In FastAPI: return RedirectResponse(url=original_url, status_code=307)
```

## Contract 3: GET /stats/{short_code}

```
Method:  GET
URL:     /stats/{short_code}
Purpose: Return analytics for a specific short URL.

Path Parameter:
  short_code: string (e.g., "Xa82Pq")

Success Response (200 OK):
{
  "original_url": "https://www.google.com",
  "short_code": "Xa82Pq",
  "clicks": 15,
  "created_at": "2026-07-23T11:45:00Z"
}

Error Responses:
  404 — {"detail": "Short URL not found"} if code doesn't exist in DB
```

---

## Route Ordering — The Critical Detail

```
/stats/{short_code} and /{short_code} could conflict.

GET /stats/abc → is this the stats for code "abc"?
              → or is this a redirect for code "stats" with subpath "abc"?

FastAPI routes: matched TOP TO BOTTOM.

Register:
  @router.get("/stats/{short_code}")   ← FIRST (specific)
  def get_stats(...): ...

  @router.get("/{short_code}")          ← SECOND (generic)
  def redirect(...): ...

GET /stats/abc arrives:
  FastAPI checks /stats/{short_code} → MATCH. Uses get_stats.
  Never reaches /{short_code}.

If reversed:
  GET /stats/abc → /{short_code} matches first with short_code="stats"
  That's wrong. Entire routing broken.

Rule: SPECIFIC routes before GENERIC pattern routes. Always.
```

---

# SECTION 8 — SHORT CODE GENERATION STRATEGIES

## The Biggest Design Decision

Version 1 needs a short code. There are multiple strategies. Each has tradeoffs.

---

## Strategy 1 — Random Characters ✅ Our Choice for Version 1

```python
import secrets
import string

def generate_short_code(length: int = 6) -> str:
    characters = string.ascii_letters + string.digits   # 62 chars: a-z A-Z 0-9
    return ''.join(secrets.choice(characters) for _ in range(length))

# Example outputs: "aB92Kx", "Yz31Pm", "Qr54Nt"
# 62^6 = 56,800,235,584 possible codes (56 billion)
```

```
Pros:
  → Simple to implement
  → No dependencies
  → 56 billion possible codes (plenty for Version 1)
  → Cannot be guessed sequentially (non-predictable)

Cons:
  → Must check database for collision (rare but possible)
  → Need retry logic if collision occurs
  → Collision probability grows as DB fills up

Why secrets.choice() and NOT random.choice()?
  random.choice: pseudo-random. Predictable if seed is known.
  secrets.choice: OS-level cryptographic randomness. Unpredictable.
  Short codes are shared publicly — make them non-guessable.
```

## Strategy 2 — Base62 Encoding

```python
BASE62 = string.digits + string.ascii_letters  # "0123456789abcdefghijklm..."

def to_base62(number: int) -> str:
    if number == 0:
        return BASE62[0]
    result = []
    while number:
        number, remainder = divmod(number, 62)
        result.append(BASE62[remainder])
    return ''.join(reversed(result))

# ID 1 → "1"
# ID 62 → "Z0"
# ID 125 → "cb"
# ID 1000000 → "4c92"
```

```
How it works:
  Take the database ID (auto-increment integer).
  Convert that integer to Base62 string.
  The short code IS the Base62 encoding of the ID.

Pros:
  → Zero collision risk (each ID is unique, each encoding is unique)
  → Short codes are shorter for small IDs
  → No database lookup needed before insertion
  → Deterministic: same ID always → same code

Cons:
  → Sequential: IDs 1,2,3 → codes "1","2","3" (guessable)
  → Attackers can enumerate all URLs
  → To unsort: shuffle the alphabet or add a salt
  → Slightly more complex implementation
```

## Strategy 3 — UUID-Based

```python
import uuid

def generate_code() -> str:
    return str(uuid.uuid4()).replace("-", "")[:8]
    # "3b9ac9ff"
```

```
Pros:
  → Extremely unlikely to collide (128-bit randomness)
  → No database lookup needed

Cons:
  → 8 characters minimum for reasonable uniqueness
  → Less elegant for a URL shortener (codes look random hash-like)
  → Hexadecimal only (0-9, a-f) — fewer characters used
```

## Strategy 4 — Hash of the Original URL

```python
import hashlib

def generate_code(original_url: str) -> str:
    hash_value = hashlib.md5(original_url.encode()).hexdigest()
    return hash_value[:6]
```

```
Pros:
  → Deterministic: same URL always gets same code
  → Could detect duplicate URLs before INSERT

Cons:
  → Hash collision: different URLs might get same code
  → URL "google.com" and "GOOGLE.COM" might collide
  → Handling collisions adds complexity
  → Not random — predictable from the URL
```

## Strategy Comparison

```
Strategy          Collision Risk   Predictable   Implementation
────────────────────────────────────────────────────────────────
Random (v1)       Rare but possible  No           Simple + retry
Base62            Zero               Yes (by ID)  Medium
UUID              Extremely rare     No           Simple
Hash              Possible           Yes (by URL) Complex
```

**Version 1 Choice: Random Characters.**

Simple, good enough, fast to build, non-predictable. Collision retry logic is a few lines of code. The probability is negligible at our scale.

---

# SECTION 9 — COMPLETE DESIGN SUMMARY

## The shortened_urls Table (Final Version)

```
Column       Type          Constraint            Purpose
──────────────────────────────────────────────────────────────────
id           SERIAL        PRIMARY KEY           Internal unique identifier
original_url TEXT          NOT NULL              The destination URL
short_code   VARCHAR(10)   UNIQUE, NOT NULL      The code users share
clicks       INTEGER       DEFAULT 0             Total redirect count
created_at   TIMESTAMP     DEFAULT NOW()         When the URL was created
```

## The Three Endpoints (Final Contracts)

```
POST /shorten
  Input:   {"url": "https://..."}
  Output:  {"original_url": "...", "short_code": "abc", "short_url": "http://localhost:8000/abc"}
  Status:  201 Created

GET /stats/{short_code}        ← REGISTERED FIRST (specific)
  Input:   short_code in path
  Output:  {"original_url": "...", "short_code": "...", "clicks": 15, "created_at": "..."}
  Status:  200 OK (or 404)

GET /{short_code}              ← REGISTERED SECOND (generic)
  Input:   short_code in path
  Output:  HTTP 307 Redirect → Location: original_url
  Status:  307 (or 404)
```

---

# SECTION 10 — INTERVIEW QUESTIONS

## Q1. Why use an internal id if short_code is already unique?

Internal and external identifiers serve different purposes. The id is the stable database identifier — used for internal foreign keys and database operations. The short_code is the external identifier — what users see and share. If the short code format ever changes (from random to Base62, for example), the database structure remains unchanged. Separating concerns: internal identity vs external address.

## Q2. Why use TEXT instead of VARCHAR(255) for URLs?

Many real URLs exceed 255 characters. Amazon product URLs, Google searches with query parameters, and social media redirects commonly reach 400–800 characters. Using VARCHAR(255) would silently reject valid URLs. TEXT imposes no artificial limit. In PostgreSQL, TEXT and VARCHAR have identical storage performance — the only difference is the length constraint.

## Q3. What is a database constraint and why does it matter?

A constraint is a rule enforced at the database level, independent of application code. NOT NULL ensures required fields always have values. UNIQUE ensures no duplicates. DEFAULT sets automatic values. Constraints are the last line of defense — even if application code has a bug, the database rules hold. "Defense in depth" — multiple layers of validation (Pydantic, then PostgreSQL constraints).

## Q4. Why must short_code be indexed?

Without an index, every GET /{short_code} request requires a full table scan — reading every row to find a match. With 10 million rows and millions of daily redirects, this is catastrophically slow. The UNIQUE constraint on short_code automatically creates a B-tree index in PostgreSQL. With the index, lookups are O(log n) — about 20 comparisons for 10 million rows.

## Q5. What is an API contract and why define it before coding?

An API contract is a precise definition of what a client sends and what the server returns, agreed upon before implementation. Without contracts, backends and frontends often use different field names or structures, causing integration failures. With contracts, both sides implement against the same specification and connect correctly on first try. Contracts also document expected error responses.

## Q6. Why use HTTP 307 instead of 301 for redirects?

HTTP 301 (Permanent) is cached by browsers — subsequent visits bypass the server, making click counting impossible and preventing URL changes. HTTP 307 (Temporary) is not cached — every visit reaches the server, allowing click increment, validation, and future redirect changes. For any URL shortener with analytics, 307 is the only correct choice.

## Q7. What are the tradeoffs between random codes and Base62 encoding?

Random codes are simple to implement, non-predictable (harder to enumerate), but require collision checking and retry logic. Base62 encodes the auto-increment ID, guaranteeing zero collisions and shorter codes for early entries, but is sequential (codes 1,2,3 → "1","2","3"), allowing users to enumerate all shortened URLs. Version 1 uses random codes for simplicity and non-predictability.

## Q8. Why register /stats/{short_code} BEFORE /{short_code}?

FastAPI matches routes top-to-bottom. If /{short_code} is registered first, a request to /stats/abc would match /{short_code} with short_code="stats", which is wrong. Registering the more specific /stats/{short_code} first ensures it matches before the generic /{short_code} pattern catches everything. Specific routes must always be declared before generic pattern routes.

---

# SECTION 11 — LEETCODE #523: CONTINUOUS SUBARRAY SUM

## Problem

Given array `nums` and integer `k`, return `True` if there exists a **continuous subarray of size at least 2** whose elements sum to a **multiple of k**.

```
nums = [23,2,4,6,7], k = 6  →  True   ([2,4] sums to 6)
nums = [23,2,6,4,7], k = 6  →  True   (entire array sums to 42 = 7×6)
nums = [23,2,6,4,7], k = 13 →  False
```

**Key constraint:** Length ≥ 2 (single elements don't count).

---

## Understanding "Multiple of k"

```
x is a multiple of k if x % k == 0.

6  % 6 = 0  ✅
12 % 6 = 0  ✅
18 % 6 = 0  ✅
5  % 6 = 5  ❌
```

---

## Connection to the Prefix Sum Journey

```
Day 37  #1480 Running Sum of 1d Array   → Accumulate running total
Day 37  #303  Range Sum Query           → prefix[right] - prefix[left-1]
Day 49  #560  Subarray Sum Equals K    → prefix + HashMap, count all
Day 50  #523  Continuous Subarray Sum  → prefix % k + HashMap, find one

Each builds on the previous. The same core idea — richer application each time.
```

---

## Approach 1 — Brute Force O(n²)

```python
class Solution(object):
    def checkSubarraySum(self, nums, k):
        for start in range(len(nums)):
            current_sum = 0

            for end in range(start, len(nums)):
                current_sum += nums[end]

                if end - start + 1 >= 2 and current_sum % k == 0:
                    return True

        return False
```

**Dry run on [23,2,4,6,7], k=6:**

```
Start=0: 23, 25, 29(29%6≠0), 35(35%6≠0), 42(42%6=0 but length=5, ✅ but let's continue)
Start=1: 2, 6(6%6=0, length=2) → True ✅
```

**Why it's too slow:**

```
n = 100,000
Nested loops: 100,000 × 100,000 = 10,000,000,000 operations
Python: ~10 million ops/second
Time: ~1,000 seconds. Time limit exceeded.
```

---

## The Core Mathematical Observation

This is the foundation of the entire efficient solution:

```
If two Prefix Sums have the same remainder when divided by k,
then their difference is divisible by k.

Proof:
  prefix_A = 29,  29 % 6 = 5
  prefix_B = 11,  11 % 6 = 5

  Both have remainder 5.
  29 - 11 = 18
  18 % 6 = 0 ✅

Why?
  29 = q₁ × 6 + 5
  11 = q₂ × 6 + 5
  29 - 11 = (q₁ - q₂) × 6 + 5 - 5 = (q₁ - q₂) × 6

  The difference is exactly a multiple of 6.
```

**Consequence for our problem:**

```
If prefix_sum at index i and prefix_sum at index j have the same remainder mod k,
then the subarray from index j+1 to i has sum divisible by k.

We just need to find ANY two indices with the same remainder.
```

---

## Approach 2 — Prefix Sum % k + HashMap O(n) ✅ Submitted

```python
class Solution(object):
    def checkSubarraySum(self, nums, k):
        Running_Prefix = 0
        HashMap = {0: -1}     # ← CRITICAL: remainder 0 seen "before index 0"

        for i in range(len(nums)):
            Running_Prefix += nums[i]
            remainder = Running_Prefix % k

            if remainder in HashMap:
                diff = i - HashMap[remainder]   # distance between indices
                if diff >= 2:                   # subarray length at least 2
                    return True
            else:
                HashMap[remainder] = i          # store FIRST occurrence only

        return False
```

---

## Four Critical Design Questions

### Why `HashMap = {0: -1}` (Not Empty)?

```
nums = [6, 6], k = 6

Index 0: Running_Prefix = 6, remainder = 0
  Is 0 in HashMap?

Without {0:-1}: No → skip → store HashMap = {0: 0}
Index 1: Running_Prefix = 12, remainder = 0
  Is 0 in HashMap? Yes, at index 0
  diff = 1 - 0 = 1
  1 >= 2? NO → miss valid answer!

With {0:-1}: At index 0, remainder = 0 in HashMap at -1
  diff = 0 - (-1) = 1 ← still wrong here

Wait, let me re-trace with {0:-1}:
Index 0: Running_Prefix = 6, remainder = 0
  Is 0 in HashMap? Yes (at -1)
  diff = 0 - (-1) = 1 → 1 >= 2? No → don't overwrite (already exists)
Index 1: Running_Prefix = 12, remainder = 0
  Is 0 in HashMap? Yes (at -1)
  diff = 1 - (-1) = 2 → 2 >= 2? YES → return True ✅

Without {0:-1}:
  No early entry of 0 → at index 0, store {0:0}
  At index 1: diff = 1 - 0 = 1 → MISS!

{0:-1} represents: "Before any element was processed, the prefix sum was 0."
It anchors subarrays that begin at index 0.
```

### Why Store REMAINDERS, Not Prefix Sums?

```
We don't care about the exact prefix sum value.
We care whether two prefix sums share the same remainder.
Storing remainders directly:
  → Smaller HashMap (at most k unique keys, not n)
  → O(min(n,k)) space instead of O(n)
  → Directly captures what we're searching for
```

### Why Store the FIRST Index (Not Latest)?

```
The condition is: diff = current_index - stored_index >= 2

If a remainder appears multiple times:
  Index 0: remainder = 5 → store {5: 0}
  Index 2: remainder = 5 → diff = 2-0 = 2 → Valid! Return True.
  Index 3: remainder = 5 → (if we hadn't returned) diff = 3-0 = 3 → also valid

Storing the EARLIEST occurrence gives the LARGEST possible diff.
Storing the latest would shrink diff and might miss the length-2 requirement.
Storing the earliest maximizes our chance of satisfying diff >= 2.

Rule: Only store if NOT already in HashMap (else: block ensures this).
```

### Why `diff >= 2` (Not `diff >= 1`)?

```
diff = current_index - stored_index

The subarray elements are from stored_index+1 to current_index.
Number of elements = current_index - stored_index = diff.

diff = 1: only one element → invalid (need at least 2)
diff = 2: two elements → valid ✅
diff = 3: three elements → valid ✅

So we check diff >= 2.
```

---

## Complete Dry Run — [23, 2, 4, 6, 7], k = 6

```
Initial: Running_Prefix = 0, HashMap = {0: -1}

Index 0: nums[0] = 23
  Running_Prefix = 23
  remainder = 23 % 6 = 5
  5 in HashMap? NO
  Store: HashMap = {0:-1, 5:0}

Index 1: nums[1] = 2
  Running_Prefix = 25
  remainder = 25 % 6 = 1
  1 in HashMap? NO
  Store: HashMap = {0:-1, 5:0, 1:1}

Index 2: nums[2] = 4
  Running_Prefix = 29
  remainder = 29 % 6 = 5
  5 in HashMap? YES (at index 0)
  diff = 2 - 0 = 2
  2 >= 2? YES → return True ✅

Subarray identified: elements at indices 1 to 2 = [2, 4]
Sum = 6, which is 6 % 6 = 0. ✅
```

---

## Dry Run 2 — nums = [23,2,6,4,7], k = 6

```
Index 0: Running_Prefix=23, rem=5, store {0:-1, 5:0}
Index 1: Running_Prefix=25, rem=1, store {0:-1, 5:0, 1:1}
Index 2: Running_Prefix=31, rem=1, in HashMap at 1
  diff = 2-1 = 1 → 1 >= 2? NO → continue (don't overwrite)
Index 3: Running_Prefix=35, rem=5, in HashMap at 0
  diff = 3-0 = 3 → 3 >= 2? YES → return True ✅

Subarray: indices 1 to 3 = [2, 6, 4], sum = 12 = 2×6 ✅
```

---

## Common Mistakes

```
Mistake 1: Missing {0:-1}
  HashMap = {}  ← WRONG
  HashMap = {0:-1}  ← CORRECT
  Subarrays starting at index 0 are never detected otherwise.

Mistake 2: Overwriting first occurrence
  HashMap[remainder] = i  (unconditionally)  ← WRONG
  Only store if NOT already present:
  else: HashMap[remainder] = i  ← CORRECT

Mistake 3: Storing prefix sums instead of remainders
  HashMap[Running_Prefix] = i  ← WRONG (for this problem)
  HashMap[Running_Prefix % k] = i  ← CORRECT

Mistake 4: Using count += 1 (from #560 habit)
  #523 only asks True/False, not count.
  First valid finding → return True immediately.

Mistake 5: Forgetting diff >= 2 check
  diff >= 1 allows single-element subarrays → WRONG
  diff >= 2 ensures at least 2 elements → CORRECT
```

---

## #560 vs #523 — Side-by-Side Comparison

```
Feature                 #560 Subarray = k        #523 Subarray % k = 0
───────────────────────────────────────────────────────────────────────
Store in HashMap        Prefix sum               Prefix sum % k (remainder)
HashMap value           Frequency (count)        First index seen
Initial HashMap         {0: 1}                   {0: -1}
Action on match         count += HashMap[need]   if diff >= 2: return True
Overwrite?              Always update (+=1)       Never overwrite first index
Return                  Total count              True/False
What we search for      prefix - k               same remainder as before
Extra constraint        None                     Subarray length >= 2
```

---

## Complexity

```
Time:   O(n) — single pass, O(1) HashMap operations
Space:  O(min(n, k)) — HashMap stores at most k unique remainders
        (there are only k possible remainders: 0, 1, 2, ..., k-1)
```

**Result:** ✅ Accepted | 103/103 test cases | Runtime: 58ms

---

# SECTION 12 — IMPORTANT THINGS TO KNOW

```
 1. A database stores the STATE of the application.
    Design columns around what state you need to preserve.

 2. TEXT over VARCHAR(255) for URLs.
    Many real URLs exceed 255 characters. Never reject valid data.

 3. Use id as internal primary key.
    Short codes can change. Internal IDs should be stable.

 4. UNIQUE constraint on short_code creates an index automatically in PostgreSQL.
    No separate CREATE INDEX needed.

 5. Constraints are the last defense against bad data.
    NOT NULL, UNIQUE, DEFAULT — enforce these at the database level.

 6. API contracts must be defined before coding.
    Field name mismatches between frontend and backend waste hours.

 7. Register /stats/{short_code} BEFORE /{short_code}.
    FastAPI routes match top-to-bottom. Specific before generic.

 8. 307 Temporary Redirect for URL shortener.
    Never 301 — click counting is impossible with browser caching.

 9. secrets.choice() for short code generation.
    random.choice() is predictable. Use cryptographic randomness.

10. Random codes need collision detection and retry.
    Probability is very low but must be handled.

11. Base62 encoding: no collision, but sequential (guessable).
    Good for systems that don't care about enumeration.

12. For #523: store remainder (% k), not prefix sum.
    Mathematical basis: equal remainders → divisible difference.

13. HashMap = {0: -1} for #523 (index-based).
    HashMap = {0: 1} for #560 (frequency-based).
    Both initialize with "before the array" concept. Details differ.

14. Never overwrite first occurrence of remainder in #523.
    Using else: ensures only first index is stored.

15. diff >= 2 checks subarray length at least 2.
    diff = current_index - stored_index = number of elements in subarray.
```

---

# REVISION SHEET

```
═══════════════════════════════════════════════════════════
DAY 50 — URL SHORTENER + #523 REVISION
═══════════════════════════════════════════════════════════

DATABASE TABLE:
  shortened_urls:
    id           SERIAL        PRIMARY KEY
    original_url TEXT          NOT NULL
    short_code   VARCHAR(10)   UNIQUE NOT NULL
    clicks       INTEGER       DEFAULT 0
    created_at   TIMESTAMP     DEFAULT NOW()

COLUMN CHOICES:
  TEXT (not VARCHAR(255)) for URLs
  SERIAL for id (not using short_code as PK)
  DEFAULT 0 for clicks
  UNIQUE creates index automatically

THREE ENDPOINTS (order matters!):
  POST /shorten → create + return (201)
  GET /stats/{short_code} → analytics (200/404)  ← FIRST
  GET /{short_code} → 307 redirect (307/404)     ← SECOND

SHORT CODE STRATEGIES:
  Random: Simple, non-predictable, needs collision retry
  Base62: No collision, sequential (guessable by ID)
  Version 1: Random characters, 6 chars, secrets.choice()

LEETCODE #523 PATTERN:
  Running_Prefix = 0
  HashMap = {0: -1}   ← remainder → first index

  For i, num in enumerate(nums):
    Running_Prefix += num
    remainder = Running_Prefix % k
    if remainder in HashMap:
      if i - HashMap[remainder] >= 2: return True
    else:
      HashMap[remainder] = i   ← store FIRST time only
  return False

KEY DIFFERENCES #560 vs #523:
  #560: {0:1} frequency, always update, return count
  #523: {0:-1} first index, never overwrite, return True/False

COMPLEXITY #523:
  Time: O(n). Space: O(min(n,k)).
```

---

## LeetCode Solved This Day

| Problem | Difficulty | Topic | Status | Runtime |
|---------|-----------|-------|--------|---------|
| #523 Continuous Subarray Sum | Medium | Prefix Sum % k + HashMap | ✅ Accepted 103/103 | 58ms |

---

*Day 50 Complete. URL Shortener schema finalized. API contracts defined. Short code strategy chosen. LeetCode Prefix Sum + Modulo pattern mastered. Implementation starts next day.* ✅
