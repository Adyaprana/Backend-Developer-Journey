# THEORY 1 — What is an ORM?
# Definition: ORM stands for -> Object Relational Mapper
# It is a tool that allows Python objects (classes and instances) to represent rows and tables in a relational database.

# Instead of writing SQL manually:
# SELECT * FROM users;

# You write Python:
# users = session.query(User).all()
# SQLAlchemy converts the Python code into SQL behind the scenes.


# Why ORM Exists

# Imagine every feature required writing SQL.
# Login
# SELECT * FROM users
# WHERE email='abc@gmail.com';

# Create User
# INSERT INTO users...

# Update User
# UPDATE users...

# Delete User
# DELETE...
# Hundreds of SQL queries.
# ORM lets you write Python instead.

# Real Analogy
# Think of ORM as a translator.
# Python -> SQLAlchemy -> SQL -> PostgreSQL

# You speak Python.
# SQLAlchemy speaks SQL.
# PostgreSQL understands SQL.

# Interview Definition: ORM (Object Relational Mapping) maps database tables to Python classes and database rows to Python objects, allowing developers to interact with databases using Python instead of raw SQL.



