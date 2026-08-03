## DAY-46 Authentication Explained
``` 
Chapter 1
Project Architecture

Chapter 2
database.py
(Line by line)

Chapter 3
models.py
(Line by line)

Chapter 4
schemas.py
(Line by line)

Chapter 5
crud.py
(Line by line)

Chapter 6
security.py
(Line by line)

Chapter 7
routers/users.py
(Line by line)

Chapter 8
routers/auth.py
(Line by line)

Chapter 9
Request Flow

Chapter 10
JWT Flow

Chapter 11
Password Hashing Flow

Chapter 12
Interview Questions

Chapter 13
Things Juniors Usually Don't Understand

Chapter 14
Industry Best Practices
```


# FastAPI Authentication Internals
## Complete Developer Guide (Built From Our Backend Learning Project)

---

# Chapter 1 — Understanding the Whole Project Before Reading the Code

> "Never read code line by line before understanding the architecture."

This is one of the biggest mistakes beginners make.

They immediately open `main.py` and start reading code.

Professional backend engineers do the opposite.

Before reading a single line of code they ask:

> **"What problem is this application trying to solve?"**

Only after answering that question do they start exploring the codebase.

This chapter exists for that exact reason.

---

## What Are We Building?

Our project is a simple **User Management API** built using FastAPI.

The application allows clients to:

- Register new users
- Log in securely
- Store user data inside PostgreSQL
- Protect private endpoints using JWT Authentication
- Perform CRUD operations on users

Unlike our previous CLI project (GuessWise), this application communicates through HTTP.

Instead of typing commands into a terminal, clients send HTTP requests.

Example:

```
POST /register
```

or

```
GET /users
```

Our backend receives those requests, processes them, interacts with the database if needed, and finally sends an HTTP response back.

---

# The Big Picture

Every request follows the same journey.

```
                Browser / Postman / Mobile App

                           │
                           ▼

                    HTTP Request

                           │
                           ▼

                      FastAPI App

                           │
                           ▼

                   Route (Router File)

                           │
                           ▼

                    Business Logic

                           │
                           ▼

                     CRUD Functions

                           │
                           ▼

                    SQLAlchemy ORM

                           │
                           ▼

                     PostgreSQL Database

                           │
                           ▼

                     SQLAlchemy ORM

                           │
                           ▼

                     FastAPI Response

                           │
                           ▼

                       JSON Response
```

This entire flow happens every time a client communicates with our API.

---

# Understanding Every Folder

Our project currently looks like this:

```
backend-learning/

│
├── main.py
├── database.py
├── models.py
├── schemas.py
├── crud.py
├── security.py
│
├── routers/
│   ├── users.py
│   └── auth.py
│
└── requirements.txt
```

At first this may look like many files.

In reality every file has **exactly one responsibility**.

Professional software is built by separating responsibilities.

This idea is called the **Single Responsibility Principle (SRP).**

Instead of creating one giant file with 1000 lines of code, we divide the project into small independent modules.

---

## main.py

Think of this as the application's front door.

Its responsibilities are very small.

It:

- Creates the FastAPI application
- Includes routers
- Starts the application
- Performs startup configuration

Notice something.

`main.py` should NOT contain database logic.

It should NOT contain SQL queries.

It should NOT contain authentication logic.

It simply assembles the application.

---

## database.py

This file is responsible for connecting to PostgreSQL.

It knows:

- Which database to connect to
- How to create database sessions
- How to provide database connections to endpoints

Nothing more.

---

## models.py

This file represents our database.

Every SQLAlchemy model corresponds to one database table.

Example:

```
class User(Base)
```

↓

becomes

```
users
```

inside PostgreSQL.

Models describe how data is stored.

---

## schemas.py

Schemas are completely different from models.

Models describe

> Database tables.

Schemas describe

> API data.

Whenever a client sends JSON to our application,

Pydantic validates that JSON using schemas.

Schemas never communicate directly with PostgreSQL.

---

## crud.py

CRUD stands for

- Create
- Read
- Update
- Delete

Instead of writing SQL queries inside route functions,

we move database operations into this file.

This keeps the project organized.

---

## security.py

This file contains security-related helper functions.

Examples:

- Hash password
- Verify password
- Generate JWT
- Decode JWT

It knows nothing about users.

It only understands security.

---

## routers/

Instead of placing every endpoint inside `main.py`, we organize endpoints into routers.

Example:

```
users.py
```

contains

```
/users
/users/{id}
```

while

```
auth.py
```

contains

```
/login
/register
```

This keeps endpoints grouped by feature.

---

# Why So Many Files?

Because backend applications grow.

Imagine placing everything inside one file.

```
main.py

3000+ lines
```

Finding a single bug would become painful.

Instead we organize code by responsibility.

Professional backend projects are designed to be easy to read months or years later.

---

# The Architecture

Our backend follows a layered architecture.

```
Client

↓

Router

↓

CRUD

↓

SQLAlchemy Model

↓

Database
```

Each layer has one responsibility.

This is almost identical to what we built in GuessWise.

The only difference is that our Presentation Layer is now HTTP instead of a CLI.

---

# Request Lifecycle

Suppose a client sends

```
GET /users
```

The request travels through several layers.

```
Client

↓

FastAPI

↓

Router

↓

CRUD Function

↓

SQLAlchemy

↓

PostgreSQL

↓

CRUD

↓

Router

↓

FastAPI

↓

JSON Response

↓

Client
```

Understanding this flow is far more important than memorizing syntax.

Every backend framework follows this same basic architecture.

---

# Chapter Summary

By the end of this chapter you should understand:

✅ The purpose of the entire project.

✅ The responsibility of every file.

✅ Why professional projects are split into multiple modules.

✅ The overall request lifecycle.

If you understand this chapter, reading the code becomes dramatically easier.

---

# Chapter 2 — main.py (The Entry Point of Our Application)

Every FastAPI project begins with one file.

```
main.py
```

Think of this file as the application's **main entrance**.

Nothing in the application can happen until this file starts.

If this file disappears,

your backend no longer exists.

---

## What Does main.py Actually Do?

Many beginners think

> "main.py contains all my code."

This is not true.

Its real job is much simpler.

It acts as the **Application Composer.**

Imagine building a car.

The engine,

the wheels,

the steering,

the seats

are all built separately.

At the end,

someone assembles them into one complete car.

`main.py` performs the same job.

It assembles all parts of the application.

---

## The Startup Sequence

When we execute

```bash
uvicorn main:app --reload
```

Python performs the following steps.

```
Import main.py

↓

Execute every line

↓

Create FastAPI()

↓

Load Routers

↓

Load Database

↓

Application Ready

↓

Wait for Requests
```

Notice something important.

Python executes `main.py` **only once** during startup.

The endpoint functions inside it are **not** executed immediately.

Only their registration happens.

---

## Why Don't Requests Start Immediately?

When FastAPI sees

```python
@app.get("/users")
```

it does **not** call that function.

Instead it stores a mapping similar to this:

```
"/users"

↓

get_users()
```

Later,

when a request arrives,

FastAPI checks its routing table.

```
Incoming Request

↓

"/users"

↓

Found

↓

Execute get_users()
```

This explains why decorators are used.

Decorators register routes rather than executing them.

---

## main.py Should Stay Small

A common beginner mistake is writing everything inside `main.py`.

```
Database Logic

Authentication

SQL Queries

JWT

CRUD

Everything...
```

This quickly becomes unmaintainable.

Professional projects keep `main.py` focused on:

- creating the FastAPI application
- registering routers
- startup configuration
- middleware
- application settings

Business logic belongs elsewhere.

---

## Mental Model

Whenever you open `main.py`, remember this sentence:

> **main.py does not contain the application. It assembles the application.**

That one idea explains why almost every professional FastAPI project keeps this file surprisingly small.

---

---

# Chapter 3 — database.py (The Bridge Between FastAPI and PostgreSQL)

At this point we understand that `main.py` assembles the application.

The next question naturally becomes:

> **"How does our application actually talk to PostgreSQL?"**

That responsibility belongs entirely to one file.

```
database.py
```

This file is one of the most important files in any FastAPI backend.

It contains **zero business logic**.

It doesn't know what a User is.

It doesn't know how Login works.

It doesn't know JWT.

Its only job is to establish communication with the database.

Think of it like this.

```
FastAPI

↓

database.py

↓

PostgreSQL
```

Everything that wants to use the database must go through this bridge.

---

# Why Do We Need database.py?

Imagine every endpoint created its own database connection.

```
@app.get("/users")

↓

Connect Database

↓

Run Query

↓

Disconnect
```

Now imagine another endpoint.

```
@app.post("/users")

↓

Connect Again

↓

Run Query

↓

Disconnect
```

Another endpoint.

```
@app.put("/users/1")

↓

Connect Again

↓

Run Query

↓

Disconnect
```

Soon every endpoint starts repeating the same code.

Professional engineers hate repetition.

Instead,

we centralize database configuration into one place.

That place is `database.py`.

---

# Let's Read the File

The first lines are

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
```

Let's understand them one by one.

---

## create_engine()

This is the very first object SQLAlchemy needs.

Think of the Engine as:

> **The connection manager.**

It knows

- which database to use
- which driver to use
- how to communicate with PostgreSQL

Notice something.

The Engine does **NOT** execute SQL.

It simply knows **how to reach the database.**

Think of it like Google Maps.

Google Maps knows how to reach your destination.

It doesn't actually drive the car.

---

# DATABASE_URL

Usually you'll see something like

```python
DATABASE_URL = "postgresql+psycopg2://postgres:password@localhost:5432/backend_db"
```

At first this looks scary.

Let's break it apart.

```
postgresql
```

↓

Which database?

Answer:

PostgreSQL.

---

```
psycopg2
```

↓

Which Python driver?

SQLAlchemy itself cannot speak PostgreSQL.

It needs a translator.

That translator is

```
psycopg2
```

---

```
postgres
```

↓

Database username.

---

```
password
```

↓

Database password.

---

```
localhost
```

↓

Database server.

Since PostgreSQL is installed on our own computer,

localhost simply means

"My own machine."

---

```
5432
```

↓

Default PostgreSQL port.

Exactly like websites use port 80 or 443,

PostgreSQL listens on 5432.

---

```
backend_db
```

↓

Database name.

---

Putting everything together,

the URL literally means

> "Connect to the PostgreSQL database named backend_db running on my computer using this username and password."

---

# Engine Creation

Next we usually write

```python
engine = create_engine(DATABASE_URL)
```

What actually happens?

SQLAlchemy creates an Engine object.

Notice carefully.

It **does NOT** connect to PostgreSQL immediately.

This surprises many beginners.

Instead,

it simply prepares itself.

The actual connection happens later,

when someone asks for a session.

---

# SessionLocal

Next comes

```python
SessionLocal = sessionmaker(...)
```

This is probably the most confusing line for beginners.

Think of it this way.

The Engine is like

```
A Car Factory
```

It doesn't produce a car until you ask.

SessionLocal is the machine that builds cars.

Every time FastAPI receives a request,

it creates a brand-new Session.

```
Request

↓

SessionLocal()

↓

New Database Session
```

Each request gets its own session.

No sharing.

No conflicts.

---

# Why Not Share One Session?

Imagine two users.

```
User A

↓

Update User

```

At exactly the same time

```
User B

↓

Delete User
```

If both shared the same database session,

chaos could happen.

Instead,

every request receives an isolated session.

This keeps data consistent and thread-safe.

---

# declarative_base()

Another mysterious line is

```python
Base = declarative_base()
```

Think of Base as

> **The parent of every database model.**

Later we'll write

```python
class User(Base):
```

Without Base,

SQLAlchemy wouldn't know

that User is supposed to become a database table.

Base acts like a registration system.

Whenever a class inherits from Base,

SQLAlchemy remembers it.

Later,

when we call

```python
Base.metadata.create_all()
```

SQLAlchemy creates tables for every registered model.

---

# get_db()

This is arguably the most important function in the file.

```python
def get_db():
```

Every request follows this lifecycle.

```
Request Starts

↓

Open Session

↓

Give Session To Endpoint

↓

Endpoint Uses Database

↓

Response Sent

↓

Close Session
```

This ensures every database connection is cleaned up properly.

No memory leaks.

No orphaned connections.

---

# Why Do We Use yield?

Instead of

```python
return db
```

we use

```python
yield db
```

This is a special FastAPI pattern.

`yield` pauses the function.

FastAPI gives the session to the endpoint.

After the endpoint finishes,

the function resumes,

allowing the cleanup code to execute.

This guarantees

```
db.close()
```

always runs,

even if an exception occurs.

---

# Mental Model

Whenever you think about `database.py`,

remember this sentence.

> **database.py does not store data. It manages database connections.**

Everything else in the application depends on it.

---

# Chapter Summary

By the end of this chapter you should understand:

✅ Why database.py exists.

✅ What the Engine does.

✅ What SessionLocal creates.

✅ Why every request gets its own database session.

✅ Why Base is required.

✅ Why get_db() uses yield.

---

# Chapter 4 — models.py (Turning Python Classes Into Database Tables)

Now that our application knows **how to connect to PostgreSQL,**

the next question becomes:

> **"What should be stored inside the database?"**

That answer lives inside

```
models.py
```

This file defines the structure of our database.

If `database.py` builds the bridge,

then `models.py` decides **what travels across it.**

---

# What Is A Model?

A SQLAlchemy Model is simply a Python class that represents one database table.

For example,

this class

```python
class User(Base):
```

eventually becomes

```
users
```

inside PostgreSQL.

Think of models as blueprints.

They describe

- columns
- data types
- constraints
- relationships

They do **not** contain API validation.

That's Pydantic's job.

---

# One Class = One Table

Whenever you see

```python
class User(Base):
```

you should immediately think

```
Database Table
```

If tomorrow we create

```python
class Product(Base):
```

SQLAlchemy creates

```
products
```

If we create

```python
class Order(Base):
```

SQLAlchemy creates

```
orders
```

One model.

One table.

---

# __tablename__

Inside every model you'll see

```python
__tablename__ = "users"
```

This tells SQLAlchemy

what the actual database table should be called.

Without it,

SQLAlchemy would try to generate names automatically.

Professional projects almost always define it explicitly.

---

# Columns

Every attribute declared with

```python
Column(...)
```

becomes a database column.

For example

```python
id = Column(Integer)
```

↓

becomes

```
id INTEGER
```

inside PostgreSQL.

---

# Primary Key

You'll usually see

```python
primary_key=True
```

A primary key uniquely identifies every row.

Imagine two users named

```
John
```

Names can repeat.

Emails might even change.

But IDs never repeat.

That's why almost every table has

```
id
```

as its primary key.

---

# nullable=False

Example

```python
name = Column(
    String,
    nullable=False
)
```

This means

the database refuses to store

```
NULL
```

inside that column.

If someone tries,

PostgreSQL throws an error.

Notice something.

Validation happens in two places.

```
Pydantic

↓

Client Validation
```

and

```
PostgreSQL

↓

Database Validation
```

This is called

**Defence in Depth.**

Even if one layer fails,

the other still protects your data.

---

# unique=True

For email columns,

we usually write

```python
unique=True
```

Why?

Because

```
adya@gmail.com
```

should belong to only one account.

The database itself enforces this rule.

No duplicate emails can exist.

---

# Default Values

Sometimes you'll see

```python
default=True
```

or

```python
default=datetime.utcnow
```

If the application doesn't provide a value,

SQLAlchemy automatically inserts the default.

For example,

new users become active immediately,

and created_at records the current timestamp.

---

# Why Models Don't Validate Requests

Many beginners ask,

"Why not use SQLAlchemy models directly in the API?"

Because models describe

**how data is stored.**

Schemas describe

**how data enters and leaves the API.**

Keeping them separate follows the Single Responsibility Principle and makes the application easier to maintain.

---

# Mental Model

Whenever you open `models.py`,

remember:

> **Models describe the database—not the API.**

---

# Chapter Summary

By the end of this chapter you should understand:

✅ One model becomes one table.

✅ One Column becomes one database field.

✅ Why Base is inherited.

✅ Why primary keys exist.

✅ Why nullable and unique matter.

✅ Why models and schemas are different.

---


---

# Chapter 5 — schemas.py (Teaching FastAPI What Valid Data Looks Like)

So far we've learned two important things.

`database.py` knows **how to connect** to PostgreSQL.

`models.py` knows **how data is stored** inside PostgreSQL.

Now another question appears.

> **"How does FastAPI know whether the JSON sent by a client is valid?"**

That is the job of

```
schemas.py
```

This file is responsible for **data validation**.

It sits between the client and our application.

Think of it as a security guard.

```
Client

↓

Schema Validation

↓

FastAPI

↓

CRUD

↓

Database
```

Nothing reaches our application until it passes schema validation.

---

# What Is A Schema?

A Schema is simply a blueprint that describes

**what data is allowed.**

Suppose a client sends

```json
{
    "name":"Adyaprana",
    "email":"adya@gmail.com"
}
```

Our application needs to answer questions like

- Does "name" exist?
- Is it a string?
- Is it too short?
- Is the email valid?
- Is any required field missing?

Instead of writing hundreds of `if` statements,

Pydantic performs all of this automatically.

---

# BaseModel

Every schema begins with

```python
class UserBase(BaseModel):
```

Notice something.

Our SQLAlchemy models inherit from

```python
Base
```

Our Pydantic schemas inherit from

```python
BaseModel
```

Although they look similar,

they solve completely different problems.

```
Base

↓

Database Tables
```

```
BaseModel

↓

API Validation
```

Never confuse these two.

---

# Why UserBase Exists

Instead of repeating

```python
name
email
```

inside every schema,

we create one parent class.

```
UserBase

↓

name

email
```

Then

```
UserCreate

↓

inherits

↓

UserBase
```

Now every child automatically receives

```
name

email
```

This follows the DRY Principle.

**Don't Repeat Yourself.**

Professional engineers always try to eliminate duplicate code.

---

# UserCreate

Whenever someone registers,

FastAPI expects

```json
{
    "name":"Adyaprana",
    "email":"adya@gmail.com"
}
```

UserCreate describes exactly what that request should contain.

Later,

when authentication is added,

this schema will also contain

```
password
```

because users must provide one during registration.

---

# UserUpdate

Updating data is different from creating data.

Imagine changing only your email.

```
PATCH /users/5

{
    "email":"new@gmail.com"
}
```

The client isn't changing

```
name
```

Therefore,

every field becomes optional.

That's why we use

```
Optional
```

instead of making every field mandatory.

---

# UserResponse

One of the biggest security concepts in backend development is

**Never return everything you store.**

Suppose our database contains

```
id

name

email

hashed_password

created_at

is_active
```

Should the client receive

```
hashed_password
```

Absolutely not.

Instead,

we create a response schema.

```
UserResponse
```

Only the fields inside this schema will be returned.

This acts like a filter.

Even if our SQLAlchemy model contains twenty columns,

the API returns only the safe ones.

---

# model_config = ConfigDict(from_attributes=True)

This line confuses almost everyone.

Imagine SQLAlchemy returns

```
User Object
```

instead of JSON.

FastAPI needs to convert

```
SQLAlchemy Object

↓

Pydantic Model

↓

JSON
```

The configuration

```python
from_attributes=True
```

tells Pydantic

> "Read values directly from SQLAlchemy model objects."

Without this,

FastAPI wouldn't know how to serialize SQLAlchemy objects correctly.

---

# Why We Separate Models And Schemas

Many beginners ask

"Why not use SQLAlchemy models everywhere?"

Imagine changing your database.

Perhaps tomorrow

you add

```
hashed_password
```

Should every API suddenly expose passwords?

Of course not.

Keeping Models and Schemas separate prevents these kinds of mistakes.

Professional applications almost always separate

```
Database

↓

Models
```

and

```
API

↓

Schemas
```

---

# Mental Model

Whenever you open

```
schemas.py
```

remember this sentence.

> **Schemas describe what the API accepts and returns—not what the database stores.**

---

# Chapter Summary

By the end of this chapter you should understand:

✅ Why Pydantic exists.

✅ Why BaseModel is required.

✅ Why UserBase exists.

✅ Why UserCreate and UserUpdate are different.

✅ Why UserResponse improves security.

✅ Why Models and Schemas are separate.

---

# Chapter 6 — crud.py (The Heart of Business Logic)

At this point we know

how to connect to PostgreSQL,

and

how to validate incoming data.

Now comes the real work.

Suppose someone sends

```
POST /users
```

Who actually inserts that user into PostgreSQL?

The answer is

```
crud.py
```

CRUD stands for

```
Create

Read

Update

Delete
```

Nearly every backend application spends most of its life performing these four operations.

---

# Why Does crud.py Exist?

Many beginners write code like this.

```
Route

↓

SQL Query

↓

Return Response
```

Soon another route appears.

Then another.

Eventually

every endpoint contains SQLAlchemy code.

This becomes messy.

Instead,

professional projects separate responsibilities.

```
Router

↓

CRUD

↓

Database
```

The Router handles HTTP.

CRUD handles data.

Database handles storage.

Each layer performs one job.

---

# create_user()

Suppose a client sends

```
POST /users
```

FastAPI validates the request.

Then

the Router calls

```
crud.create_user()
```

This function creates a SQLAlchemy object.

```
User Object

↓

db.add()

↓

Database Session
```

Notice something important.

Nothing is stored yet.

---

# db.add()

Many beginners think

```
db.add()
```

immediately inserts data.

It doesn't.

It simply tells SQLAlchemy

> "Track this object."

Think of it like placing a letter inside an envelope.

You still haven't mailed it.

---

# db.commit()

This is when the actual database transaction happens.

```
Session

↓

Commit

↓

PostgreSQL
```

Only after commit does PostgreSQL permanently save the record.

Without commit,

everything disappears when the request finishes.

---

# db.refresh()

Another line that confuses beginners.

Suppose PostgreSQL automatically generates

```
id = 15
```

Our Python object still doesn't know this.

```
refresh()

↓

Reload Data

↓

Updated Python Object
```

Now

```
user.id
```

contains the correct database value.

---

# get_users()

This function performs one simple task.

```
Database

↓

SELECT *

↓

Return List
```

Notice that

the function knows nothing about HTTP.

It doesn't know

```
GET /users
```

It simply knows

"Fetch all users."

That's good architecture.

---

# get_user()

Instead of retrieving every record,

this function retrieves exactly one.

```
WHERE id = ?
```

If nothing is found,

SQLAlchemy returns

```
None
```

The Router later decides

whether that means

```
404 Not Found
```

Notice the separation.

CRUD retrieves data.

Router decides the HTTP response.

---

# update_user()

Updating follows a simple process.

```
Find User

↓

Does User Exist?

↓

Yes

↓

Update Fields

↓

Commit

↓

Refresh

↓

Return Updated Object
```

If the user doesn't exist,

CRUD simply returns

```
None
```

Again,

CRUD does not generate HTTP responses.

That is the Router's responsibility.

---

# delete_user()

Deleting follows almost the same flow.

```
Find User

↓

Delete Object

↓

Commit

↓

Return Deleted User
```

Simple.

Every CRUD function follows the same basic pattern.

---

# Why CRUD Doesn't Raise HTTPException

Many beginners ask

"Why not raise HTTPException inside crud.py?"

Because CRUD shouldn't know

that FastAPI even exists.

Imagine tomorrow

you replace FastAPI with Django.

CRUD should continue working.

This is called

**Loose Coupling.**

Our business logic depends only on SQLAlchemy,

not on FastAPI.

That makes the code easier to reuse and test.

---

# Complete Request Flow

Suppose a client creates a user.

The request travels like this.

```
Client

↓

Router

↓

Schema Validation

↓

CRUD

↓

SQLAlchemy Model

↓

Database

↓

CRUD

↓

Router

↓

Response Schema

↓

JSON

↓

Client
```

Every layer has exactly one responsibility.

This is the architecture used by professional backend applications.

---

# Mental Model

Whenever you open

```
crud.py
```

remember this sentence.

> **CRUD knows how to manipulate data—not how to communicate over HTTP.**

That single idea explains why CRUD should remain independent of FastAPI.

---

# Chapter Summary

By the end of this chapter you should understand:

✅ Why CRUD exists.

✅ Why Routers should remain thin.

✅ Why db.add(), commit(), and refresh() are separate.

✅ Why CRUD should not raise HTTPException.

✅ How a request travels from the client to PostgreSQL and back.

---


---

# Chapter 7 — security.py (The Security Toolbox of Our Application)

At this point our backend can

- connect to PostgreSQL
- validate requests
- perform CRUD operations

But there is still one huge problem.

Anyone who knows an email and password could potentially access our system if we simply stored passwords in plain text.

Professional applications never do that.

Instead, they introduce a dedicated security layer.

That layer lives inside

```
security.py
```

This file is one of the most important files in the project.

Unlike `crud.py`, it knows absolutely nothing about users.

It doesn't know what a database is.

It doesn't know what a router is.

It doesn't even know what FastAPI is.

It only knows one thing.

> **Security.**

---

# Why Does security.py Exist?

Imagine putting password hashing directly inside every route.

```
Register Route

↓

Hash Password
```

Later,

Login Route

↓

Verify Password

Later,

Admin Route

↓

Verify Token

Soon every endpoint starts repeating the same code.

Professional developers avoid duplicate logic.

Instead,

all security-related code lives inside one place.

```
security.py
```

This follows the **Single Responsibility Principle.**

---

# Responsibilities of security.py

Think of this file as a toolbox.

Whenever another part of the application needs security,

it comes here.

This file usually contains functions like

```
Hash Password

Verify Password

Create JWT Token

Decode JWT Token

Verify JWT

Create Access Token
```

Notice something.

It doesn't perform Login.

It doesn't Register Users.

Those are business operations.

It simply provides security utilities.

---

# Password Hashing

Suppose a user registers.

They send

```
Password

↓

"MyPassword123"
```

Should we store this?

Absolutely not.

Instead,

security.py performs

```
"MyPassword123"

↓

bcrypt

↓

$2b$12$XgM...

↓

Database
```

The database never sees the original password.

Only the hash.

---

# Why Can't We Reverse A Hash?

Many beginners think

"Can we convert the hash back into the original password?"

No.

Hashing is intentionally one-way.

```
Password

↓

Hash

↓

Impossible To Reverse
```

Even the developer cannot recover the original password.

The only way to check a password is

```
Entered Password

↓

Hash Again

↓

Compare

↓

Match?
```

---

# bcrypt

bcrypt is one of the most trusted password hashing algorithms.

Why?

Because it was specifically designed for passwords.

Unlike normal hashing algorithms,

bcrypt is intentionally slow.

That might sound bad,

but it's actually a security feature.

Imagine a hacker trying one billion passwords.

If hashing takes longer,

attacking becomes dramatically more difficult.

---

# Salt

bcrypt automatically adds something called a Salt.

Think of a salt as random data added before hashing.

Example

```
Password

↓

Random Salt

↓

Hash
```

Even if two users choose

```
password123
```

their hashes will still look completely different.

This prevents attackers from using precomputed lookup tables.

---

# Verifying Passwords

During Login,

the user enters

```
"MyPassword123"
```

Our database contains

```
$2b$12$XgM...
```

bcrypt performs

```
Entered Password

↓

Hash Internally

↓

Compare

↓

True / False
```

Notice something.

We never compare plain text passwords.

We compare hashes.

---

# JWT Creation

After the password is verified,

security.py creates a JWT.

```
User

↓

Authenticated

↓

Create JWT

↓

Return Token
```

The JWT becomes the user's identity card.

Instead of sending

```
Email

Password
```

with every request,

the client sends

```
Bearer Token
```

This is much safer.

---

# JWT Verification

Whenever a protected endpoint is accessed,

security.py performs

```
Receive Token

↓

Decode

↓

Verify Signature

↓

Verify Expiration

↓

Return User Information
```

If anything fails,

access is denied.

---

# Why Routers Should Never Handle Security

A router should never know

how JWT works.

It should simply ask

```
security.py

↓

Is this token valid?
```

The router doesn't care

how verification happens.

This separation keeps our code clean and reusable.

---

# Mental Model

Whenever you open

```
security.py
```

remember this sentence.

> **security.py does not know users. It only knows security.**

---

# Chapter Summary

By the end of this chapter you should understand

✅ Why security.py exists.

✅ Why passwords are hashed.

✅ Why bcrypt is used.

✅ Why JWT generation belongs here.

✅ Why routers should never implement security logic.

---

# Chapter 8 — users.py (The User Router)

Now that we understand

- Database
- Models
- Schemas
- CRUD
- Security

we need something that connects all of them together.

That job belongs to the Router.

For user-related endpoints,

the file is usually

```
routers/users.py
```

---

# What Is A Router?

A Router is simply a collection of related endpoints.

Imagine a large shopping website.

It might have

```
Products

Orders

Users

Authentication

Payments

Reviews
```

Would we put every endpoint inside

```
main.py
```

No.

That file would become thousands of lines long.

Instead,

we organize endpoints by feature.

```
users.py

↓

All User Endpoints
```

```
auth.py

↓

Login

Register

Refresh Token
```

```
products.py

↓

Product Endpoints
```

This makes navigation much easier.

---

# Responsibilities of users.py

This router only deals with user operations.

Examples

```
GET /users

GET /users/{id}

PUT /users/{id}

DELETE /users/{id}
```

Notice something.

It doesn't know

how passwords are hashed.

It doesn't know

how JWT is generated.

Those responsibilities belong elsewhere.

---

# The Router Is A Traffic Controller

Think of the router like an airport controller.

A plane arrives.

The controller doesn't repair the aircraft.

The controller simply decides

where it should go.

Similarly,

when a request arrives

```
GET /users
```

the router decides

```
↓

crud.get_users()
```

It doesn't execute SQL itself.

---

# Typical Request Flow

Suppose a client sends

```
GET /users
```

The router receives it.

```
Client

↓

Router

↓

CRUD

↓

Database

↓

CRUD

↓

Router

↓

JSON

↓

Client
```

Notice how the router sits between the client and the business logic.

---

# Dependency Injection

You'll often see

```python
db: Session = Depends(get_db)
```

inside router functions.

The router doesn't create database sessions.

Instead,

FastAPI injects one automatically.

```
Request

↓

FastAPI

↓

get_db()

↓

Database Session

↓

Router
```

This keeps routers simple.

---

# HTTPException

Suppose a user doesn't exist.

CRUD returns

```
None
```

Now the router decides

```
↓

404 Not Found
```

Why here?

Because routers understand HTTP.

CRUD doesn't.

This separation is extremely important.

---

# Response Models

Routers also decide

what gets returned.

Example

```python
response_model=UserResponse
```

This tells FastAPI

```
Database Object

↓

UserResponse

↓

JSON
```

Even if the SQLAlchemy model contains

```
hashed_password
```

the response model removes it automatically.

This protects sensitive information.

---

# Why Routers Should Stay Small

A common beginner mistake is writing

```
Database Queries

JWT

Password Hashing

Validation

Business Logic

Everything...
```

inside the router.

Professional routers should mostly do four things.

1. Receive requests.

2. Validate input.

3. Call CRUD or Services.

4. Return responses.

Nothing more.

---

# Mental Model

Whenever you open

```
users.py
```

remember

> **Routers receive HTTP requests and delegate the real work elsewhere.**

They coordinate.

They don't perform business logic.

---

# Chapter Summary

By the end of this chapter you should understand

✅ Why routers exist.

✅ Why endpoints are grouped by feature.

✅ Why routers call CRUD instead of SQLAlchemy directly.

✅ Why routers raise HTTPException.

✅ Why response models improve security.

---

---

# Chapter 9 — auth.py (The Authentication Router)

So far we have learned:

- `database.py` manages database connections.
- `models.py` describes database tables.
- `schemas.py` validates API data.
- `crud.py` performs database operations.
- `security.py` handles hashing and JWT.

Now we need a place where all of these pieces come together.

That place is

```
routers/auth.py
```

This file is responsible for **authentication endpoints**.

Authentication answers one simple question.

> **"Who is the user making this request?"**

Unlike `users.py`, this router doesn't manage user information.

Instead, it manages identity.

---

# Responsibilities of auth.py

This router usually contains endpoints like

```
POST /register

POST /login

GET /me

POST /refresh
```

Notice something.

These endpoints are completely different from CRUD.

CRUD manipulates data.

Authentication verifies identity.

---

# Why Is Authentication Separate?

Imagine putting login inside

```
users.py
```

Soon that file would contain

```
Register

Login

Logout

CRUD

JWT

Password Hashing

Profile

Everything...
```

Eventually the file becomes impossible to maintain.

Professional projects separate features.

```
users.py

↓

User Management
```

```
auth.py

↓

Authentication
```

This makes the project easier to understand.

---

# Registration Flow

Suppose a new user wants to create an account.

The client sends

```
POST /register
```

with

```json
{
    "name":"Adyaprana",
    "email":"adya@gmail.com",
    "password":"secret123"
}
```

Now the router begins working.

```
Request

↓

Schema Validation

↓

Hash Password

↓

CRUD

↓

Database

↓

Response
```

Notice something important.

The Router **never** hashes the password itself.

Instead it asks

```
security.py

↓

hash_password()
```

Likewise,

the Router doesn't insert data into PostgreSQL.

Instead it asks

```
crud.py

↓

create_user()
```

Every layer performs exactly one responsibility.

---

# Login Flow

Registration creates a user.

Login verifies a user.

Suppose the client sends

```json
{
    "email":"adya@gmail.com",
    "password":"secret123"
}
```

The router performs these steps.

```
Receive Login Request

↓

Find User

↓

Verify Password

↓

Generate JWT

↓

Return Token
```

If any step fails,

authentication fails.

---

# Password Verification

Notice the order.

```
Client Password

↓

Find Database User

↓

Retrieve Hashed Password

↓

bcrypt.verify()

↓

True?

↓

Create Token
```

The original password stored in the database is **never** read.

Only the hash is compared.

---

# Creating The Token

After successful verification,

the router asks

```
security.py

↓

create_access_token()
```

The router doesn't know

how JWT works.

It simply requests a token.

This keeps responsibilities separated.

---

# Returning The Token

Instead of returning

```
Login Successful
```

we return

```json
{
    "access_token":"eyJhbGc...",
    "token_type":"bearer"
}
```

Why?

Because every future request will use this token.

Think of it as giving the client a digital identity card.

---

# OAuth2PasswordBearer

One line often confuses beginners.

```python
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login"
)
```

This line **does not perform login.**

It simply tells FastAPI

> "Whenever a protected endpoint is accessed,
look inside the Authorization header
and extract the Bearer token."

Think of it as a token extractor.

Nothing more.

---

# Protected Endpoint

Suppose we have

```
GET /profile
```

The client sends

```
Authorization

Bearer eyJhbGc...
```

FastAPI extracts the token.

The router verifies it.

If valid,

the request continues.

Otherwise,

FastAPI returns

```
401 Unauthorized
```

before our endpoint even runs.

---

# Why auth.py Doesn't Talk To PostgreSQL Directly

Notice something.

The router never executes SQL.

Instead,

it asks

```
crud.py

↓

Find User
```

This keeps the Router independent from database logic.

Professional projects always separate these responsibilities.

---

# Mental Model

Whenever you open

```
auth.py
```

remember

> **Authentication routers verify identity. They do not perform security or database operations themselves.**

---

# Chapter Summary

By the end of this chapter you should understand

✅ Why authentication has its own router.

✅ Why password hashing belongs in security.py.

✅ Why database queries belong in crud.py.

✅ Why routers coordinate instead of doing everything.

✅ Why login returns JWT instead of user credentials.

---

# Chapter 10 — Complete JWT Authentication Flow (From Login To Protected Route)

Now it's time to connect everything we've learned.

Forget individual files.

Imagine the application is already complete.

A user opens your frontend.

Clicks

```
Login
```

What happens next?

Let's follow the entire journey.

---

# Step 1 — User Enters Credentials

The frontend collects

```
Email

Password
```

Example

```json
{
    "email":"adya@gmail.com",
    "password":"secret123"
}
```

Nothing has happened yet.

The user is **not authenticated**.

---

# Step 2 — Login Request

The frontend sends

```
POST /login
```

↓

FastAPI receives it.

↓

Pydantic validates it.

If required fields are missing,

FastAPI immediately returns

```
422 Unprocessable Entity
```

The Router is never executed.

---

# Step 3 — Find User

Validation succeeds.

The router asks

```
crud.py

↓

Find User By Email
```

CRUD queries PostgreSQL.

Two possibilities exist.

```
User Found
```

or

```
User Not Found
```

If no user exists,

authentication immediately fails.

---

# Step 4 — Verify Password

Suppose the user exists.

Database returns

```
Email

Hashed Password
```

The router sends both passwords to

```
security.py

↓

verify_password()
```

bcrypt performs

```
Entered Password

↓

Hash

↓

Compare

↓

True / False
```

Only if verification succeeds does the application continue.

---

# Step 5 — Generate JWT

Now the application knows

the user is genuine.

security.py creates

```
Header

↓

Payload

↓

Signature

↓

JWT
```

Example

```
eyJhbGc...

eyJzdWI...

f2M8...
```

The server signs this token using its secret key.

---

# Step 6 — Send Token To Client

The server responds

```json
{
    "access_token":"eyJhbGc...",
    "token_type":"bearer"
}
```

The frontend stores this token.

Usually inside

```
Memory

or

Secure Cookie

or

Local Storage
```

(Production applications often prefer **HTTP-only secure cookies** over local storage for better protection against XSS attacks.)

---

# Step 7 — Client Requests Protected Data

Later,

the frontend requests

```
GET /users
```

This time,

it includes

```
Authorization

Bearer eyJhbGc...
```

Notice

The password is **not** sent again.

Only the token.

---

# Step 8 — FastAPI Extracts The Token

FastAPI sees

```
Authorization

Bearer ...
```

OAuth2PasswordBearer extracts

only

```
eyJhbGc...
```

and passes it into the authentication dependency.

---

# Step 9 — Verify JWT

security.py performs

```
Decode Token

↓

Verify Signature

↓

Verify Expiration

↓

Read Payload
```

Three outcomes are possible.

```
Valid Token

↓

Continue
```

```
Expired Token

↓

401 Unauthorized
```

```
Invalid Signature

↓

401 Unauthorized
```

The protected endpoint executes only if the token is valid.

---

# Step 10 — Current User

Once verification succeeds,

the application knows

```
User ID

Email

Subject
```

contained inside the JWT.

It may optionally fetch the latest user information from PostgreSQL before continuing.

Now the endpoint finally runs.

---

# The Complete Journey

```
Client

↓

POST /login

↓

Schema Validation

↓

CRUD

↓

Find User

↓

Verify Password

↓

Generate JWT

↓

Return Token

↓

Client Stores Token

↓

GET /protected-route

↓

Authorization: Bearer <token>

↓

FastAPI

↓

Verify JWT

↓

Current User

↓

Protected Endpoint

↓

JSON Response
```

This is the complete authentication lifecycle used by countless modern APIs.

---

# Why JWT Is Powerful

Without JWT,

every request would need

```
Email

Password
```

Again.

And again.

And again.

Instead,

authentication happens once.

Future requests only send

```
Bearer Token
```

This keeps communication both secure and efficient.

---

# Mental Model

Whenever you think about JWT,

remember

> **A JWT is not a password. It is proof that the user has already been authenticated.**

---

# Chapter Summary

By the end of this chapter you should understand

✅ The complete login lifecycle.

✅ How JWT is generated.

✅ How JWT is verified.

✅ How protected routes work.

✅ Why passwords are never sent after login.

✅ Why authentication and authorization are separate concepts.

---

---

# Chapter 11 — Password Hashing Deep Dive (Understanding bcrypt Internals)

At this point we know that passwords should never be stored in plain text.

We also know that bcrypt converts

```
MyPassword123
```

into something like

```
$2b$12$K2xjPjM0xW...
```

But a good backend engineer should ask one more question.

> **"How does bcrypt actually work?"**

This chapter answers that question.

---

# Why Can't We Store Plain Passwords?

Imagine your database looks like this.

| Email | Password |
|--------|----------|
| adya@gmail.com | mypassword123 |
| john@gmail.com | hello123 |
| alice@gmail.com | admin123 |

Now imagine someone steals your database.

Every user's password is immediately exposed.

This has happened to many companies over the years.

Professional applications assume that

> **One day the database might leak.**

Therefore,

even if someone steals the database,

they should never be able to recover user passwords.

That's why we hash them.

---

# Hashing Is A One-Way Process

Hashing works like this.

```
Password

↓

Hash Function

↓

Hash
```

Unlike encryption,

there is no reverse process.

```
Password

↓

Hash

❌

Cannot Recover Original Password
```

Once hashed,

the original password is mathematically impractical to recover.

---

# Then How Does Login Work?

Many beginners ask

> "If we can't recover the password,
how do we compare it?"

The answer is simple.

Suppose the database stores

```
$2b$12$ABCXYZ...
```

The user enters

```
MyPassword123
```

bcrypt performs

```
Entered Password

↓

Hash Again

↓

Compare

↓

Match?
```

The original password is never needed.

---

# Why Not Use Python's hash() Function?

Python already has

```python
hash("password")
```

Why don't we use it?

Because it was never designed for password security.

Python's `hash()`:

- Changes between program executions.
- Is designed for hash tables and dictionaries.
- Is fast.

Fast is actually bad for password hashing.

Attackers can test millions of passwords every second.

bcrypt is intentionally slow.

That makes brute-force attacks much harder.

---

# What Makes bcrypt Special?

bcrypt provides several important security features.

### 1. It Is Slow

Suppose hashing takes

```
0.3 seconds
```

Now imagine an attacker trying

```
1 billion passwords
```

That would take an enormous amount of time.

This is exactly why bcrypt exists.

---

### 2. Automatic Salt

bcrypt automatically generates a random value called a **Salt**.

Think of a Salt as extra random data.

```
Password

+

Random Salt

↓

bcrypt

↓

Hash
```

Now imagine two users choose

```
password123
```

Without Salt

```
Hash A

=

Hash B
```

With Salt

```
Hash A

≠

Hash B
```

Even identical passwords produce completely different hashes.

This prevents attackers from recognizing users with the same password.

---

### 3. Cost Factor

bcrypt also stores something called the **Cost Factor**.

Example

```
$2b$12$...
```

The number

```
12
```

represents the computational cost.

Higher cost means

- Better security
- Slower hashing

Professional applications choose a balance between performance and security.

---

# Why Do We Hash During Registration?

Registration Flow

```
Client

↓

Password

↓

bcrypt.hash()

↓

Database
```

The original password exists only briefly in memory.

After hashing,

it is discarded.

Only the hash reaches PostgreSQL.

---

# Why Do We Verify During Login?

Login Flow

```
Entered Password

↓

bcrypt.verify()

↓

Stored Hash

↓

True / False
```

Notice

We never compare plain text passwords.

We compare the entered password against the stored hash.

---

# Common Beginner Mistake

Many beginners think

```
Stored Hash

↓

Decrypt

↓

Password
```

This is impossible.

Hashing is not encryption.

Passwords are **never decrypted**.

---

# Mental Model

Whenever you think about password hashing,

remember

> **The server never remembers your password. It only remembers proof that it once knew your password.**

---

# Chapter Summary

By the end of this chapter you should understand

✅ Why passwords are hashed.

✅ Why hashing cannot be reversed.

✅ Why bcrypt is preferred.

✅ What Salt does.

✅ What the Cost Factor means.

✅ Why login verifies instead of decrypting.

---

# Chapter 12 — Dependency Injection Deep Dive (The Magic Behind Depends)

This chapter explains one of the most confusing concepts in FastAPI.

Many beginners write

```python
db: Session = Depends(get_db)
```

without understanding

who calls `get_db()`,

where `db` comes from,

or why it suddenly appears inside the function.

Let's solve that mystery.

---

# What Is Dependency Injection?

Imagine a restaurant.

A chef cooks food.

Does the chef grow vegetables?

Raise chickens?

Make plates?

No.

Everything the chef needs is provided.

```
Restaurant

↓

Ingredients

↓

Chef

↓

Food
```

This idea is called **Dependency Injection**.

Someone else provides what you need.

---

# Without Dependency Injection

Suppose every endpoint creates its own database session.

```python
@app.get("/users")
def get_users():

    db = SessionLocal()

    ...
```

Another endpoint

```python
@app.post("/users")

db = SessionLocal()
```

Another endpoint

```python
@app.delete("/users")

db = SessionLocal()
```

Soon,

the same code appears everywhere.

This violates the DRY Principle.

---

# With Dependency Injection

Instead,

FastAPI creates the session.

```python
db: Session = Depends(get_db)
```

Now our endpoint simply says

> "I need a database session."

FastAPI replies

> "I'll provide one."

This makes endpoints much cleaner.

---

# What Does Depends() Actually Do?

Many beginners think

```
Depends()

↓

Creates Database
```

Not exactly.

Depends simply tells FastAPI

> "Before executing this endpoint,
run another function first."

That function is

```
get_db()
```

---

# The Hidden Flow

When a request arrives,

FastAPI performs

```
Request

↓

See Depends()

↓

Call get_db()

↓

Receive Session

↓

Pass Session Into Endpoint

↓

Execute Endpoint

↓

Close Session
```

Notice

Your endpoint never creates the session.

FastAPI does.

---

# Why Does get_db() Use yield?

Suppose

```python
return db
```

was used.

FastAPI would receive the session,

but it wouldn't know

when to close it.

Instead,

we write

```python
yield db
```

Think of `yield` as a pause button.

```
Open Session

↓

yield

↓

Endpoint Executes

↓

Resume Function

↓

Close Session
```

This guarantees cleanup.

Even if an exception occurs,

the database session is still closed.

---

# Dependency Injection Isn't Only For Databases

Many beginners think Depends is only used for SQLAlchemy.

Actually,

FastAPI can inject anything.

Examples

```
Database Session

Current User

JWT Token

Configuration

Logger

Cache

Settings

API Client
```

Any reusable dependency can be injected.

---

# get_current_user()

Authentication uses exactly the same mechanism.

Suppose we write

```python
current_user = Depends(get_current_user)
```

FastAPI performs

```
Request

↓

Extract JWT

↓

Verify JWT

↓

Find User

↓

Pass User Into Endpoint
```

Your endpoint immediately receives

```
current_user
```

without writing any authentication logic.

That's the real power of Dependency Injection.

---

# Why This Is Better

Imagine verifying JWT inside every endpoint.

```
Decode Token

↓

Verify Signature

↓

Find User
```

Again.

Again.

Again.

Instead,

we place all of that logic inside

```
get_current_user()
```

Every protected endpoint simply writes

```python
Depends(get_current_user)
```

One line.

Professional applications rely heavily on this pattern.

---

# Mental Model

Whenever you see

```python
Depends(...)
```

remember

> **My endpoint is requesting something that FastAPI will provide before it runs.**

The endpoint doesn't create it.

FastAPI injects it.

---

# Chapter Summary

By the end of this chapter you should understand

✅ What Dependency Injection is.

✅ Why Depends() exists.

✅ Why get_db() uses yield.

✅ Why FastAPI manages database sessions.

✅ Why get_current_user() is also a dependency.

✅ Why Dependency Injection reduces duplicate code.

---

---

# Chapter 13 — Complete Request Lifecycle (From Browser to Database and Back)

Congratulations.

At this point you've learned every major component of our backend:

- `main.py`
- `database.py`
- `models.py`
- `schemas.py`
- `crud.py`
- `security.py`
- `routers/users.py`
- `routers/auth.py`

Now let's connect everything together.

This chapter follows **one complete request** through the entire backend.

Understanding this flow is much more important than memorizing syntax.

---

# Scenario

A user wants to log in.

They enter

```
Email

Password
```

and click

```
Login
```

Let's follow the journey.

---

# Step 1 — Browser Creates HTTP Request

The frontend creates

```
POST /login
```

with

```json
{
    "email":"adya@gmail.com",
    "password":"secret123"
}
```

Nothing has reached Python yet.

This is still happening inside the browser.

---

# Step 2 — HTTP Request Reaches Uvicorn

The request arrives at

```
http://localhost:8000/login
```

Uvicorn receives it.

Remember:

FastAPI is **not** the web server.

Uvicorn is.

Its job is to

- Listen on port 8000
- Accept HTTP requests
- Forward them to FastAPI

```
Browser

↓

Uvicorn
```

---

# Step 3 — FastAPI Receives The Request

FastAPI now begins processing.

First,

it checks

```
HTTP Method

↓

POST
```

Then

```
URL

↓

/login
```

It searches its routing table.

```
POST /login

↓

Found

↓

auth.py
```

The correct router is selected.

---

# Step 4 — Dependency Injection Starts

Before the endpoint executes,

FastAPI checks

```
Depends(...)
```

If dependencies exist,

they execute first.

Example

```
Depends(get_db)
```

↓

Create Database Session

If authentication is required

```
Depends(get_current_user)
```

↓

Verify JWT

↓

Load Current User

Only after every dependency succeeds

does the endpoint continue.

---

# Step 5 — Pydantic Validation

Before your function executes,

FastAPI validates the request body.

Incoming JSON

↓

Schema

↓

Valid?

If validation fails,

FastAPI immediately returns

```
422 Unprocessable Entity
```

Your endpoint never runs.

This is why Pydantic is so powerful.

---

# Step 6 — Router Executes

Now FastAPI finally calls

```
login()
```

inside

```
auth.py
```

The Router itself remains very small.

It simply coordinates.

```
Router

↓

CRUD

↓

Security

↓

Response
```

---

# Step 7 — CRUD Communicates With PostgreSQL

The Router asks

```
crud.get_user_by_email()
```

CRUD creates SQLAlchemy queries.

```
SQLAlchemy

↓

PostgreSQL

↓

User Object
```

Notice

CRUD never returns JSON.

It returns Python objects.

---

# Step 8 — Security Layer

The Router now asks

```
security.verify_password()
```

If correct

↓

Generate JWT

↓

Return Token

If incorrect

↓

401 Unauthorized

Again,

the Router never hashes passwords itself.

---

# Step 9 — Response Model

Suppose authentication succeeds.

FastAPI now prepares the response.

If

```
response_model=UserResponse
```

is used,

FastAPI filters the output.

Only safe fields remain.

Sensitive information

like

```
hashed_password
```

is automatically removed.

---

# Step 10 — JSON Response

FastAPI converts

Python Objects

↓

JSON

↓

HTTP Response

↓

Browser

The client finally receives

```json
{
    "access_token":"eyJhbGc...",
    "token_type":"bearer"
}
```

---

# Complete Request Flow

```
                Browser

                   │

                   ▼

             HTTP Request

                   │

                   ▼

               Uvicorn

                   │

                   ▼

               FastAPI

                   │

                   ▼

        Dependency Injection

                   │

                   ▼

         Pydantic Validation

                   │

                   ▼

             Router (auth.py)

                   │

        ┌──────────┴──────────┐

        ▼                     ▼

   security.py            crud.py

        │                     │

        ▼                     ▼

    JWT / bcrypt        SQLAlchemy ORM

                              │

                              ▼

                         PostgreSQL

                              │

                              ▼

                       SQLAlchemy Model

                              │

                              ▼

                        Response Model

                              │

                              ▼

                          JSON Response

                              │

                              ▼

                            Browser
```

Everything you've learned over Days 43–46 fits into this single diagram.

This is the architecture used by thousands of production FastAPI applications.

---

# Mental Model

Whenever you're confused,

return to this sentence:

> **Every request follows the same journey: Client → FastAPI → Validation → Router → Business Logic → Database → Response.**

If you understand this,

you understand backend architecture.

---

# Chapter Summary

By the end of this chapter you should understand

✅ How a request travels through the application.

✅ The order in which FastAPI executes components.

✅ Where validation occurs.

✅ Where security occurs.

✅ Where database queries occur.

✅ Where JSON responses are generated.

---

# Chapter 14 — Interview Guide, Best Practices & Senior Engineer Notes

Congratulations.

You now understand how a complete FastAPI backend works.

This final chapter summarizes the lessons that every backend engineer should remember.

---

# Most Common Interview Questions

### 1. What is FastAPI?

A modern Python web framework for building high-performance APIs using type hints, automatic validation, dependency injection, and automatic OpenAPI documentation.

---

### 2. What is Pydantic?

A data validation library.

It validates incoming and outgoing API data using Python type hints.

---

### 3. Difference Between Models And Schemas?

Models

↓

Database Structure

Schemas

↓

API Request & Response Validation

---

### 4. Why Use SQLAlchemy?

Because it allows us to work with Python objects instead of writing raw SQL for every operation.

---

### 5. What Is CRUD?

Create

Read

Update

Delete

The four basic database operations.

---

### 6. What Is Dependency Injection?

A design pattern where required objects are provided automatically instead of being created manually.

FastAPI implements this using

```
Depends()
```

---

### 7. Why Use JWT?

JWT allows stateless authentication.

The server doesn't need to remember logged-in users.

Clients prove their identity by sending a signed token.

---

### 8. Why Hash Passwords?

Because passwords should never be stored in plain text.

Hashing protects user credentials even if the database is compromised.

---

### 9. Difference Between Authentication And Authorization?

Authentication

↓

Who are you?

Authorization

↓

What are you allowed to do?

---

### 10. What Is OAuth2PasswordBearer?

A FastAPI dependency that extracts the Bearer token from the Authorization header.

It **does not** authenticate users by itself.

---

# Common Beginner Mistakes

❌ Putting SQL queries inside routers.

✔ Database logic belongs inside CRUD or service layers.

---

❌ Returning database models directly.

✔ Use Response Schemas.

---

❌ Storing passwords directly.

✔ Always hash passwords.

---

❌ Returning passwords inside API responses.

✔ Never expose sensitive information.

---

❌ Writing huge `main.py`.

✔ Split routes into routers.

---

❌ Creating database sessions manually everywhere.

✔ Use Dependency Injection.

---

❌ Hardcoding SECRET_KEY.

✔ Store secrets inside environment variables.

---

# Senior Engineer Notes

As applications grow,

new layers appear.

```
Routers

↓

Services

↓

Repositories

↓

Models

↓

Database
```

Notice

CRUD often evolves into

```
Repositories

+

Services
```

This separation becomes useful in larger projects.

---

Production applications also introduce

- Docker
- Alembic Migrations
- Redis
- Celery / Background Tasks
- Logging
- Monitoring
- Unit Testing
- CI/CD
- Environment Variables
- API Versioning

Don't worry if your project doesn't include these yet.

Those topics come later in your roadmap.

---

# Best Practices

Always

✅ Use virtual environments.

✅ Separate Models and Schemas.

✅ Keep Routers thin.

✅ Keep Business Logic outside Routers.

✅ Use Dependency Injection.

✅ Hash passwords.

✅ Use JWT expiration.

✅ Validate every request.

✅ Return proper HTTP status codes.

✅ Write readable code.

---

# Learning Checklist

After completing Days 43–46,

you should confidently understand

☑ FastAPI

☑ Uvicorn

☑ Routing

☑ Path Parameters

☑ Query Parameters

☑ Pydantic

☑ SQLAlchemy

☑ PostgreSQL

☑ CRUD

☑ Dependency Injection

☑ JWT

☑ bcrypt

☑ Password Hashing

☑ OAuth2PasswordBearer

☑ Protected Routes

☑ Response Models

☑ Layered Architecture

---

# Final Message

Congratulations.

Over these four days, you've moved from writing simple API endpoints to understanding the architecture of a production-style backend.

Remember this:

> **Great backend engineers don't memorize code. They understand the responsibilities of each layer and how those layers communicate.**

Syntax changes.

Frameworks evolve.

Architectural thinking lasts throughout your career.

Keep building.

Keep asking *why* before *how*.

That's how you'll become the kind of backend engineer who can confidently design, build, debug, and scale real-world applications.

---

# End of Guide