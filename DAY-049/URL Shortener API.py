# 🚀 Backend Developer Journey — Project 1 (URL Shortener API)

# Day 49 — Architecture & Project Design










# Step 1 — Why Do We Need Architecture?

# Imagine you're building a house. Would you start by placing bricks? No.
# You would first decide: Number of floors, Rooms, Plumbing, Electrical wiring, Foundation.

# Software is exactly the same.
# If we immediately start writing code, we'll soon end up with: main.py, helpers.py, utils.py, crud.py, new_crud.py, crud_final.py, crud_final2.py
# Everything becomes tangled. Professional software avoids this by defining architecture first.

# What is Software Architecture?
# Architecture defines:
# Where code should live.
# Who is responsible for what.
# How different parts communicate.
# What depends on what.
# Think of it as a blueprint for the software.









# Step 2 — Choosing an Architecture

# There are several common backend architectures.
# | Architecture           | Best For                     |     Complexity    |
# | ---------------------- | ---------------------------- | ----------------- |
# | MVC                    | Small web apps               | ⭐               |
# | Layered Architecture   | APIs & business applications | ⭐⭐            |
# | Clean Architecture     | Large enterprise systems     | ⭐⭐⭐⭐       |
# | Hexagonal Architecture | Highly scalable services     | ⭐⭐⭐⭐⭐    |
# | Microservices          | Very large organizations     | ⭐⭐⭐⭐⭐    |

# Should We Use Clean Architecture?
# A lot of tutorials say: "Always use Clean Architecture."

# In reality, that's not always the best choice.
# For Version 1 of our project, full Clean Architecture would introduce unnecessary complexity.
# Instead, we'll use Layered Architecture with clean boundaries. This gives us most of the benefits while keeping the project approachable. As the project grows (authentication, Redis, analytics, Docker), we can gradually evolve toward a more complex architecture if needed.

# Our Architecture:

#         Client
#            │
#            ▼
#      FastAPI Router
#            │
#            ▼
#     Service Layer
#            │
#            ▼
#    Repository Layer
#            │
#            ▼
#   PostgreSQL Database

# Every layer has exactly one responsibility.


# Layer Responsibilities:

# 1. Router Layer
# Handles HTTP concerns only.

# Responsibilities:
# Receive requests
# Validate input
# Call service methods
# Return responses
# Should not contain business logic or database queries.


# 2. Service Layer
# This is the heart of the application.

# Responsibilities:
# Business rules
# Validation beyond schema checks
# Generate short codes
# Coordinate repositories
# Decide application behavior
# This is where most of our logic will live.


# 3. Repository Layer
# Responsible only for data access.

# Responsibilities:
# Create records
# Read records
# Update records
# Delete records (future)
# It should not know about HTTP or business rules.


# 4. Database Layer
# Stores persistent data.
# For Version 1, we'll use PostgreSQL through SQLAlchemy.

# Request Flow 

# Creating a Short URL:
# Client
#    │
# POST /shorten
#    │
# Router
#    │
# Service
#    │
# Generate Code
#    │
# Repository
#    │
# PostgreSQL
#    │
# Return Result

# Redirecting:
# Browser
#    │
# GET /abc123
#    │
# Router
#    │
# Service
#    │
# Repository
#    │
# Database Lookup
#    │
# Increment Click Count
#    │
# Return Redirect

# Viewing Statistics:
# Client
#    │
# GET /stats/abc123
#    │
# Router
#    │
# Service
#    │
# Repository
#    │
# Database
#    │
# Return JSON














# Step 3 — Designing the Folder Structure

# url_shortener_api/
# │
# ├── app/
# │   ├── routers/
# │   ├── services/
# │   ├── repositories/
# │   ├── models/
# │   ├── schemas/
# │   ├── database/
# │   ├── core/
# │   └── utils/
# ├── tests/
# ├── requirements.txt
# ├── .env
# ├── .gitignore
# └── README.md
# This structure is intentionally small but leaves room for future growth.


# Folder Responsibilities:
# | Folder          | Responsibility                             |
# | --------------- | ------------------------------------------ |
# | `routers/`      | API endpoints and request handling         |
# | `services/`     | Business logic                             |
# | `repositories/` | Database operations                        |
# | `models/`       | SQLAlchemy ORM models                      |
# | `schemas/`      | Pydantic request/response models           |
# | `database/`     | Database connection and session management |
# | `core/`         | Configuration, settings, shared components |
# | `utils/`        | Small reusable helper functions            |
# | `tests/`        | Unit and integration tests                 |



# Why Separate Models and Schemas?
# Many beginners think they are the same. They are not.

# Models: Represent database tables.
# Example: a ShortenedURL model maps directly to the shortened_urls table.

# Schemas: Represent data exchanged through the API.
# Example: a request body for creating a short URL or a response body for returning statistics.

# Keeping them separate lets us change the API without changing the database, and vice versa.



# Why Have a Service Layer?

# You might wonder: "Why not let the router call the repository directly?"
# That works for tiny demos, but as features grow, business rules become scattered across endpoints.

# The service layer keeps business logic in one place, making it easier to test, reuse, and maintain.





# Architecture Principles for This Project/

# We'll follow these rules throughout development:

# One responsibility per layer.
# Routers never access the database directly.
# Repositories never contain business logic.
# Services coordinate the application's behavior.
# Utilities remain small and generic.
# Configuration stays centralized.

# These conventions will make later features—like authentication, Redis caching, and analytics—much easier to integrate.

