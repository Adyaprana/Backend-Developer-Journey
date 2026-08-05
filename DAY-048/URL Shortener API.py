# 🚀 Backend Developer Journey — Project 1 (URL Shortener API)

# Backend Developer Journey — Project 1
## URL Shortener API
### Version 1.0
### (Continuation from Day 48 of my 420-Day Backend Journey)

# Current Phase: Day 48
# Today's objectives:
# • Discuss project requirements
# • Understand URL shortening
# • Discuss real-world systems like Bitly
# • Gather functional and non-functional requirements
# • Decide architecture
# • Draw complete data flow
# • Design folder structure
# • Design database schema
# Do NOT write implementation code until architecture is finalized.





# Day 48 — Project Kickoff
# Project - URL Shortener API v1.0

# Think of it as building a mini Bitly, not a CRUD demo.
# The purpose isn't just to shorten URLs it's to learn how backend engineers think while designing services.




# Step 1 — Understanding the Problem
# Imagine someone gives you this URL: https://www.amazon.in/Samsung-Galaxy-S24-Ultra-5G-Storage/dp/B0CT5DJ6XZ/ref=sr_1_1?crid=...
# It is: ugly, difficult to share, difficult to remember, difficult to type

# Instead we create: https://our-domain.com/aB92Kx

# When someone visits: GET /aB92Kx
# our backend immediately redirects them to the original URL.
# That's the entire business idea. Simple. But behind that simplicity lies a lot of engineering.





# What Does Our Backend Actually Do?
# Instead of thinking about APIs first, think about responsibilities.

# Our service must answer four questions.

# 1. Can I store a long URL?
# Example: Original URL -> Database

# 2. Can I generate a unique short code?
# Example: https://google.com -> Xa82Pw
# The generated code must be unique, short, URL-safe, fast to generate

# 3. Can I redirect users?
# Someone visits: ourdomain.com/Xa82Pw
# The backend should: Find Xa82Pw -> Look up database -> Find original URL -> Increase click count -> Return Redirect

# 4. Can I show analytics?
# For example: Original URL, Clicks, Created At
# Later we'll expand this to include much richer analytics.





# Functional Requirements (What the system must do)

# For Version 1, our API should support exactly these features:

# URL Creation: Accept a valid long URL, Generate a unique short code, Store it in PostgreSQL, Return the shortened URL.
# URL Redirection: Accept a short code, Find the corresponding URL, Increase the click count, Redirect the user to the original URL.

# Statistics
# Return: original URL, short code, click count, created time
# That's it:- No authentication, No users, No expiration, No QR codes, No Redis.

# Keeping Version 1 focused is an engineering decision that reduces complexity while delivering a complete, usable product.







# Non-Functional Requirements (How the system should behave)

# Professional teams always define these.
# For v1, our goals are:
# | Requirement           | Why it matters                           |
# | --------------------- | ---------------------------------------- |
# | Fast responses        | Redirects should feel instant            |
# | Reliable              | URLs should never disappear unexpectedly |
# | Maintainable          | Easy to add features later               |
# | Scalable architecture | Ready for authentication, caching, etc.  |
# | Clean code            | Easy to understand and modify            |
# | RESTful API           | Follows industry conventions             |

# These don't add features, but they determine the quality of the system.





# Who Are the Actors?
# Our first version has only one actor.

# User
# The user can: Create URL -> Visit URL -> View Statistics
# No login is required in v1.





# User Stories
# Backend teams often write requirements as user stories.

# Story 1
# As a user, I want to shorten a long URL so that it is easier to share.
# Story 2
# As a user, I want anyone who opens my short URL to be redirected automatically.
# Story 3
# As a user, I want to know how many times my short link has been used.
# These stories guide our design and testing.






# Version 1 Scope
# To avoid overengineering, let's clearly define what is in and out of scope.

# Included:
# URL shortening
# Unique short code generation
# Redirecting to original URLs
# Click counting
# URL statistics
# PostgreSQL persistence
# FastAPI REST API
# Swagger documentation

# Not Included
# User accounts
# JWT authentication
# Custom aliases
# URL expiration
# QR codes
# Redis caching
# Docker
# CI/CD
# Rate limiting
# Analytics dashboard





# High-Level System Flow
# Before discussing folder structure or database tables, it's useful to visualize the entire lifecycle of a request.

# Create Short URL:
# Client -> POST /shorten -> FastAPI Router -> Service Layer -> Generate Unique Code -> Repository Layer -> PostgreSQL -> Return Short URL

# When someone opens the short URL:
# Browser -> GET /{short_code} -> Router -> Service -> Repository -> Database Lookup -> Increment Click Count -> Return HTTP Redirect (307) 

# For statistics:
# Client -> GET /stats/{short_code} -> Router -> Service -> Repository -> Database -> JSON Response


# Interview Questions
# What is the difference between functional and non-functional requirements?
# Why do software teams define project scope before implementation?
# What is a URL shortener, and how does it work internally?
# Why is a redirect endpoint different from a normal GET endpoint?
# Why are user stories useful during software development?
# What are the core responsibilities of a URL shortening service?
# Why should Version 1 avoid unnecessary features like authentication or Redis?