# DAY 46 — JWT Authentication & Login System

# Before We Write Any Code
# Let's ask an engineering question.
# Suppose  application has this endpoint:

# GET /users -> Anyone can access it.
# Now imagine another endpoint:
# GET /profile -> Should everyone see your profile? Of course not.

# How does the backend know who is making the request?
# That's where authentication comes in.






# Chapter 1 — Authentication vs Authorization

# Many beginners confuse these two.
# Think of entering an airport.

# Authentication
# Security asks: "Who are you?"
# You show your passport. They verify your identity.
# This is Authentication.

# Authorization
# After entering, you try to access the pilot's cockpit.
# Security says: "You're authenticated, but you're not allowed to enter."
# This is Authorization.

# Remember
# Authentication -> Identity -> "Who are you?"
# Authorization -> Permissions -> "What are you allowed to do?"
# Authentication always comes first.






# Chapter 2 — The Biggest Beginner Mistake

# Suppose someone registers.
# They send:
{
    "email":"adya@gmail.com",
    "password":"mypassword123"
}
# Should we save this?
# Database, email, adya@gmail.com, password, mypassword123

# Never.
# If your database is leaked Every user's password is exposed.

# What Should We Store Instead?
# We store a hash.
# Example: mypassword123 becomes $2b$12$L3CjP2lD...
# This process is called Hashing.

# Notice: 
# Password -> Hash Function -> Hash
# But you cannot reverse it. That's the important difference. 

# Encryption vs Hashing
# Many developers mix these up.

# Encryption
# Original -> Encrypt -> Encrypted -> Decrypt -> Original
# Reversible.

# Hashing
# Password -> Hash -> Impossible to recover original password
# One-way Passwords should always be hashed, not encrypted.







# Chapter 3 — Why bcrypt?

# Python has: hash()
# Should we use it? No.
# Python's built-in hash() changes between program executions and is not designed for password security.

# bcrypt is specifically designed for password hashing.
# It is:
# Slow (making brute-force attacks expensive)
# Salted automatically
# Widely trusted
# Industry standard

# Hashing Flow 
# User registers: Password -> bcrypt.hash() -> Store Hash -> Database

# Later User logs in.
# Entered Password -> bcrypt.verify() -> Stored Hash -> Match? -> Login Success

# Notice: The original password is never stored.







# Chapter 4 — What Happens After Login?
# Suppose login succeeds. 
# Does the backend remember the user forever? No.

# HTTP is stateless.
# Every request is independent. So how do we remember the user? We issue a token.


# What is a JWT?
# JWT stands for JSON Web Token
# It is simply a digitally signed string containing claims about the user.
# Think of it like a movie ticket. The cinema doesn't remember every visitor.
# You carry the ticket.
# Every time you enter: Customer -> Shows Ticket -> Verified -> Allowed In
# JWT works the same way.


# JWT Structure
# A JWT has three parts: 
# Header . Payload . Signature
# Example: xxxxx.yyyyy.zzzzz
# Separated by dots.

# 1. Header
# Contains metadata.
# Example:
{
  "alg": "HS256",
  "typ": "JWT"
}
# It tells the server which signing algorithm was used.

# 2. Payload
# Contains information (claims).
# Example:
{
  "sub": "adya@gmail.com",
  "user_id": 1,
  "exp": 1782000000
}
# Typical claims include:
# Subject (sub)
# User ID
# Expiration time (exp)
# Avoid storing sensitive information like passwords in a JWT.

# 3. Signature
# The server signs the token using a secret key.
# Header + Payload + SECRET_KEY -> Signature
# This prevents clients from tampering with the payload.


# Complete Login Flow
# Let's trace the entire authentication process.
# Registration
# Client -> POST /register -> Password -> bcrypt Hash -> PostgreSQL

# Login
# Client -> POST /login -> Verify Password -> Generate JWT -> Return Token

# Access Protected Route
# Client -> Authorization: Bearer <token> -> FastAPI -> Verify JWT -> Endpoint Executes


# What is Authorization: Bearer?
# Requests to protected endpoints include a header like:
# Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
# Bearer means: "I am presenting this token as proof of authentication."
# FastAPI extracts and verifies it before your endpoint runs.

# OAuth2PasswordBearer
# FastAPI provides a helper:
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# What does it do?
# It tells FastAPI:
# Look for the Authorization header.
# Expect the Bearer <token> format.
# Extract the token string.
# Make it available to your endpoint.

# Think of it as a parser, not a login system.
# It does not authenticate users by itself—it simply retrieves the token from incoming requests.


# Protected Routes
# Consider: GET /profile
# Without authentication: Anyone can access it.
# With JWT: Request -> Authorization Header -> Extract Token -> Verify Signature -> Verify Expiration -> Load Current User -> Endpoint Executes
# Only valid tokens reach the endpoint.


# Why Do Tokens Expire?
# Suppose a token never expires.
# If someone steals it. They could use it forever.
# Instead, JWTs include an expiration time.
# Issue Token -> Valid for 30 minutes -> Expires -> Login Again
# Short-lived tokens reduce risk.


# Project Structure for Authentication
# As your project grows, authentication is usually separated into dedicated modules.
# backend-learning/
# ├── main.py
# ├── database.py
# ├── models.py
# ├── schemas.py
# ├── crud.py
# ├── auth.py        ← Hashing & JWT
# ├── security.py    ← Password verification & token helpers
# └── routers/
# Keeping authentication isolated makes the code easier to maintain and test.


# Packages We'll Use
# pip install python-jose passlib bcrypt

# Each package has a specific role:
# | Package       | Purpose                                  |
# | ------------- | ---------------------------------------- |
# | `python-jose` | Create and verify JWT tokens             |
# | `passlib`     | High-level password hashing interface    |
# | `bcrypt`      | Secure hashing algorithm used by Passlib |


# Architecture
# By the end of Day 46, your mental model should look like this:
# Register -> Hash Password -> Store User -> Login -> Verify Password -> Generate JWT -> Client Stores Token -> Bearer Token -> Protected Route -> Verify JWT -> Authorized Response


# Industry Best Practices
# As a backend engineer, keep these rules in mind:
# ❌ Never store plain-text passwords.
# ✅ Hash every password with bcrypt (or another strong password hashing algorithm).
# ❌ Never include passwords or other secrets inside JWT payloads.
# ✅ Always set token expiration.
# ✅ Keep your SECRET_KEY in environment variables, never hard-code it.
# ✅ Separate authentication logic from business logic.





# Step 1: Understand the Evolution
# current application looks like this:
# Browser -> main.py -> crud.py -> models.py -> PostgreSQL

# Anyone can call
# POST /users
# GET /users
# PUT /users/{id}
# DELETE /users/{id}
# There is no security.

# Now we'll evolve it.
# Browser -> Login -> JWT Token -> Protected Endpoints -> crud.py -> Database
# Notice something?
# We're not replacing your CRUD. We're adding security before it.


# Step 2: What Needs to Change?
# Your current User model only contains: name, email, is_active, created_at

# But authentication requires a password.
# So the first change is:
# hashed_password = Column(
#     String,
#     nullable=False
# )

# Notice: hashed_password NOT password
# Because passwords are never stored directly.


# Step 3: Your Schemas Will Grow
# Currently you have: UserBase -> UserCreate -> UserUpdate -> UserResponse

# Now we expand it:
# UserBase
#    ↓
# UserCreate
#   ├── name
#   ├── email
#   └── password
#    ↓
# UserLogin
#   ├── email
#   └── password
#    ↓
# UserResponse

# Notice something?
# Only UserCreate and UserLogin contain plain passwords.
# UserResponse never includes a password.


# Step 4: Add Two New Files
# We'll create:
# backend-learning/
# ├── auth.py
# ├── security.py
# Each has one responsibility.

# security.py
# Think of it as: The Security Toolbox
# It doesn't know anything about users.
# It only knows how to:
# Hash Password
# Verify Password
# Create JWT
# Verify JWT
# Nothing else.

# auth.py
# Think of it as: The Authentication Manager
# It knows: 
# Register User
# Login User
# Get Current User
# Protected Routes
# It uses functions from security.py.

# Think of it like this: auth.py -> security.py -> python-jose, bcrypt, passlib



# Step 5: Your Folder Structure Becomes
# backend-learning/
# ├── main.py
# ├── database.py
# ├── models.py
# ├── schemas.py
# ├── crud.py
# ├── security.py   
# ├── auth.py       
# └── requirements.txt
# This is the same structure you'll see in many production FastAPI projects.


# Step 6: What Happens During Registration?
# Today your flow is:
# POST /users -> Save User

# After authentication:
# POST /register -> Receive Password -> Hash Password -> Save Hash -> Database

# Notice: The password exists in plain text only briefly in memory while processing the request. The database only stores the hash.


# Step 7: Login Flow
# User sends:
{
    "email":"adya@gmail.com",
    "password":"secret123"
}
#           ↓
# Database returns hashed_password -> Verify -> Correct? -> Generate JWT -> Return Token


# Step 8: Using the Token
# Next request:
# GET /users Authorization: Bearer eyJhbGciOi...
#   ↓
# FastAPI -> Verify JWT -> Current User -> CRUD -> Response
# Now only authenticated users can access protected endpoints.


