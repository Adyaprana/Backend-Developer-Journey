# DAY 45 — Database Integration (FastAPI + PostgreSQL + SQLAlchemy)

# Yesterday, our API looked like this:
# @app.post("/users")
# # def create_user(user: UserCreate):
#     return user

# We validated the request. But where is the data stored? Nowhere.

# The moment the request finishes...
# Client -> POST /users -> FastAPI -> Validate -> Return Response -> ❌ Data disappears
# Because RAM is temporary. If you restart your server, everything disappears.

# A real application needs persistent storage. That's why we use databases.

# How Does FastAPI Reach PostgreSQL
# This is the complete flow.
# Client -> FastAPI -> Pydantic Schema -> SQLAlchemy ORM -> PostgreSQL -> SQLAlchemy -> FastAPI -> JSON Response

# Notice something. FastAPI never talks directly to PostgreSQL.
# SQLAlchemy sits in between. 

# Why Not Write SQL Yourself?
# You could write:
# INSERT INTO users(name, email)
# VALUES ('Adya', 'adya@gmail.com');

# Nothing wrong with that. But imagine writing SQL for:
# 50 tables
# 300 queries
# relationships
# updates
# filtering

# It becomes difficult to maintain.
# Instead, SQLAlchemy lets you work with Python objects.

# Instead of: INSERT INTO users ...
# We write:
# user = User(
#     name="Adya",
#     email="adya@gmail.com"
# )
# db.add(user)

# Much cleaner. Industry Standard Project Structure 

# Yesterday we only had => main.py

# Today our project starts becoming a real backend.

# app/
# │
# ├── main.py
# ├── database.py      ← Database connection
# ├── models.py        ← SQLAlchemy models
# ├── schemas.py       ← Pydantic models
# ├── crud.py          ← Database operations
# └── requirements.txt

# Later we'll make it even more modular. But this is the perfect starting structure.


# What Does Each File Do?
# database.py -> Think of this as "Database Manager."

# Its responsibilities:
# connect to PostgreSQL
# create engine
# create session
# provide database connection
# Nothing else.

# models.py -> Think of it as "Database Blueprint."

# Example: Users Table
# | id | name | email | password |

# This table becomes
# class User(Base):
# SQLAlchemy creates the actual table.

# schemas.py
# This has nothing to do with PostgreSQL.
# This is purely request and response validation.

# Example: 
# UserCreate -> receives data from the client.
# UserResponse -> returns data to the client.

# This Is Extremely Important
# Its not Model == Schema

# They're completely different.
# SQLAlchemy Model Represents: 
# Database Table: PostgreSQL -> users table -> class User(Base):

# Pydantic Schema Represents:
# API Data: Incoming JSON -> Validation -> Python Object

# Think like this: Browser -> Schema -> Model -> Database
# Two different jobs.



# The Biggest New Concept Today is Dependency Injection

# Imagine a restaurant. Customer orders pizza. Does the chef bring flour from home? No. The restaurant gives the chef ingredients.

# That's Dependency Injection.
# Someone else provides what you need.

# Without Dependency Injection:
# def create_user():
#     db = Session()

# Every function creates its own database connection. Very bad.

# Instead:
# def create_user(db=Depends(get_db)):
# FastAPI says Don't worry. I'll provide the database session.

# What is get_db() -> Imagine this function.
# def get_db():
#     db = Session()
#     try:
#         yield db
#     finally:
#         db.close()

# This means
# When request starts -> Open database connection -> Give it to endpoint -> Endpoint finishes -> Automatically close connection (No leaks)

# Think visually.
# Request -> Open Session -> Endpoint Uses DB -> Response -> Close Session
# This happens for every request.

# Why Use yield Instead of return?
# This is one of FastAPI's clever features.
# If we did return db FastAPI wouldn't know when to close it. With yield db
# FastAPI pauses the function, lets the endpoint use the session, then resumes the function after the response is sent and executes the cleanup code.
# This pattern ensures sessions are always closed properly.



# CRUD ->  Every backend application eventually performs four basic operations.

# Create:
# POST /users (Insert new record)

# Read:
# GET /users (Retrieve records)

# Update:
# PUT /users/1 (Modify record)

# Delete:
# DELETE /users/1 (Remove record)

# Almost every backend application is built around these operations.



# Today's Architecture
# Browser -> POST /users -> FastAPI -> UserCreate Schema -> CRUD Function -> SQLAlchemy Model -> Database Session -> PostgreSQL



# Part 1 — Environment Setup
# Create a virtual environment
# Install FastAPI, SQLAlchemy, PostgreSQL driver
# Verify PostgreSQL connection

# Part 2 — database.py
# Understand the Engine
# Understand SessionLocal
# Understand Base
# Understand get_db()

# Part 3 — models.py
# Create the User SQLAlchemy model
# Learn how Python classes become database tables

# Part 4 — schemas.py
# Create UserCreate and UserResponse
# Learn why schemas and models are separate

# Part 5 — CRUD Operations
# Create 
# Read
# Update
# Delete

# Part 6 — Test Everything
# Use Swagger to verify every endpoint
# Confirm data is actually stored in PostgreSQL

