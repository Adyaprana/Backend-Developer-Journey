
# 📖 THEORY 2 — Installing SQLAlchemy
# Install packages: pip install sqlalchemy psycopg2-binary

# What is SQLAlchemy?
# SQLAlchemy is Python's most popular ORM.

# It supports:
# PostgreSQL
# MySQL
# SQLite
# Oracle
# SQL Server

# What is psycopg2-binary?
# Python itself cannot communicate with PostgreSQL.
# It needs a driver, That driver is psycopg2-binary
# Think of it like a USB cable connecting Python to PostgreSQL.





# 📖 THEORY 3 — SQLAlchemy Architecture
# Python Code -> SQLAlchemy ORM -> SQL Statements -> psycopg2 Driver -> PostgreSQL Database

from sqlalchemy import create_engine
DATABASE_URL = "postgresql://postgres:postgres123@localhost:5432/backend_journey"
engine = create_engine(DATABASE_URL)


# Understanding DATABASE_URL
# postgresql:// Database type
#     ↓
# postgres Username
#     ↓
# password
#     ↓
# localhost Server
#     ↓
# 5432 Port
#     ↓
# mydatabase
# Database name





# 📖 THEORY 5 — Base Class

# Every SQLAlchemy model inherits from Base.

# from sqlalchemy.orm import declarative_base
# Base = declarative_base()
# Think of Base as the parent class for all tables.





# 📖 THEORY 6 — Models
# Instead of SQL
# CREATE TABLE users...

# Use python:
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
# Python class -> Database table

# How Mapping Works
# Python -> class User(Base):
#        ↓   
# Database users

# Python -> name = Column(String)
#       ↓
# Database name VARCHAR





# 📖 THEORY 7 — Create Tables
# Once models are defined
Base.metadata.create_all(engine)

# SQLAlchemy automatically creates tables.
# No need to manually write
# CREATE TABLE





# 📖 THEORY 8 — Sessions

# A Session is how Python talks to the database.
# Think of it as: Python -> Session -> Database
# Without a Session: nothing is saved.

# Create Session
from sqlalchemy.orm import sessionmaker
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()




# 📖 THEORY 9 — INSERT
# Create object
new_user = User(
    name="Adyaprana",
    email="adya@gmail.com"
)
# Save
session.add(new_user)
session.commit()

# Equivalent SQL
# INSERT INTO users(name,email)
# VALUES(...)





# 📖 THEORY 10 — SELECT
# All users
users = session.query(User).all()

# First user
user = session.query(User).first()
# Filter
user = session.query(User).filter(
    User.id == 1
).first()

# Equivalent SQL
# SELECT *
# FROM users
# WHERE id = 1;






# 📖 THEORY 11 — UPDATE
user = session.query(User).first()
user.name = "Rahul"
session.commit()

# Equivalent SQL
# UPDATE users
# SET name='Rahul'
# WHERE id=1;



# 📖 THEORY 12 — DELETE
user = session.query(User).first()
session.delete(user)
session.commit()

# Equivalent SQL
# DELETE FROM users;






# 📖 THEORY 13 — Relationships
# One User -> Many Orders

# Python
# class User(Base):
#     orders = relationship(
#         "Order",
#         back_populates="user"
#     )
# # Order
# class Order(Base):
#     user_id = Column(
#         Integer,
#         ForeignKey("users.id")
#     )
#     user = relationship(
#         "User",
#         back_populates="orders"
#     )








# 📖 THEORY 15 — SQLAlchemy vs Raw SQL
# Raw SQL -> SELECT * FROM users;
# SQLAlchemy -> session.query(User).all()

# For DELETE
# Raw SQL -> DELETE FROM users;
# SQLAlchemy -> session.delete(user)






# 📖 THEORY 16 — SQLAlchemy + FastAPI
# This is how nearly every FastAPI project works.

# Frontend -> FastAPI Endpoint -> SQLAlchemy Session -> PostgreSQL -> Response
# Example:
# @app.get("/users")
#       ↓
# session.query(User).all()
#       ↓
# JSON Response
# This is why SQLAlchemy is one of the most important skills for Python backend developers.






# 📖 THEORY 17 — ORM Advantages
# Advantages:
# ✅ Less SQL to write
# ✅ Easier maintenance
# ✅ Database independent
# ✅ Safer
# ✅ Cleaner code

# Disadvantages
# ❌ Slight learning curve
# ❌ Complex queries sometimes need raw SQL
# ❌ Can hide performance problems if misused






# 📖 THEORY 18 — SQLAlchemy 2.0 (Bonus)
# Modern SQLAlchemy (2.x) encourages a newer query style.

# Example:
from sqlalchemy import select
stmt = select(User)
users = session.execute(stmt).scalars().all()
# You'll still encounter the classic session.query(...) style in many tutorials and existing codebases, so it's useful to recognize both.







# Full Working CRUD Example (SQLite)
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "postgresql+psycopg2://postgres:postgres123@localhost:5432/backend_journey"

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# CREATE
user = User(name="Adyaprana", email="adya@gmail.com")
session.add(user)
session.commit()

# READ
users = session.query(User).all()

print("\nUsers:")
for u in users:
    print(u.id, u.name, u.email)

# UPDATE
first_user = session.query(User).first()

if first_user:
    first_user.name = "Updated Adyaprana"
    session.commit()

# DELETE
last_user = session.query(User).order_by(User.id.desc()).first()

if last_user:
    session.delete(last_user)
    session.commit()

print("\nCRUD operations completed successfully.")

session.close()

# Backend Flow:
# User clicks Login -> FastAPI -> SQLAlchemy -> PostgreSQL -> User Table -> Python Objects -> JSON Response -> Frontend


