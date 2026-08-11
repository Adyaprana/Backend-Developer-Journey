# 🚀 Backend Developer Journey — Project 1 (URL Shortener API)

# Day 50 — Database Design & API Contracts (Engineering First)



# Step 1 — Before Designing the Database
# Let's ask the most important question.

# What is a Database?
# Many beginners answer: "A database stores data."
# That isn't wrong. But engineers think differently.
# A database stores the state of the application.
# Our application's state is: "Which short code belongs to which original URL?"
# Everything else is derived from that.







# Step 2 — What Information Do We Actually Need?

# Imagine a user submits: https://www.google.com
# What do we need to remember forever? Let's think.
# Original URL? -> Obviously yes. Without it we cannot redirect.
# Short Code? -> Yes. Otherwise we cannot find the URL later.

# ID? -> Do we really need it?
# This is actually an interesting question.
# Could we use the short code as the primary key?
# Technically... Yes. Many systems actually do.
# But should we? 

# Click Count? -> Yes. Otherwise /stats becomes impossible.
# Created Time? -> Yes. Useful for: Analytics, Sorting, Expiration (future), Auditing

# Version 1 Database Requirements
# We only need these five pieces of information: 
# id
# original_url
# short_code
# clicks
# created_at







# Step 3 — Column by Column Design

# 1. id 
# Question: Should we even have an ID?
# There are two common approaches.

# Option A
# id Auto Increment Integer
# Example: 1, 2, 3, 4, 5
# Advantages: Fast, Small, Easy joins, Industry standard
# Disadvantages: Users never see it.

# Option B
# Use short_code as Primary Key.
# Advantages: One less column.
# Disadvantages: Changing short codes later becomes painful, Foreign keys become larger, Indexes become larger.

# Engineering Decision
# We will use id as the internal primary key.
# Because internal identifiers should stay internal.
# Even if someday we change the short code algorithm,
# the database remains stable. This is how many production systems are designed.


# 2. original_url
# Question. What type: VARCHAR, TEXT, CHAR.

# Some URLs are tiny. Some URLs can exceed 1000 characters.
# If we choose VARCHAR(255)
# we might reject perfectly valid URLs.

# Professional choice: TEXT
# Why -> No unnecessary limits.
# PostgreSQL handles it efficiently.

# 3. short_code
# This is the star of our project.
# Example: Xa82Pq Should it be TEXT or VARCHAR?
# It must be unique, It should be indexed for fast lookups, It will never be null.

# 4. clicks
# Simple integer. Starts at 0
# Every redirect increments it. Should clicks ever be negative? Never.

# 5. created_at
# We want PostgreSQL to automatically record when a URL is created.
# No need for the client to send this value.








# Step 4 — Constraints
# Constraints protect data quality.
# Think of them as database-level rules.

# Primary Key -> id Every row is unique.

# NOT NULL -> Should the original URL be nullable -> No. A shortened URL without an original URL makes no sense. Same for the short code.

# UNIQUE -> Should two rows have the same short code -> Absolutely not. So short_code must be unique.

# DEFAULT -> clicks should start at 0 without us manually assigning it every time.







# Step 5 — Indexes
# Imagine we eventually have: 10 million rows.
# A user requests: GET /abc123
# How does PostgreSQL find it -> Without an index, it may scan row by row. That's slow. 
# With an index on short_code, lookups become much faster.

# For our project:
# id is indexed automatically because it's the primary key.
# short_code should also be indexed (and its unique constraint creates an index in PostgreSQL).








# Step 6 — API Contracts
# Before coding, let's define how clients will interact with our service.

# POST /shorten
# Request:
{
  "url": "https://www.google.com"
}
# Response
{
  "original_url": "https://www.google.com",
  "short_code": "Xa82Pq",
  "short_url": "http://localhost:8000/Xa82Pq"
}

# GET /{short_code}
# No JSON response.
# Instead: HTTP Redirect to the original URL.

# GET /stats/{short_code}
# Response
{
  "original_url": "https://www.google.com",
  "short_code": "Xa82Pq",
  "clicks": 15,
  "created_at": "2026-07-23T11:45:00Z"
}








# Step 7 — The Biggest Design Decision
# We now reach the heart of the project.
# How do we generate the short code?

# There are several real-world strategies:

# 1. Random Characters
# Example: aX92Pk
# Pros: Simple, Easy to implement, Good enough for Version 1.
# Cons: Must check for collisions.

# 2. Base62 Encoding
# Convert an internal numeric ID into a short Base62 string.
# Example: 125 → cb
# Pros: No collisions, Short codes, Predictable.
# Cons: Sequential URLs can be guessed.

# 3. UUID-Based
# Generate a UUID and shorten part of it.
# Pros: Extremely unlikely to collide.
# Cons: Longer than necessary, Less elegant for a URL shortener.
    
# 4. Hashing
# Hash the original URL.
# Pros: Deterministic.
# Cons: Handling duplicates and collisions adds complexity.
