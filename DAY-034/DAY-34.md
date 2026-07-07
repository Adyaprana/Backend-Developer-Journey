# DAY 34 — SQLAlchemy ORM: PYTHON + POSTGRESQL

> **Goal:** Connect Python to PostgreSQL using SQLAlchemy — define models as classes, perform full CRUD, handle relationships, and understand how FastAPI connects to databases.
>
> **Week:** W5 — SQL + PostgreSQL (Days 29–42)
>
> **Status:** ✅

---

# 🎯 Learning Roadmap

```
SQLAlchemy ORM — Python + PostgreSQL

  ✅ pip install sqlalchemy psycopg2-binary
  ✅ Define models as Python classes (not raw SQL)
  ✅ Create tables, insert records, query, update, delete
  ✅ Relationships in SQLAlchemy: ForeignKey, relationship()
  ✅ This is exactly how FastAPI connects to databases

  ▶ Patrick Loeber SQLAlchemy Tutorial (English)
```

## Day 34 Checklist

- [ ] Install sqlalchemy and psycopg2-binary
- [ ] Write the DATABASE_URL and explain each part
- [ ] Create an engine with create_engine()
- [ ] Define a model class with Base and __tablename__
- [ ] Create tables with Base.metadata.create_all()
- [ ] INSERT a record with session.add() + session.commit()
- [ ] SELECT all records with session.query(Model).all()
- [ ] UPDATE a record by fetching then modifying then committing
- [ ] DELETE a record with session.delete() + session.commit()
- [ ] Add a ForeignKey and relationship() between two models
- [ ] Solve LeetCode 610 — Triangle Judgement ✅
- [ ] Solve LeetCode 1527 — Patients With a Condition ✅

---

# SECTION 1 — WHAT IS AN ORM?

## Definition

**ORM = Object Relational Mapper**

An ORM is a tool that lets you interact with a relational database using your programming language — in this case Python — instead of writing raw SQL.

```
Without ORM (raw SQL):
  cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
  result = cursor.fetchone()
  user = {"id": result[0], "name": result[1], "email": result[2]}

With ORM (SQLAlchemy):
  user = session.query(User).filter(User.email == email).first()
  print(user.name)   # Python object with attributes
```

Same result. ORM code is cleaner, safer, and easier to maintain.

---

## The Translation Chain

```
You write Python
      ↓
SQLAlchemy ORM
      ↓
SQL Statements (SQLAlchemy generates these)
      ↓
psycopg2 driver (sends SQL to PostgreSQL)
      ↓
PostgreSQL Database
      ↓
Result comes back through the same chain
      ↓
Python objects (you work with these)
```

**You speak Python. SQLAlchemy speaks SQL. PostgreSQL understands SQL.**

---

## Why ORM Exists

```
Real backend application has hundreds of operations:
  → User login
  → User registration
  → Fetch products
  → Place order
  → Update cart
  → Cancel order
  → Admin analytics
  → ...

Without ORM: every operation = raw SQL string
  Hard to maintain
  Easy to make mistakes
  SQL injection risk if not careful
  Database-specific syntax

With ORM:
  Python code that reads naturally
  Type safety
  Automatic parameterization (SQL injection prevention)
  Easy to switch databases (SQLite for dev, PostgreSQL for production)
  Works with FastAPI dependency injection
```

---

## ORM vs Raw SQL — When to Use Which

```
Use ORM (SQLAlchemy) for:
  ✅ Standard CRUD operations (90% of your code)
  ✅ Relationships between models
  ✅ When you want clean, maintainable code
  ✅ FastAPI + database integration

Use Raw SQL for:
  ✅ Very complex queries (window functions, complex CTEs)
  ✅ Performance-critical queries that ORM can't optimize well
  ✅ Database-specific features
  ✅ Bulk operations on millions of rows

SQLAlchemy supports both:
  session.query(User).all()         → ORM style
  session.execute("SELECT ...")     → Raw SQL when needed
```

---

# SECTION 2 — INSTALLATION

## Install Required Packages

```bash
# In your terminal (with virtual environment activated)
pip install sqlalchemy psycopg2-binary

# Verify installation
python -c "import sqlalchemy; print(sqlalchemy.__version__)"
python -c "import psycopg2; print(psycopg2.__version__)"
```

**What each package does:**

```
sqlalchemy:
  The ORM itself.
  Defines models, sessions, queries, relationships.
  Converts Python code to SQL.

psycopg2-binary:
  The PostgreSQL database driver.
  A "binary" package (no compilation needed — easier to install).
  psycopg2 is the cable that connects Python to PostgreSQL.
  SQLAlchemy tells it what SQL to send; psycopg2 sends it.
```

**Why two packages?**

```
SQLAlchemy doesn't know how to talk to PostgreSQL directly.
It only knows how to generate SQL.

psycopg2 knows how to talk to PostgreSQL.
It sends SQL over TCP/IP to the database.

Together: Python → SQLAlchemy (generate SQL) → psycopg2 (send SQL) → PostgreSQL
```

---

# SECTION 3 — ENGINE AND CONNECTION

## The DATABASE_URL

```python
DATABASE_URL = "postgresql+psycopg2://postgres:postgres123@localhost:5432/backend_journey"

# Breaking it down:
# postgresql        → Database type (tells SQLAlchemy which dialect to use)
# +psycopg2         → The driver to use for communication
# postgres          → PostgreSQL username
# postgres123       → PostgreSQL password
# @localhost        → Server address (localhost = your own machine)
# :5432             → Port (5432 is PostgreSQL's default port)
# /backend_journey  → Database name
```

**For production (environment variables — never hardcode credentials):**

```python
import os

DATABASE_URL = os.getenv("DATABASE_URL")
# In .env file: DATABASE_URL=postgresql+psycopg2://user:pass@host:5432/dbname
# Never commit .env to GitHub!
```

---

## Creating the Engine

```python
from sqlalchemy import create_engine

DATABASE_URL = "postgresql+psycopg2://postgres:postgres123@localhost:5432/backend_journey"

engine = create_engine(
    DATABASE_URL,
    echo=True,         # Set to True during development: prints SQL statements
    pool_size=5,       # Number of connections in the pool
    max_overflow=10    # Additional connections above pool_size if needed
)

# Test the connection
from sqlalchemy import text

with engine.connect() as conn:
    result = conn.execute(text("SELECT version();"))
    print(result.fetchone())
```

**What is `echo=True`?**

```
With echo=True, SQLAlchemy prints every SQL statement it generates.
Essential for debugging and learning.
Turn off (echo=False) in production to avoid log spam.

Example output:
  2026-06-01 10:30:00 INFO sqlalchemy.engine.Engine SELECT * FROM users WHERE id = 1
```

---

# SECTION 4 — MODELS (PYTHON CLASSES = DATABASE TABLES)

## The Base Class

```python
from sqlalchemy.orm import declarative_base

Base = declarative_base()

# Every model inherits from Base
# Base tracks all models and knows how to create their tables
```

---

## Defining a Simple Model

```python
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"    # Name of the database table

    # Columns
    id         = Column(Integer, primary_key=True)          # PK, auto-increment
    name       = Column(String(100), nullable=False)        # NOT NULL
    email      = Column(String(255), unique=True, nullable=False)  # UNIQUE + NOT NULL
    password   = Column(String(255), nullable=False)
    is_active  = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

# How Python maps to SQL:
# class User(Base)      → CREATE TABLE users (...)
# __tablename__ = "users" → table name in PostgreSQL
# Column(Integer, primary_key=True)  → id INTEGER PRIMARY KEY
# Column(String(100), nullable=False)→ name VARCHAR(100) NOT NULL
# Column(String, unique=True)        → email VARCHAR UNIQUE
```

---

## All Column Types

```python
from sqlalchemy import (
    Column, Integer, BigInteger, String, Text,
    Boolean, Float, Numeric, Date, DateTime,
    ForeignKey
)

class Product(Base):
    __tablename__ = "products"

    id          = Column(Integer,  primary_key=True)
    name        = Column(String(150), nullable=False)
    description = Column(Text)                              # Unlimited text
    price       = Column(Numeric(10, 2), nullable=False)    # DECIMAL(10,2)
    stock       = Column(Integer, default=0)
    rating      = Column(Float)                             # Float
    is_active   = Column(Boolean, default=True)
    created_at  = Column(DateTime, default=datetime.utcnow)

# SQLAlchemy → PostgreSQL type mapping:
# Integer    → INTEGER
# BigInteger → BIGINT
# String(n)  → VARCHAR(n)
# Text       → TEXT
# Boolean    → BOOLEAN
# Float      → FLOAT
# Numeric    → DECIMAL/NUMERIC
# Date       → DATE
# DateTime   → TIMESTAMP
```

---

# SECTION 5 — CREATING TABLES

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime

DATABASE_URL = "postgresql+psycopg2://postgres:postgres123@localhost:5432/backend_journey"

engine = create_engine(DATABASE_URL, echo=True)
Base   = declarative_base()

class User(Base):
    __tablename__ = "users"
    id         = Column(Integer, primary_key=True)
    name       = Column(String(100), nullable=False)
    email      = Column(String(255), unique=True, nullable=False)
    is_active  = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

# This creates the table in PostgreSQL if it doesn't exist
# Equivalent to: CREATE TABLE IF NOT EXISTS users (...)
Base.metadata.create_all(engine)
print("Tables created successfully.")

# To drop all tables (careful!):
# Base.metadata.drop_all(engine)
```

---

# SECTION 6 — SESSIONS

## What is a Session?

```python
from sqlalchemy.orm import sessionmaker

# Create a session factory
SessionLocal = sessionmaker(bind=engine)

# Create an actual session
session = SessionLocal()

# A session is your communication channel to the database.
# Think of it as:
#   session.add(obj)     → stage a change
#   session.commit()     → permanently save all staged changes
#   session.rollback()   → cancel all staged changes
#   session.close()      → close the connection

# Session lifecycle:
# 1. Open session
# 2. Perform operations (add, query, update, delete)
# 3. Commit (or rollback on error)
# 4. Close session
```

---

## Session as Context Manager (Recommended)

```python
from contextlib import contextmanager

@contextmanager
def get_session():
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

# Usage:
with get_session() as session:
    user = User(name="Adyaprana", email="adya@example.com", password="hash")
    session.add(user)
# Auto commits on success, auto rollbacks on error
```

---

# SECTION 7 — CRUD OPERATIONS

## CREATE — INSERT a Record

```python
# Method 1: Add one record
session = SessionLocal()

new_user = User(
    name="Adyaprana",
    email="adya@example.com",
    password="hashed_password_here"
)

session.add(new_user)     # Stage the INSERT
session.commit()          # Execute: INSERT INTO users (name, email, password) VALUES (...)
session.refresh(new_user) # Reload from DB to get auto-generated id

print(f"Created user with id: {new_user.id}")
session.close()


# Method 2: Add multiple records
users_to_add = [
    User(name="Rahul", email="rahul@example.com", password="hash2"),
    User(name="Priya", email="priya@example.com", password="hash3"),
    User(name="Amit",  email="amit@example.com",  password="hash4"),
]

session.add_all(users_to_add)
session.commit()
print(f"Added {len(users_to_add)} users.")
```

---

## READ — Query Records

```python
# Get ALL records
all_users = session.query(User).all()
for user in all_users:
    print(user.id, user.name, user.email)

# Get FIRST record
first_user = session.query(User).first()
print(first_user.name)

# Get by PRIMARY KEY
user = session.query(User).get(1)   # equivalent to WHERE id = 1
# Modern style:
from sqlalchemy import select
user = session.execute(select(User).where(User.id == 1)).scalar_one_or_none()

# Filter with .filter()
user = session.query(User).filter(User.email == "adya@example.com").first()
user = session.query(User).filter(User.id == 1).first()

# Filter with multiple conditions
active_users = session.query(User).filter(
    User.is_active == True,
    User.name.like("A%")    # name starts with A
).all()

# ORDER BY
users_by_name = session.query(User).order_by(User.name.asc()).all()
users_by_date = session.query(User).order_by(User.created_at.desc()).all()

# LIMIT and OFFSET (pagination)
page = 1
per_page = 10
users = session.query(User).order_by(User.id).limit(per_page).offset((page-1)*per_page).all()

# COUNT
total = session.query(User).count()
active_count = session.query(User).filter(User.is_active == True).count()

# Check existence
exists = session.query(User).filter(User.email == "adya@example.com").first() is not None
```

---

## UPDATE — Modify a Record

```python
# Method 1: Fetch → Modify → Commit
user = session.query(User).filter(User.id == 1).first()
if user:
    user.name = "Adyaprana Pradhan"
    user.is_active = False
    session.commit()
    print(f"Updated: {user.name}")

# Method 2: Bulk update (without loading objects)
from sqlalchemy import update

session.execute(
    update(User)
    .where(User.is_active == False)
    .values(is_active=True)
)
session.commit()
print("All inactive users activated.")
```

---

## DELETE — Remove a Record

```python
# Method 1: Fetch → Delete → Commit
user = session.query(User).filter(User.id == 1).first()
if user:
    session.delete(user)
    session.commit()
    print("User deleted.")

# Method 2: Bulk delete (without loading)
from sqlalchemy import delete

session.execute(
    delete(User).where(User.is_active == False)
)
session.commit()
print("All inactive users deleted.")
```

---

# SECTION 8 — RELATIONSHIPS

## One-to-Many Relationship

```python
from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id    = Column(Integer, primary_key=True)
    name  = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False)

    # Relationship: one user has many orders
    orders = relationship("Order", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User id={self.id} name={self.name}>"


class Order(Base):
    __tablename__ = "orders"

    id          = Column(Integer, primary_key=True)
    user_id     = Column(Integer, ForeignKey("users.id"), nullable=False)  # FK
    amount      = Column(Numeric(10, 2), nullable=False)
    status      = Column(String(20), default="pending")
    created_at  = Column(DateTime, default=datetime.utcnow)

    # Relationship: each order belongs to one user
    user = relationship("User", back_populates="orders")

    def __repr__(self):
        return f"<Order id={self.id} amount={self.amount} status={self.status}>"
```

**How relationship() works:**

```
user.orders         → access all orders for this user (no extra query needed with eager loading)
order.user          → access the user for this order

SQLAlchemy handles the JOIN automatically.
Without relationship(): you'd need to write JOIN queries manually.
```

---

## Using Relationships

```python
# Create user with orders
new_user = User(name="Adyaprana", email="adya@example.com")
session.add(new_user)
session.flush()   # Get the user.id without committing

# Add orders to this user
order1 = Order(user_id=new_user.id, amount=89999, status="pending")
order2 = Order(user_id=new_user.id, amount=1200,  status="delivered")
session.add_all([order1, order2])
session.commit()


# Alternative: Add orders through the relationship directly
user = User(name="Rahul", email="rahul@example.com")
user.orders = [
    Order(amount=2500, status="shipped"),
    Order(amount=500,  status="pending"),
]
session.add(user)
session.commit()


# Access orders through relationship
user = session.query(User).filter(User.id == 1).first()
for order in user.orders:          # No extra SQL query needed
    print(f"  Order: ₹{order.amount} — {order.status}")


# Access user through order
order = session.query(Order).first()
print(f"Order belongs to: {order.user.name}")
```

---

## Many-to-Many Relationship

```python
# Many-to-Many requires an association table
from sqlalchemy import Table

# Association table (junction table)
student_courses = Table(
    "student_courses",
    Base.metadata,
    Column("student_id", Integer, ForeignKey("students.id")),
    Column("course_id",  Integer, ForeignKey("courses.id"))
)

class Student(Base):
    __tablename__ = "students"
    id      = Column(Integer, primary_key=True)
    name    = Column(String(100))
    courses = relationship("Course", secondary=student_courses, back_populates="students")

class Course(Base):
    __tablename__ = "courses"
    id       = Column(Integer, primary_key=True)
    name     = Column(String(100))
    students = relationship("Student", secondary=student_courses, back_populates="courses")


# Usage
python_course = Course(name="Python Backend")
sql_course    = Course(name="SQL + PostgreSQL")

adya  = Student(name="Adyaprana")
rahul = Student(name="Rahul")

adya.courses  = [python_course, sql_course]
rahul.courses = [python_course]

session.add_all([adya, rahul])
session.commit()

# Query
student = session.query(Student).filter_by(name="Adyaprana").first()
for course in student.courses:
    print(course.name)   # Python Backend, SQL + PostgreSQL
```

---

# SECTION 9 — COMPLETE PROJECTS

## Project 1: Book Management System

```python
# full-sqlalchemy-books.py
from sqlalchemy import create_engine, Column, Integer, String, Float, text
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "postgresql+psycopg2://postgres:postgres123@localhost:5432/backend_journey"

engine = create_engine(DATABASE_URL, echo=False)
Base   = declarative_base()


class Book(Base):
    __tablename__ = "books"

    id       = Column(Integer, primary_key=True, autoincrement=True)
    title    = Column(String(100), nullable=False)
    author   = Column(String(100), nullable=False)
    price    = Column(Float, nullable=False)
    quantity = Column(Integer, default=0)

    def __repr__(self):
        return f"<Book '{self.title}' by {self.author} — ₹{self.price}>"


# Create table
Base.metadata.create_all(engine)

# Session
Session = sessionmaker(bind=engine)
session = Session()


# ── CREATE ───────────────────────────────────────────────────────
print("=== CREATING BOOKS ===")
books = [
    Book(title="Atomic Habits",    author="James Clear",        price=599.0,  quantity=10),
    Book(title="Clean Code",       author="Robert C. Martin",   price=899.0,  quantity=5),
    Book(title="Python Crash Course", author="Eric Matthes",   price=749.0,  quantity=8),
    Book(title="System Design Interview", author="Alex Xu",    price=1299.0, quantity=3),
]
session.add_all(books)
session.commit()
print(f"Added {len(books)} books.\n")


# ── READ (All) ──────────────────────────────────────────────────
print("=== ALL BOOKS ===")
all_books = session.query(Book).order_by(Book.title).all()
for book in all_books:
    print(f"  [{book.id}] {book.title} by {book.author} — ₹{book.price} (qty: {book.quantity})")
print()


# ── READ (Filter) ───────────────────────────────────────────────
print("=== SEARCH: Books under ₹800 ===")
cheap_books = session.query(Book).filter(Book.price < 800).all()
for book in cheap_books:
    print(f"  {book.title} — ₹{book.price}")
print()


# ── UPDATE ──────────────────────────────────────────────────────
print("=== UPDATE: Change price of Atomic Habits ===")
book = session.query(Book).filter_by(title="Atomic Habits").first()
if book:
    old_price = book.price
    book.price = 649.0
    session.commit()
    print(f"  Updated: {book.title} price ₹{old_price} → ₹{book.price}")
print()


# ── DELETE ──────────────────────────────────────────────────────
print("=== DELETE: Remove Clean Code ===")
book = session.query(Book).filter_by(title="Clean Code").first()
if book:
    session.delete(book)
    session.commit()
    print(f"  Deleted: Clean Code")
print()


# ── FINAL STATE ─────────────────────────────────────────────────
print("=== FINAL STATE ===")
remaining = session.query(Book).order_by(Book.price).all()
for book in remaining:
    print(f"  {book.title} — ₹{book.price}")


session.close()
print("\nDone.")
```

---

## Project 2: Student Database

```python
# student-db.py
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "postgresql+psycopg2://postgres:postgres123@localhost:5432/backend_journey"

engine = create_engine(DATABASE_URL, echo=False)
Base   = declarative_base()


class Student(Base):
    __tablename__ = "students"

    id         = Column(Integer, primary_key=True)
    name       = Column(String(100), nullable=False)
    age        = Column(Integer)
    department = Column(String(50))
    gpa        = Column(Float)

    def __repr__(self):
        return f"<Student {self.name} ({self.department}) GPA: {self.gpa}>"


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Insert students
session.add_all([
    Student(name="Adyaprana", age=23, department="MCA",  gpa=9.2),
    Student(name="Rahul",     age=24, department="MCA",  gpa=8.5),
    Student(name="Priya",     age=22, department="BCA",  gpa=9.5),
    Student(name="Amit",      age=25, department="MBA",  gpa=7.8),
    Student(name="Sneha",     age=21, department="BCA",  gpa=9.0),
])
session.commit()

# Query examples
print("Top students (GPA >= 9.0):")
top_students = session.query(Student).filter(Student.gpa >= 9.0).order_by(Student.gpa.desc()).all()
for s in top_students:
    print(f"  {s.name} — {s.department} — GPA: {s.gpa}")

print("\nMCA students:")
mca = session.query(Student).filter(Student.department == "MCA").all()
for s in mca:
    print(f"  {s.name}")

session.close()
```

---

## Project 3: E-Commerce with Relationships

```python
# ecommerce-orm.py
from sqlalchemy import create_engine, Column, Integer, String, Numeric, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from datetime import datetime

DATABASE_URL = "postgresql+psycopg2://postgres:postgres123@localhost:5432/backend_journey"

engine = create_engine(DATABASE_URL, echo=False)
Base   = declarative_base()


class User(Base):
    __tablename__ = "users"
    id     = Column(Integer, primary_key=True)
    name   = Column(String(100), nullable=False)
    email  = Column(String(255), unique=True, nullable=False)
    orders = relationship("Order", back_populates="user", lazy="joined")


class Product(Base):
    __tablename__ = "products"
    id          = Column(Integer, primary_key=True)
    name        = Column(String(150), nullable=False)
    price       = Column(Numeric(10, 2), nullable=False)
    stock       = Column(Integer, default=0)
    order_items = relationship("OrderItem", back_populates="product")


class Order(Base):
    __tablename__ = "orders"
    id          = Column(Integer, primary_key=True)
    user_id     = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at  = Column(DateTime, default=datetime.utcnow)
    status      = Column(String(20), default="pending")
    user        = relationship("User", back_populates="orders")
    items       = relationship("OrderItem", back_populates="order")


class OrderItem(Base):
    __tablename__ = "order_items"
    id         = Column(Integer, primary_key=True)
    order_id   = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity   = Column(Integer, nullable=False)
    price      = Column(Numeric(10, 2), nullable=False)
    order      = relationship("Order", back_populates="items")
    product    = relationship("Product", back_populates="order_items")


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Create a user
user = User(name="Adyaprana", email="adya@example.com")
session.add(user)
session.flush()

# Create products
p1 = Product(name="Laptop",   price=80000, stock=10)
p2 = Product(name="Mouse",    price=1200,  stock=50)
p3 = Product(name="Keyboard", price=2500,  stock=30)
session.add_all([p1, p2, p3])
session.flush()

# Place an order
order = Order(user_id=user.id, status="pending")
session.add(order)
session.flush()

# Add items to order
session.add_all([
    OrderItem(order_id=order.id, product_id=p1.id, quantity=1, price=p1.price),
    OrderItem(order_id=order.id, product_id=p2.id, quantity=2, price=p2.price),
])

# Update stock
p1.stock -= 1
p2.stock -= 2

session.commit()

# Query: user's orders with items
user = session.query(User).filter_by(name="Adyaprana").first()
print(f"User: {user.name}")
for order in user.orders:
    print(f"  Order #{order.id} — {order.status}")
    for item in order.items:
        print(f"    {item.product.name} × {item.quantity} = ₹{item.price * item.quantity}")

session.close()
```

---

# SECTION 10 — SQLAlchemy + FASTAPI

## How FastAPI Connects to the Database

```python
# database.py — the central database configuration
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:postgres123@localhost:5432/backend_journey")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """FastAPI dependency that provides a database session per request."""
    db = SessionLocal()
    try:
        yield db          # Provide session to the route
        db.commit()       # Commit at end of successful request
    except Exception:
        db.rollback()     # Rollback if any error
        raise
    finally:
        db.close()        # Always close the session
```

```python
# models.py
from database import Base
from sqlalchemy import Column, Integer, String, Boolean

class User(Base):
    __tablename__ = "users"
    id       = Column(Integer, primary_key=True, index=True)
    name     = Column(String(100), nullable=False)
    email    = Column(String(255), unique=True, nullable=False)
    is_active = Column(Boolean, default=True)
```

```python
# main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db, engine, Base
from models import User
from pydantic import BaseModel

# Create all tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI()

class UserCreate(BaseModel):
    name: str
    email: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    is_active: bool

    class Config:
        from_attributes = True  # Allows SQLAlchemy objects → Pydantic

@app.post("/users", response_model=UserResponse, status_code=201)
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    # Check if email already exists
    existing = db.query(User).filter(User.email == user_data.email).first()
    if existing:
        raise HTTPException(status_code=409, detail="Email already registered")

    # Create new user
    new_user = User(name=user_data.name, email=user_data.email)
    db.add(new_user)
    db.flush()         # Get the id before commit
    return new_user    # get_db() commits at the end


@app.get("/users", response_model=list[UserResponse])
def get_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(User).offset(skip).limit(limit).all()


@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    return None

# Run with: uvicorn main:app --reload
# Test at: http://localhost:8000/docs  (Swagger UI — auto-generated!)
```

---

# SECTION 11 — LEETCODE SOLUTIONS

## LeetCode 610 — Triangle Judgement

```sql
-- ═══════════════════════════════════════════════════════════════
-- LeetCode #610 — Triangle Judgement
-- Difficulty: Easy | Status: ✅ Accepted (11/11 test cases)
-- Runtime: 227ms | Memory: 0.00 MB | Beats memory: 100%
-- Topic: CASE WHEN (SQL's if-else)
-- ═══════════════════════════════════════════════════════════════

-- Problem: Classify each row as "Yes" (valid triangle) or "No"

DROP TABLE IF EXISTS Triangle;
CREATE TABLE Triangle (x INT, y INT, z INT);
INSERT INTO Triangle VALUES (13,15,30),(10,20,15),(7,8,10),(5,6,12);

SELECT * FROM Triangle;

-- SOLUTION: CASE is SQL's if-else statement
SELECT
    x,
    y,
    z,
    CASE
        WHEN x + y > z
         AND y + z > x
         AND x + z > y
        THEN 'Yes'
        ELSE 'No'
    END AS triangle
FROM Triangle;

-- Triangle Inequality Theorem:
-- A valid triangle requires all three conditions:
--   x + y > z
--   y + z > x
--   x + z > y
-- If ANY ONE fails → Not a triangle

-- CASE Syntax:
-- CASE
--   WHEN condition THEN result
--   WHEN condition THEN result
--   ELSE default_result
-- END

-- Why not WHERE?
-- WHERE would REMOVE rows that fail the condition.
-- We need to LABEL every row as Yes or No.
-- CASE labels without removing.

-- Expected output:
-- x  | y  | z  | triangle
-- 13 | 15 | 30 | No    (13+15=28, not > 30)
-- 10 | 20 | 15 | Yes   (all conditions met)
--  7 |  8 | 10 | Yes
--  5 |  6 | 12 | No    (5+6=11, not > 12)
```

---

## LeetCode 1527 — Patients With a Condition

```sql
-- ═══════════════════════════════════════════════════════════════
-- LeetCode #1527 — Patients With a Condition
-- Difficulty: Easy | Status: ✅ Accepted (17/17 test cases)
-- Runtime: 216ms | Memory: 0.00 MB | Beats memory: 100%
-- Topic: LIKE + Wildcards
-- ═══════════════════════════════════════════════════════════════

-- Problem: Find patients with Type I Diabetes (condition code starts with DIAB1)

DROP TABLE IF EXISTS Patients;
CREATE TABLE Patients (
    patient_id INT PRIMARY KEY,
    patient_name VARCHAR(100),
    conditions VARCHAR(255)
);

INSERT INTO Patients VALUES
(1,'Daniel','YFEV COUGH'),
(2,'Alice','DIAB100 MYOP'),
(3,'Bob','ACNE DIAB100'),
(4,'George','DIAB201'),
(5,'Tom','FEVER');

SELECT * FROM Patients;

-- SOLUTION: LIKE with % wildcard
SELECT patient_id, patient_name, conditions
FROM Patients
WHERE conditions LIKE 'DIAB1%'       -- Case 1: DIAB1 is the FIRST condition
   OR conditions LIKE '% DIAB1%';    -- Case 2: DIAB1 comes AFTER a space

-- LIKE Wildcards:
-- %  = matches zero or more of any characters
-- _  = matches exactly ONE character

-- Pattern meanings:
-- 'DIAB1%'   → starts with DIAB1 (DIAB100, DIAB1XYZ, etc.)
-- '% DIAB1%' → space, then DIAB1 (any characters, space, DIAB1, any characters)

-- Why TWO conditions?
-- "DIAB100 MYOP" → starts with DIAB1  → LIKE 'DIAB1%' catches it
-- "ACNE DIAB100" → DIAB1 after space   → LIKE '% DIAB1%' catches it

-- Why NOT just LIKE '%DIAB1%'?
-- It would also match "XXDIAB100" where DIAB1 is in the MIDDLE of another code.
-- We need DIAB1 to be a WORD BOUNDARY (start OR after space).

-- Expected output:
-- patient_id | patient_name | conditions
-- 2          | Alice        | DIAB100 MYOP   (starts with DIAB1)
-- 3          | Bob          | ACNE DIAB100   (DIAB1 after space)
-- Note: DIAB201 does NOT start with DIAB1 → excluded
```

---

# SECTION 12 — IMPORTANT THINGS TO KNOW

```
 1. ORM = Object Relational Mapper. Maps Python classes to database tables.
    Class = Table. Class instance = Row. Attribute = Column.

 2. SQLAlchemy requires a driver. For PostgreSQL: psycopg2-binary.
    SQLAlchemy generates SQL; psycopg2 sends it to PostgreSQL.

 3. DATABASE_URL format:
    dialect+driver://username:password@host:port/database_name

 4. create_engine() creates the connection configuration.
    It does NOT immediately connect — it connects when needed (lazy).

 5. Use echo=True during development to see generated SQL.
    Turn off (echo=False) in production.

 6. declarative_base() creates the parent class for all models.
    Every model class must inherit from Base.

 7. __tablename__ specifies the database table name.
    It is NOT optional — SQLAlchemy won't know which table to use without it.

 8. Base.metadata.create_all(engine) creates all tables that don't exist.
    It does NOT modify existing tables (no column additions or changes).

 9. Session is required for every database operation.
    Without commit(), changes are NOT saved to disk.

10. session.add() → stages an INSERT.
    session.commit() → actually executes the INSERT permanently.
    session.rollback() → cancels all staged changes.
    session.refresh(obj) → reloads object from DB (to get auto-generated id).

11. ForeignKey("users.id") creates the FK constraint.
    The string must match tablename.columnname exactly.

12. relationship() is NOT stored in the database.
    It only exists in Python to navigate between objects.
    back_populates links the two sides of the relationship.

13. lazy="joined" loads related objects in the same query (eager loading).
    lazy="select" (default) loads related objects in a separate query (N+1 risk!).

14. cascade="all, delete-orphan" means:
    When a parent is deleted, all its children are also deleted.
    Never leave orphan records.

15. In FastAPI: Depends(get_db) injects a database session per request.
    The session is committed at end of successful request, rolled back on error.

16. SQLAlchemy 2.0 introduces a newer syntax:
    select(User).where(User.id == 1) instead of query(User).filter(User.id == 1)
    Both work. The newer style is preferred in new projects.

17. CASE WHEN in SQL is if-else for columns.
    Useful for classifying rows, converting values, conditional aggregation.

18. LIKE with % is for pattern matching in strings.
    'X%' = starts with X.  '%X' = ends with X.  '%X%' = contains X.
    'X_' = X followed by exactly one character.

19. Never store plain text passwords. Store bcrypt/argon2 hashes.
    SQLAlchemy doesn't handle hashing — that's your application logic.

20. Use pool_size and max_overflow in create_engine() for production.
    Connection pooling reuses database connections (much more efficient).
```

---

# SECTION 13 — INTERVIEW QUESTIONS

## Q1. What is an ORM?

An ORM (Object Relational Mapper) is a tool that maps database tables to programming language classes, and database rows to class instances. Instead of writing SQL strings, you write code in your language (Python) and the ORM generates and executes the appropriate SQL. SQLAlchemy is Python's most popular ORM. It maps Python classes to PostgreSQL tables, and class instances to individual rows.

---

## Q2. What is SQLAlchemy and why is it used with FastAPI?

SQLAlchemy is Python's most widely-used database toolkit. It provides both a low-level Core API and a high-level ORM. FastAPI uses SQLAlchemy for database access because it integrates cleanly with FastAPI's dependency injection system (`Depends(get_db)`), supports async operation, handles connection pooling, and works with all major databases (PostgreSQL, MySQL, SQLite).

Every FastAPI application that stores data uses SQLAlchemy (or a similar ORM like Tortoise-ORM for async).

---

## Q3. What does `declarative_base()` do?

`declarative_base()` creates a base class that all SQLAlchemy models inherit from. The Base class maintains a registry of all models and knows how to create their corresponding database tables. When you call `Base.metadata.create_all(engine)`, SQLAlchemy looks at all registered models and creates their tables in the database.

---

## Q4. What is the difference between `session.add()` and `session.commit()`?

`session.add(obj)` stages the object for insertion — it tells SQLAlchemy "I want to insert this." The actual SQL INSERT has not been sent to the database yet.

`session.commit()` finalizes all staged changes — it sends the SQL to PostgreSQL, makes the changes permanent, and releases locks. Without commit, no changes are saved.

The pattern is always: stage changes → verify (optional) → commit.

---

## Q5. What is a relationship() in SQLAlchemy?

`relationship()` is a Python-level attribute that allows you to navigate between related objects without writing JOIN queries. It is NOT stored in the database (only the ForeignKey column is).

```python
class User(Base):
    orders = relationship("Order", back_populates="user")

# Then you can do:
user = session.query(User).first()
user.orders   # Returns all Order objects for this user
              # SQLAlchemy handles the JOIN automatically
```

---

## Q6. What is CASE WHEN in SQL?

CASE WHEN is SQL's conditional expression — the equivalent of if-else. It evaluates conditions and returns different values based on which condition is true. It is used as a column in SELECT, not as a row filter (that's WHERE). Key syntax:

```sql
CASE
    WHEN condition1 THEN value1
    WHEN condition2 THEN value2
    ELSE default_value
END AS column_name
```

---

## Q7. What do LIKE and % wildcards do?

LIKE is a SQL operator for pattern matching in strings. `%` is a wildcard that matches zero or more of any characters.

```
'DIAB1%'   → starts with DIAB1
'%DIAB1'   → ends with DIAB1
'%DIAB1%'  → contains DIAB1 anywhere
'_IABA'    → _ matches exactly one character
'% DIAB1%' → space, then DIAB1 (word boundary match)
```

LIKE is case-insensitive in some databases. In PostgreSQL, use ILIKE for case-insensitive matching.

---

## Q8. What is the N+1 problem in SQLAlchemy? How do you prevent it?

N+1 occurs when SQLAlchemy uses lazy loading by default. When you access `user.orders`, it fires a new SELECT query for EACH user. For 100 users, that's 101 queries.

```python
# N+1 (BAD) — lazy loading:
users = session.query(User).all()
for user in users:
    print(user.orders)   # New SELECT for each user

# FIX — eager loading:
from sqlalchemy.orm import joinedload
users = session.query(User).options(joinedload(User.orders)).all()
for user in users:
    print(user.orders)   # Data already loaded in first query
```

---

# REVISION SHEET

```
═══════════════════════════════════════════════════════════
SQLAlchemy ORM — ONE-PAGE REVISION
═══════════════════════════════════════════════════════════

INSTALLATION:
  pip install sqlalchemy psycopg2-binary

DATABASE_URL:
  "postgresql+psycopg2://user:password@localhost:5432/dbname"

SETUP:
  engine = create_engine(DATABASE_URL, echo=True)
  Base   = declarative_base()
  Session = sessionmaker(bind=engine)

MODEL:
  class User(Base):
      __tablename__ = "users"
      id    = Column(Integer, primary_key=True)
      name  = Column(String(100), nullable=False)
      email = Column(String(255), unique=True)

CREATE TABLES:
  Base.metadata.create_all(engine)

CRUD:
  session.add(obj)        → Stage INSERT
  session.commit()        → Save permanently
  session.query(M).all()  → SELECT * FROM table
  session.query(M).filter(M.id == 1).first()  → WHERE
  obj.attribute = value; session.commit()  → UPDATE
  session.delete(obj); session.commit()    → DELETE

RELATIONSHIPS:
  FK: user_id = Column(Integer, ForeignKey("users.id"))
  user_rel = relationship("User", back_populates="orders")

FASTAPI:
  def get_db(): yield session  (dependency injection)
  @app.get("/users")
  def get_users(db: Session = Depends(get_db)):
      return db.query(User).all()

CASE WHEN (SQL if-else):
  CASE WHEN condition THEN value ELSE default END AS col

LIKE (pattern matching):
  'X%'    → starts with X
  '%X'    → ends with X
  '% X%'  → X after a space (word boundary)
  '%X%'   → X anywhere

KEY RULES:
  ❌ No __tablename__ → SQLAlchemy won't know which table
  ❌ No commit() → changes not saved
  ❌ Lazy loading in loops → N+1 problem
  ✅ Use eager loading: options(joinedload(Model.relation))
  ✅ Use get_db() context for session lifecycle in FastAPI
```

---

## LeetCode Solved This Day

| Problem | Difficulty | Topic | Status | Runtime |
|---------|-----------|-------|--------|---------|
| #610 Triangle Judgement | Easy | CASE WHEN | ✅ Accepted 11/11 | 227ms |
| #1527 Patients With a Condition | Easy | LIKE + Wildcards | ✅ Accepted 17/17 | 216ms |

---

## 🎥 Recommended Resource

> **▶ Patrick Loeber SQLAlchemy Tutorial (English)**
>
> The clearest SQLAlchemy tutorial available. Covers models, sessions, CRUD, and relationships in a practical, code-first style. After this, SQLAlchemy in FastAPI will feel natural.

---

*Day 34 Complete.* ✅
