# DAY 46 — JWT Authentication: Login System, Password Hashing & Protected Routes

> **Phase:** 02 — FastAPI Backend (Days 43–90)
>
> **Week:** W7 — FastAPI Core (Days 43–49)
>
> **Goal:** Build a complete JWT authentication system — register, login, hash passwords with bcrypt, generate and verify tokens, protect routes.
>
> **Install:** `pip install python-jose passlib bcrypt`
>
> **Status:** ✅ Day 46 Complete — Full authentication system working

---

# 🎯 Learning Roadmap

```
JWT Authentication — Login System

  ✅ pip install python-jose passlib bcrypt
  ✅ Understand JWT: header.payload.signature structure
  ✅ Hash passwords with bcrypt — never store plain passwords
  ✅ Create access token, verify token, protected routes
  ✅ OAuth2PasswordBearer — FastAPI's built-in auth scheme

  ▶ fastapi.tiangolo.com/tutorial/security/
  ▶ freeCodeCamp FastAPI full course — auth section
```

## Day 46 Checklist

- [ ] Explain Authentication vs Authorization from memory
- [ ] Explain why passwords must never be stored plain-text
- [ ] Explain hashing vs encryption (and why passwords use hashing)
- [ ] Explain the three parts of a JWT
- [ ] Write `hash_password()` and `verify_password()` from memory
- [ ] Write `create_access_token()` from memory
- [ ] Write `decode_access_token()` from memory
- [ ] Write the `/register` endpoint with email-duplicate check
- [ ] Write the `/login` endpoint using OAuth2PasswordRequestForm
- [ ] Write `get_current_user()` dependency
- [ ] Write a protected endpoint using `Depends(get_current_user)`
- [ ] Test the complete flow in Swagger: register → login → access protected route
- [ ] Explain `OAuth2PasswordBearer` and what it does NOT do

---

# SECTION 1 — BEFORE WRITING ANY CODE: THE ENGINEERING QUESTION

## Why Do We Need Authentication?

Until Day 45, your API had no security:

```
GET  /users        → Anyone can read all users
POST /users        → Anyone can create users
PUT  /users/1      → Anyone can edit any user
DELETE /users/1    → Anyone can delete any user
```

This is fine for learning. **Catastrophic for production.**

A real application needs to know:

```
Who is making this request?

GET /profile — who's profile?
PUT /users/5 — should this person be able to edit user 5?
DELETE /users/3 — is the caller an admin?
```

**Authentication answers: "Who are you?"**

---

## Authentication vs Authorization — The Airport Analogy

```
You enter an airport.

Security checks your passport.
They verify: "Is this person who they say they are?"
= AUTHENTICATION

After passing security, you walk toward the pilot's cockpit.
Guard says: "Your identity is verified — but you're not allowed in here."
= AUTHORIZATION

AUTHENTICATION → Identity → "Who are you?"
AUTHORIZATION  → Permission → "What are you allowed to do?"

Authentication ALWAYS comes first.
You cannot authorize someone whose identity is unverified.
```

---

# SECTION 2 — PASSWORD SECURITY: THE BIGGEST BEGINNER MISTAKE

## Never Store Plain Text Passwords

Suppose a user registers:

```json
{
  "email": "adya@gmail.com",
  "password": "mypassword123"
}
```

Should you save this to the database?

```
email    | password
──────────────────────────────
adya@... | mypassword123    ← NEVER DO THIS
```

**What happens when your database is leaked?**

```
Every user's password is exposed immediately.
Those passwords are likely reused on other sites.
Your users' Gmail, banking, and social accounts are compromised.
You face legal liability.
Your company reputation is destroyed.
```

This has happened to major companies. It is always catastrophic.

---

## What to Store Instead — Hashing

```
User sends:     mypassword123
                     ↓
              bcrypt hash function
                     ↓
Database stores: $2b$12$L3CjP2lD...Xqm8

The original password is NEVER stored.
The database only sees the hash.
Even developers cannot recover the password.
```

---

## Hashing vs Encryption — Critical Distinction

```
ENCRYPTION (reversible):
  Original → Encrypt with key → Encrypted value
  Encrypted value → Decrypt with key → Original

  Used for: storing credit card numbers, API keys
  Can be reversed if you have the key.

HASHING (one-way, irreversible):
  Password → Hash function → Hash value
  Hash value → ??? → IMPOSSIBLE to reverse

  Used for: passwords
  Cannot be reversed. Ever.
  Even with the hash, you cannot get the original password back.

PASSWORDS MUST ALWAYS BE HASHED. NOT ENCRYPTED.
```

**Why?** If encryption is used for passwords and the encryption key is leaked, ALL passwords are exposed. With hashing, there is nothing to leak that gives back the originals.

---

## Why bcrypt (Not Python's Built-in `hash()`)?

```python
# Python's built-in hash() — DO NOT USE FOR PASSWORDS
hash("mypassword")   # → Some integer

Problems:
  → Changes between Python versions and program runs
  → Designed for hash tables, NOT security
  → Extremely fast (attackers can test billions per second)
  → Not salted (same password always produces same hash)
```

**Why bcrypt is the industry standard:**

```
1. DESIGNED for passwords — not a general hash function
2. SLOW by design — makes brute-force attacks expensive
3. AUTOMATIC SALT — same password produces different hash every time
4. COST FACTOR — you can make it slower as hardware improves
5. TRUSTED — used by Facebook, GitHub, banks, and thousands of companies

bcrypt cost factor 12 → 0.3 seconds per hash
Attacker tests 1 billion passwords → 300,000,000 seconds → ~9.5 years
```

---

## The Salt — Why Two Users Get Different Hashes

```
User A: password = "password123"
User B: password = "password123"

WITHOUT salt:
  Both produce: $2b$same_hash_here
  Attacker sees two identical hashes → knows two users share a password
  Precomputed lookup table (rainbow table) can crack both at once

WITH salt (bcrypt auto-adds this):
  User A gets: $2b$12$XgM5yW...UNIQUE_SALT...A
  User B gets: $2b$12$PqK3mN...DIFFERENT_SALT...B
  Same password → completely different hashes
  Rainbow table attack fails completely
```

bcrypt handles salt automatically. You never need to manage it.

---

# SECTION 3 — WHAT IS JWT?

## Definition

JWT = JSON Web Token.

A digitally signed string that proves a user has authenticated.

```
After login, client receives a token.
Instead of sending email+password with every request,
the client sends this token.
Server verifies the token — no database lookup needed (usually).
```

**The movie ticket analogy:**

```
Cinema doesn't remember every visitor.
You show your ticket at the door.
If ticket is valid → you enter.

JWT is your digital ticket.
Issue once at login.
Present on every protected request.
```

---

## JWT Structure: Three Parts

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9
        .
eyJzdWIiOiJhZHlhQGdtYWlsLmNvbSIsImV4cCI6MTc4MjAwMDAwMH0
        .
f2M8_XqZlVoQhI-k4xRHMLJdPqWJMHPBP9LoZY7yvLQ

PART 1: Header
PART 2: Payload
PART 3: Signature

Separated by dots.
```

### Part 1 — Header

```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```

```
alg: "HS256" → HMAC-SHA256 signing algorithm
typ: "JWT"   → token type

This is Base64-encoded (not encrypted — anyone can decode it).
It tells the server which algorithm was used to sign the token.
```

### Part 2 — Payload (Claims)

```json
{
  "sub": "adya@gmail.com",
  "user_id": 1,
  "exp": 1782000000
}
```

```
sub: "subject" — who this token represents (usually email or user_id)
exp: expiration timestamp (Unix epoch time)
     After this time, the token is invalid

IMPORTANT: The payload is Base64-encoded, NOT encrypted.
           Anyone who has the token can decode and read the payload.
           NEVER put passwords, credit cards, or sensitive data in the payload.
           Only put identifiers (email, user_id).
```

### Part 3 — Signature

```
HMAC-SHA256(
    base64(Header) + "." + base64(Payload),
    SECRET_KEY
)
```

```
The signature is what makes JWT secure.

Server combines Header + Payload and signs with a SECRET_KEY.
Result: unique cryptographic signature.

When client sends the token:
  Server recalculates the signature from Header + Payload
  Compares with the signature in the token
  If they match → token is genuine (not tampered)
  If they don't match → token was modified → REJECTED

Client cannot:
  → Change user_id from 1 to 999
    (signature would no longer match → rejected)
  → Change expiration to future date
    (signature changes → rejected)
  → Create a fake token
    (they don't have SECRET_KEY → can't sign correctly)
```

---

## Why Tokens Expire

```
If tokens never expired:

  Someone steals a token from a packet sniffer.
  They use it forever.
  User changes password — token still works!
  No way to revoke it.

With expiration (30 minutes):

  Token stolen.
  Attacker uses it for up to 30 minutes.
  After 30 minutes: token rejected.
  Damage is limited.

Short-lived access tokens are a security best practice.
Longer-lived refresh tokens are used for "stay logged in" features.
```

---

# SECTION 4 — THE COMPLETE AUTHENTICATION FLOW

```
REGISTRATION:
Client → POST /register → {name, email, password}
                ↓
        Pydantic validates (min_length, email format)
                ↓
        Check if email already exists (400 if it does)
                ↓
        hash_password(password) → $2b$12$...
                ↓
        User(name, email, hashed_password) → db.add() → db.commit()
                ↓
        Return UserResponse (id, name, email — NO password)


LOGIN:
Client → POST /login → {username: "adya@gmail.com", password: "secret"}
                ↓
        OAuth2PasswordRequestForm parses the form data
                ↓
        get_user_by_email(email) → User from database
                ↓
        verify_password(plain, hashed) → True/False
                ↓ (True)
        create_access_token({"sub": user.email}) → JWT string
                ↓
        Return {"access_token": "eyJ...", "token_type": "bearer"}


PROTECTED REQUEST:
Client → GET /users + Authorization: Bearer eyJ...
                ↓
        OAuth2PasswordBearer extracts token from header
                ↓
        Depends(get_current_user) runs:
          decode_access_token(token) → payload {"sub": "adya@gmail.com"}
          get_user_by_email(payload["sub"]) → User object
                ↓
        User passed to endpoint as current_user
                ↓
        Endpoint executes with verified identity
```

---

# SECTION 5 — COMPLETE PROJECT STRUCTURE

```
backend-learning/
│
├── main.py           ← App entry point + router registration
├── database.py       ← Engine, Session, Base, ensure_schema(), get_db()
├── models.py         ← SQLAlchemy ORM models (users table)
├── schemas.py        ← Pydantic validation models
├── crud.py           ← Database operations (pure data logic)
├── security.py       ← Password hashing + JWT functions
│
└── routers/
    ├── auth.py       ← /register, /login, get_current_user
    └── users.py      ← Protected /users CRUD endpoints
```

---

# SECTION 6 — THE COMPLETE CODE (EVERY FILE)

## requirements.txt

```
fastapi
uvicorn
sqlalchemy
psycopg2-binary
email-validator
python-jose
passlib
bcrypt
```

```bash
pip install -r requirements.txt
```

---

## database.py — Connection + Schema Migration

```python
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "postgresql+psycopg2://postgres:postgres123@localhost:5432/backend_journey"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()


def ensure_schema():
    """
    Apply lightweight dev migrations that create_all() cannot handle.
    create_all() creates new tables but never alters existing ones.
    """
    inspector = inspect(engine)

    if not inspector.has_table("users"):
        return

    columns = {col["name"] for col in inspector.get_columns("users")}

    if "hashed_password" not in columns:
        with engine.begin() as conn:
            conn.execute(
                text(
                    "ALTER TABLE users "
                    "ADD COLUMN hashed_password VARCHAR NOT NULL DEFAULT ''"
                )
            )


def get_db():
    """Provide a database session for each request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### `ensure_schema()` — The Problem It Solves

```
Day 45: User model had no password column.
Day 46: We added hashed_password to the model.

create_all() behavior:
  → If 'users' table doesn't exist: creates it with hashed_password ✅
  → If 'users' table EXISTS from Day 45: SKIPS IT ← the problem

Result: table exists but is missing hashed_password column.
Every INSERT fails with "column does not exist".

ensure_schema() solution:
  → Inspect the existing table
  → Check if 'hashed_password' column exists
  → If not: run ALTER TABLE to add it
  → This bridges the gap between old schema and new model

In production: use Alembic migrations instead.
In development: this lightweight approach is acceptable.
```

---

## models.py — User Table with Password Column

```python
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), nullable=False)

    email = Column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )

    # Store the hash only — never the plain password
    hashed_password = Column(
        String,
        nullable=False,
    )

    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.utcnow)
```

**The key addition — `hashed_password`:**

```python
hashed_password = Column(String, nullable=False)

# Column name: hashed_password — NOT password
# This naming convention FORCES the developer to remember:
#   "This stores a hash, NOT a plain password"

# nullable=False → every user MUST have a password
# String (no length) → VARCHAR in PostgreSQL, unlimited length
#   bcrypt hashes are always 60 characters, but leaving it
#   unlimited is safer if we ever change algorithms

# NEVER:
password = Column(String, nullable=False)        # misleading name
plain_password = Column(String, nullable=False)  # catastrophically wrong concept
```

---

## schemas.py — All Validation Schemas

```python
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    name: str = Field(min_length=3, max_length=100)
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(min_length=8)
    # Now includes password — user must provide it during registration
    # Note: password is NOT in UserResponse — it's never returned


class UserUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=3, max_length=100)
    email: Optional[EmailStr] = None


class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    is_active: bool
    # hashed_password is NOT here — it never reaches the client


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
```

### The Schema Hierarchy

```
UserBase                  → shared: name + email
  └── UserCreate          → adds: password (POST /register body)
  └── UserResponse        → adds: id + is_active (what API returns)
                            NOTE: no password here!

UserUpdate                → all Optional (PATCH body)

Token                     → what /login returns
    access_token: str
    token_type: "bearer"
```

### Why `password` Is in `UserCreate` but Not `UserResponse`

```
Client SENDS:                    Client RECEIVES:
{                                {
  "name": "Adyaprana",             "id": 1,
  "email": "adya@gmail.com",       "name": "Adyaprana",
  "password": "secret123"          "email": "adya@gmail.com",
}                                  "is_active": true
                                 }
                                 (NO password. NEVER.)

Client sends password once during registration.
Server hashes it, stores the hash.
Password never leaves the server again.
```

---

## security.py — The Security Toolbox

```python
from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "change-this-to-a-long-random-secret-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    if not hashed_password:
        return False
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(
    data: dict,
    expires_delta: timedelta | None = None,
) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta
        if expires_delta is not None
        else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> dict | None:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None
```

### Every Line Explained

**`CryptContext` — the password hashing manager:**

```python
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# CryptContext is passlib's abstraction layer.
# schemes=["bcrypt"] → use bcrypt for hashing
# deprecated="auto"  → auto-handle old hash formats during upgrades

# Why not call bcrypt directly?
# If you change from bcrypt to argon2 in the future:
#   Direct bcrypt: change every single hash/verify call
#   CryptContext:  change one line here → everything updates
```

**`SECRET_KEY` — the signing secret:**

```python
SECRET_KEY = "change-this-to-a-long-random-secret-in-production"

# This is used to sign and verify JWTs.
# Anyone with this key can create valid tokens.
# MUST be kept secret. NEVER commit to GitHub.

# In production:
import os
SECRET_KEY = os.getenv("SECRET_KEY")

# Generate a strong secret:
# python -c "import secrets; print(secrets.token_hex(32))"
```

**`hash_password()`:**

```python
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# "secret123" → "$2b$12$L3CjP2lD...abc"
# bcrypt automatically:
#   1. Generates a random salt
#   2. Applies the cost factor (12 rounds by default)
#   3. Combines salt + password + hashing → output
#   4. Encodes everything into the $2b$12$... format
# The salt is stored inside the hash string itself.
```

**`verify_password()`:**

```python
def verify_password(plain_password: str, hashed_password: str) -> bool:
    if not hashed_password:
        return False
    return pwd_context.verify(plain_password, hashed_password)

# pwd_context.verify() does:
#   1. Extract the salt from the stored hash
#   2. Hash the plain_password using that same salt
#   3. Compare the result to the stored hash
#   4. Return True if they match, False otherwise

# The plain_password is NEVER compared directly to the stored hash.
# Salt extraction is automatic — you don't manage it.

# Guard: if not hashed_password: return False
# Protects against users without passwords (edge case from Day 45 migration)
```

**`create_access_token()`:**

```python
def create_access_token(
    data: dict,                        # {"sub": "adya@gmail.com"}
    expires_delta: timedelta | None = None,
) -> str:
    to_encode = data.copy()            # Don't modify the original dict
    expire = datetime.now(timezone.utc) + (
        expires_delta
        if expires_delta is not None
        else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})  # Add expiration to payload
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# data.copy() — never mutate the caller's dict
# datetime.now(timezone.utc) — always use UTC for consistency
# "exp" claim — JWT standard expiration key
# jwt.encode() — signs Header + Payload with SECRET_KEY
# Returns: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIi..."
```

**`decode_access_token()`:**

```python
def decode_access_token(token: str) -> dict | None:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None

# jwt.decode() does THREE things:
#   1. Verifies the signature (Header + Payload matches SECRET_KEY)
#   2. Checks expiration (raises JWTError if expired)
#   3. Returns the payload dict if everything is valid

# If anything fails → JWTError is raised → we catch it → return None
# Caller checks: if payload is None: raise 401

# JWTError covers:
#   → Invalid signature (token was tampered)
#   → Token expired
#   → Malformed token
#   → Wrong algorithm
```

---

## crud.py — Database Operations (With Password Handling)

```python
from sqlalchemy.orm import Session

import models
import schemas
from security import hash_password


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        name=user.name,
        email=user.email,
        hashed_password=hash_password(user.password),  # Hash here
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_users(db: Session):
    return db.query(models.User).all()


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def update_user(db: Session, user_id: int, user: schemas.UserUpdate):
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

### Key Changes from Day 45

**`create_user()` now hashes the password:**

```python
db_user = models.User(
    name=user.name,
    email=user.email,
    hashed_password=hash_password(user.password),  # ← NEW
)

# user.password comes from UserCreate schema (plain text from client)
# hash_password() converts it to a bcrypt hash
# The hash is stored, the plain password is discarded immediately
# user.password never reaches the database
```

**`get_user_by_email()` is new:**

```python
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

# Required for login: user identifies themselves by email
# Required for registration: check if email already taken
# Different from get_user() which searches by id
```

---

## routers/auth.py — Registration, Login, get_current_user

```python
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import get_db
from security import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_access_token,
    decode_access_token,
    verify_password,
)

router = APIRouter(tags=["auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> models.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception

    email: str | None = payload.get("sub")
    if email is None:
        raise credentials_exception

    user = crud.get_user_by_email(db, email)
    if user is None:
        raise credentials_exception

    return user


@router.post(
    "/register",
    response_model=schemas.UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = crud.get_user_by_email(db, user.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    return crud.create_user(db, user)


@router.post("/login", response_model=schemas.Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = crud.get_user_by_email(db, form_data.username)

    if user is None or not verify_password(
        form_data.password,
        user.hashed_password,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    return schemas.Token(access_token=access_token)
```

### `OAuth2PasswordBearer` — What It Does and Does NOT Do

```python
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

# WHAT IT DOES:
#   → Tells FastAPI: "This API uses Bearer token authentication"
#   → Adds an "Authorize" button to Swagger UI at /docs
#   → Extracts the token string from Authorization: Bearer <token> header
#   → Makes the token available as a string to endpoints that depend on it

# WHAT IT DOES NOT DO:
#   → Does NOT verify the token
#   → Does NOT authenticate the user
#   → Does NOT check the database
#   → Does NOT decode the JWT
#   → It is PURELY a token extractor

# It's like an envelope opener.
# It opens the envelope (Authorization header) and gives you the letter (token).
# Whether the letter is valid is up to get_current_user() to decide.
```

### `get_current_user()` — The Authentication Dependency

```python
def get_current_user(
    token: str = Depends(oauth2_scheme),   # Get token from header
    db: Session = Depends(get_db),          # Get database session
) -> models.User:

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Step 1: Decode the JWT
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception
    # None means: expired, tampered, invalid signature, or malformed

    # Step 2: Extract the user identifier from payload
    email: str | None = payload.get("sub")
    if email is None:
        raise credentials_exception
    # "sub" was set in create_access_token({"sub": user.email})

    # Step 3: Verify user still exists in database
    user = crud.get_user_by_email(db, email)
    if user is None:
        raise credentials_exception
    # User might have been deleted after token was issued

    return user
    # This User object is injected into every protected endpoint
```

**Why `credentials_exception` is defined once (not repeated 3 times):**

```python
# All three failure cases return the same 401 response.
# We DON'T tell the client WHICH check failed.
# Security principle: don't reveal why authentication failed.
# "Invalid token" reveals nothing about your system.
# "Token expired" reveals when it was issued.
# "User not found" reveals you have a user lookup.
# Generic message: more secure.
```

**Why we look up the user from the database (not just trust the JWT):**

```python
user = crud.get_user_by_email(db, email)

# We could just trust the email from the JWT payload.
# Why do we look it up again?
#
# Scenario: User account deleted after token was issued.
# If we trust JWT: deleted user can still access the API until token expires.
# If we check DB: deleted user gets 401 immediately.
#
# Scenario: User deactivated/banned.
# If we trust JWT: banned user keeps access.
# If we check DB: we can check is_active and return 401.
#
# Database lookup cost (one SELECT): ~1ms. Worth it for correctness.
```

### `/register` Endpoint

```python
@router.post(
    "/register",
    response_model=schemas.UserResponse,
    status_code=status.HTTP_201_CREATED,   # 201 Created, not 200 OK
)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = crud.get_user_by_email(db, user.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,    # 409 Conflict also valid
            detail="Email already registered",
        )
    return crud.create_user(db, user)
```

```
Registration flow:
  1. Pydantic validates: name ≥ 3 chars, valid email, password ≥ 8 chars
  2. Check if email already exists → 400 if so
  3. crud.create_user() → hash password → INSERT → db.commit()
  4. Return UserResponse (id, name, email, is_active — NO password)

Why 201 instead of 200?
  200 OK: request processed, resource existed
  201 Created: a new resource was created
  Semantically correct for POST /register
```

### `/login` Endpoint

```python
@router.post("/login", response_model=schemas.Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = crud.get_user_by_email(db, form_data.username)

    if user is None or not verify_password(
        form_data.password,
        user.hashed_password,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    return schemas.Token(access_token=access_token)
```

**`OAuth2PasswordRequestForm`:**

```python
form_data: OAuth2PasswordRequestForm = Depends()

# This special form expects x-www-form-urlencoded content (not JSON).
# It provides:
#   form_data.username  ← the email (confusingly named "username" by OAuth2 spec)
#   form_data.password  ← the password

# In Swagger (/docs):
# Clicking "Authorize" opens a dialog asking for username and password.
# This is why the Swagger docs say "username" — it's the OAuth2 standard.
# Your users type their EMAIL in the username field.
```

**Security: Combine user-not-found and wrong-password into one check:**

```python
if user is None or not verify_password(form_data.password, user.hashed_password):
    raise HTTPException(status_code=401, ...)

# WRONG approach (insecure):
if user is None:
    raise HTTPException(detail="User not found")  # reveals email existence
if not verify_password(...):
    raise HTTPException(detail="Wrong password")  # reveals email is valid

# Attacker could enumerate which emails are registered.
# Combined check: "Incorrect email or password" reveals nothing.
```

---

## routers/users.py — Protected CRUD Routes

```python
"""
User CRUD routes — all protected by JWT.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import get_db
from routers.auth import get_current_user

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=schemas.UserResponse, status_code=201)
def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),   # ← Protected
):
    existing = crud.get_user_by_email(db, user.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db, user)


@router.get("", response_model=list[schemas.UserResponse])
def get_users(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),   # ← Protected
):
    return crud.get_users(db)


@router.get("/{user_id}", response_model=schemas.UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),   # ← Protected
):
    user = crud.get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}", response_model=schemas.UserResponse)
def update_user(
    user_id: int,
    user: schemas.UserUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),   # ← Protected
):
    updated_user = crud.update_user(db, user_id, user)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user


@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),   # ← Protected
):
    deleted_user = crud.delete_user(db, user_id)
    if deleted_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}
```

### How `Depends(get_current_user)` Protects Every Endpoint

```python
current_user: models.User = Depends(get_current_user)

# When FastAPI sees this dependency:
#   1. OAuth2PasswordBearer extracts token from Authorization header
#      → If no header: 401 Unauthorized immediately
#   2. get_current_user() runs:
#      → decode_access_token() checks signature + expiration
#      → get_user_by_email() verifies user still exists
#      → If anything fails: 401 Unauthorized
#   3. Only if everything passes: endpoint function runs

# The endpoint never runs unless authentication succeeds.
# current_user is the verified User object from the database.
# You can use it inside the endpoint:
#   print(current_user.name)
#   check if current_user.id == user_id (ownership check)
```

---

## main.py — Application Entry Point

```python
from fastapi import FastAPI

import models  # noqa: F401 — ensure models are registered with Base
from database import Base, engine, ensure_schema
from routers import auth, users

app = FastAPI(
    title="Backend Learning API",
    description="FastAPI + PostgreSQL with JWT authentication",
)

ensure_schema()                          # Fix missing hashed_password column
Base.metadata.create_all(bind=engine)   # Create tables if they don't exist

app.include_router(auth.router)         # /register, /login
app.include_router(users.router)        # /users (all protected)


@app.get("/")
def home():
    return {
        "message": "FastAPI + PostgreSQL working!",
        "docs": "/docs",
        "steps": [
            "POST /register with name, email, password",
            "Click Authorize in /docs — email goes in username, then password",
            "Call protected /users routes",
        ],
    }
```

**`import models  # noqa: F401`:**

```python
# models.py defines class User(Base).
# Base.metadata only knows about User if models.py has been imported.
# If models.py is never imported, create_all() creates NO tables.
# This import ensures models are registered before create_all() runs.
# noqa: F401 tells linters: "I know this import isn't used directly —
#              it's intentional for its side effect (registering models)."
```

---

# SECTION 7 — THE COMPLETE FLOW: TEST IN SWAGGER

## Step 1: Start the Server

```bash
python -m uvicorn main:app --reload
```

## Step 2: Open Swagger

```
http://127.0.0.1:8000/docs
```

## Step 3: Register a User

```
POST /register
{
  "name": "Adyaprana",
  "email": "adya@gmail.com",
  "password": "secret123"
}
```

**Response (201 Created):**

```json
{
  "name": "Adyaprana",
  "email": "adya@gmail.com",
  "id": 1,
  "is_active": true
}
```

Password NOT in response. bcrypt hash stored in database.

## Step 4: Try Protected Route Without Token

```
GET /users
```

**Response (401):**

```json
{
  "detail": "Not authenticated"
}
```

Good. Route is protected.

## Step 5: Login

```
POST /login
username: adya@gmail.com
password: secret123
```

**Response (200):**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

## Step 6: Authorize in Swagger

Click the **Authorize** button (lock icon) in Swagger UI.
Enter username = `adya@gmail.com`, password = `secret123`.
Click Authorize. Swagger now includes the Bearer token automatically.

## Step 7: Access Protected Route

```
GET /users
```

**Response (200):**

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

**The complete flow works.**

---

# SECTION 8 — COMPLETE REQUEST LIFECYCLE (DAY 46)

```
Browser
   │
   │ POST /users (Authorization: Bearer eyJ...)
   ▼
Uvicorn (parses HTTP, forwards to FastAPI)
   │
   ▼
FastAPI matches route: GET /users → get_users()
   │
   ▼
Dependency Resolution (before endpoint runs):
  Depends(get_db) → SessionLocal() → db session
  Depends(get_current_user):
    Depends(oauth2_scheme) → extracts "eyJ..." from header
    decode_access_token("eyJ..."):
      → Verify signature with SECRET_KEY
      → Check exp claim (not expired)
      → Return payload {"sub": "adya@gmail.com"}
    get_user_by_email(db, "adya@gmail.com") → User object
   │
   ▼ (all dependencies resolved successfully)
get_users(db=..., current_user=User(id=1, name="Adya", ...))
   │
   ▼
crud.get_users(db) → SELECT * FROM users → [User, User, ...]
   │
   ▼
FastAPI applies list[UserResponse] response_model
  → filters each User through UserResponse
  → removes hashed_password
   │
   ▼
Serialize to JSON
   │
   ▼
HTTP 200 + JSON → Browser
   │
   ▼
get_db() resumes after yield → db.close()
```

---

# SECTION 9 — CONCEPTS LEARNED TODAY

## Security Architecture — "Defence in Depth"

```
Layer 1 (Pydantic): password must be ≥ 8 characters
Layer 2 (bcrypt):   password is hashed before storage
Layer 3 (JWT):      token signed with SECRET_KEY
Layer 4 (get_current_user): token decoded, expiration checked, user verified
Layer 5 (response_model):   hashed_password never returned to client
```

Every layer protects independently. If one fails, others still protect.

## Stateless Authentication

```
Traditional (session-based):
  Login → Server creates session in memory → Client gets session_id cookie
  Every request → Server looks up session → Expensive at scale

JWT (stateless):
  Login → Server creates signed JWT → Client stores it
  Every request → Server VERIFIES JWT signature (no DB lookup usually)
  → Scales horizontally (any server can verify, no shared state)
```

## The Sub Claim

```python
# "sub" = subject = who the token is about
create_access_token(data={"sub": user.email})

# Later:
email = payload.get("sub")

# JWT standard: "sub" is the canonical claim for user identity.
# We use email as the subject — unique and human-readable.
# Alternative: use user.id (integer) for slightly faster DB lookup.
```

---

# SECTION 10 — IMPORTANT THINGS TO KNOW

```
 1. Authentication = "Who are you?"
    Authorization = "What are you allowed to do?"

 2. Never store plain-text passwords. Ever.
    hash_password() converts → irreversible bcrypt hash.

 3. Hashing ≠ Encryption.
    Encryption can be reversed. Hashing cannot.
    Passwords must be HASHED.

 4. bcrypt is slow by design. This prevents brute-force attacks.
    Python's hash() is fast — never use it for passwords.

 5. bcrypt adds salt automatically. Same password → different hash every time.

 6. JWT = Header.Payload.Signature (three parts, dot-separated).
    Payload is Base64-encoded (NOT encrypted) — anyone can decode it.
    Never put passwords or sensitive data in JWT payload.

 7. OAuth2PasswordBearer only EXTRACTS the token from the header.
    It does NOT verify or authenticate. That's get_current_user()'s job.

 8. OAuth2PasswordRequestForm uses "username" field even for email.
    This is the OAuth2 specification standard.

 9. SECRET_KEY must NEVER be hardcoded in production.
    Use environment variables. Never commit it to GitHub.

10. Token expiration limits damage if a token is stolen.
    30-minute access tokens are common.

11. Combine "user not found" and "wrong password" into one error message.
    "Incorrect email or password" — never reveal which one failed.

12. get_current_user() should verify the user still exists in the database.
    JWT payload can outlive the user's account.

13. ensure_schema() is a development workaround for create_all() limitations.
    Production: use Alembic for migrations.

14. import models (even if unused) is required so Base.metadata knows about tables.
    Without it: create_all() creates no tables.

15. 201 Created is the correct status code for successful resource creation.
    Use status.HTTP_201_CREATED for POST /register.
```

---

# SECTION 11 — INTERVIEW QUESTIONS

## Q1. What is the difference between authentication and authorization?

Authentication answers "Who are you?" — verifying identity (login). Authorization answers "What are you allowed to do?" — checking permissions (admin vs regular user). Authentication always happens first; you cannot authorize an unidentified request.

## Q2. Why do we hash passwords instead of encrypting them?

Encryption is reversible — if the encryption key is stolen, all passwords are exposed. Hashing is one-way — even with the hash, you cannot recover the original password. If the database is compromised, hashed passwords are useless to the attacker (assuming a strong algorithm like bcrypt). Passwords should always be hashed, never encrypted.

## Q3. What are the three parts of a JWT?

Header (algorithm metadata), Payload (claims — user email, expiration), Signature (HMAC of Header + Payload using SECRET_KEY). Only the signature provides security. The header and payload are Base64-encoded and readable by anyone — never store sensitive data in the payload.

## Q4. What does `OAuth2PasswordBearer` do?

It is a FastAPI dependency that extracts the Bearer token from the `Authorization: Bearer <token>` HTTP header. It does NOT verify the token, decode it, or authenticate the user. It is purely a string extractor. The actual token verification happens in `get_current_user()`.

## Q5. What does `get_current_user()` do step by step?

It receives the token from `oauth2_scheme`, calls `decode_access_token()` which verifies the JWT signature and expiration, extracts the `sub` (email) from the payload, looks up the user in the database, and returns the User object. If any step fails, it raises 401 Unauthorized. It is used as `Depends(get_current_user)` in every protected endpoint.

## Q6. Why does the login endpoint combine "user not found" and "wrong password" into one error?

If separate errors were returned, an attacker could enumerate which email addresses are registered in your system (user not found = this email doesn't exist; wrong password = this email exists). Combining them into "Incorrect email or password" prevents this information disclosure attack.

## Q7. Why do JWT tokens expire?

If tokens were permanent and one was stolen (e.g., XSS, packet sniffing), the attacker could use it forever. With expiration (typically 30 minutes), the damage is time-limited. The user re-authenticates and gets a new token. The stolen token becomes useless after expiration.

## Q8. Why does `get_current_user()` look up the user in the database instead of just trusting the JWT?

The JWT contains an email, but the user might have been deleted, deactivated, or banned after the token was issued. Trusting only the JWT would allow deleted users to keep accessing the API until their token expires. Checking the database ensures the user still exists and is valid on every protected request.

---

# REVISION SHEET

```
═══════════════════════════════════════════════════════════
JWT AUTHENTICATION — DAY 46 REVISION
═══════════════════════════════════════════════════════════

INSTALL:
  pip install python-jose passlib bcrypt

AUTHENTICATION FLOW:
  Register: name+email+password → hash password → store user
  Login:    email+password → verify hash → return JWT
  Protected: Bearer token → decode → verify → inject current_user

JWT STRUCTURE:
  Header.Payload.Signature
  Header: algorithm metadata
  Payload: {"sub": email, "exp": timestamp} — NOT encrypted
  Signature: HMAC(header+payload, SECRET_KEY) — proves authenticity

SECURITY.PY FUNCTIONS:
  hash_password(pw)           → bcrypt hash string
  verify_password(plain, hash) → True/False
  create_access_token(data, expires) → JWT string
  decode_access_token(token)  → dict or None

KEY CONCEPTS:
  OAuth2PasswordBearer   → extracts token from header (not authenticator)
  OAuth2PasswordRequestForm → form data (username field = email)
  get_current_user()     → decode JWT + verify user in DB → inject
  Depends(get_current_user) → protects any endpoint

ERROR RULES:
  Combine "not found" + "wrong password" → "Incorrect email or password"
  Never reveal which check failed (information disclosure)
  Use status.HTTP_401_UNAUTHORIZED for auth failures

SECURITY PRINCIPLES:
  ❌ Never store plain passwords
  ❌ Never put sensitive data in JWT payload
  ❌ Never hardcode SECRET_KEY
  ✅ Always hash with bcrypt
  ✅ Always set token expiration
  ✅ Always use environment variables for secrets
  ✅ Separate security.py from business logic

BCRYPT:
  Slow by design (brute-force resistance)
  Auto-generates salt (same password → different hash)
  Salt embedded in hash string (no separate storage needed)
  Industry standard for password hashing
```

---

*Day 46 Complete. JWT authentication system fully working. Register → Login → Protected routes. Backend security fundamentals mastered.* ✅

