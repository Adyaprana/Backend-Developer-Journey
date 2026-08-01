# DAY 45 — FastAPI + PostgreSQL + SQLAlchemy: Full Database Integration + LeetCode Optimal Prefix Products

> **Phase:** 02 — FastAPI Backend (Days 43–90)
>
> **Week:** W7 — FastAPI Core (Days 43–49)
>
> **Goal:** Build the first production-style FastAPI backend connected to PostgreSQL using SQLAlchemy. Full CRUD with dependency injection, layered architecture, and response filtering.
>
> **LeetCode:** #238 Product of Array Except Self ✅ (Optimal O(1) space — 43ms · Accepted 24/24)
>
> **Status:** ✅ Day 45 Complete — Full CRUD API connected to PostgreSQL. Data actually persists.

---

# 🎯 Learning Roadmap

```
FastAPI + PostgreSQL + SQLAlchemy

  ✅ database.py   — Engine, Session, Base, get_db()
  ✅ models.py     — SQLAlchemy ORM models (database tables)
  ✅ schemas.py    — Pydantic models (request/response validation)
  ✅ crud.py       — Database operations (create, read, update, delete)
  ✅ main.py       — FastAPI routes + Dependency Injection
  ✅ Dependency Injection — Depends(get_db)
  ✅ 500 Error Debugging — old table schema conflict
  ✅ LeetCode #238 Optimal — O(1) extra space prefix products
```

## Day 45 Checklist

- [ ] Explain why yesterday's API lost data on restart
- [ ] Draw the full architecture: Client → FastAPI → Pydantic → CRUD → SQLAlchemy → PostgreSQL
- [ ] Explain what engine, SessionLocal, and Base do
- [ ] Explain `get_db()` and why it uses `yield` not `return`
- [ ] Explain Dependency Injection with `Depends(get_db)`
- [ ] Explain the difference between SQLAlchemy Model and Pydantic Schema
- [ ] Explain `from_attributes=True` in Pydantic
- [ ] Write all 5 CRUD endpoints from memory
- [ ] Explain `HTTPException(status_code=404, detail="...")`
- [ ] Explain why `create_all()` doesn't update existing tables
- [ ] Solve LeetCode #238 optimal (O(1) space) from memory

---

# SECTION 1 — THE PROBLEM WITH YESTERDAY'S API

## Data Disappears on Restart

Yesterday's API returned the user object — but never saved it anywhere:

```python
# DAY 44 — Data was never persisted
@app.post("/users")
def create_user(user: UserCreate):
    return user   # ← just echoes the input back. Gone after restart.
```

```
Client → POST /users → FastAPI → Validate → Return Response

❌ Data disappears when the server restarts.
❌ Data disappears when the request finishes.
❌ Two clients can't see each other's data.
❌ Useless for a real application.
```

## RAM vs Disk

```
RAM (temporary):
  → Python variables, lists, dicts
  → Survives only while the program runs
  → Fast but volatile
  → "Where your Python code runs"

Disk/Database (permanent):
  → PostgreSQL stores data on disk
  → Survives restarts, crashes, power cuts
  → Slightly slower but durable
  → "Where your data lives forever"

A real backend must write to disk.
That's why we integrate PostgreSQL today.
```

---

# SECTION 2 — THE COMPLETE ARCHITECTURE

## How FastAPI Reaches PostgreSQL

```
Client (Browser/Postman)
        │
        │ HTTP POST /users {"name": "Adya", "email": "adya@gmail.com"}
        ▼
Uvicorn (network server — parses TCP + HTTP)
        │
        ▼
FastAPI (routes the request to create_user endpoint)
        │
        ▼
Pydantic Schema (UserCreate — validates name, email)
        │
        ▼
Dependency Injection: Depends(get_db) → provides database session
        │
        ▼
CRUD Layer: crud.create_user(db, user)
        │
        ▼
SQLAlchemy ORM: User(name=..., email=...) → db.add() → db.commit()
        │
        ▼
psycopg2 driver (translates Python to PostgreSQL protocol)
        │
        ▼
PostgreSQL (stores permanently in users table)
        │
        ▼
SQLAlchemy returns the saved User object
        │
        ▼
FastAPI applies UserResponse schema (filters output)
        │
        ▼
JSON Response: {"id": 1, "name": "Adya", "email": "...", "is_active": true}
        │
        ▼
Client receives response
```

**Notice: FastAPI never talks directly to PostgreSQL.** SQLAlchemy sits in between.

---

## Why Not Write Raw SQL?

```python
# You COULD write this:
cursor.execute("INSERT INTO users(name, email) VALUES (%s, %s)", (name, email))

# Nothing wrong. But imagine doing this for:
# → 50 tables
# → 300 queries
# → Complex relationships
# → Dynamic filtering
# → Type safety

# It becomes unmaintainable.
# SQLAlchemy lets you work with Python objects instead.

# Instead of: INSERT INTO users ...
user = User(name="Adya", email="adya@gmail.com")
db.add(user)
db.commit()
# SQLAlchemy generates the SQL for you.
```

---

## Project Structure

```
backend-learning/
│
├── main.py          ← FastAPI app + routes
├── database.py      ← Connection configuration
├── models.py        ← SQLAlchemy ORM models (database tables)
├── schemas.py       ← Pydantic models (API validation)
├── crud.py          ← Database operations
└── requirements.txt
```

**What each file does:**

```
database.py  → "Database Manager"
               How to connect. Engine. Session. Base. get_db().
               
models.py    → "Database Blueprint"
               Python classes → PostgreSQL tables.
               User class → users table.
               
schemas.py   → "API Contract"
               Nothing to do with PostgreSQL.
               Validates incoming JSON. Shapes outgoing JSON.
               
crud.py      → "Database Operations"
               Create, Read, Update, Delete.
               No FastAPI decorators here. Pure database logic.
               
main.py      → "Traffic Controller"
               Registers routes. Injects sessions. Calls CRUD.
```

---

# SECTION 3 — DATABASE.PY (COMPLETE EXPLANATION)

## The Complete File

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "postgresql+psycopg2://postgres:postgres123@localhost:5432/backend_journey"


engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()


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

---

## DATABASE_URL — The Connection String

```python
DATABASE_URL = "postgresql+psycopg2://postgres:postgres123@localhost:5432/backend_journey"
```

```
postgresql     → database type (tells SQLAlchemy: use PostgreSQL SQL dialect)
+psycopg2      → the driver that physically sends SQL over the network
                 (installed with: pip install psycopg2-binary)
postgres       → PostgreSQL username
postgres123    → PostgreSQL password (NEVER commit this to GitHub!)
@localhost     → host (our own machine in development)
:5432          → port (PostgreSQL default — usually don't change this)
/backend_journey → database name (must exist in PostgreSQL)
```

**In production:** Use environment variables:

```python
import os
DATABASE_URL = os.getenv("DATABASE_URL")
# Set in .env file or deployment platform
# Never hardcode credentials
```

---

## engine — The Connection Factory

```python
engine = create_engine(DATABASE_URL)
```

```
The Engine is the BRIDGE between SQLAlchemy and PostgreSQL.

create_engine() does NOT connect immediately (lazy connection).
It creates a connection POOL — a set of reusable connections.

When any query runs:
  1. Engine grabs an available connection from the pool
  2. Query executes
  3. Connection returns to the pool

Why connection pooling?
  Opening a new TCP connection to PostgreSQL takes ~5ms.
  Pooling reuses existing connections.
  1000 requests/second → same 10 connections, not 1000 new ones.
  Massive performance improvement.
```

---

## SessionLocal — The Session Factory

```python
SessionLocal = sessionmaker(
    autocommit=False,   # Don't auto-commit after every operation
    autoflush=False,    # Don't auto-flush before queries
    bind=engine,        # Which engine to use
)
```

```
sessionmaker() creates a FACTORY — a blueprint for making sessions.
SessionLocal itself is NOT a session.
Calling SessionLocal() gives you ONE session.

Session = one conversation with PostgreSQL.
  db = SessionLocal()    → open the conversation
  db.query(...)          → ask a question
  db.add(obj)            → stage an insert
  db.commit()            → save permanently
  db.close()             → end the conversation

autocommit=False:
  Changes must be explicitly committed.
  Without this: every db.add() would immediately commit.
  With this: you can add multiple objects and commit once.
  Safer. More control.

autoflush=False:
  Don't automatically flush pending changes before queries.
  More predictable behavior.
```

---

## Base — The Model Registry

```python
Base = declarative_base()
```

```
Base is the parent class for ALL SQLAlchemy models.

Every model inherits from Base:
  class User(Base): ...
  class Product(Base): ...
  class Order(Base): ...

Base tracks all these models.
When you call Base.metadata.create_all(engine),
it creates ALL registered tables at once.

Without Base:
  SQLAlchemy doesn't know your models exist.
  create_all() creates nothing.
```

---

## get_db() — The Session Provider

```python
def get_db():
    """Provide a database session for each request."""
    db = SessionLocal()     # Open a session
    try:
        yield db            # ← Give session to endpoint
    finally:
        db.close()          # ← Always close, even on error
```

**Why `yield` instead of `return`?**

```python
# If we used return:
def get_db():
    db = SessionLocal()
    return db               # ← FastAPI gets the session
                            # But nobody ever calls db.close()!
                            # Connection leak. PostgreSQL runs out of connections.

# With yield (generator function):
def get_db():
    db = SessionLocal()
    try:
        yield db            # ← FastAPI gets the session here
        # ... endpoint runs ...
    finally:
        db.close()          # ← This runs AFTER the endpoint finishes
```

```
The yield pattern creates a generator.
FastAPI knows about generator dependencies (functions using yield).

Timeline:
  Request arrives
  │
  get_db() starts → db = SessionLocal()
  │
  yield db  ← FastAPI receives db here, pauses get_db()
  │
  Your endpoint runs with db
  │
  Endpoint finishes (success or error)
  │
  FastAPI resumes get_db() after yield
  │
  finally: db.close() runs
  │
  Connection returned to pool

This guarantees EVERY session is closed properly.
No connection leaks. No hanging transactions.
```

---

# SECTION 4 — MODELS.PY (SQLALCHEMY ORM MODELS)

## The Complete File

```python
from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Integer,
    String,
)

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    name = Column(
        String(100),
        nullable=False,
    )

    email = Column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )

    is_active = Column(
        Boolean,
        default=True,
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
    )
```

---

## Line-by-Line Explanation

**`class User(Base):`**

```
Inheriting from Base does several things:
  1. Registers this class with SQLAlchemy's table registry
  2. Enables SQLAlchemy's declarative mapping system
  3. Makes Base.metadata.create_all() include this table
  4. Enables relationship navigation
```

**`__tablename__ = "users"`**

```
REQUIRED. Tells SQLAlchemy: "Map this class to the 'users' table in PostgreSQL."
Without it: SQLAlchemy raises an error.
Convention: plural lowercase snake_case.
  User class → users table
  OrderItem class → order_items table
```

**`id = Column(Integer, primary_key=True, index=True)`**

```
Integer        → PostgreSQL INTEGER data type
primary_key=True → This column uniquely identifies every row.
                   Automatically: NOT NULL + UNIQUE
index=True     → Creates a database index for fast lookups.
                 SELECT * FROM users WHERE id=42 → uses index → O(log n)

Note: In GuessWise we used SERIAL (auto-increment) explicitly.
      SQLAlchemy with Integer + primary_key uses SERIAL automatically in PostgreSQL.
```

**`name = Column(String(100), nullable=False)`**

```
String(100)    → VARCHAR(100) in PostgreSQL. Max 100 characters.
nullable=False → This field is required. NOT NULL constraint.
                 Inserting without name → PostgreSQL error.
```

**`email = Column(String(255), unique=True, nullable=False, index=True)`**

```
String(255)    → VARCHAR(255). Standard for emails.
unique=True    → UNIQUE constraint. No two users can have the same email.
nullable=False → Required. NOT NULL.
index=True     → Creates an index. login queries (WHERE email=?) are fast.
```

**`is_active = Column(Boolean, default=True)`**

```
Boolean        → PostgreSQL BOOLEAN.
default=True   → When a User is created without specifying is_active,
                 it defaults to True (active).
                 Note: This is a SQLAlchemy-level default, not a PostgreSQL DEFAULT.
                 SQLAlchemy sets it before INSERT.
```

**`created_at = Column(DateTime, default=datetime.utcnow)`**

```
DateTime       → PostgreSQL TIMESTAMP.
default=datetime.utcnow → When user is created, SQLAlchemy sets created_at
                           to current UTC time automatically.

IMPORTANT: datetime.utcnow (no parentheses) vs datetime.utcnow() (with parentheses):
  datetime.utcnow   → SQLAlchemy stores the FUNCTION and calls it at insert time ✅
  datetime.utcnow() → Python evaluates it NOW (when the class is defined) ❌
                      All users get the same timestamp (when server started)
```

---

## SQLAlchemy → PostgreSQL Type Mapping

```
SQLAlchemy Type    PostgreSQL Type    Python Type
───────────────────────────────────────────────────
Integer            INTEGER            int
String(n)          VARCHAR(n)         str
Text               TEXT               str
Boolean            BOOLEAN            bool
Float              FLOAT              float
Numeric(p,s)       DECIMAL(p,s)       Decimal
DateTime           TIMESTAMP          datetime
Date               DATE               date
JSON               JSONB              dict/list
```

---

# SECTION 5 — SCHEMAS.PY (PYDANTIC MODELS)

## The Complete File

```python
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    name: str = Field(min_length=3, max_length=100)
    email: EmailStr


class UserCreate(UserBase):
    pass
    # password: str = Field(min_length=8)  ← add when implementing auth


class UserUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=3, max_length=100)
    email: Optional[EmailStr] = None


class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    is_active: bool
```

---

## The Schema Hierarchy

```
UserBase (shared fields — name, email)
    │
    ├── UserCreate (POST /users body)
    │     → Inherits name + email from UserBase
    │     → Will add password field when implementing auth
    │
    └── UserResponse (what API returns)
          → Inherits name + email from UserBase
          → Adds id, is_active (from database, not sent by client)
          → Has from_attributes=True

UserUpdate (standalone — all fields Optional for partial updates)
    → name: Optional
    → email: Optional
    → Only send what you want to change
```

---

## UserBase — Shared Fields

```python
class UserBase(BaseModel):
    name: str = Field(min_length=3, max_length=100)
    email: EmailStr
```

```
DRY principle: Don't Repeat Yourself.
Both UserCreate and UserResponse need name and email.
Define them once in UserBase, inherit in both.

If the validation rule for name changes:
  Change it in UserBase → both UserCreate and UserResponse update.
  No need to change in two places.
```

---

## UserCreate — The Input Schema

```python
class UserCreate(UserBase):
    pass
    # password: str = Field(min_length=8)
```

```
Currently inherits: name + email from UserBase.
Nothing extra yet.

The commented-out password field will be added when we implement
authentication in a future day.

Why is the password field commented out, not just missing?
  → Reminder that it belongs here
  → Shows the expected evolution of this schema
  → Future developer (or future you) knows to uncomment it
```

---

## UserUpdate — The Partial Update Schema

```python
class UserUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=3, max_length=100)
    email: Optional[EmailStr] = None
```

```
For PATCH/PUT requests: only send what you want to change.

If client sends:
  {"name": "New Name"}       → only name updates, email unchanged
  {"email": "new@x.com"}     → only email updates, name unchanged
  {}                          → nothing updates

Optional[str] with default=None means:
  "If client doesn't send this field, it's None (don't update it)"

In crud.update_user():
  if user.name is not None:
      db_user.name = user.name
  if user.email is not None:
      db_user.email = user.email
  → Only updates fields that were actually sent
```

---

## UserResponse — The Output Schema

```python
class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    is_active: bool
```

**`from_attributes=True` — The Critical Setting:**

```python
# Without from_attributes=True:
# crud.get_user() returns: User(id=1, name="Adya", email="adya@gmail.com", ...)
# This is a SQLAlchemy model object (not a dict)

# FastAPI tries to convert it to UserResponse.
# Pydantic tries: UserResponse(User_object)
# It would fail because Pydantic expects a dict, not an SQLAlchemy object.

# With from_attributes=True (Pydantic v2) / orm_mode=True (Pydantic v1):
# Pydantic can READ attributes from Python objects (not just dicts)
# user_response.id = User_object.id ← reads from object attribute
# user_response.name = User_object.name ← reads from object attribute

# Without it: ValidationError crash
# With it: SQLAlchemy object → Pydantic model works perfectly
```

---

## MODEL vs SCHEMA — The Most Important Distinction

```
SQLAlchemy Model (models.py):       Pydantic Schema (schemas.py):
──────────────────────────────      ──────────────────────────────
Represents a DATABASE TABLE         Represents API DATA SHAPE
Stored in PostgreSQL                Used for validation + docs
Has database columns                Has field validators
class User(Base)                    class UserCreate(BaseModel)
SQLAlchemy maps it to SQL           Pydantic validates JSON

When does each live?
Model:  EXISTS in database as a table. Rows are stored permanently.
Schema: EXISTS only during the request/response cycle. Temporary.

Flow:
Browser → JSON → UserCreate (Pydantic schema validates)
                    ↓
               User (SQLAlchemy model inserts to DB)
                    ↓
            PostgreSQL stores permanently
                    ↓
               User (SQLAlchemy model reads from DB)
                    ↓
           UserResponse (Pydantic schema filters output)
                    ↓
              JSON → Browser
```

---

# SECTION 6 — CRUD.PY (DATABASE OPERATIONS)

## The Complete File

```python
from sqlalchemy.orm import Session

import models
import schemas


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        name=user.name,
        email=user.email,
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def get_users(db: Session):
    return db.query(models.User).all()


def get_user(db: Session, user_id: int):
    return (
        db.query(models.User)
        .filter(models.User.id == user_id)
        .first()
    )


def update_user(
    db: Session,
    user_id: int,
    user: schemas.UserUpdate,
):
    db_user = get_user(db, user_id)

    if not db_user:
        return None

    if user.name is not None:
        db_user.name = user.name

    if user.email is not None:
        db_user.email = user.email

    db.commit()
    db.refresh(db_user)

    return db_user


def delete_user(db: Session, user_id: int):
    db_user = get_user(db, user_id)

    if not db_user:
        return None

    db.delete(db_user)
    db.commit()

    return db_user
```

---

## create_user() — Explained

```python
def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        name=user.name,
        email=user.email,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
```

```
Step 1: models.User(name=user.name, email=user.email)
  Creates a SQLAlchemy model instance (not yet in database).
  db_user is a Python object in RAM.
  id is None (not assigned yet).

Step 2: db.add(db_user)
  Stages the object for insertion.
  The INSERT SQL is prepared but NOT yet sent to PostgreSQL.
  Equivalent to: "I want to insert this when we commit."

Step 3: db.commit()
  Executes: INSERT INTO users (name, email, is_active, created_at) VALUES (...)
  PostgreSQL assigns id=1 (auto-increment).
  Changes are permanently saved.

Step 4: db.refresh(db_user)
  After commit, db_user.id is still None in Python's memory.
  db.refresh() runs: SELECT * FROM users WHERE id=1
  Now db_user has: id=1, created_at=..., is_active=True
  This is necessary because PostgreSQL generated some values (id, created_at).

Step 5: return db_user
  Returns the complete User object with all database-assigned values.
  FastAPI applies UserResponse schema to filter it.
```

**Why db.refresh() after commit?**

```
PostgreSQL generates:
  id = 1 (auto-increment)
  created_at = 2026-07-10 10:30:00 (database default)
  is_active = True (database default)

After commit(), SQLAlchemy's local cache doesn't automatically have these.
db.refresh(db_user) syncs the object with the actual database state.
Without refresh(): db_user.id would still be None → 500 error when FastAPI tries to include it in UserResponse.
```

---

## get_users() — Explained

```python
def get_users(db: Session):
    return db.query(models.User).all()
```

```
db.query(models.User) → SELECT * FROM users
.all()                → fetch ALL rows as a list of User objects

Returns: [User(id=1, ...), User(id=2, ...), ...]
FastAPI applies list[UserResponse] to each object in the list.

For large tables, you'd add pagination:
  .offset(skip).limit(limit)
  → SELECT * FROM users LIMIT 10 OFFSET 20
```

---

## get_user() — Explained

```python
def get_user(db: Session, user_id: int):
    return (
        db.query(models.User)
        .filter(models.User.id == user_id)
        .first()
    )
```

```
db.query(models.User)        → SELECT * FROM users
.filter(models.User.id == 1) → WHERE id = 1
.first()                     → LIMIT 1 → returns ONE User object or None

Why .first() not .one()?
  .first() → returns None if not found (safe)
  .one()   → raises an exception if not found or multiple found

In the endpoint, we check:
  if user is None:
      raise HTTPException(status_code=404, detail="User not found")
```

---

## update_user() — Explained

```python
def update_user(db, user_id, user: schemas.UserUpdate):
    db_user = get_user(db, user_id)   # Step 1: find it

    if not db_user:
        return None                   # Not found → endpoint raises 404

    if user.name is not None:         # Step 2: update only sent fields
        db_user.name = user.name

    if user.email is not None:
        db_user.email = user.email

    db.commit()                       # Step 3: save changes
    db.refresh(db_user)               # Step 4: sync with database

    return db_user
```

```
This is a PARTIAL UPDATE — PUT endpoint, but only updates what was sent.

Why check `if user.name is not None`?
  Client sends: {"name": "New Name"}  → email not sent → user.email = None
  Without the check: db_user.email = None → email erased!
  With the check: None means "don't touch this field"

SQLAlchemy tracks what changes:
  db_user.name = "New Name"
  → SQLAlchemy marks this as "dirty" (changed)
  db.commit()
  → UPDATE users SET name='New Name' WHERE id=1
  → Only changed fields are updated. Efficient.
```

---

## delete_user() — Explained

```python
def delete_user(db: Session, user_id: int):
    db_user = get_user(db, user_id)   # Step 1: find it

    if not db_user:
        return None                   # Not found

    db.delete(db_user)                # Step 2: mark for deletion
    db.commit()                       # Step 3: execute DELETE

    return db_user                    # Return what was deleted (for response)
```

```
db.delete(db_user)
  → Marks the object for deletion (not yet deleted)

db.commit()
  → Executes: DELETE FROM users WHERE id = 1

return db_user
  → We return the deleted user so the endpoint can confirm what was deleted
  → The endpoint returns: {"message": "User deleted successfully"}
  → (We don't use the returned object for the message, but it's good practice)
```

---

# SECTION 7 — MAIN.PY (ROUTES + DEPENDENCY INJECTION)

## The Complete File

```python
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import Base, engine, get_db

app = FastAPI()

# Create all database tables
Base.metadata.create_all(bind=engine)


@app.get("/")
def home():
    return {"message": "FastAPI + PostgreSQL working!"}


@app.post("/users", response_model=schemas.UserResponse)
def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db),
):
    return crud.create_user(db, user)


@app.get("/users", response_model=list[schemas.UserResponse])
def get_users(db: Session = Depends(get_db)):
    return crud.get_users(db)


@app.get("/users/{user_id}", response_model=schemas.UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
):
    user = crud.get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.put("/users/{user_id}", response_model=schemas.UserResponse)
def update_user(
    user_id: int,
    user: schemas.UserUpdate,
    db: Session = Depends(get_db),
):
    updated_user = crud.update_user(db, user_id, user)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user


@app.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
):
    deleted_user = crud.delete_user(db, user_id)
    if deleted_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}
```

---

## Base.metadata.create_all(bind=engine)

```python
Base.metadata.create_all(bind=engine)
```

```
This runs once when the server starts.
It generates and executes:

CREATE TABLE IF NOT EXISTS users (
    id         SERIAL PRIMARY KEY,
    name       VARCHAR(100) NOT NULL,
    email      VARCHAR(255) UNIQUE NOT NULL,
    is_active  BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP
);

"IF NOT EXISTS" means: only creates if the table doesn't already exist.
Safe to run on every startup.

IMPORTANT: create_all() does NOT update existing tables.
  If you add a new column to the User model and restart:
  create_all() sees the table exists → skips it → new column missing.
  Solution: Use Alembic for migrations (future day).
  Dev fix: DROP TABLE users; then restart → create_all recreates it.
```

---

## Dependency Injection — `Depends(get_db)`

```python
db: Session = Depends(get_db)
```

**The restaurant analogy:**

```
Customer orders pizza.
Does the chef bring flour from home? No.
The restaurant provides ingredients to the chef.
That's Dependency Injection: someone else provides what you need.
```

**Without Dependency Injection (BAD):**

```python
def create_user(user: schemas.UserCreate):
    db = SessionLocal()  # Every function creates its own session
    result = crud.create_user(db, user)
    db.close()           # Easy to forget!
    return result
# Problems:
# → Easy to forget db.close() → connection leak
# → Hard to test (can't inject a mock session)
# → Session not shared across the request
```

**With Dependency Injection (GOOD):**

```python
def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db),  # FastAPI provides this
):
    return crud.create_user(db, user)
# Benefits:
# → FastAPI opens AND closes the session automatically
# → Same session used throughout the request
# → Easy to test (inject a test session)
# → Clean code — endpoint focuses on business logic
```

**How Depends() works:**

```
When FastAPI sees: db: Session = Depends(get_db)

It does:
  1. Calls get_db()  (which is a generator)
  2. Runs up to the yield  → gets the session
  3. Passes session to your endpoint as db
  4. Your endpoint runs
  5. Resumes get_db() after yield
  6. Runs finally: db.close()

This happens for EVERY request automatically.
```

---

## HTTPException — Returning Errors

```python
from fastapi import HTTPException

if user is None:
    raise HTTPException(
        status_code=404,
        detail="User not found",
    )
```

```
HTTPException is how you return HTTP error responses in FastAPI.

status_code=404 → HTTP 404 Not Found
detail="User not found" → Goes into the response body as {"detail": "User not found"}

Common status codes:
  200 → OK (success, automatic for normal returns)
  201 → Created (use for resource creation)
  400 → Bad Request (client sent bad data)
  401 → Unauthorized (not logged in)
  403 → Forbidden (logged in but not allowed)
  404 → Not Found (resource doesn't exist)
  409 → Conflict (e.g., email already exists)
  422 → Unprocessable Entity (Pydantic validation failed — auto)
  500 → Internal Server Error (your code crashed)

raise vs return:
  raise HTTPException → immediately stops the function, sends error
  return user → normal success response
```

---

## All 5 Endpoints

```
Method  URL                  Body          Response
──────────────────────────────────────────────────────────────
GET     /                    —             {"message": "..."}
POST    /users               UserCreate    UserResponse
GET     /users               —             list[UserResponse]
GET     /users/{user_id}     —             UserResponse or 404
PUT     /users/{user_id}     UserUpdate    UserResponse or 404
DELETE  /users/{user_id}     —             {"message": "..."} or 404
```

---

# SECTION 8 — DEBUGGING: THE 500 ERROR

## What Happened

During testing, a 500 Internal Server Error appeared immediately after startup.

```
uvicorn main:app --reload
→ Server starts
→ Test POST /users
→ 500 Internal Server Error
```

## The Root Cause

```
An old `users` table existed from GuessWise (Day 41) with a DIFFERENT schema.

Old schema (GuessWise):
  users table:
    id, name, email, password (hashed), is_active, created_at

New schema (Day 45):
  users table:
    id, name, email, is_active, created_at (no password column)

Base.metadata.create_all() saw: "users table already exists → skip"
→ Table was NOT recreated with the new schema
→ SQLAlchemy's User model expected certain columns
→ They didn't match → 500 error
```

## The Fix (Development)

```sql
-- In pgAdmin or psql:
DROP TABLE users;

-- Then restart the server.
-- Base.metadata.create_all() recreates users with the new schema.
```

## The Real Lesson

```
create_all() only CREATES. Never MODIFIES.

The professional solution: Alembic (database migration tool)
  → Tracks schema changes
  → Generates SQL to migrate existing tables
  → Never needs to DROP tables
  → Safe in production

For now (development): dropping and recreating is acceptable.
In production: never drop tables — use Alembic migrations.
```

---

# SECTION 9 — COMPLETE TEST SESSION (SWAGGER)

## Open Swagger

```
http://127.0.0.1:8000/docs
```

## Test 1: Create User (POST /users)

```json
{
  "name": "Adyaprana",
  "email": "adya@gmail.com"
}
```

**Response:**

```json
{
  "name": "Adyaprana",
  "email": "adya@gmail.com",
  "id": 1,
  "is_active": true
}
```

Data is now in PostgreSQL. Restart the server → data still there.

## Test 2: Get All Users (GET /users)

```json
[
  {
    "name": "Adyaprana",
    "email": "adya@gmail.com",
    "id": 1,
    "is_active": true
  }
]
```

## Test 3: Get One User (GET /users/1)

```json
{
  "name": "Adyaprana",
  "email": "adya@gmail.com",
  "id": 1,
  "is_active": true
}
```

## Test 4: Get Non-Existent User (GET /users/999)

```json
{
  "detail": "User not found"
}
HTTP 404
```

## Test 5: Update User (PUT /users/1)

```json
{
  "name": "Adya Pradhan"
}
```

**Response:**

```json
{
  "name": "Adya Pradhan",
  "email": "adya@gmail.com",
  "id": 1,
  "is_active": true
}
```

Only name updated. Email unchanged.

## Test 6: Delete User (DELETE /users/1)

```json
{
  "message": "User deleted successfully"
}
HTTP 200
```

---

# SECTION 10 — REQUIREMENTS.TXT

```
fastapi
uvicorn
sqlalchemy
psycopg2-binary
email-validator
```

**Install all at once:**

```bash
pip install -r requirements.txt
```

**Why each package:**

```
fastapi        → the web framework
uvicorn        → the ASGI server
sqlalchemy     → the ORM (Python → SQL)
psycopg2-binary → PostgreSQL driver (Python → PostgreSQL protocol)
email-validator → enables EmailStr validation in Pydantic
```

---

# SECTION 11 — CONCEPTS LEARNED TODAY

## Dependency Injection

```
"Don't create your dependencies. Receive them."

Instead of: db = SessionLocal() inside every function
Use:        db: Session = Depends(get_db)

FastAPI provides the session. You use it. FastAPI cleans it up.
Same pattern used in Java (Spring), C# (.NET), Angular.
```

## The yield Pattern (Generator Dependencies)

```python
def get_db():
    db = SessionLocal()
    try:
        yield db      # Pause here, give db to endpoint
    finally:
        db.close()    # Always run this, even if endpoint throws exception
```

## Layered Architecture

```
Each layer has ONE responsibility:
  Routing:    main.py         (HTTP verbs, URLs, status codes)
  Validation: schemas.py      (input/output contracts)
  Logic:      crud.py         (database operations)
  Schema:     models.py       (table definitions)
  Config:     database.py     (connection, session)
```

## db.refresh() After Commit

```
After INSERT, PostgreSQL generates values (id, created_at).
db.refresh(obj) re-reads the row to get these generated values.
Without it: db_user.id = None → response error.
```

## from_attributes=True

```
Allows Pydantic to read from SQLAlchemy objects (attribute access).
Without it: Pydantic expects a dict. SQLAlchemy returns an object. Crash.
```

---

# SECTION 12 — INTERVIEW QUESTIONS

## Q1. What is SQLAlchemy ORM?

SQLAlchemy ORM (Object Relational Mapper) maps Python classes to database tables. You define a class with attributes (User with name, email), and SQLAlchemy automatically generates INSERT, SELECT, UPDATE, DELETE SQL. You work with Python objects instead of SQL strings, making code more maintainable and safer.

## Q2. What is the difference between engine, SessionLocal, and Session?

The Engine is the connection pool configuration — created once, shared by all requests. SessionLocal is a session factory — calling it creates a new Session. A Session is one active conversation with PostgreSQL — it tracks changes, executes queries, and manages a transaction.

## Q3. Why does get_db() use `yield` instead of `return`?

`yield` makes get_db() a generator function. FastAPI supports generator dependencies — it runs the function up to `yield`, gives the yielded value to the endpoint, runs the endpoint, then resumes the generator after `yield` to execute cleanup code (db.close()). With `return`, the cleanup code would never run, causing connection leaks.

## Q4. What does `Depends(get_db)` do?

It's FastAPI's Dependency Injection. When FastAPI sees `db: Session = Depends(get_db)` in a function signature, it calls get_db() for you, passes the yielded session as `db`, and ensures cleanup runs after the request. You don't manage session lifecycle — FastAPI does.

## Q5. What is the difference between SQLAlchemy models and Pydantic schemas?

SQLAlchemy models (models.py) represent database tables. They inherit from Base and define columns. They are used for database operations. Pydantic schemas (schemas.py) represent API data shapes. They inherit from BaseModel and define validation rules. They are used for request/response handling. The two have completely different purposes and should never be mixed.

## Q6. Why use `from_attributes=True` in UserResponse?

Without it, Pydantic expects a dict to create a model. But crud functions return SQLAlchemy model objects (not dicts). `from_attributes=True` tells Pydantic: "Read field values from object attributes (obj.name, obj.email) instead of dict keys." This enables SQLAlchemy objects to be directly converted to Pydantic response models.

## Q7. What does `create_all()` do and what are its limitations?

`Base.metadata.create_all(bind=engine)` generates `CREATE TABLE IF NOT EXISTS` SQL for every registered SQLAlchemy model and executes it. It only creates missing tables — it never modifies existing ones. If you add a column to a model, create_all() won't add it to the existing table. Production solution: use Alembic for database migrations.

## Q8. Why raise HTTPException instead of returning an error dict?

`raise HTTPException(status_code=404)` immediately stops the function and sends a proper HTTP error response with the correct status code. If you returned `{"error": "not found"}` the HTTP status would still be 200 (success), which misleads clients. HTTPException ensures the status code, headers, and body are all correct.

## Q9. Explain the full request lifecycle for POST /users.

Client sends POST /users with JSON body → Uvicorn receives HTTP request → FastAPI matches route → Pydantic validates JSON as UserCreate (422 if invalid) → FastAPI calls get_db() via Depends → Session is opened → create_user endpoint runs → crud.create_user() creates User model → db.add() stages INSERT → db.commit() executes INSERT → db.refresh() reads generated values → User object returned → FastAPI applies UserResponse schema (filters output) → Serialized to JSON → HTTP 200 response → Client → get_db() resumes, db.close() runs.

---

# SECTION 13 — LEETCODE #238: OPTIMAL SOLUTION (O(1) SPACE)

## The Previous Solution (Day 44 — O(n) extra space)

```python
# Day 44: used separate left[] and right[] arrays
left = []
right = [1] * len(nums)
# Extra space: O(n) for left + O(n) for right = O(2n)
```

## Today's Optimal Solution (O(1) extra space)

**Key Insight:** We can reuse the `answer` array to temporarily store left products, then multiply by a running right product in-place.

```python
class Solution(object):
    def productExceptSelf(self, nums):
        answer = [1] * len(nums)

        # PASS 1: Store left products in answer array
        for i in range(len(nums)):
            if i == 0:
                left_product = 1
            else:
                left_product *= nums[i - 1]
            answer[i] = left_product

        # PASS 2: Multiply by right product in-place
        for i in reversed(range(len(nums))):
            if i == len(nums) - 1:
                right_product = 1
            else:
                right_product *= nums[i + 1]
            answer[i] *= right_product

        return answer
```

## Complete Dry Run

```
nums = [1, 2, 3, 4]

PASS 1 (Left Products):
  answer = [1, 1, 1, 1]  (initialized)

  i=0: i==0 → left_product=1         answer=[1,1,1,1]
  i=1: left_product = 1×nums[0]=1×1=1  answer=[1,1,1,1]
  i=2: left_product = 1×nums[1]=1×2=2  answer=[1,1,2,1]
  i=3: left_product = 2×nums[2]=2×3=6  answer=[1,1,2,6]

After Pass 1:
  answer = [1, 1, 2, 6]  ← left products stored here

PASS 2 (Multiply by Right Products):
  Traverse reversed: 3 → 2 → 1 → 0

  i=3: i==len-1 → right_product=1
       answer[3] = 6×1 = 6           answer=[1,1,2,6]
       
  i=2: right_product = 1×nums[3]=1×4=4
       answer[2] = 2×4 = 8           answer=[1,1,8,6]
       
  i=1: right_product = 4×nums[2]=4×3=12
       answer[1] = 1×12 = 12         answer=[1,12,8,6]
       
  i=0: right_product = 12×nums[1]=12×2=24
       answer[0] = 1×24 = 24         answer=[24,12,8,6]

Return: [24, 12, 8, 6] ✅
```

## Why This Is Better

```
Day 44 Solution:
  left[]    → O(n) extra space
  right[]   → O(n) extra space
  answer[]  → required (doesn't count)
  Total extra: O(2n) = O(n)

Day 45 Optimal:
  answer[]  → reused for left products
  right_product  → one variable O(1)
  Total extra: O(1)

Same O(n) time complexity.
Halved the memory usage.
This is what interviewers want.
```

## The Two-Pass Pattern

```
Pass 1: Left products stored IN the answer array.
        (No separate left array needed)

Pass 2: Right product maintained in ONE variable.
        Multiply answer[i] by right_product in-place.
        (No separate right array needed)

Result: Same output. One array instead of three.
```

**Result:** ✅ Accepted | 24/24 test cases | Runtime: 43ms

---

# SECTION 14 — IMPORTANT THINGS TO KNOW

```
 1. DATABASE_URL format: dialect+driver://user:pass@host:port/dbname
    Never hardcode credentials in production. Use environment variables.

 2. create_engine() creates a connection pool, not a single connection.
    Connections are reused across requests for performance.

 3. sessionmaker() creates a Session FACTORY. Call it to get one Session.
    Session = one active database conversation.

 4. get_db() uses yield (generator) so FastAPI can clean up after use.
    The finally block runs even if the endpoint raises an exception.

 5. Base.metadata.create_all() only creates MISSING tables.
    It never modifies existing ones. Use Alembic to update existing tables.

 6. db.add() stages an INSERT. db.commit() executes it permanently.
    Without commit(): the INSERT is never saved.

 7. db.refresh(obj) syncs a Python object with its current database state.
    Required after INSERT to get PostgreSQL-generated values (id, created_at).

 8. from_attributes=True in Pydantic allows reading from SQLAlchemy objects.
    Without it: Pydantic can only read from dicts. SQLAlchemy returns objects.

 9. Depends(get_db) injects a managed session into your endpoint.
    FastAPI handles opening AND closing. You never call SessionLocal() directly.

10. SQLAlchemy models (Base subclasses) ≠ Pydantic schemas (BaseModel subclasses).
    Model = database table. Schema = API data contract. Never mix them.

11. raise HTTPException(status_code=404) stops the function immediately.
    If you return {"error": "..."} with status 200, clients are misled.

12. UserBase → shared base fields.
    UserCreate → input schema (has password when auth is added).
    UserUpdate → all Optional for partial updates.
    UserResponse → output schema (no password, has id).

13. For the update endpoint: only update fields that are NOT None.
    if user.name is not None: db_user.name = user.name
    This implements partial updates (PATCH-style even on PUT).

14. Alembic is the migration tool for SQLAlchemy.
    It tracks schema changes and generates ALTER TABLE SQL.
    Never use DROP TABLE in production — use Alembic.

15. Product Array O(1) space: use answer array for left products.
    Traverse reversed with a single right_product variable.
    Two passes, no extra arrays.
```

---

# REVISION SHEET

```
═══════════════════════════════════════════════════════════
FASTAPI DAY 45 — DATABASE INTEGRATION REVISION
═══════════════════════════════════════════════════════════

ARCHITECTURE:
  main.py → schemas.py → crud.py → models.py → database.py → PostgreSQL

DATABASE.PY:
  engine = create_engine(DATABASE_URL)         ← connection pool
  SessionLocal = sessionmaker(bind=engine)     ← session factory
  Base = declarative_base()                   ← model parent
  def get_db(): yield db                       ← session per request

MODELS.PY:
  class User(Base):
      __tablename__ = "users"
      id = Column(Integer, primary_key=True, index=True)
      name = Column(String(100), nullable=False)
      email = Column(String(255), unique=True, nullable=False)
      is_active = Column(Boolean, default=True)
      created_at = Column(DateTime, default=datetime.utcnow)

SCHEMAS.PY:
  UserBase     → name + email (shared)
  UserCreate   → inherits UserBase (POST body)
  UserUpdate   → all Optional (PATCH/PUT body)
  UserResponse → id + is_active + from_attributes=True

CRUD:
  create_user: db.add() → db.commit() → db.refresh()
  get_users:   db.query(User).all()
  get_user:    .filter(User.id==id).first()
  update_user: fetch → modify fields → commit → refresh
  delete_user: fetch → db.delete() → commit

MAIN.PY:
  Base.metadata.create_all(bind=engine)  ← on startup
  Depends(get_db)  ← inject session into endpoints
  HTTPException(status_code=404)  ← for not found

KEY CONCEPTS:
  ORM: Python objects → SQL (no raw SQL needed)
  DI: FastAPI provides session, you just use it
  from_attributes: Pydantic reads SQLAlchemy objects
  create_all: creates missing tables only
  Alembic: needed for schema changes in production

PRODUCT ARRAY OPTIMAL:
  answer = [1] * n
  Pass 1 (L→R): answer[i] = cumulative left product
  Pass 2 (R→L): answer[i] *= running right_product
  O(n) time, O(1) extra space
```

---

## LeetCode Solved This Day

| Problem | Difficulty | Topic | Status | Runtime |
|---------|-----------|-------|--------|---------|
| #238 Product of Array Except Self (Optimal) | Medium | Prefix Product + In-place O(1) space | ✅ Accepted 24/24 | 43ms |

---

*Day 45 Complete. FastAPI + PostgreSQL + SQLAlchemy all connected. First real persistent API built. Data survives restarts.* ✅
