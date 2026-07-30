# DAY 44 — Pydantic Models & Request/Response Validation

# Yesterday we built this:

# @app.get("/")
# def home():
#     return {"message": "Hello"}

# Easy. Now imagine we're building a real application.
# A user wants to register.
# They send:
{
    "name": "Adyaprana",
    "email": "adya@gmail.com",
    "password": "12345678"
}
# How does FastAPI know
# name should be string?
# email should be string?
# password required?
# age optional?
# email valid?
# password length?
# Without validation... backend becomes dangerous.





# Chapter 1 — Life Before Pydantic

# Imagine Flask. You'd manually do something like:
# data = request.json
# name = data["name"]
# email = data["email"]
# password = data["password"]
# Then check: if not isinstance(name, str):
# Then: if len(password) < 8:
# Then: if "@" not in email:

# Imagine writing this for 100 APIs.
# Very repetitive, Very error-prone.


# Enter Pydantic
# Pydantic says: Describe your data once. I'll validate everything.
# Think of Pydantic as JSON -> Pydantic -> Clean Python Object

# Instead of manually checking data, Pydantic does it automatically.

# What is BaseModel?
# You'll always start with: from pydantic import BaseModel
# Think of BaseModel as A blueprint describing what valid data looks like.

# Example:
from pydantic import BaseModel
class User(BaseModel):
    name: str
    age: int
# This says: A valid User must have
# name → string
# age → integer
# Nothing more, Nothing less.
# This Looks Like a Python Class...
# But instead of storing business logic, it stores data validation rules.
# Think of it like: Car class -> behavior -> drive()
# vs
# User BaseModel -> data -> validate()







# Chapter 2 — Your First Request Body
# Let's create our first POST endpoint.

from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI()
class User(BaseModel):
    name: str
    age: int
@app.post("/users")
def create_user(user: User):
    return user

# Notice something different.

# Yesterday: def get_user(user_id: int):
# Today: def create_user(user: User):

# Instead of an integer, FastAPI expects an entire object.
# Client sends
{
    "name": "Adyaprana",
    "age": 22
}
# FastAPI automatically -> creates
User(
    name="Adyaprana",
    age=22
)

# Then passes it into 
create_user()
# No parsing. No JSON handling. No manual validation.







# Chapter 3 — Swagger Changes Automatically
# Go to /docs
# You'll now notice something new.
# Instead of GET you'll see POST

# Click Try it Out
# Swagger automatically generates
# {
#   "name": "string",
#   "age": 0
# }
# You didn't create that form. Pydantic did.
# Automatic Type Conversion Suppose client sends
{
    "name": "Adyaprana",
    "age": "22"
}
# Age is text. Your model says age: int Pydantic converts "22" -> 22

# Automatic Validation
# Now try
{
    "name": "Adyaprana",
    "age": "hello"
}
# Can hello become an integer No.

# FastAPI immediately returns 422
# without calling your function. Your endpoint never runs.

# Why 422?
# Why not 400 Bad Request?
# Because HTTP 400 means
# Request format itself is invalid.
# But here JSON format is correct.
# Example
{
    "age":"hello"
}
# This is valid JSON.
# The problem is the data doesn't match the schema. That's exactly what 422 Unprocessable Entity means.

# "I understand your request. But I cannot process these values."


# Optional Fields
# Suppose age isn't required.
from typing import Optional
class User(BaseModel):
    name: str
    age: Optional[int] = None
# Now
# Both work.
{
    "name":"Adyaprana"
}
# and
{
    "name":"Adyaprana",
    "age":22
}
# Default Values
# Example
class User(BaseModel):
    name: str
    country: str = "India"
# Client sends
{
    "name":"Adyaprana"
}
# Result becomes
User(
    name="Adyaprana",
    country="India"
)
# Automatically. Field Validation Pydantic becomes really powerful here.

from pydantic import BaseModel, Field
class User(BaseModel):
    name: str = Field(min_length=3)
    age: int = Field(gt=0)
# Now Jo fails. Age-5 fails. Without writing even one if statement.

# Another example
class Product(BaseModel):
    price: float = Field(gt=0)
# Negative prices? Impossible.

# Better Email Validation
# Instead of email: str Use

from pydantic import EmailStr
# Then email: EmailStr Now abc fails. abc@gmail.com passes. Response Models

# This is one of the most important backend concepts.
# Suppose database contains
{
    "id":1,
    "name":"Adyaprana",
    "email":"adya@gmail.com",
    "password":"secret123"
}

# Should an API return password? ever. Instead
# Create another model.
class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

# Then
# @app.get("/users/{id}", response_model=UserResponse)
# Even if your function accidentally returns
{
    "id":1,
    "name":"Adyaprana",
    "email":"adya@gmail.com",
    "password":"secret123"
}

# FastAPI filters it. Client only receives
{
    "id":1,
    "name":"Adyaprana",
    "email":"adya@gmail.com"
}

# This is incredibly important for security.

# Real Industry Pattern You'll rarely use one model.
# Instead: UserCreate Used for POST requests. Contains password -> UserUpdate -> Used for PATCH. -> UserResponse -> Returned to client. No password. UserDB
# Internal database model.
# This separation prevents accidental data leaks and keeps each model focused on a single purpose.






# main.py :

from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel, EmailStr, Field

app = FastAPI()


class UserCreate(BaseModel):
    name: str = Field(min_length=3, max_length=50)
    email: EmailStr
    age: Optional[int] = Field(default=None, gt=0)
    country: str = "India"


@app.post("/users")
def create_user(user: UserCreate):
    return {
        "message": "User created successfully!",
        "user": user,
    }

# Then experiment in Swagger with these cases:
# Valid data:
{
  "name": "Adyaprana",
  "email": "adya@gmail.com",
  "age": 22
}

# Invalid email:
{
  "name": "Adyaprana",
  "email": "not-an-email",
  "age": 22
}

# Name too short:
{
  "name": "Jo",
  "email": "adya@gmail.com"
}

# Negative age:

{
  "name": "Adyaprana",
  "email": "adya@gmail.com",
  "age": -5
}
# Omit country and observe that "India" is filled in automatically.









# 1. Pydantic BaseModel

# You learned that: class UserCreate(BaseModel):
# is not just another Python class. 
# It is a schema that defines:
# What data is expected
# What type each field should have
# Which fields are required
# Which fields are optional
# Validation rules
# Default values
# Think of it as the contract between your API and its clients.

# 2. Request Body
# Yesterday (Day 43), your API accepted data from:
# Path parameters and Query parameters
# Today, it accepts an entire JSON object:
{
  "name": "Adyaprana",
  "email": "adya@gmail.com",
  "age": 22
}
# FastAPI automatically converts that JSON into a Python object.
# This is a huge productivity gain.

# 3. Type Conversion
# You saw that:
{
  "age": "22"
}
# becomes age = 22
#  without writing: int(age)
# FastAPI + Pydantic handle that for you.

# 4. Automatic Validation
# You intentionally broke the input.
# Examples:
# invalid email
# negative age
# short name
# FastAPI immediately returned: 422 Unprocessable Entity
# without entering your endpoint.
# This means: Invalid data never reaches your business logic.
# That's exactly how professional APIs should behave.

# 5. Default Values
# You learned: country: str = "India"
# If the client doesn't provide it: FastAPI automatically fills it.
# No if statement needed.

# 6. Optional Fields
# age: Optional[int] = None
# Now age can be omitted.
# Without Optional: Age is required.

# 7. Field Validation
# Instead of writing
# if len(name) < 3: 
# you simply declare:
# Field(min_length=3)
# This is called declarative validation.
# You're describing the rules rather than manually checking them.

# 8. Email Validation
# Instead of email: str you used EmailStr
# That gives much stronger validation with almost no extra code.

# 9. Response Models
# This is the most important concept from today.
# Suppose your database stores:
{
    "id":1,
    "name":"Adyaprana",
    "email":"adya@gmail.com",
    "password":"secret123"
}
# Should the API return the password?
# Never. Response models act like a security filter.
# Even if your function returns too much information, FastAPI only sends the fields defined in the response model.
# This is why experienced backend engineers create separate schemas such as:
# UserCreate
# UserUpdate
# UserResponse
# rather than using one model everywhere. The Bigger Picture Let's connect everything you've learned so far.

# Day 43
# The client sends a request. Browser -> FastAPI

# Day 44
# FastAPI validates the incoming data.
# Browser -> JSON -> Pydantic Validation -> Python Object -> Your Function

# So now the request lifecycle looks like:
# Client -> HTTP Request -> Uvicorn -> FastAPI -> Pydantic Validation -> Python Object -> Your Endpoint -> Python Dictionary -> JSON Response -> Client
