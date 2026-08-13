# 🚀 Backend Developer Journey — Project 1 (URL Shortener API)

# Day 52 — First Database Model
# Today, Python will create a PostgreSQL table. This is where SQLAlchemy starts showing its real power.

# Step 1 — What is an ORM? 
# Before touching the keyboard, only one concept. Imagine we want to create this table manually.

# CREATE TABLE shortened_urls (
#     id SERIAL PRIMARY KEY,
#     original_url TEXT NOT NULL,
#     short_code VARCHAR(10) UNIQUE NOT NULL,
#     clicks INTEGER DEFAULT 0,
#     created_at TIMESTAMP
# );
 
# That's pure SQL. But we're writing Python. Instead of SQL, we write: class ShortenedURL(Base): ...

# SQLAlchemy translates our Python class into SQL. That's why it's called an Object Relational Mapper (ORM).
# Think of it like this: Python Class → SQLAlchemy ORM → PostgreSQL Table
# We'll build in this order: Base → Model → Create Tables → Run App → Check pgAdmin











# Step 2 — Where should Base live?
# This is our first engineering decision today.

# Many tutorials do this: models.py
# Base = declarative_base()
# Works.
# But later, if you have:
# 10 models
# 20 models
# 50 models
# Every model needs Base.
# So instead of putting it inside one model, we'll keep it in the database layer.

# Our structure becomes:
# app/
# │
# ├── database/
# │     ├── database.py
# │     └── base.py   👈 NEW
# │
# ├── models/

# This keeps responsibilities clean.
# database.py → Database connection
# base.py → Base class
# models/ → Database models












# Step 3 — Create base.py
# Create a new file: app/database/base.py

# from sqlalchemy.orm import DeclarativeBase
# class Base(DeclarativeBase):
#     """
#     Base class for all SQLAlchemy models.
#     """
#     pass

# Let's Understand It
# In SQLAlchemy 2.0, this is the modern way.

# Old tutorials use:

# from sqlalchemy.orm import declarative_base
# Base = declarative_base()

# You'll still see it everywhere. It still works. But DeclarativeBase is the recommended approach for new SQLAlchemy 2.x projects.

# What does Base actually do?
# Every model will inherit from it.

# Example: class ShortenedURL(Base):
# By inheriting from Base, SQLAlchemy knows: "This class represents a database table."
# Without Base, it's just a normal Python class.















# Step 4 — Create Our First Model
# Create a new file: app/models/shortened_url.py

# Now write this:
# from datetime import datetime

# from sqlalchemy import DateTime, Integer, String, Text
# from sqlalchemy.orm import Mapped, mapped_column

# from app.database.base import Base


# class ShortenedURL(Base):
#     __tablename__ = "shortened_urls"

#     id: Mapped[int] = mapped_column(
#         Integer,
#         primary_key=True,
#         index=True
#     )

#     original_url: Mapped[str] = mapped_column(
#         Text,
#         nullable=False
#     )

#     short_code: Mapped[str] = mapped_column(
#         String(10),
#         unique=True,
#         nullable=False,
#         index=True
#     )

#     clicks: Mapped[int] = mapped_column(
#         Integer,
#         default=0,
#         nullable=False
#     )

#     created_at: Mapped[datetime] = mapped_column(
#         DateTime,
#         default=datetime.utcnow,
#         nullable=False
#     )


# 1. __tablename__
# __tablename__ = "shortened_urls"
# This tells SQLAlchemy: "Create a PostgreSQL table named shortened_urls."
# Without it, SQLAlchemy would try to generate a table name automatically, which we don't want.


# 2. id
# id: Mapped[int]
# This says:
# Python type → int
# Database type → INTEGER
# Primary Key → Yes
# Indexed → Yes
# This becomes: id INTEGER PRIMARY KEY


# 3. original_url
# Text
# Remember our Day 50 discussion?
# We chose TEXT because URLs can be long. Good! We're following our own design.


# 4. short_code
# String(10)
# For Version 1, 10 characters is more than enough.
# Examples: aBc123XyZ, K9LmP2QaR
# Later, if we decide on a different algorithm, changing this to String(12) or String(8) is easy.


# 5. clicks
# default=0
# Every new shortened URL starts with: 0 clicks
# Exactly what we designed.


# 6. created_at
# default=datetime.utcnow
# Notice something important.
# We wrote: default=datetime.utcnow
# NOT default=datetime.utcnow() Why? This is a classic interview question.

# If you write: datetime.utcnow()
# the function runs once, when Python imports the file. Every row would get the same timestamp. Instead, by passing the function itself: datetime.utcnow
# SQLAlchemy calls it every time a new row is created. That means every record gets its own creation time.










# Step 5 — How does SQLAlchemy know about our model?

# This is the missing link.
# Right now we have: Base & ShortenedURL(Base) Database (still doesn't know about the model)

# Think of it like this:
# Teacher (Base)
#     ↓
# Student (ShortenedURL)
#     ↓
# School Registry (metadata)
#     ↓
# School Database (PostgreSQL)

# metadata is like a registry. Every model that inherits from Base automatically registers itself inside: Base.metadata
# Later we'll tell SQLAlchemy: "Take everything in this registry and create the corresponding tables."













# Step 6 — Import the Model
# Open main.py
# Add this import: from app.models.shortened_url import ShortenedURL
# You might think: "But I'm not using ShortenedURL anywhere!"

# Exactly. This is one of those Python/SQLAlchemy behaviors that confuses almost everyone the first time.
# Why import it if we don't use it -> Because Python only executes a file when it is imported.
# When this line runs: from app.models.shortened_url import ShortenedURL
# Python executes: class ShortenedURL(Base):
# and SQLAlchemy registers it inside: Base.metadata
# Without importing it, SQLAlchemy doesn't even know the model exists.











# Step 7 — Create the Tables

# Now add these imports in main.py:
# from app.database.base import Base
# from app.database.database import engine

# Then, just before creating the FastAPI app, add: Base.metadata.create_all(bind=engine)
# Your main.py should now look roughly like this:

# from fastapi import FastAPI
# from app.database.base import Base
# from app.database.database import engine
# from app.models.shortened_url import ShortenedURL

# Base.metadata.create_all(bind=engine)

# app = FastAPI(
#     title="URL Shortener API",
#     version="1.0.0",
#     description="A URL Shortener API built with FastAPI and PostgreSQL."
# )

# @app.get("/")
# def root():
#     return {
#         "message": "Welcome to URL Shortener API 🚀"
#     }

# if __name__ == "__main__":
#     import uvicorn

#     uvicorn.run(
#         "main:app",
#         host="127.0.0.1",
#         port=8000,
#         reload=True
#     )

# What does create_all() do?

# Think of it like this:
# Base.metadata
#       │
#       ▼
# Looks at every registered model
#       │
#       ▼
# Checks PostgreSQL
#       │
#       ▼
# Table exists?
#       │
#       ├── Yes → Do nothing
#       └── No → Create it
# That's why it's safe to run every time the application starts.
# It doesn't delete tables. It doesn't recreate existing tables. It only creates missing ones.

# url_shortener_api/
# │
# ├── app/
# │   ├── core/
# │   ├── database/
# │   │     ├── base.py
# │   │     └── database.py
# │   │
# │   ├── models/
# │   │     └── shortened_url.py   ✅
# │   │
# │   ├── repositories/
# │   ├── routers/
# │   ├── schemas/
# │   ├── services/
# │   └── utils/
# │
# ├── tests/
# │
# ├── .env
# ├── main.py
# ├── requirements.txt
# └── README.md




# 🧠 Important Concepts

# 1. What is an ORM?
# Answer: ORM stands for Object Relational Mapper. It converts Python classes into database tables.
# Python Class → SQLAlchemy ORM → PostgreSQL Table
# Without ORM: CREATE TABLE users (...)
# With ORM: class User(Base):

# 2. What is Base?
# Answer: Base is the parent class for all database models.
# If a class inherits from Base, SQLAlchemy treats it as a database table.
# Example: class ShortenedURL(Base):
# Without Base, it's just a normal Python class.

# 3. Why use DeclarativeBase?
# Answer: DeclarativeBase is the modern SQLAlchemy 2.x way of creating the base class.
# Old: Base = declarative_base()
# Modern:
# class Base(DeclarativeBase):
#     pass

# 4. What is __tablename__?
# Answer: It tells SQLAlchemy the name of the database table.
# Example:__tablename__ = "shortened_urls"
# Creates: shortened_urls

# 5. What is Mapped?
# Answer: Mapped is a type hint that tells SQLAlchemy: "This Python attribute is mapped to a database column."
# Example: id: Mapped[int]
# means Python type → int || Database column → Integer

# 6. What is mapped_column()?
# Answer: It defines the properties of a database column.
# Example:
# mapped_column(
#     Integer,
#     primary_key=True
# )
# This creates an integer primary key column.

# 7. What is Metadata?
# Answer: Metadata is SQLAlchemy's registry of all models.
# Think of it as a list.
# Base -> Metadata -> ShortenedURL
# When we call: Base.metadata.create_all()
# SQLAlchemy creates all registered tables.

# 8. Why did we import the model in main.py?
# Answer: Because Python only registers a model when its file is imported.
# Without: from app.models.shortened_url import ShortenedURL
# SQLAlchemy doesn't know the model exists. No model = No table.

# 9. What does create_all() do?
# Answer: It checks every model registered in Base.metadata.
# If a table doesn't exist, it creates it. If it already exists, it does nothing. It does not delete or recreate existing tables.

# 10. Why did we use Text for original_url?
# Answer: URLs can be very long. Using Text avoids unnecessary length limits.

# 11. Why is short_code unique?
# Answer: Every short URL must point to exactly one original URL. If duplicates were allowed, the redirect would be ambiguous.

# 12. Why use datetime.now(UTC) instead of datetime.utcnow()?
# Answer: datetime.utcnow() is deprecated.
# Modern Python recommends timezone-aware datetimes.
# So we use:
# default=lambda: datetime.now(UTC)


# 🔥 Interview Questions

# Q1. What is SQLAlchemy?
# Answer: SQLAlchemy is a Python ORM that lets us work with databases using Python classes instead of writing raw SQL for every operation.

# Q2. What is the difference between ORM and SQL?
# Answer: SQL is the language used to communicate with databases. ORM is a tool that converts programming language objects into SQL automatically.

# Q3. Why do models inherit from Base?
# Answer: Because SQLAlchemy only recognizes classes that inherit from Base as database models.

# Q4. What is the purpose of __tablename__?
# Answer: It specifies the name of the database table for the model.

# Q5. What is the difference between Mapped and mapped_column()?
# Answer: Mapped defines the Python type. mapped_column() defines the database column configuration.
# Example:
# id: Mapped[int] = mapped_column(Integer)

# Q6. What is a Primary Key?
# Answer: A primary key uniquely identifies each row in a table.
# In This project: id -> is the primary key.

# Q7. Why do we use unique=True?
# Answer: To prevent duplicate values.
# In This project: short_code -> must always be unique.

# Q8. What does nullable=False mean?
# Answer: The column cannot contain NULL. Every record must have a value.

# Q9. Why do we use default=0 for clicks?
# Answer: Every newly created shortened URL starts with zero clicks.

# Q10. What does Base.metadata.create_all() do?
# Answer: It creates all tables registered in SQLAlchemy metadata if they don't already exist.



# ⭐ Most Important Things to Remember

# ORM converts Python classes into database tables.
# Every model must inherit from Base.
# __tablename__ decides the table name.
# Mapped + mapped_column() is the modern SQLAlchemy 2.x style.
# Models are registered in Base.metadata.
# create_all() creates missing tables from the registered models.
# A model must be imported before SQLAlchemy can create its table.