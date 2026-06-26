# THEORY 2 — WHAT IS REST?

# REST means: Representational State Transfer
# REST is a style for designing APIs.
# Created by: Roy Fielding
# REST is not a protocol, REST is an architectural style.

# Good REST APIs are:
# Simple
# Predictable
# Scalable

# Bad API:
# /getUserData123

# Good REST API:
# /users/1




# THEORY 3 — 6 REST CONSTRAINTS

# 1. Client Server
# Frontend and Backend are separate.
# Example: React Frontend & FastAPI Backend
# Frontend doesn't care how backend works.
# Backend doesn't care how frontend looks.

# Client: -->
# Browser
# Mobile App
# React Frontend

# Server: --> 
# Backend
# Database Logic
# Separated.

# 2. Stateless -->Every request is independent.
# Example: 
# Request 1: GET /users
# Request 2: GET /posts
# Server should not depend on previous request.

# 3. Cacheable --> Responses can be cached.
# Example:
# Logo image.
# Don't download again.
# Use cache.
# Faster.

# 4. Uniform Interface --> Standard URLs.
# Example:
# /users
# /users/1
# /posts
# /posts/10
# Not weird names.

# 5. Layered System --> Client doesn't know:
# Load Balancer
# Gateway
# Microservice
# Database
# Everything is hidden.
# It only talks to API.

# 6. Code On Demand --> Optional.
# Server can send executable code.
# Rarely used.


