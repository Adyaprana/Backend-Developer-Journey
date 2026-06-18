# DAY 7 MISSION — REST DAY + DEEP UNDERSTANDING DAY

# Week 1 Revision Checklist

# Variables
name = "Adyaprana"
age = 23


# Input
name = input("Enter Name: ")


# Conditions
if age >= 18:
    print("Adult")


# Loops
for i in range(5):
    print(i)


# Lists
skills = ["Python","SQL"]


# Dictionaries
student = {
    "name":"Adyaprana"
}

#-----------------------------------------#
# What Is Backend?
# Most beginners think:

# Frontend = Website
# Backend = Magic
# Wrong.
#-----------------------------------------#

# Example:
# Instagram (When you open Instagram)

# Frontend:
# Buttons
# Images
# Videos
# Design

# Backend:
# User Login
# Database
# Messages
# Likes
# Comments
# Followers

# Backend handles logic.
#-----------------------------------------#

# Backend Analogy
# Restaurant Example:

# Customer: --> I want Pizza
# Waiter: --> Takes request
# Kitchen: --> Makes pizza

# Backend = Kitchen
# Frontend = Waiter
# Database = Storage Room
#-----------------------------------------#

# Client Server Model

# Client --> Browser, Mobile App, Frontend
# Examples: --> Chrome, Instagram App, WhatsApp

# Server --> Backend Application
# Examples: --> FastAPI, Django, Flask

# Flow: --> Client -> Request -> Server -> Response -> Client
#-----------------------------------------#

# Example
# You search: (weather in Bangalore)

# Browser sends request.
# Server processes.
# Server sends result.
# Browser displays result.
#-----------------------------------------#

# What Is An API?
# API = Application Programming Interface

# Think of API as a waiter.
# Customer: Give me Pizza
# Waiter: API
# Kitchen: Backend
#-----------------------------------------#

# Real Example
# You open: (YouTube)

# YouTube frontend asks:
# Give me videos

# Backend sends:
{
  "title":"Python Tutorial",
  "views":50000
}
#-----------------------------------------#

# What Is JSON?

# You will see JSON daily.
# Example:
{
  "name":"Adyaprana",
  "age":23,
  "city":"Bangalore"
}
# Looks familiar?

# Because:
{
 "name":"Adyaprana",
 "age":23,
 "city":"Bangalore"
}
# is basically a Python dictionary. That's why dictionaries were important.
#-----------------------------------------#

# How Google Login Works
# Simple version:

# Step 1
# Enter Email

# Step 2
# Frontend sends request.
# POST /login

# Step 3
# Backend checks database.

# Step 4
# If correct:
# Login Success
# If wrong:
# Invalid Password
#-----------------------------------------#

# What Is A Database?
# Database = Digital Storage.

# Examples:(Users, Orders, Products, Payments)

# Stored inside: 
# PostgreSQL
# MySQL
# SQLite

# Instead of:
# name = "Adyaprana"
# for every user,

# database stores:

# ID	Name
# 1	  Adyaprana
# 2	  Rahul
# 3	  Amit
#-----------------------------------------#

# Q1. What is Frontend?
# Answer: Part users interact with.

# Q2. What is Backend?
# Answer: Handles business logic, APIs and databases.

# Q3. What is Client?
# Answer: Application requesting data.
# Examples: Browser, Mobile App

# Q4. What is Server?
# Answer: Application responding to requests.

# Q5. What is API?
# Answer: Communication bridge between applications.

# Q6. What is JSON?
# Answer: Data exchange format.

# Q7. Why are Dictionaries important for backend?
# Answer: JSON data maps directly to Python dictionaries.

# Q8. What is Database?
# Answer: Structured storage for application data.

# Q9. What is PostgreSQL?
# Answer: A relational database used heavily in backend development.

# Q10. Why learn Python before FastAPI?
# Answer: FastAPI is built using Python.
