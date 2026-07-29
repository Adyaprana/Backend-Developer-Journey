# Chapter 1 — Before FastAPI

# Imagine you wrote this Python program: 
print("Hello World")

# How do you run it?
# python main.py -> Python executes the file. Then Program ends.
# Nothing waits for another user.

# Now imagine Google.
# Millions of users open Google every second.
# Can Google do:
print("Hello")
exit()
# No. -> A backend server must stay alive forever.
# Like this: User 1 → Request -> Response -> (waiting...) -> User 2 → Request -> Response -> (waiting...) -> User 3... -> Forever

# This is the first major difference between a Python script and a backend server.






# Chapter 2 — What is FastAPI?
# FastAPI is NOT a programming language. It is NOT a database. It is NOT a server. FastAPI is a web framework.
# Its job is to help us answer HTTP requests.

# Imagine a receptionist 
# Visitor: "I need Room 101." -> Receptionist -> Guides visitor.
# FastAPI is that receptionist.
# When someone requests: GET /users
# FastAPI says: "I know which Python function should handle this."






# Chapter 3 — Then what is Uvicorn?

# FastAPI -> Knows routing, Knows validation, Knows documentation, Knows request parsing.
# Uvicorn -> Knows networking, Knows ports, Knows sockets, Knows HTTP, Runs forever.

# Think of it like this: Customer -> Restaurant Door -> Waiter -> Chef
# Who opens the restaurant?
# Not the chef. The restaurant itself.
# Similarly,

# Browser -> Uvicorn -> FastAPI -> Code
# FastAPI never opens Port 8000. Uvicorn does.






# Chapter 4 — Install FastAPI

# Create a new folder. -> backend-learning/
# Open it in VS Code. Open Terminal. Install FastAPI and Uvicorn: pip install fastapi uvicorn

# Verify installation:
# pip show fastapi
# pip show uvicorn
# You should see version information.






# Chapter 5 — Project Structure
# Today we keep it simple.
# backend-learning/
# │
# ├── main.py
# ├── .venv/
# └── requirements.txt (later)
# Don't overcomplicate it.
# We'll organize the project properly once we understand the basics.






# Chapter 6 — Your First FastAPI App
# Create: main.py
# Write this:
from fastapi import FastAPI
app = FastAPI()
@app.get("/")
def home():
    return {"message": "Welcome to my first FastAPI application!"}

# Line 1 -> from fastapi import FastAPI
# We're importing the FastAPI class from the FastAPI package.
# Think of it like importing Path from pathlib or datetime from the standard library.

# Line 2 -> app = FastAPI()
# This creates your application object.
# This object stores: Routes, Documentation, Middleware, Configuration, Event handlers
# Almost everything revolves around this app instance.

# Line 3 -> @app.get("/")
# This is a decorator.
# This decorator tells FastAPI: "If someone sends a GET request to /, call the function below."
# Notice that the function isn't called here. The decorator registers it with the application.

# Line 4 -> def home():
# This is just a normal Python function.
# FastAPI will call it when a matching request arrives.

# Line 5 ->     return {"message": "Welcome to my first FastAPI application!"}
# You're returning a Python dictionary.
# FastAPI automatically converts it into JSON.

# You write: {"message": "Hello"}
# The client receives: {"message": "Hello"}
# This automatic serialization is one of FastAPI's conveniences.







# Chapter 7 — Run the Server
# Open Terminal.
# Run: python -m uvicorn main:app --reload

# Let's break this command down:
# uvicorn: Start the Uvicorn server.
# main: The filename (main.py), without the .py extension.
# app The application object inside main.py.
# Specifically: app = FastAPI()
# --reload
# Development mode.
# Whenever you save your file, Uvicorn automatically reloads the server. No need to restart it manually. 





# Chapter 8 — What Happens Internally?
# When you visit: http://127.0.0.1:8000/
# The flow is: Browser -> GET/ -> Uvicorn -> FastAPI -> home() -> Dictionary -> JSON -> Browser
# That's the complete request lifecycle for your first endpoint.





# Chapter 9 — Swagger UI
# Now open: http://127.0.0.1:8000/docs
# You'll see an interactive API documentation page.
# This is generated automatically from your FastAPI application.
# Why is this valuable
# No separate documentation tool.
# Easy endpoint testing.
# Clear request/response structure.
# Excellent for frontend developers and API consumers.
# As your API grows, the documentation updates automatically.



# Swagger UI (Browser)
#         │
#         │ HTTP GET Request
#         ▼
# http://127.0.0.1:8000/
#         │
#         ▼
#       Uvicorn
#         │
#         ▼
#       FastAPI
#         │
#         ▼
#   Route Matching
#         │
#         ▼
#   @app.get("/")
#         │
#         ▼
#       home()
#         │
#         ▼
# Python Dictionary
#         │
#         ▼
#    JSON Encoder
#         │
#         ▼
# HTTP Response (200)
#         │
#         ▼
#     Swagger UI



# Chapter 10 - Path Parameters and Query Parameters
# 1. Path Parameters
# @app.get("/users/{user_id}")
# You'll learn how FastAPI extracts values directly from the URL.

# 2. Query Parameters
# @app.get("/items")
# Used like: /items?skip=0&limit=10



# Imagine you're building Instagram.
# Suppose someone opens: https://instagram.com/adyaprana

# How does Instagram know whose profile to show?
# It extracts: adyaprana
# from the URL. That value identifies one specific resource.
# That's exactly what a Path Parameter is.


# Path Parameters

# Suppose we write:
from fastapi import FastAPI
app = FastAPI()
@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {
        "user_id": user_id
    }

# Notice this part: "/users/{user_id}"
# Those curly braces {} are special.
# They tell FastAPI: "Whatever comes here in the URL, store it in the variable user_id."

# Example 1
# You visit: http://127.0.0.1:8000/users/5

# FastAPI internally does something like: user_id = 5
# get_user(user_id)
# So your function receives: user_id = 5
# and returns {"user_id": 5}

# Example 2
# Visit: /users/100
# Internally: user_id = 100
# Response: {"user_id": 100}

# Example 3
# Visit: /users/999
# Response: {"user_id": 999}

# Same function. Different values.

# Why is user_id: int important?
# Look carefully: def get_user(user_id: int):
# We wrote: :int
# Remember Python Type Hints?
# FastAPI uses them heavily.
# Suppose someone visits:/users/25
# FastAPI converts: "25" -> 25 (an integer)

# before your function runs. Now suppose someone visits: /users/hello
# You never wrote: 
# try:
#     ...
# except:

# Yet FastAPI immediately returns: 422 Unprocessable Entity Because user_id must be int
# FastAPI validates it automatically. That's one reason FastAPI is loved.







# Query Parameters
# Now let's look at another situation. Suppose you're building Amazon.
# Do you always want all products, No.

# Sometimes you want:
# only 10 products
# page 2
# sorted by price
# The resource is still: /products
# You're just changing how you fetch it. That's what query parameters do.

# Suppose we write:
@app.get("/items")
def get_items(skip: int = 0, limit: int = 10):
    return {
        "skip": skip,
        "limit": limit
    }

# Notice something. There are no curly braces.

# Now visit: /items

# Response: 
# {
#     "skip": 0,
#     "limit": 10
# }
# Because we gave default values.

# Now visit: /items?skip=20

# FastAPI reads: skip = 20 but limit wasn't provided.
# So it stays: 10
# Response:
# {
#     "skip":20,
#     "limit":10
# }
# Visit: /items?skip=40&limit=5
# FastAPI automatically parses
# skip = 40
# limit = 5
# Response:
# {
#     "skip":40,
#     "limit":5
# }
# Internal Flow

# When you type: /items?skip=40&limit=5
# FastAPI internally behaves almost like this:
# skip = 40
# limit = 5
# get_items(skip, limit)
# You don't write the parsing logic.
# FastAPI does it for you.

# Path Parameter vs Query Parameter:
# | Path Parameter                 | Query Parameter               |
# | ------------------------------ | ----------------------------- |
# | Identifies a specific resource | Modifies how data is returned |
# | Required                       | Usually optional              |
# | Written using `{}`             | Written after `?`             |
# | Example: `/users/5`            | Example: `/users?limit=10`    |

# Real Examples 
# GitHub: /users/octocat
# octocat is a path parameter because it identifies one user.

# YouTube Search: /results?search_query=fastapi
# search_query is a query parameter because it's filtering the results.

# Amazon: /products?category=laptop&page=2
# Both are query parameters.

# LeetCode: /problems/two-sum
# two-sum is effectively a path parameter because it identifies one problem.

# Modify your main.py to include these two endpoints:
@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id}

@app.get("/items")
def get_items(skip: int = 0, limit: int = 10):
    return {
        "skip": skip,
        "limit": limit
    }

# # Then test these URLs one by one:
# http://127.0.0.1:8000/users/7
# http://127.0.0.1:8000/users/100
# http://127.0.0.1:8000/users/abc
# # (Observe what FastAPI does.)
# http://127.0.0.1:8000/items
# http://127.0.0.1:8000/items?skip=20
# http://127.0.0.1:8000/items?skip=50&limit=5