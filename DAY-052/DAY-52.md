# DAY 52 — URL Shortener: SQLAlchemy Model, Base, Database Layer Restructure + LeetCode Reader & Writer

> **Phase:** 02 — FastAPI Backend (Days 43–90)
>
> **Week:** W8 — Project 1 Build (Days 50–56)
>
> **Project:** URL Shortener API v1.0 — ORM Model & Architecture Refinement
>
> **LeetCode:** #283 Move Zeroes ✅ (2ms · Beats 93.10%)
>
> **Status:** ✅ Day 52 Complete — ShortenedURL ORM model written, Base extracted, database layer restructured, table created in PostgreSQL

---

# 🎯 What Day 52 Is About

```
Day 52 — Building the Data Layer

  ✅ Why Base deserves its own file (base.py)
  ✅ Restructuring database/ into a proper package
  ✅ ShortenedURL ORM model (full SQLAlchemy 2.0 syntax)
  ✅ Every column designed with real engineering reasoning
  ✅ DateTime with timezone — UTC everywhere
  ✅ lambda for default vs direct function reference
  ✅ Base.metadata.create_all() — tables appear in PostgreSQL
  ✅ Verified in pgAdmin: shortened_urls table exists
  ✅ LeetCode #283 — Move Zeroes (Reader & Writer pattern)
```

**Today's milestone:** The database table physically exists in PostgreSQL. The Python model maps to it perfectly. The data layer is complete and ready for CRUD operations.

---

# SECTION 1 — WHY THIS DAY MATTERS

## What Exists After Day 51

```
url-shortener/
├── main.py        ← GET / endpoint, server runs
├── database.py    ← engine, SessionLocal, get_db()
├── .env           ← DATABASE_URL
├── .gitignore
└── requirements.txt
```

**What's missing:**

```
❌ The shortened_urls table doesn't exist in PostgreSQL yet.
❌ No Python class maps to that table.
❌ No CRUD operations possible without the model.
```

The server runs but the core feature (shorten URLs) cannot work yet.

---

## The Goal of Day 52

```
After Day 52:
  ✅ Base → base.py (declarative base extracted)
  ✅ database/ package → clean separation of concerns
  ✅ ShortenedURL model → Python class = PostgreSQL table
  ✅ Table created in PostgreSQL via create_all()
  ✅ pgAdmin shows shortened_urls with all 5 columns
```

Every future CRUD operation (create URL, increment clicks, read stats) depends on the model being correct.

---

# SECTION 2 — THE RESTRUCTURED DATABASE LAYER

## Why Extract Base to Its Own File?

In Day 45 (and Day 51), we had:

```python
# database.py (Day 51 — everything in one file)
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()   # ← mixed with engine and session config
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
```

**The problem with this structure:**

```
models/shortened_url.py needs to import Base.
database.py needs to be imported to get Base.

database.py imports:
  os, dotenv, sqlalchemy...

When models/shortened_url.py imports from database.py:
  ALL of database.py runs.
  .env is loaded.
  engine is created (connects to PostgreSQL).
  SessionLocal is created.

Problem: Just defining a model causes a database connection!
         In tests, you can't import a model without connecting to the database.
         In CI/CD pipelines, models can't be inspected without credentials.
         Bad coupling.
```

**The clean solution: `base.py`**

```python
# app/database/base.py
# This file does ONE thing: define Base.
# No .env loading. No engine. No session. Just Base.
```

## New Folder Structure

```
url-shortener/
│
├── app/
│   │
│   ├── database/
│   │   ├── __init__.py        ← makes database/ a Python package
│   │   ├── base.py            ← ✅ NEW: just Base
│   │   └── database.py        ← engine, SessionLocal, get_db()
│   │
│   └── models/
│       ├── __init__.py
│       └── shortened_url.py   ← ✅ NEW: ShortenedURL ORM class
│
├── main.py
├── .env
├── .gitignore
└── requirements.txt
```

**Dependency flow:**

```
base.py
  ↓ imported by
models/shortened_url.py  (imports Base from base.py — no engine needed)
  ↓ AND
database.py              (imports Base from base.py for create_all)
  ↓
main.py (imports engine + Base for create_all, imports router)
```

**Key insight:** `base.py` has no dependencies. Everything else depends on it. This is the correct direction.

---

# SECTION 3 — BASE.PY (THE COMPLETE FILE)

## The File

```python
# app/database/base.py

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy models.

    Every model inherits from Base.
    Base.metadata.create_all() uses Base to know which tables to create.
    """
    pass
```

---

## Every Line Explained

### `from sqlalchemy.orm import DeclarativeBase`

```python
from sqlalchemy.orm import DeclarativeBase

# DeclarativeBase is SQLAlchemy 2.0's modern way to create the base class.
# It replaces the older declarative_base() function call.

# SQLAlchemy 1.x (old style — still works but deprecated):
from sqlalchemy.orm import declarative_base
Base = declarative_base()

# SQLAlchemy 2.x (new style — what we use):
from sqlalchemy.orm import DeclarativeBase
class Base(DeclarativeBase):
    pass

# Why the change?
# The class-based approach allows type checking tools (mypy, Pylance)
# to understand the relationships between models better.
# It's more Pythonic — using a class instead of a function call.
# SQLAlchemy 2.0+ is the industry standard as of 2024-2026.
```

### `class Base(DeclarativeBase): pass`

```python
class Base(DeclarativeBase):
    pass

# class Base → We're creating a new class named Base.
# (DeclarativeBase) → It inherits from SQLAlchemy's declarative system.

# What inheriting from DeclarativeBase gives you:
#   1. A metadata object (Base.metadata) that tracks all registered tables.
#   2. A mapping system that connects Python attributes to SQL columns.
#   3. create_all() and drop_all() functionality.

# pass → This class adds nothing beyond what DeclarativeBase provides.
# It's intentionally empty — Base is just the foundation.

# Every model then inherits from Base:
# class ShortenedURL(Base): ...
# class User(Base): ...
# Base.metadata knows about ALL of them.
```

### Why `pass` and Not Just Use DeclarativeBase Directly?

```python
# Why not use DeclarativeBase directly?
# Option A: Direct use (doesn't work this way)
from sqlalchemy.orm import DeclarativeBase
class ShortenedURL(DeclarativeBase):  # ← wrong!
    ...

# Each model can only inherit from ONE declarative base.
# If ShortenedURL inherits from DeclarativeBase directly,
# it becomes its OWN base — separate from User's base.
# create_all() would create ShortenedURL's table, not User's.
# They're isolated. Can't have foreign keys between them.

# Option B: Our approach (correct)
class Base(DeclarativeBase):
    pass

class ShortenedURL(Base):  # ← inherits from shared Base
    ...
class User(Base):          # ← inherits from shared Base
    ...

# Now both share Base.metadata.
# create_all() creates ALL tables at once.
# Foreign keys between tables work.
# This is the correct pattern.
```

---

# SECTION 4 — DATABASE.PY (UPDATED)

## The Updated File

```python
# app/database/database.py

import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL is None:
    raise ValueError("DATABASE_URL is not set in the .env file.")

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def get_db():
    """
    Provide a database session for each request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

**What changed from Day 51:**

```
Day 51: Base was defined here
Day 52: Base moved to base.py

database.py no longer imports or defines Base.
database.py is purely about connection management.
One file, one responsibility.

database.py's responsibility:
  → Read DATABASE_URL from environment
  → Create the engine (connection pool)
  → Create SessionLocal (session factory)
  → Provide get_db() for Dependency Injection
```

---

# SECTION 5 — SHORTENED_URL.PY (THE ORM MODEL)

## The Complete File

```python
# app/models/shortened_url.py

from datetime import datetime, UTC

from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class ShortenedURL(Base):
    __tablename__ = "shortened_urls"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    original_url: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    short_code: Mapped[str] = mapped_column(
        String(10),
        unique=True,
        nullable=False,
        index=True
    )

    clicks: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False
    )
```

---

## Deep Explanation of Every Line

### Imports

```python
from datetime import datetime, UTC
```

```
datetime → the class that represents a date+time moment
UTC      → the UTC timezone object (added in Python 3.11)

Why import UTC?
  "2026-07-25 09:00:00" → Ambiguous. Is this IST? EST? UTC?
  "2026-07-25 09:00:00+00:00" → UTC. Unambiguous.

Professional APIs store all timestamps in UTC.
Clients convert to local time as needed.
If you store in IST and a user is in London, they see wrong times.
UTC is universal. Store in UTC. Display locally.

Alternative (older Python):
  from datetime import timezone
  datetime.now(timezone.utc)

Modern Python 3.11+:
  from datetime import UTC
  datetime.now(UTC)
  → Cleaner. We use this.
```

```python
from sqlalchemy import DateTime, Integer, String, Text
```

```
These are SQLAlchemy's column type objects.
They map to PostgreSQL types:

DateTime  → TIMESTAMP WITH TIME ZONE
Integer   → INTEGER
String(n) → VARCHAR(n)
Text      → TEXT

You don't write SQL types directly.
You use these Python objects → SQLAlchemy generates the SQL.
```

```python
from sqlalchemy.orm import Mapped, mapped_column
```

```
Mapped[T]       → Type hint for a mapped column.
                  Mapped[int] = this column holds integers.
                  Mapped[str] = this column holds strings.
                  Provides IDE autocomplete and type checking.

mapped_column() → Defines the column's database properties.
                  Replaces the old Column() syntax.

Old SQLAlchemy 1.x (still works):
  id = Column(Integer, primary_key=True)

New SQLAlchemy 2.x (what we use):
  id: Mapped[int] = mapped_column(Integer, primary_key=True)

The new syntax is:
  → Type-safe (mypy understands it)
  → More readable (type hint makes intent clear)
  → Industry standard for 2024+ projects
```

```python
from app.database.base import Base
```

```
Import our shared Base class from base.py.
ShortenedURL inherits from this Base.
Base.metadata then knows about the shortened_urls table.
When we call Base.metadata.create_all(engine), this table is created.

Why from app.database.base and not from app.database.database?
  base.py: No side effects. Just defines Base. Safe to import anywhere.
  database.py: Loads .env, creates engine, connects to DB. Heavy. Not safe for models.

The separation prevents models from accidentally triggering database connections.
```

---

### The Class

```python
class ShortenedURL(Base):
    __tablename__ = "shortened_urls"
```

```
class ShortenedURL(Base):
  → Creates a SQLAlchemy ORM model.
  → Inherits from Base (connects it to Base.metadata).
  → Every instance of ShortenedURL = one row in the table.

__tablename__ = "shortened_urls"
  → Required. Tells SQLAlchemy the exact table name in PostgreSQL.
  → Without it: SQLAlchemy raises a configuration error.
  → Convention: plural lowercase snake_case.
    User → users
    ShortenedURL → shortened_urls
    OrderItem → order_items

  What happens when you instantiate:
  url = ShortenedURL(original_url="https://google.com", short_code="aB92Kx")
  → url is a Python object with attributes
  → db.add(url) → SQLAlchemy prepares: INSERT INTO shortened_urls (...)
  → db.commit() → PostgreSQL executes the INSERT
```

---

### Column 1: id

```python
id: Mapped[int] = mapped_column(
    Integer,
    primary_key=True,
    index=True
)
```

```
Mapped[int]
  → Type hint. This column holds Python int values.
  → Pylance gives autocomplete: url.id works correctly.

Integer
  → Maps to PostgreSQL INTEGER type.
  → SQLAlchemy generates: id INTEGER

primary_key=True
  → This column is the Primary Key.
  → Automatically implies: UNIQUE + NOT NULL
  → SQLAlchemy detects Integer primary key → uses SERIAL in PostgreSQL
    (auto-increment: 1, 2, 3, 4...)
  → You never specify id when inserting.
    PostgreSQL generates it automatically.

index=True
  → Creates a B-tree index on this column.
  → Primary keys already get an index from PostgreSQL.
  → This makes the intent explicit for documentation purposes.
  → Redundant but harmless and communicative.

Generated SQL:
  id SERIAL PRIMARY KEY

Why SERIAL and not INTEGER?
  SQLAlchemy detects Integer + primary_key=True
  For PostgreSQL: generates SERIAL (auto-increment sequence)
  For SQLite: generates AUTOINCREMENT
  The ORM handles dialect-specific SQL automatically.
```

---

### Column 2: original_url

```python
original_url: Mapped[str] = mapped_column(
    Text,
    nullable=False
)
```

```
Mapped[str]
  → Python string type for this column.

Text
  → PostgreSQL TEXT type. No length limit.
  → Why not String(255)?
    Amazon URLs exceed 255 chars regularly.
    TEXT is safer — no artificial ceiling.
  → PostgreSQL treats TEXT and VARCHAR identically in performance.
    The ONLY difference is the length constraint.

nullable=False
  → NOT NULL in SQL.
  → Every shortened URL MUST have an original URL.
  → Without it: you could insert a row with no original_url.
    Redirect would fail: "redirect to None"?

Generated SQL:
  original_url TEXT NOT NULL
```

---

### Column 3: short_code

```python
short_code: Mapped[str] = mapped_column(
    String(10),
    unique=True,
    nullable=False,
    index=True
)
```

```
Mapped[str]
  → Python string.

String(10)
  → PostgreSQL VARCHAR(10). Maximum 10 characters.
  → Why VARCHAR (not TEXT) for short codes?
    We WANT the length enforced.
    Short codes should be short.
    VARCHAR(10) prevents accidentally inserting 200-char codes.
    The limit is meaningful here.

unique=True
  → Creates a UNIQUE constraint in PostgreSQL.
  → Automatically creates a B-tree index (free!).
  → No two rows can have the same short_code.
  → Fundamental requirement: one code → one URL.
  → Even if application code has a bug and tries to insert a duplicate,
    PostgreSQL rejects it at the database level.

nullable=False
  → Every shortened URL must have a code.
  → A row without a short_code is useless.

index=True
  → Actually redundant here (unique=True already creates an index).
  → We include it for explicit documentation of intent.
  → "This column will be looked up frequently."

Generated SQL:
  short_code VARCHAR(10) UNIQUE NOT NULL

Why is the index on short_code CRITICAL for performance?
  Every redirect: SELECT * FROM shortened_urls WHERE short_code = 'aB92Kx';
  Without index: full table scan (read every row) → O(n)
  With index: B-tree lookup → O(log n) → ~20 steps for 1M rows
  At scale (millions of redirects/day): 1000x performance difference.
```

---

### Column 4: clicks

```python
clicks: Mapped[int] = mapped_column(
    Integer,
    default=0,
    nullable=False
)
```

```
Mapped[int]
  → Python int. Counts are integers.

Integer
  → PostgreSQL INTEGER. Stores up to 2,147,483,647.
  → 2 billion clicks per URL before overflow.
  → Overkill for most URLs. Appropriate for future scale.

default=0
  → SQLAlchemy-level default.
  → When creating a ShortenedURL without specifying clicks,
    SQLAlchemy sets it to 0 before INSERT.
  → You never write: ShortenedURL(..., clicks=0)
    You write:       ShortenedURL(original_url=..., short_code=...)
    And clicks is automatically 0.

  IMPORTANT: This is a SQLAlchemy-level default, NOT a PostgreSQL DEFAULT.
  PostgreSQL's column definition does NOT have DEFAULT 0.
  SQLAlchemy sets the value in Python before sending the INSERT.

  For a PostgreSQL-level DEFAULT (runs even with raw SQL):
  Use: server_default="0"
  mapped_column(Integer, server_default="0", nullable=False)

nullable=False
  → clicks must always have a value. Not optional.
  → Prevents NULL click counts (which would break SUM operations).

Generated SQL:
  clicks INTEGER NOT NULL
  (SQLAlchemy sets value to 0 in Python, then inserts the 0)
```

---

### Column 5: created_at (Most Complex — Read Carefully)

```python
created_at: Mapped[datetime] = mapped_column(
    DateTime(timezone=True),
    default=lambda: datetime.now(UTC),
    nullable=False
)
```

```
Mapped[datetime]
  → Python datetime object for this column.
  → Pylance understands: url.created_at is a datetime.
```

**`DateTime(timezone=True)` — The Timezone Decision:**

```
DateTime(timezone=False) → TIMESTAMP without time zone
  Stores: "2026-07-25 09:00:00"
  Ambiguous: Is this IST? UTC? EST?
  BAD for APIs used across timezones.

DateTime(timezone=True) → TIMESTAMP WITH TIME ZONE (TIMESTAMPTZ)
  Stores: "2026-07-25 03:30:00+00:00" (UTC)
  Always UTC internally in PostgreSQL.
  Unambiguous globally.
  GOOD for any serious API.

Why does timezone matter in production?
  Your server is in Mumbai (UTC+5:30).
  User opens a short URL from New York (UTC-4).
  Without timezone: "created at 09:00" — 9am in Mumbai? 9am in NY?
  With timezone UTC: "created at 03:30 UTC"
    → Server can display "09:00 AM IST" to the Mumbai user
    → Or "11:30 PM EDT" to the New York user
  Same timestamp. Different display. Always correct.
```

**`default=lambda: datetime.now(UTC)` — The Lambda Trap:**

```python
# WHY LAMBDA? — One of the most important Python ORM gotchas.

# WRONG approach — direct function reference without lambda:
default=datetime.now(UTC)
# datetime.now(UTC) is called NOW (when Python imports this file)
# The result is stored as a constant: "2026-07-25 09:00:00"
# EVERY row created will have the SAME timestamp — when the module loaded!
# Hours, days, weeks later: still the same timestamp. Bug.

# WRONG approach — passing function reference without call:
default=datetime.now
# datetime.now is the function. But SQLAlchemy calls it WITHOUT arguments.
# datetime.now() with no args → naive datetime (no timezone info)
# We need: datetime.now(UTC) → timezone-aware
# Wrong function call signature → TypeError or wrong timezone.

# CORRECT approach — lambda:
default=lambda: datetime.now(UTC)
# lambda: → creates a zero-argument function
# datetime.now(UTC) → called INSIDE the lambda, NOT at import time
# SQLAlchemy stores the lambda, calls it fresh for EACH new row
# Every row gets the actual current time when it's inserted

# Equivalent to:
def get_current_utc():
    return datetime.now(UTC)
default=get_current_utc   # function reference without ()

# Lambda is just cleaner:
default=lambda: datetime.now(UTC)
```

**The Rule:**

```
For default values that must be EVALUATED at insert time (not import time):
  ✅ Use lambda: datetime.now(UTC)
  ❌ Never use datetime.now(UTC) (evaluated once at import)
  ❌ Never use datetime.now without UTC (naive datetime)

For literal defaults (same value always):
  ✅ default=0     → fine, 0 is always 0
  ✅ default=False → fine, False is always False
  ❌ default=[]    → DANGEROUS! Same list shared by all instances
```

**Generated SQL:**

```sql
created_at TIMESTAMP WITH TIME ZONE NOT NULL
```

---

# SECTION 6 — HOW THE MODEL MAPS TO THE TABLE

## The Python ↔ PostgreSQL Mapping

```
Python ShortenedURL class          PostgreSQL shortened_urls table
──────────────────────────────     ────────────────────────────────────────
class ShortenedURL(Base)     →     CREATE TABLE shortened_urls (
__tablename__ = "shortened_urls"
id: Mapped[int]              →       id SERIAL PRIMARY KEY,
  primary_key=True
original_url: Mapped[str]    →       original_url TEXT NOT NULL,
  nullable=False
short_code: Mapped[str]      →       short_code VARCHAR(10) UNIQUE NOT NULL,
  unique=True, nullable=False
clicks: Mapped[int]          →       clicks INTEGER NOT NULL,
  default=0, nullable=False
created_at: Mapped[datetime] →       created_at TIMESTAMPTZ NOT NULL
  timezone=True, nullable=False  );
```

---

## SQLAlchemy 2.0 vs 1.x Syntax Comparison

```python
# OLD SQLAlchemy 1.x (still works, but not recommended for new projects):
class ShortenedURL(Base):
    __tablename__ = "shortened_urls"
    id = Column(Integer, primary_key=True, index=True)
    original_url = Column(Text, nullable=False)
    short_code = Column(String(10), unique=True, nullable=False, index=True)
    clicks = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))

# NEW SQLAlchemy 2.0 (what we use — Mapped + mapped_column):
class ShortenedURL(Base):
    __tablename__ = "shortened_urls"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    original_url: Mapped[str] = mapped_column(Text, nullable=False)
    short_code: Mapped[str] = mapped_column(String(10), unique=True, nullable=False, index=True)
    clicks: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False)

# Differences:
# 1. Mapped[T] type hint → IDE understands the type
# 2. mapped_column() instead of Column()
# 3. Type information in Mapped[int] instead of just in Column(Integer)
# 4. Better mypy/Pylance support
# 5. SQLAlchemy 2.0 is the current standard
```

---

# SECTION 7 — CREATING THE TABLE (create_all)

## Updated main.py

```python
# main.py

import app.models.shortened_url  # noqa: F401 — registers model with Base
from app.database.base import Base
from app.database.database import engine

from fastapi import FastAPI

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="URL Shortener API",
    version="1.0.0",
    description="A URL Shortener API built with FastAPI and PostgreSQL."
)


@app.get("/")
def root():
    return {"message": "Welcome to URL Shortener API 🚀"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
```

---

## `import app.models.shortened_url  # noqa: F401`

```python
import app.models.shortened_url  # noqa: F401

# This is the most commonly confused line in FastAPI database setup.

# Why import the model if we don't use it directly?
# SQLAlchemy's Base only knows about a model IF that model's module
# has been imported.

# Base.metadata is like a registry:
# When Python loads shortened_url.py, the class definition runs.
# class ShortenedURL(Base) → this line registers ShortenedURL with Base.metadata.

# If shortened_url.py is NEVER imported:
#   class ShortenedURL never executes.
#   Base.metadata has no tables registered.
#   Base.metadata.create_all(engine) creates NO tables.
#   Server starts. PostgreSQL still empty. Bug.

# With the import:
#   shortened_url.py loads → class ShortenedURL(Base) registers.
#   Base.metadata knows about shortened_urls.
#   create_all() generates and executes CREATE TABLE shortened_urls (...).
#   Table exists.

# noqa: F401 → tells linters "I know this import looks unused.
#               It's intentional — for its side effect (registration)."
#               Without noqa, flake8 warns: "imported but unused."
```

## `Base.metadata.create_all(bind=engine)`

```python
Base.metadata.create_all(bind=engine)

# This runs ONCE when the FastAPI application starts (not per request).

# What it generates:
CREATE TABLE IF NOT EXISTS shortened_urls (
    id           SERIAL                    PRIMARY KEY,
    original_url TEXT                      NOT NULL,
    short_code   CHARACTER VARYING(10)     UNIQUE NOT NULL,
    clicks       INTEGER                   NOT NULL,
    created_at   TIMESTAMP WITH TIME ZONE NOT NULL
);

# IF NOT EXISTS → Safe to run every server restart.
# If the table already exists: nothing happens. No error.
# If the table doesn't exist: creates it.

# What it does NOT do:
# → Never modifies an existing table's columns.
# → Adding a new column to the model → restart → column NOT added.
# → For column changes: need Alembic (future day).
```

---

## Verifying in pgAdmin

```
After starting the server and visiting http://127.0.0.1:8000/

Open pgAdmin 4.
Navigate:
  Servers → PostgreSQL 18 → Databases → url_shortener_db
  → Schemas → public → Tables → shortened_urls

Expected columns:
  id           integer    (SERIAL PRIMARY KEY)
  original_url text       NOT NULL
  short_code   varchar(10) UNIQUE NOT NULL
  clicks       integer    NOT NULL
  created_at   timestamptz NOT NULL

Expected indexes (right-click → Properties → Indexes):
  shortened_urls_pkey    → on id (from PRIMARY KEY)
  shortened_urls_short_code_key → on short_code (from UNIQUE)
  ix_shortened_urls_id   → on id (from index=True)
  ix_shortened_urls_short_code → on short_code (from index=True)
```

**If you see these 5 columns and the indexes: the model is working perfectly.**

---

# SECTION 8 — ARCHITECTURE AFTER DAY 52

## The Import Graph

```
base.py
  ↑ imported by
  ├── models/shortened_url.py
  │     (class ShortenedURL(Base))
  │
  └── main.py
        ↑ also imports
        ├── app.database.database (engine)
        └── app.models.shortened_url (triggers registration)
```

## The Dependency Direction

```
base.py  ← no dependencies (pure)
  ↓
models/shortened_url.py ← depends only on base.py and sqlalchemy
  ↓
main.py ← depends on everything, orchestrates startup
```

**Nothing flows backwards.** `base.py` doesn't know about `database.py`. `database.py` doesn't know about the models. This is clean architecture.

---

# SECTION 9 — CONCEPTS CONSOLIDATED TODAY

## SQLAlchemy 2.0 Model Syntax

```
Mapped[T]            → Type hint for type safety and IDE support
mapped_column()      → Column definition (replaces Column())
DeclarativeBase      → Modern base class (replaces declarative_base())
primary_key=True     → PK, UNIQUE, NOT NULL, SERIAL (for integers)
unique=True          → UNIQUE constraint + automatic index
nullable=False       → NOT NULL constraint
index=True           → explicit B-tree index creation
default=0            → SQLAlchemy sets value before INSERT (not PostgreSQL DEFAULT)
server_default="0"   → PostgreSQL-level DEFAULT (runs in raw SQL too)
DateTime(timezone=True) → TIMESTAMPTZ (timezone-aware timestamps)
lambda: datetime.now(UTC) → evaluated fresh per row, not once at import
```

## The Import Registration Trick

```python
# models MUST be imported before create_all()
import app.models.shortened_url  # noqa: F401
Base.metadata.create_all(bind=engine)

# The import side-effect registers the model with Base.metadata.
# Without it: create_all() creates no tables.
```

## Timezone Best Practice

```
Always:
  Store in UTC: datetime.now(UTC)
  Use TIMESTAMPTZ: DateTime(timezone=True)
  Use lambda: to get fresh time per row

Never:
  Store local time (ambiguous)
  Use naive datetime without timezone
  datetime.now(UTC) without lambda (frozen to import time)
```

---

# SECTION 10 — LEETCODE #283: MOVE ZEROES

## Problem

Given integer array `nums`, move all `0`s to the end while maintaining the relative order of non-zero elements. In-place. No extra array.

```
Input:  [0, 1, 0, 3, 12]
Output: [1, 3, 12, 0, 0]

Input:  [0]
Output: [0]
```

---

## The Critical Understanding

```
This problem asks THREE things simultaneously:
  1. Move all zeros to the END.
  2. Keep non-zero elements in the SAME relative order.
  3. Do it IN-PLACE (modify nums directly, no extra array).

This is different from:
  "Remove Element (#27)" — which removes elements completely
  "Sort the array" — which doesn't maintain relative order
```

---

## The Key Insight

```
Instead of moving zeros (complicated),
MOVE THE NON-ZEROS to the front.

The zeros fill the remaining positions automatically.

Why is this smarter?
  Moving zeros: each zero might shift many elements right → O(n²)
  Moving non-zeros: each goes exactly where it needs to → O(n)
```

---

## Brute Force — O(n²)

```python
def moveZeroes_brute(nums):
    for i in range(len(nums)):
        if nums[i] == 0:
            # Shift all elements after i one position left
            for j in range(i, len(nums) - 1):
                nums[j] = nums[j + 1]
            nums[-1] = 0   # Place zero at end

# For [0,0,0,0,1,2,3]:
# Each 0 shifts the remaining elements 1 position left.
# 4 zeros × n shifts each = O(n²) total operations.
```

---

## Optimal Solution — Reader & Writer O(n) ✅ Submitted

```python
class Solution(object):
    def moveZeroes(self, nums):
        w = 0                         # w = write pointer (where to place next non-zero)

        for i in range(len(nums)):    # i = read pointer (scans every element)

            if nums[i] != 0:          # Only process non-zero elements
                nums[w] = nums[i]     # Copy non-zero to write position

                if i != w:            # Only zero out old position if different
                    nums[i] = 0       # Clear the source (leave a zero behind)

                w += 1                # Advance write pointer

        return nums
```

---

## The `if i != w` Guard — Critical Detail

```python
if i != w:
    nums[i] = 0

# This is the most important line.

# Why do we need it?

# Scenario WITHOUT the guard, nums = [1, 2, 3]:

# i=0, w=0: nums[0]=1 ≠ 0
#   nums[0] = nums[0]  → nums[0] = 1 (no change)
#   nums[0] = 0        ← CATASTROPHE! We just zeroed out 1!
#   w=1
# Result: [0, 2, 3] ← WRONG!

# With the guard:
# i=0, w=0: same position
#   nums[0] = nums[0]  → 1 (no change)
#   i == w → SKIP zeroing
#   w=1
# i=1, w=1: same position → skip zeroing → w=2
# i=2, w=2: same position → skip zeroing → w=3
# Result: [1, 2, 3] ← CORRECT! No zeros needed. Array already good.

# Rule: Only zero out the source position when Reader has moved PAST Writer.
# When Reader == Writer: we're filling the same position. No zeroing needed.
# When Reader > Writer: we've already moved past a zero. Safe to zero old spot.
```

---

## Complete Dry Run

```
nums = [0, 1, 0, 3, 0, 0, 12, 5, 0, 8]
w = 0

i=0: nums[0]=0 → is 0 → SKIP
     [0,1,0,3,0,0,12,5,0,8]  w=0

i=1: nums[1]=1 → not 0
     nums[w=0] = nums[i=1] = 1  → [1,1,0,3,0,0,12,5,0,8]
     i(1) != w(0) → nums[1] = 0 → [1,0,0,3,0,0,12,5,0,8]
     w=1

i=2: nums[2]=0 → SKIP  w=1

i=3: nums[3]=3 → not 0
     nums[w=1] = nums[i=3] = 3  → [1,3,0,0,0,0,12,5,0,8]
     i(3) != w(1) → nums[3] = 0 → [1,3,0,0,0,0,12,5,0,8]
     w=2

i=4,5: zeros → SKIP  w=2

i=6: nums[6]=12 → not 0
     nums[w=2] = 12 → [1,3,12,0,0,0,0,5,0,8]
     i(6) != w(2) → nums[6] = 0 → [1,3,12,0,0,0,0,5,0,8]
     w=3

i=7: nums[7]=5 → not 0
     nums[w=3] = 5 → [1,3,12,5,0,0,0,0,0,8]
     i(7) != w(3) → nums[7] = 0 → [1,3,12,5,0,0,0,0,0,8]
     w=4

i=8: zero → SKIP  w=4

i=9: nums[9]=8 → not 0
     nums[w=4] = 8 → [1,3,12,5,8,0,0,0,0,0]
     i(9) != w(4) → nums[9] = 0 → [1,3,12,5,8,0,0,0,0,0]
     w=5

Final: [1, 3, 12, 5, 8, 0, 0, 0, 0, 0] ✅
```

---

## Connection to Day 51's Remove Element (#27)

```
#27 Remove Element:                #283 Move Zeroes:

k = 0                              w = 0
for i in range(len(nums)):         for i in range(len(nums)):
    if nums[i] != val:                 if nums[i] != 0:
        nums[k] = nums[i]                  nums[w] = nums[i]
        k += 1                             if i != w:
return k                                       nums[i] = 0
                                       w += 1
                                   return nums

DIFFERENCE:
#27: Elements that are val simply don't get copied.
     Old positions are not zeroed (they're "irrelevant" past k).
     Returns k (the count).

#283: Elements that are 0 don't get copied.
     Old positions ARE zeroed (they become the trailing zeros).
     Returns nums (the array).

ONE EXTRA LINE:  if i != w: nums[i] = 0
This is literally the only difference.
Pattern: identical.
```

---

## Common Mistakes

```
Mistake 1: Creating extra array
  result = [x for x in nums if x != 0]  ← violates in-place
  Solution: Two pointers on original array.

Mistake 2: Moving zeros (instead of non-zeros)
  Shifting zeros right = O(n²).
  Moving non-zeros left = O(n).
  Always think: "What's easier to move?"

Mistake 3: Forgetting if i != w
  Without it: nums where there are no zeros get corrupted.
  Example: [1,2,3] → [0,0,0] without the guard.

Mistake 4: Advancing w on every iteration
  w must advance ONLY after writing a non-zero element.
  Not every iteration.

Mistake 5: Thinking this is a different pattern from #27
  It IS #27 + one line.
  Recognize the pattern family.
```

---

## Complexity

```
Time:  O(n) — single pass. Each element touched once.
Space: O(1) — in-place. Only two pointers (i, w).

Compared to brute force:
  Brute:   O(n²) time, O(1) space
  Optimal: O(n)  time, O(1) space

Same space complexity. Better time complexity.
```

**Result:** ✅ Accepted | 75/75 test cases | Runtime: 2ms | Beats 93.10%

---

## The In-Place Modification Pattern (Complete Family)

```
All these problems share the Reader + Writer pattern:

#27  Remove Element       → copy if nums[i] != val
#283 Move Zeroes (this)   → copy if nums[i] != 0, zero old position
#26  Remove Duplicates    → copy if nums[i] != nums[i-1] (sorted)
#80  Remove Duplicates II → copy if i < 2 or nums[i] != nums[w-2]
#905 Sort By Parity       → left pointer for even, right for odd

Template:
  w = 0
  for i in range(len(nums)):
      if CONDITION(nums[i]):         # define what to KEEP
          nums[w] = nums[i]         # copy to write position
          [OPTIONAL: clean old pos]  # depends on problem
          w += 1
  return w  # or nums depending on problem
```

---

# SECTION 11 — IMPORTANT THINGS TO KNOW

```
 1. Extract Base to its own file (base.py).
    Prevents models from accidentally triggering database connections on import.

 2. SQLAlchemy 2.0 uses Mapped[T] and mapped_column() — not Column().
    Mapped[int], Mapped[str], Mapped[datetime] provide type safety.

 3. DeclarativeBase (class-based) replaces declarative_base() (function call).
    Both work. Class-based is the 2.0+ standard.

 4. DateTime(timezone=True) → TIMESTAMPTZ in PostgreSQL.
    Always store timestamps in UTC. Never local time.

 5. default=lambda: datetime.now(UTC) → evaluated fresh for each row.
    default=datetime.now(UTC) → evaluated ONCE at import. Wrong!

 6. default=0 is a SQLAlchemy-level default (sets in Python before INSERT).
    server_default="0" is a PostgreSQL-level DEFAULT (in the SQL schema).

 7. unique=True automatically creates an index. index=True is redundant but readable.

 8. Models MUST be imported before create_all() for registration to work.
    import app.models.shortened_url  # noqa: F401 is intentional.

 9. create_all() with IF NOT EXISTS is safe to run on every server restart.
    It never modifies existing tables — only creates missing ones.

10. For column additions to existing tables: use Alembic (future day).
    create_all() cannot alter existing tables.

11. Move Zeroes = Remove Element + one extra line (if i != w: nums[i] = 0).
    Recognizing the pattern family saves problem-solving time in interviews.

12. The guard `if i != w` prevents zeroing valid elements.
    When Reader == Writer: same position. Don't zero. They'd cancel each other.

13. Always move non-zeros (not zeros). Moving non-zeros is simpler and faster.
    Moving zeros = shifting everything = O(n²).
    Moving non-zeros = copy + clear = O(n).

14. Two pointer pattern: Reader (i) always moves. Writer (w) moves only on write.
    This is O(n) time, O(1) space. Optimal for in-place array problems.

15. UTC timestamps are universal. Store in UTC. Display in local time on the frontend.
    Mixed timezone storage is a source of hard-to-debug time-related bugs.
```

---

# REVISION SHEET

```
═══════════════════════════════════════════════════════════
DAY 52 — ORM MODEL + TWO POINTERS REVISION
═══════════════════════════════════════════════════════════

BASE.PY:
  from sqlalchemy.orm import DeclarativeBase
  class Base(DeclarativeBase): pass

SHORTENED_URL MODEL (key columns):
  id:          Mapped[int]      primary_key=True, index=True
  original_url: Mapped[str]     Text, nullable=False
  short_code:  Mapped[str]      String(10), unique=True, nullable=False, index=True
  clicks:      Mapped[int]      Integer, default=0, nullable=False
  created_at:  Mapped[datetime] DateTime(timezone=True),
                                default=lambda: datetime.now(UTC), nullable=False

DATETIME RULES:
  DateTime(timezone=True)     → TIMESTAMPTZ (UTC)
  lambda: datetime.now(UTC)   → fresh per row
  datetime.now(UTC)           → frozen to import time (WRONG for default)

CREATE TABLE:
  import models first (registration side effect)
  Base.metadata.create_all(bind=engine)

SQLALCHEMY 2.0 vs 1.x:
  Old: id = Column(Integer, primary_key=True)
  New: id: Mapped[int] = mapped_column(Integer, primary_key=True)

LEETCODE #283:
  w = 0
  for i in range(len(nums)):
      if nums[i] != 0:
          nums[w] = nums[i]
          if i != w: nums[i] = 0
          w += 1
  return nums
  Time O(n), Space O(1)

if i != w GUARD:
  Prevents zeroing elements when Reader and Writer are at same position
  Without it: [1,2,3] becomes [0,0,0]
  With it: [1,2,3] stays [1,2,3] correctly
```

---

## LeetCode Solved This Day

| Problem | Difficulty | Topic | Status | Runtime |
|---------|-----------|-------|--------|---------|
| #283 Move Zeroes | Easy | Two Pointers, In-Place, Reader & Writer | ✅ Accepted 75/75 | 2ms, Beats 93.10% |

---

*Day 52 Complete. Base extracted. ShortenedURL model written with SQLAlchemy 2.0 syntax. Table created in PostgreSQL. Data layer is complete. CRUD operations start next day.* ✅
