# 🚀 Backend Developer Journey — Project 1 (URL Shortener API)

# Day 54 — Repository Pattern.


# Step 1 — What is a Repository?
# Imagine someone asks: "Save this URL in the database."

# Where should that code go?

# Option 1
# Inside the router.
# @app.post("/shorten")
# def create_url():
    # SQLAlchemy code here
# Works-> Yes. | Professional-> No.

# Option 2
# Inside the service.
# def create_short_url():
    # SQLAlchemy code here
# Still works. But now your business logic and database logic are mixed.

# Option 3
# Use a Repository.
# Think of it like this: Router → Service → Repository → Database
# Every layer has one job.

# Responsibilities:

# Router:
# Receive HTTP requests.
# Validate request schema.
# Return response.

# Service:
# Business logic.
# Generate short codes.
# Decide what should happen.

# Repository:
# Talk to PostgreSQL.
# Insert data.
# Fetch data.
# Update data.
# Delete data (later).

# Real Life Analogy

# Imagine a restaurant: Customer → Waiter → Chef → Store Room
# Mapping it to our project: Client → Router (Waiter) → Service (Chef) → Repository (Store Room) → Database
# Notice something. The chef never walks into the store room. He asks someone else to bring ingredients. That's exactly what the Service does.

# Today's Repository

# We'll create:
# app/
#     repositories/
#         url_repository.py

# Initially, it will have one method.
# create_url(...)
# That's it. No updates, No deletes, No search, One responsibility.


# Suppose tomorrow we switch from PostgreSQL to MongoDB.
# Where should the change happen?
# Option A -> Router
# Option B -> Service
# Option C -> Repository

# Answer : Repository.
# Because only the Repository should know how data is stored. 
# The Service shouldn't care if the data comes from: PostgreSQL, MongoDB, Redis, CSV, API
# It only says: "Save this URL."
# The Repository decides how.
# That's called Separation of Concerns, and it's one of the main reasons we use this pattern.

# Today's Build Order:

# Create Repository
#         ↓
# Create create_url()
#         ↓
# Understand Session
#         ↓
# Insert First Row
#         ↓
# Verify in pgAdmin

# Layer Responsibilities
# Project architecture: Client → URLCreate (Schema) → Router → Service → Repository → Database
# Each layer should only know what it needs to know.

# Router knows -> Pydantic Schemas
# Because it's dealing with HTTP requests.

# Repository knows -> SQLAlchemy Models & Database Session
# Because it's dealing with the database.

# Service is the Translator
# Think of the Service as the bridge.
# Client
#     ↓
# URLCreate (Pydantic)
#     ↓
# Router
#     ↓
# Service  ← Converts data
#     ↓
# ShortenedURL (SQLAlchemy Model)
#     ↓
# Repository
#     ↓
# Database
# The Service takes the validated request data and creates a SQLAlchemy model object. The Repository doesn't need to know where that object came from.

# Why is this better -> Imagine tomorrow you stop using FastAPI and build a CLI.
# Instead of: FastAPI → Pydantic
# you have: CLI → argparse
# The Repository doesn't change. Because it only works with database models. That's a big advantage.

# A Simple Example
# Repository depends on Pydantic
# def create_url(data: URLCreate):
# Now the Repository knows about FastAPI/Pydantic. That's not ideal.

# Repository depends on Models
# def create_url(url: ShortenedURL):
# Now it only knows about the database model. That's exactly its job.

# Rule of Thumb
# If you are writing code that talks to the database, it belongs in the Repository.
# | Layer      | Knows About                  |
# | ---------- | ---------------------------- |
# | Router     | FastAPI + Pydantic           |
# | Service    | Pydantic + SQLAlchemy Models |
# | Repository | SQLAlchemy Models + Database |
# This keeps dependencies flowing in one direction.



# 🚀 Now let's build the Repository

# Create a new file: app/repositories/url_repository.py

# Add this code:
# from sqlalchemy.orm import Session
# from app.models.shortened_url import ShortenedURL
# class URLRepository:
#     """
#     Handles all database operations for shortened URLs.
#     """
#     def create(self, db: Session, url: ShortenedURL) -> ShortenedURL:
#         """
#         Save a new shortened URL to the database.
#         """
#         db.add(url)
#         db.commit()
#         db.refresh(url)
#         return url

# Understand the flow
# The Repository's job is only: Receive SQLAlchemy Model → Save to Database → Return Saved Model

# It does not: Generate short codes, Validate URLs, Build HTTP responses, Handle requests. Only database operations.
# What do these three lines do?
# db.add(url) -> Adds the object to the current session.
# db.commit() -> Permanently saves it in PostgreSQL. Without commit(), nothing is stored.
# db.refresh(url) -> Reloads the object from the database.
# This is important because PostgreSQL generates values like: id, created_at
# After refresh(), those values are available in Python.
# Example:
# Before commit: id = None
# After commit + refresh: id = 1

# Today's Goal
# app/
# │
# ├── database/
# ├── models/
# ├── schemas/
# └── repositories/
#       └── url_repository.py ✅
# We won't call it yet because the Service layer doesn't exist.

# Tomorrow, we'll build the Service, connect everything together, and then finally create our first working endpoint:
# Client → URLCreate → Router → Service → Repository → PostgreSQL → URLResponse → Client



# Create a temporary script: test_repository.py Just for learning.
# Flow: Create ShortenedURL Object → URLRepository.create() → PostgreSQL → Verify in pgAdmin

# This will let you actually see:
# db.add()
# db.commit()
# db.refresh()
# working before we introduce Services and Routers. 

# Then tomorrow we can delete this file because it was only for learning. I think that's a much better learning experience than waiting another day before seeing the Repository do something.






# We want to prove that our Repository actually works.
# Flow: Create ShortenedURL Object → Repository.create() → PostgreSQL → Check pgAdmin
# No FastAPI, No Router, No Service, Just Python → Repository → Database.


# Step 1 — One Small Change
# Before writing the test script, we need one helper.
# Open: app/database/database.py
# At the top, change this import: from sqlalchemy.orm import sessionmaker
# to: from sqlalchemy.orm import Session, sessionmaker
# Now your imports become: from sqlalchemy.orm import Session, sessionmaker
# Why? Because we'll use the Session type hint.


# Step 2 — Create the Test Script
# In the project root (same level as main.py), create: test_repository.py
# Project structure:
# url_shortener_api/
# │
# ├── app/
# ├── main.py
# ├── test_repository.py   👈 NEW


# Step 3 — Write This Code

# from app.database.database import SessionLocal
# from app.models.shortened_url import ShortenedURL
# from app.repositories.url_repository import URLRepository
# def main():
#     db = SessionLocal()
#     repository = URLRepository()
#     url = ShortenedURL(
#         original_url="https://google.com",
#         short_code="abc123"
#     )
#     saved_url = repository.create(db, url)
#     print("ID:", saved_url.id)
#     print("Original URL:", saved_url.original_url)
#     print("Short Code:", saved_url.short_code)
#     print("Clicks:", saved_url.clicks)
#     print("Created At:", saved_url.created_at)
#     db.close()
# if __name__ == "__main__":
#     main()


# Let's Understand the Flow
# Instead of our final architecture: Client → URLCreate → Router → Service → Repository → Database
# We're temporarily doing: Python Script → Repository → Database
# This isolates the Repository and lets us test it by itself. This is a common engineering practice: test one layer at a time.
# Run: python test_repository.py

# Expected output: 
# ID: 1
# Original URL: https://google.com
# Short Code: abc123
# Clicks: 0
# Created At: 2026-...

# Notice: 
# We never set: id, clicks, created_at
# Yet they have values. Why?

# id → Generated by PostgreSQL.
# clicks → Default value from our model.
# created_at → Automatically generated when the row is inserted.
# This demonstrates why db.refresh() is useful—it reloads those generated values into the Python object.

# Verify in pgAdmin
# After the script runs: Right-click: shortened_urls -> View/Edit Data -> All Rows
# You should see:   id	original_url	   short_code	clicks
                #   1	https://google.com	abc123	      0

# This script is temporary.
# After we build: Router, Service, Endpoint
# we won't need it anymore We'll either delete it or move it into a proper testing setup later. It's just a learning tool.




# 🧠 Important Concepts (Day 54)
# 1. What is the Repository Pattern?
# Answer: The Repository Pattern separates database operations from business logic.
# Flow: Client → Router → Service → Repository → Database
# The Repository's only responsibility is communicating with the database.

# 2. Why do we use a Repository?
# Without Repository: Router → Database (Business logic and database logic become mixed.)
# With Repository: Router → Service → Repository → Database (Each layer has one responsibility.)

# 3. What does the Repository know?
# The Repository knows: SQLAlchemy Models, Database Session, CRUD operations
# It should not know: FastAPI, HTTP requests,Pydantic request validation, Business rules

# 4. Why shouldn't the Repository use Pydantic Schemas?
# Because Schemas belong to the API layer. Repositories belong to the database layer.
# Keeping them separate reduces coupling and makes the Repository reusable.

# 5. What is a Session?
# A Session is a temporary conversation with the database.
# Flow: Open Session → Query/Insert/Update → Commit/Rollback → Close Session

# 6. What does db.add() do?
# Adds the object to the current SQLAlchemy session. It does not save it to PostgreSQL yet.

# 7. What does db.commit() do?
# It permanently saves the pending changes to the database. Without commit(), the data is not stored.

# 8. What does db.refresh() do?
# It reloads the object from the database. Useful for getting database-generated values like: id, created_at


# 🎤 Interview Questions

# Q1. What is the Repository Pattern?
# Answer: The Repository Pattern abstracts database operations into a dedicated layer, keeping business logic separate from persistence logic.

# Q2. Why not write SQLAlchemy code inside the Router?
# Answer: Because routers should handle HTTP requests and responses. Database logic belongs in the Repository, which improves maintainability and separation of concerns.

# Q3. What is the responsibility of the Service layer?
# Answer: The Service layer contains business logic. It coordinates repositories, applies business rules, and decides what operations should happen.

# Q4. What is the responsibility of the Repository layer?
# Answer: The Repository layer performs database operations such as creating, reading, updating, and deleting records.

# Q5. What is the difference between add() and commit()?
# Answer: add() -> places the object into the current session.
#         commit()-> writes the session's pending changes to the database.

# Q6. Why do we call refresh() after commit()?
# Answer: To reload the object with values generated by the database, such as auto-generated IDs or timestamps.

# Q7. Which layer should know about SQLAlchemy?
# Answer: The Repository layer.

# Q8. Which layer should know about Pydantic?
# Answer: The Router layer, and sometimes the Service layer as it translates validated request data into domain/database objects.

# Every layer should have a single responsibility.
# Our architecture now looks like this: Client → Router (HTTP) → Service (Business Logic) → Repository (Database Operations) → PostgreSQL
# That's the biggest lesson from today.



# 🧠 Important Concepts (Day 54)

# 1. What is the Repository Pattern?
# Answer: The Repository Pattern separates database operations from business logic.
# Flow: Client → Router → Service → Repository → Database

# 2. What does db.add() do?
# Adds an object to the current SQLAlchemy session. It does not save it to the database.

# 3. What does db.commit() do?
# Commits the current transaction and permanently saves changes to PostgreSQL. Without commit(), nothing is stored.

# 4. What does db.refresh() do?
# Reloads the object from the database. Useful for retrieving values generated by the database such as: id, created_at

# 5. Why separate Repository and Service?
# The Repository is responsible for how data is stored. The Service is responsible for what should happen according to business rules. This separation makes the code easier to maintain and test.

# 6. What is a SQLAlchemy Session?
# A Session represents one unit of work with the database.
# Flow: Open Session → Perform Operations → Commit/Rollback → Close Session

# 🎤 Interview Questions
# Q1. What is the Repository Pattern?
# Answer: The Repository Pattern abstracts all database operations into a dedicated layer, keeping persistence logic separate from business logic.

# Q2. What is the difference between add() and commit()?
# Answer: add() stages an object in the current session.
#         commit() writes the staged changes to the database.

# Q3. Why do we call refresh() after commit()?
# Answer: # To synchronize the Python object with the database and retrieve values generated during insertion, such as auto-increment IDs or timestamps.

# Q4. What is a Session in SQLAlchemy?
# Answer: A Session is a unit of work that manages database operations and transactions. It tracks changes to objects and coordinates communication with the database.

# Q5. Why should the Repository not know about Pydantic?
# Answer: Because Pydantic belongs to the API layer. The Repository should only work with SQLAlchemy models and the database, keeping concerns separated.

# The complete flow will become:

# Client → URLCreate (Schema) → Router → URLService → URLRepository → PostgreSQL
#                                            ↓
#                                    Generate Short Code
#                                            ↓
# Client ← URLResponse (Schema) ← URLService ← URLRepository ← Database