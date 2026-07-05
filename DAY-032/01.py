
# Why Database Design is Important

# Imagine you're building Amazon.
# You need to store:
# Millions of users
# Millions of products
# Millions of orders
# Reviews
# Payments
# Addresses

# If the database is poorly designed:
# Queries become slow.
# Data becomes inconsistent.
# Duplicate records appear.
# Bugs increase.
# Scaling becomes difficult.
# A well-designed database is the backbone of every backend application.








# THEORY 1 — What is a Database Schema?

# Definition: A Database Schema is the blueprint or structure of a database.
# It defines: Tables, Columns, Data types, Relationships, Constraints, Keys
# Think of it like the blueprint of a house before construction.

# Example:
# Student Table -> 
# | Column | Type    |
# | ------ | ------- |
# | id     | INTEGER |
# | name   | VARCHAR |
# | age    | INTEGER |
# | email  | VARCHAR |
# This table definition is part of the schema.

# Real Life Example
# Instagram has tables like: Users, Posts, Comments, Followers, Messages, Likes, Notifications
# That complete structure is called the database schema.

# Interview Definition: A database schema is the logical structure of a database that defines tables, columns, relationships, constraints, and data types.









# THEORY 2 — Primary Key (PK)

# Definition: A Primary Key uniquely identifies every row in a table.
# Rules: Cannot be NULL, Must be unique, One primary key per table

# Example:
# Users Table-> 
# | id | name      |
# | -- | --------- |
# | 1  | Adyaprana |
# | 2  | Rahul     |
# | 3  | Amit      |
# "id" is the Primary Key.

# SQL
# CREATE TABLE users (
    # id SERIAL PRIMARY KEY,
    # name VARCHAR(100)
# );
# Why Not Name -> Because two users can have the same name.

# Example:
# Adyaprana
# Adyaprana
# Not unique.








# THEORY 3 — Foreign Key (FK)

# Definition: A Foreign Key connects one table with another.
# Think of it as a relationship between tables.

# Example:
# Users->
# | id | name  |
# | -- | ----- |
# | 1  | Adya  |
# | 2  | Rahul |

# Orders-> 
# | order_id | user_id |
# | -------- | ------- |
# | 101      | 1       |
# | 102      | 1       |
# | 103      | 2       |
# user_id references users.id.

# SQL
# CREATE TABLE orders(
#     order_id SERIAL PRIMARY KEY,
#     user_id INTEGER REFERENCES users(id)
# );
# Why Foreign Keys?
# Without FK: You could insert user_id = 500 Even if user 500 doesn't exist. Foreign keys prevent this.








# THEORY 4 — UNIQUE Constraint

# Prevents duplicate values.
# Example: 
# Email-> 
# abc@gmail.com
# xyz@gmail.com
# abc@gmail.com ❌

# SQL
# email VARCHAR(255) UNIQUE
# Use UNIQUE for -> Email, Username, Phone Number, Aadhaar, PAN








# THEORY 5 — NOT NULL

# Makes sure data is always present.
# Example:
# Name->
# NULL ❌
# Adya ✅

# SQL
# name VARCHAR(100) NOT NULL
# Use for -> Name, Password, Email, Product Name








# THEORY 6 — Relationships

# One-to-One --> 
# Example:
# User
#  ↓
# Passport
# One user has one passport.


# One-to-Many -->
# Most common.
# Example:
# One User
#    ↓
# Many Orders

# Example: 
# User -> Adya
# Orders -> Laptop, Keyboard, Mouse
# One user -> Many orders.


# Many-to-Many
# Example
# Students
#   ↓
# Courses

# Student A -> Python, Java, SQL
# Student B -> Python, AI
# Many students take many courses.








# THEORY 8 — Indexes

# What is an Index?
# Imagine a book -> Without index: You read every page.
# With index: You directly jump to the page.
# Databases work the same way.

# Without Index:
# 1 Million rows -> Sequential search (Slow)
# With Index:
# Jump directly -> Fast

# SQL
# CREATE INDEX idx_email
# ON users(email);

# When to Create Index?
# Good: Email, Username, Product ID, Order ID, Foreign Keys, Search columns
# Bad: Don't create indexes on every column.
# Indexes also slow INSERT, UPDATE, and DELETE operations because the index must be updated too.








