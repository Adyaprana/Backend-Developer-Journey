# DAY 44 — Pydantic Models: Request/Response Validation + LeetCode Prefix Products

> **Phase:** 02 — FastAPI Backend (Days 43–90)
>
> **Week:** W7 — FastAPI Core (Days 43–49)
>
> **Goal:** Define request body models with type hints, validate input automatically, hide sensitive data with response models.
>
> **LeetCode:** #238 Product of Array Except Self ✅ (65ms · Accepted 24/24)
>
> **Status:** ✅ Day 44 Complete — Pydantic models working, validation errors understood, response filtering demonstrated

---

# 🎯 Learning Roadmap

```
Pydantic Models — Request/Response Validation

  ✅ from pydantic import BaseModel
  ✅ Define request body models with type hints
  ✅ Field validation, optional fields, default values
  ✅ Response models — what to return vs what to hide (e.g. hide passwords)
  ✅ Validation errors — FastAPI returns 422 automatically

  ▶ fastapi.tiangolo.com/tutorial/body/
```

## Day 44 Checklist

- [ ] Explain what Pydantic BaseModel is and why it exists
- [ ] Write a POST endpoint that accepts a JSON request body
- [ ] Use `Field(min_length=3)` for custom validation rules
- [ ] Use `Optional[int]` for optional fields
- [ ] Use `EmailStr` for email validation
- [ ] Set a default value for a field
- [ ] Explain what HTTP 422 means and when FastAPI sends it
- [ ] Create a `UserResponse` model that hides the password field
- [ ] Explain the difference between `UserCreate`, `UserUpdate`, `UserResponse`
- [ ] Solve LeetCode #238 using prefix and suffix products

---

# SECTION 1 — LIFE BEFORE PYDANTIC

## The Problem with Manual Validation

Yesterday your API accepted simple integers from URL paths.

Today a user wants to register. They send:

```json
{
    "name": "Adyaprana",
    "email": "adya@gmail.com",
    "password": "12345678"
}
```

How does your backend know:

```
name must be a string?
email must be a valid email (not just any string)?
password must be at least 8 characters?
age is optional?
country defaults to "India" if not provided?
price cannot be negative?
```

**Without Pydantic (manual validation in Flask style):**

```python
data = request.json

# Manual type checking
name = data.get("name")
if not isinstance(name, str):
    return {"error": "name must be a string"}, 400

# Manual length checking
if len(name) < 3:
    return {"error": "name too short"}, 400

# Manual email checking
email = data.get("email")
if "@" not in email or "." not in email:
    return {"error": "invalid email"}, 400

# Manual required field checking
password = data.get("password")
if password is None:
    return {"error": "password required"}, 400

if len(password) < 8:
    return {"error": "password too short"}, 400

# ... 50 more lines for one endpoint
# Multiply by 100 endpoints = nightmare
```

**This is:**

```
→ Extremely repetitive
→ Error-prone (you'll forget to check something)
→ Inconsistent (different developers check things differently)
→ Hard to test
→ Hard to document
```

---

## Enter Pydantic

```
JSON → Pydantic → Clean Python Object

Instead of manually checking data,
Pydantic validates it automatically.

You describe the rules ONCE.
Pydantic enforces them EVERYWHERE.
```

---

# SECTION 2 — WHAT IS PYDANTIC BASEMODEL?

## Definition

`BaseModel` is Pydantic's base class for data models. When you inherit from it, you get:

```
✅ Automatic type validation
✅ Automatic type conversion (where safe)
✅ Automatic error messages with field names
✅ JSON schema generation (for Swagger)
✅ Default value handling
✅ Optional field support
✅ Custom field validators
✅ Nested model support
```

## BaseModel vs Regular Python Class

```python
# Regular Python class — stores behavior
class Car:
    def drive(self):
        ...

# Pydantic BaseModel — stores data validation rules
class User(BaseModel):
    name: str
    age: int

# The SAME syntax, completely different PURPOSE.
# BaseModel: "I define what valid data looks like."
# Regular class: "I define what objects can do."
```

## BaseModel vs @dataclass

```
@dataclass:               BaseModel:
────────────────────────────────────────────────────
No validation             Validates types
No JSON support           Built for JSON
No error messages         Rich error messages with field locations
No schema generation      Auto-generates JSON schema (Swagger)
Just stores data          Validates AND stores data

For FastAPI request bodies: always use BaseModel.
For game models (GuessWise): @dataclass was correct (no HTTP validation needed).
```

---

# SECTION 3 — YOUR FIRST REQUEST BODY

## The Complete main.py

```python
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel, EmailStr, Field

app = FastAPI()


class UserCreate(BaseModel):
    name: str = Field(min_length=3, max_length=50)
    email: EmailStr
    age: Optional[int] = Field(default=None, gt=0)
    country: str = "India"


@app.post("/users")
def create_user(user: UserCreate):
    return {
        "message": "User created successfully!",
        "user": user,
    }
```

**Install email validation support:**

```bash
pip install "pydantic[email]"
```

---

## Line-by-Line Explanation

### Imports

```python
from typing import Optional
```

```
Optional[int] means: this field can be an int OR None.
Python built-in — not FastAPI or Pydantic specific.
```

```python
from pydantic import BaseModel, EmailStr, Field
```

```
BaseModel → base class for all our schemas
EmailStr  → a string type that validates email format specifically
Field     → provides extra validation rules beyond basic types
```

### The UserCreate Model

```python
class UserCreate(BaseModel):
    name: str = Field(min_length=3, max_length=50)
    email: EmailStr
    age: Optional[int] = Field(default=None, gt=0)
    country: str = "India"
```

**Field 1: name**

```python
name: str = Field(min_length=3, max_length=50)

# str       → must be a string (type hint)
# Field()   → adds extra rules beyond just the type
# min_length=3  → must be at least 3 characters
# max_length=50 → must be at most 50 characters

# Valid:   "Adyaprana"         ✅
# Invalid: "Jo"                ❌ (too short, 422 error)
# Invalid: "A" * 60            ❌ (too long, 422 error)
# Invalid: 123                 ❌ (not a string, 422 error)
```

**Field 2: email**

```python
email: EmailStr

# EmailStr checks:
# → Contains exactly one @
# → Has a domain part (something.something)
# → Domain has at least one dot
# → Various RFC 5322 rules

# Valid:   "adya@gmail.com"    ✅
# Invalid: "notanemail"        ❌
# Invalid: "@gmail.com"        ❌
# Invalid: "adya@"             ❌
```

**Field 3: age**

```python
age: Optional[int] = Field(default=None, gt=0)

# Optional[int]   → can be int OR None
# default=None    → if client doesn't send it, use None
# gt=0            → if provided, must be Greater Than 0

# Valid:   {"age": 22}          ✅
# Valid:   (no age field)       ✅  (becomes None)
# Invalid: {"age": 0}           ❌  (not > 0)
# Invalid: {"age": -5}          ❌  (not > 0)
# Invalid: {"age": "old"}       ❌  (not an int)
```

**Field 4: country**

```python
country: str = "India"

# str     → must be a string
# "India" → default value (not a Field object, just a plain default)

# Valid:   (no country sent)    ✅  → "India" automatically
# Valid:   {"country": "USA"}   ✅
# Invalid: {"country": 123}     ❌  (not a string)
```

### The Endpoint

```python
@app.post("/users")
def create_user(user: UserCreate):
    return {
        "message": "User created successfully!",
        "user": user,
    }
```

```
@app.post("/users")
→ This endpoint responds to HTTP POST requests (not GET)
→ POST is used for creating resources
→ The request body contains the data to create

user: UserCreate
→ FastAPI sees: "UserCreate is a BaseModel subclass"
→ FastAPI expects a JSON body matching UserCreate's schema
→ FastAPI passes the JSON through Pydantic validation
→ If validation passes: user is a UserCreate Python object
→ If validation fails: FastAPI returns 422 before calling this function
```

---

# SECTION 4 — GET vs POST: THE KEY DIFFERENCE

## What Changed From Day 43

```python
# Day 43 — GET endpoint, path/query parameters
@app.get("/users/{user_id}")
def get_user(user_id: int):
    ...

# Day 44 — POST endpoint, request body
@app.post("/users")
def create_user(user: UserCreate):
    ...
```

## HTTP Methods and Their Meaning

```
GET    → Retrieve data. Safe, idempotent. No body. Data in URL.
POST   → Create a resource. Has a request body. Not idempotent.
PUT    → Replace a resource completely.
PATCH  → Update part of a resource.
DELETE → Remove a resource.

Creating a user → POST /users
Getting a user  → GET /users/{id}
Updating email  → PATCH /users/{id}
Deleting user   → DELETE /users/{id}
```

## The Request Lifecycle (Day 44 Version)

```
Client sends HTTP POST /users
{
    "name": "Adyaprana",
    "email": "adya@gmail.com",
    "age": 22
}
        │
        ▼
Uvicorn (receives TCP connection, parses HTTP)
        │
        ▼
FastAPI (matches route: POST /users → create_user)
        │
        ▼
Pydantic validation:
  name="Adyaprana" → str, len 9, between 3-50 ✅
  email="adya@gmail.com" → valid email format ✅
  age=22 → int, > 0 ✅
  country not sent → default "India" ✅
        │
        ▼ (all passed)
UserCreate(name="Adyaprana", email="adya@gmail.com", age=22, country="India")
        │
        ▼
create_user(user) called with Python object
        │
        ▼
return {"message": "...", "user": user}
        │
        ▼
FastAPI serializes user → JSON
        │
        ▼
HTTP 200 Response
{
    "message": "User created successfully!",
    "user": {
        "name": "Adyaprana",
        "email": "adya@gmail.com",
        "age": 22,
        "country": "India"
    }
}
        │
        ▼
Client receives JSON
```

---

# SECTION 5 — VALIDATION TESTS (TRY IN SWAGGER)

## Open Swagger UI

```
http://127.0.0.1:8000/docs
```

You'll see a POST /users endpoint. Click **Try it out**.

---

## Test 1: Valid Data (should work)

```json
{
  "name": "Adyaprana",
  "email": "adya@gmail.com",
  "age": 22
}
```

**Expected response:**

```json
{
  "message": "User created successfully!",
  "user": {
    "name": "Adyaprana",
    "email": "adya@gmail.com",
    "age": 22,
    "country": "India"
  }
}
```

Notice: `country` was automatically added with default "India". You didn't send it.

---

## Test 2: Invalid Email

```json
{
  "name": "Adyaprana",
  "email": "not-an-email",
  "age": 22
}
```

**Expected response (422):**

```json
{
  "detail": [
    {
      "type": "value_error",
      "loc": ["body", "email"],
      "msg": "value is not a valid email address",
      "input": "not-an-email"
    }
  ]
}
```

Your `create_user()` function is NEVER called. Pydantic blocks it.

---

## Test 3: Name Too Short

```json
{
  "name": "Jo",
  "email": "adya@gmail.com"
}
```

**Expected response (422):**

```json
{
  "detail": [
    {
      "type": "string_too_short",
      "loc": ["body", "name"],
      "msg": "String should have at least 3 characters",
      "input": "Jo"
    }
  ]
}
```

---

## Test 4: Negative Age

```json
{
  "name": "Adyaprana",
  "email": "adya@gmail.com",
  "age": -5
}
```

**Expected response (422):**

```json
{
  "detail": [
    {
      "type": "greater_than",
      "loc": ["body", "age"],
      "msg": "Input should be greater than 0",
      "input": -5
    }
  ]
}
```

---

## Test 5: Omit Optional Age

```json
{
  "name": "Adyaprana",
  "email": "adya@gmail.com"
}
```

**Expected response (200):**

```json
{
  "message": "User created successfully!",
  "user": {
    "name": "Adyaprana",
    "email": "adya@gmail.com",
    "age": null,
    "country": "India"
  }
}
```

Age is `null` (Python `None`). Country defaulted to "India".

---

## Test 6: Custom Country

```json
{
  "name": "Adyaprana",
  "email": "adya@gmail.com",
  "country": "USA"
}
```

**Expected response (200):**

```json
{
  "user": {
    "country": "USA",
    ...
  }
}
```

When you provide country, the default is overridden.

---

# SECTION 6 — WHY HTTP 422 AND NOT 400?

```
HTTP 400 Bad Request:
  → The request format itself is wrong.
  → Malformed JSON (missing brackets, wrong syntax).
  → Example: "name": "Adya"  (forgot opening brace)

HTTP 422 Unprocessable Entity:
  → The format is correct (valid JSON).
  → But the data doesn't satisfy the schema.
  → The server understands it but cannot process these specific values.

What FastAPI sends for validation failures → 422

{
    "name": "Jo",           ← valid JSON
    "email": "bad-email"    ← valid JSON
}

This IS valid JSON. JSON parser accepts it.
BUT Pydantic can't process it.
FastAPI correctly returns 422 Unprocessable Entity.
```

---

# SECTION 7 — ALL FIELD VALIDATORS

## `Field()` Reference

```python
from pydantic import Field

# String validators
name: str = Field(min_length=3)        # minimum 3 characters
name: str = Field(max_length=50)       # maximum 50 characters
name: str = Field(pattern="^[a-zA-Z]") # regex pattern

# Numeric validators
age: int = Field(gt=0)                 # greater than 0
age: int = Field(ge=0)                 # greater than or equal to 0
age: int = Field(lt=150)               # less than 150
age: int = Field(le=150)               # less than or equal to 150
age: int = Field(multiple_of=5)        # must be multiple of 5

# Float validators
price: float = Field(gt=0.0)           # positive price
rating: float = Field(ge=1.0, le=5.0)  # between 1.0 and 5.0

# Default and description
name: str = Field(default="Unknown", description="User's full name")
id: int = Field(default=None, description="Auto-assigned database ID")

# Combining validators
username: str = Field(
    min_length=3,
    max_length=20,
    pattern="^[a-z0-9_]+$",   # only lowercase, digits, underscores
    description="Unique username"
)
```

## `Optional` Reference

```python
from typing import Optional

# Optional with default None
age: Optional[int] = None

# Optional with Field for additional validation
age: Optional[int] = Field(default=None, gt=0)
# Can be None (not provided) or an int greater than 0

# Optional with default value
country: Optional[str] = "India"
# Can be provided or defaults to "India"
```

## Available Special Types

```python
from pydantic import EmailStr, HttpUrl, PositiveInt, NegativeInt

email: EmailStr          # validates email format
website: HttpUrl         # validates URL format
age: PositiveInt         # int > 0 (same as Field(gt=0))
balance: NegativeInt     # int < 0
```

---

# SECTION 8 — TYPE CONVERSION (AUTOMATIC)

Pydantic doesn't just validate — it converts types where safe.

```python
class Item(BaseModel):
    price: float
    quantity: int
    in_stock: bool
```

```
Client sends:
{
    "price": "19.99",      ← string
    "quantity": "5",        ← string
    "in_stock": "true"      ← string
}

Pydantic converts:
  "19.99"  → 19.99  (str → float)
  "5"      → 5      (str → int)
  "true"   → True   (str → bool)

Result:
  Item(price=19.99, quantity=5, in_stock=True)
```

```
But this fails (cannot convert):
{
    "price": "free",       ← "free" → float? No!
    "quantity": 2.7,       ← 2.7 → int? Pydantic truncates to 2 (careful!)
}
```

**Important:** Pydantic is permissive with numeric conversions. `2.7` as an `int` field becomes `2` (truncated, no error). Always validate float → int conversion carefully.

---

# SECTION 9 — RESPONSE MODELS: HIDING SENSITIVE DATA

## The Security Problem

Suppose your database stores this:

```json
{
    "id": 1,
    "name": "Adyaprana",
    "email": "adya@gmail.com",
    "password": "$2b$12$hashedpassword...",
    "role": "admin",
    "internal_score": 95
}
```

Should your API return all of this to the client? **Never.**

The password must NEVER leave the server. The internal_score is private. The role might be sensitive.

---

## The Solution: Response Model

```python
from pydantic import BaseModel, EmailStr

# What the CLIENT sends (input):
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str     # accepted from client

# What the API returns (output — filtered):
class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    # password is NOT here → never returned
    # role is NOT here → never returned

# The endpoint with response_model:
@app.post("/users", response_model=UserResponse)
def create_user(user: UserCreate):
    # Imagine this comes from the database:
    db_user = {
        "id": 1,
        "name": user.name,
        "email": user.email,
        "password": user.password,    # in the dict
        "role": "user"                # in the dict
    }
    return db_user  # FastAPI FILTERS this through UserResponse
    # Client receives ONLY: id, name, email
    # password and role are REMOVED automatically
```

**Even if your function returns too much, `response_model` acts as a security filter:**

```
Function returns:          Client receives:
────────────────────       ──────────────────
{                          {
  "id": 1,                   "id": 1,
  "name": "Adya",     →      "name": "Adya",
  "email": "...",            "email": "..."
  "password": "...",       }
  "role": "admin"           (password gone!)
}                           (role gone!)
```

---

## The Real Industry Pattern: Multiple Models Per Entity

Professional FastAPI applications use separate models for each purpose:

```python
from pydantic import BaseModel, EmailStr, Field
from typing import Optional


# Used when creating a new user (POST /users)
# Accepts password, doesn't have id
class UserCreate(BaseModel):
    name: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=8)
    country: str = "India"


# Used when partially updating a user (PATCH /users/{id})
# Everything optional (only send what you want to change)
class UserUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    country: Optional[str] = None
    # password has its own separate endpoint (/users/{id}/password)


# Used in API responses (GET /users, POST /users response)
# No password. Has id (assigned by database).
class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    country: str
    # is_active: bool  ← could add this
    # created_at: datetime  ← could add this


# Internal database model (used by SQLAlchemy or internal logic)
# NOT exposed to API
class UserDB(BaseModel):
    id: int
    name: str
    email: EmailStr
    password_hash: str   # hashed, never plain text
    country: str
    is_active: bool
```

**Why separate models?**

```
UserCreate:   "What the client SENDS to create a user"
UserUpdate:   "What the client SENDS to update a user"
UserResponse: "What the API SENDS BACK to the client"
UserDB:       "What's stored in the database"

Each model has ONE clear purpose.
This prevents accidental data leaks.
Makes each model smaller and easier to understand.
Makes testing simpler (test each model independently).
```

---

# SECTION 10 — THE UPDATED REQUEST LIFECYCLE

```
Day 43 lifecycle:
  Client → HTTP GET → Uvicorn → FastAPI → Function → Dict → JSON → Client

Day 44 lifecycle:
  Client
    │
    │ HTTP POST /users + JSON body
    ▼
  Uvicorn (receives TCP, parses HTTP)
    │
    ▼
  FastAPI (matches route: POST /users → create_user)
    │
    ▼
  Pydantic Validation:
    → Type checking (str, int, etc.)
    → Field validators (min_length, gt, etc.)
    → Email format check (EmailStr)
    → Default values (country="India")
    → Optional handling (age=None if missing)
    │
    ├── FAILS → HTTP 422 + detailed error → Client
    │            (create_user never called)
    │
    └── PASSES → UserCreate Python object
                    │
                    ▼
                create_user(user) called
                    │
                    ▼
                Function returns dict/UserResponse
                    │
                    ▼
                response_model FILTERS (if specified)
                    │
                    ▼
                FastAPI serializes → JSON
                    │
                    ▼
                HTTP 200 + JSON → Client
```

---

# SECTION 11 — CONCEPTS LEARNED TODAY

## Declarative Validation

```
Instead of: "Check if name is a string, if len > 3, if len < 50..."
You say:    "name: str = Field(min_length=3, max_length=50)"

This is declarative: you DESCRIBE the rule.
Pydantic ENFORCES it.
No if statements. No try/except. No manual checking.
```

## Schema as Contract

```
UserCreate is a CONTRACT between your API and its clients.

It says: "If you want to create a user, send EXACTLY this structure."
         "If you don't, you get a 422 error."

This contract is:
  → Enforced automatically (by Pydantic)
  → Documented automatically (in Swagger)
  → Type-safe (Python type hints)
  → Self-describing (clients can read the JSON schema)
```

## Separation of Input and Output Models

```
Input model:  What can come IN to your API
Output model: What goes OUT of your API

These are DIFFERENT concerns.
Mixing them causes security vulnerabilities.

The classic bug:
  → User sends password in UserCreate
  → Developer forgets to remove it from the response
  → Password returned to client accidentally

With separate models:
  → UserCreate has password (input only)
  → UserResponse doesn't have password (output only)
  → Impossible to accidentally leak it
```

---

# SECTION 12 — INTERVIEW QUESTIONS

## Q1. What is Pydantic and why does FastAPI use it?

Pydantic is a Python data validation library that uses type hints to define schemas. FastAPI uses it because it provides automatic validation, type conversion, and JSON schema generation from the same class definition. One Pydantic model simultaneously validates input, converts types, enforces constraints, and generates the Swagger documentation.

## Q2. What is the difference between BaseModel and a regular Python class?

A regular Python class stores behavior (methods). A Pydantic BaseModel stores data validation rules. When data is assigned to a BaseModel field, Pydantic automatically validates the type, converts it if possible, and raises a ValidationError if it fails. Regular classes have none of this behavior by default.

## Q3. What does `Optional[int] = None` mean?

`Optional[int]` means the field can be an integer or `None`. `= None` sets the default to `None`, making the field not required in the JSON request. If the client doesn't send this field, it defaults to `None`. If the client sends an integer, Pydantic validates it as `int`. If the client sends something that can't be an integer, FastAPI returns 422.

## Q4. Why does FastAPI return 422 and not 400 for validation errors?

HTTP 400 means the request format is invalid (malformed JSON, missing headers). HTTP 422 means the format is correct (valid JSON), but the data values don't satisfy the schema constraints. FastAPI uses 422 because the client's JSON is perfectly valid JSON — Pydantic just can't process those specific values against the declared schema.

## Q5. What is a response model and why is it important for security?

A response model (specified with `response_model=UserResponse`) defines exactly what fields the API returns. Even if the function returns a database record containing sensitive fields like `password_hash` or `role`, FastAPI filters the output through the response model and removes any fields not defined in it. This prevents accidental data leaks — you can never return a password if it's not in the response model.

## Q6. What is the difference between UserCreate, UserUpdate, and UserResponse?

`UserCreate`: input model for POST requests. Accepts password, no id (not yet assigned). `UserUpdate`: input model for PATCH requests. All fields are Optional since you only send what you want to change. `UserResponse`: output model for any response. No password, has id (assigned by database). This separation ensures each model is focused on one purpose and prevents security issues from mixing input/output schemas.

## Q7. What does `Field(gt=0)` mean?

`Field()` provides validation rules beyond the basic type. `gt=0` means "greater than 0". Similarly: `ge=0` (≥ 0), `lt=100` (< 100), `le=100` (≤ 100), `min_length=3` (string minimum length), `max_length=50` (string maximum length). Without these, you'd write `if age <= 0: raise ...` manually. With Field, Pydantic enforces it automatically.

## Q8. What happens when Pydantic validation fails?

FastAPI immediately returns an HTTP 422 response with a detailed error in the `detail` array. Each error object contains: `type` (what went wrong), `loc` (where in the request — "body", "email"), `msg` (human-readable message), and `input` (the value that failed). Your endpoint function is NEVER called — the validation failure is caught before your code runs.

---

# SECTION 13 — LEETCODE #238: PRODUCT OF ARRAY EXCEPT SELF

## Problem

Given integer array `nums`, return array `answer` where `answer[i]` is the product of all elements EXCEPT `nums[i]`.

```
nums    = [1,  2,  3,  4]
answer  = [24, 12, 8,  6]

answer[0] = 2×3×4 = 24   (everything except nums[0]=1)
answer[1] = 1×3×4 = 12   (everything except nums[1]=2)
answer[2] = 1×2×4 = 8    (everything except nums[2]=3)
answer[3] = 1×2×3 = 6    (everything except nums[3]=4)
```

**Constraint:** No division allowed. Must be O(n).

## Why No Division?

```
Naïve approach with division:
  total = 1 × 2 × 3 × 4 = 24
  answer[i] = total / nums[i]
  answer[0] = 24 / 1 = 24  ✅
  answer[1] = 24 / 2 = 12  ✅

Problems:
  1. Division by zero if any nums[i] == 0
  2. Integer division precision issues
  3. Problem explicitly forbids it
```

## The Prefix-Suffix Product Approach

**Key observation:**

```
For each position i:
  answer[i] = (product of everything to the LEFT of i)
              × (product of everything to the RIGHT of i)

Position 0:  left=1 (nothing left), right=2×3×4=24  → 1×24=24
Position 1:  left=1, right=3×4=12                   → 1×12=12
Position 2:  left=1×2=2, right=4                    → 2×4=8
Position 3:  left=1×2×3=6, right=1 (nothing right)  → 6×1=6
```

**We build two arrays:**

```
nums:   [1,   2,   3,   4]

left:   [1,   1,   2,   6]
  left[0] = 1          (nothing to the left)
  left[1] = 1×1 = 1   (just nums[0])
  left[2] = 1×2 = 2   (nums[0]×nums[1])
  left[3] = 2×3 = 6   (nums[0]×nums[1]×nums[2])

right:  [24,  12,  4,   1]
  right[0] = 2×3×4 = 24
  right[1] = 3×4 = 12
  right[2] = 4
  right[3] = 1          (nothing to the right)

answer[i] = left[i] × right[i]:
  answer[0] = 1×24 = 24 ✅
  answer[1] = 1×12 = 12 ✅
  answer[2] = 2×4  = 8  ✅
  answer[3] = 6×1  = 6  ✅
```

## The Complete Solution

```python
class Solution(object):
    def productExceptSelf(self, nums):
        answer = []
        left = []
        right = [1] * len(nums)

        # Build LEFT products
        for i in range(len(nums)):
            if i == 0:
                left_product = 1          # Nothing to the left of index 0
            else:
                left_product *= nums[i-1] # Multiply by the element just before i
            left.append(left_product)

        # Build RIGHT products (traverse backwards)
        for i in reversed(range(len(nums))):
            if i == len(nums) - 1:
                right_product = 1          # Nothing to the right of the last element
            else:
                right_product *= nums[i+1] # Multiply by the element just after i
            right[i] = right_product

        # Combine: answer[i] = left[i] × right[i]
        for i in range(len(nums)):
            answer.append(right[i] * left[i])

        return answer
```

## Complete Dry Run

```
nums = [1, 2, 3, 4]

STEP 1: Build LEFT array (product of everything to the left)

i=0: i==0, so left_product=1.  left=[1]
i=1: left_product = 1 × nums[0] = 1×1 = 1.  left=[1,1]
i=2: left_product = 1 × nums[1] = 1×2 = 2.  left=[1,1,2]
i=3: left_product = 2 × nums[2] = 2×3 = 6.  left=[1,1,2,6]

STEP 2: Build RIGHT array (product of everything to the right)

right = [1, 1, 1, 1]  (initialized)

i=3: i==len-1, so right_product=1.  right=[1,1,1,1]
i=2: right_product = 1 × nums[3] = 1×4 = 4.  right=[1,1,4,1]
i=1: right_product = 4 × nums[2] = 4×3 = 12. right=[1,12,4,1]
i=0: right_product = 12 × nums[1] = 12×2 = 24.right=[24,12,4,1]

STEP 3: Combine

i=0: answer[0] = left[0] × right[0] = 1×24 = 24
i=1: answer[1] = left[1] × right[1] = 1×12 = 12
i=2: answer[2] = left[2] × right[2] = 2×4  = 8
i=3: answer[3] = left[3] × right[3] = 6×1  = 6

Return: [24, 12, 8, 6] ✅
```

## Why `right_product *= nums[i+1]` in Reversed Loop

```python
for i in reversed(range(len(nums))):
    if i == len(nums) - 1:
        right_product = 1
    else:
        right_product *= nums[i+1]
    right[i] = right_product
```

```
We go RIGHT TO LEFT (reversed).
At each position i, right_product accumulates
the product of all elements to the RIGHT of i.

i=3: right_product=1 (nothing to the right)
i=2: right_product = 1 × nums[3] = 1×4 = 4
     (everything to the right of index 2 = just nums[3])
i=1: right_product = 4 × nums[2] = 4×3 = 12
     (everything to right of index 1 = nums[2]×nums[3])
i=0: right_product = 12 × nums[1] = 24
     (everything to right of index 0 = nums[1]×nums[2]×nums[3])

The pattern: each iteration multiplies by nums[i+1]
because i+1 is the position just to the right of where we are.
```

## Complexity

```
Time:  O(n) — three separate passes over the array
Space: O(n) — left and right arrays each of size n

Can you do O(1) space?
  Use the answer array as the left array.
  Then pass right-to-left with a running right product.
  Space: O(1) extra (output array doesn't count).
```

## The Prefix-Suffix Pattern

```
This problem extends the prefix sum pattern to prefix products.

The idea: "For each position, you need something from the left AND the right."

Pattern: Build left array → Build right array → Combine.

Same logic appears in:
  #42 Trapping Rain Water  (max from left, max from right)
  #135 Candy               (min from left, min from right)
  #238 This problem        (product from left, product from right)
```

**Result:** ✅ Accepted | 24/24 test cases | Runtime: 65ms

---

# SECTION 14 — IMPORTANT THINGS TO KNOW

```
 1. Pydantic BaseModel is the foundation of FastAPI request/response handling.
    Import with: from pydantic import BaseModel

 2. Install email validation support separately:
    pip install "pydantic[email]"
    Without this, EmailStr raises an ImportError.

 3. Optional[int] means int or None. The field is not required.
    age: int = None  ← also works but Optional[int] is more explicit.

 4. Field() provides extra validation: min_length, max_length, gt, ge, lt, le.
    name: str = Field(min_length=3, max_length=50)

 5. HTTP 422 = validation failed.
    HTTP 400 = malformed request format (bad JSON syntax).

 6. Your endpoint function is NEVER called if Pydantic validation fails.
    The 422 response is sent directly by FastAPI, before your code runs.

 7. response_model filters the output — sensitive fields are removed.
    Even if your function returns {"password": "..."}, it won't reach the client.

 8. Always create separate models for input and output:
    UserCreate (input) vs UserResponse (output).
    Never use the same model for both.

 9. Pydantic does automatic type conversion where safe:
    "22" → 22 (str to int). "hello" → TypeError (422 sent).

10. POST endpoints accept a request body. GET endpoints do not.
    Use POST for creating resources.
    Use GET for retrieving resources.

11. Swagger auto-generates a request body form from your BaseModel.
    You can test all validation directly in /docs without Postman.

12. Pydantic v2 (current) is faster and stricter than Pydantic v1.
    Some tutorials show Pydantic v1 syntax. Check your version:
    pip show pydantic

13. gt means greater than (strictly). ge means greater than or equal.
    Field(gt=0) rejects 0. Field(ge=0) accepts 0.

14. For the Product Array problem: never use division when 0 could be present.
    The prefix-suffix approach works regardless of zeros.

15. The connection: Pydantic models in FastAPI are used the same way
    SQLAlchemy models are used in GuessWise.
    One describes API schema. The other describes DB schema.
    Both use Python classes with type hints to define structure.
```

---

# REVISION SHEET

```
═══════════════════════════════════════════════════════════
FASTAPI DAY 44 — PYDANTIC REVISION
═══════════════════════════════════════════════════════════

BASIC MODEL:
  from pydantic import BaseModel
  class User(BaseModel):
      name: str
      age: int

POST ENDPOINT:
  @app.post("/users")
  def create_user(user: User):
      return user

FIELD VALIDATORS:
  name: str = Field(min_length=3, max_length=50)
  age: int = Field(gt=0)
  price: float = Field(ge=0.0, le=9999.99)

OPTIONAL:
  age: Optional[int] = None
  age: Optional[int] = Field(default=None, gt=0)

DEFAULT VALUE:
  country: str = "India"

EMAIL VALIDATION:
  from pydantic import EmailStr
  email: EmailStr

RESPONSE MODEL:
  @app.post("/users", response_model=UserResponse)
  → Filters output. Removes fields not in UserResponse.

MODEL PATTERN:
  UserCreate   → POST body input (has password)
  UserUpdate   → PATCH body input (all Optional)
  UserResponse → API output (no password, has id)
  UserDB       → Internal/database model

HTTP STATUS:
  200 → Success
  422 → Validation failed (Pydantic rejection)
  400 → Bad format (malformed JSON)

PRODUCT ARRAY #238:
  left[i]  = product of everything left of i
  right[i] = product of everything right of i
  answer[i] = left[i] × right[i]
  Time O(n), Space O(n). No division needed.
```

---

## LeetCode Solved This Day

| Problem | Difficulty | Topic | Status | Runtime |
|---------|-----------|-------|--------|---------|
| #238 Product of Array Except Self | Medium | Prefix Product + Suffix Product | ✅ Accepted 24/24 | 65ms |

---

*Day 44 Complete. Pydantic models working. Validation automatic. Response filtering understood. Phase 2 continues.* ✅