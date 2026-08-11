# 🚀 Backend Developer Journey — Project 1 (URL Shortener API)

# Day 51 — The Project Comes to Life

# Step 1 — Create the Virtual Environment
# Inside the project: python -m venv .venv
# Why first -> Because every Python project should have an isolated environment.






# Step 2 — Activate It
# Windows: .venv\Scripts\activate
# Then confirm: 
# python --version
# pip --version

# something like: 
# Python 3.12.3
# pip 24.0 







# Step 3 — Install Only What We Need Right Now

# Just the core dependencies:
# fastapi
# uvicorn
# sqlalchemy
# psycopg2-binary
# python-dotenv

# Later we'll add:
# Alembic
# pytest
# httpx
# Docker
# Redis
# etc.
# No need to install everything today.







# Step 4 — Freeze Requirements
# pip freeze > requirements.txt
# Now anyone can recreate your environment.

# pip install -r requirements.txt
# pip list
# Package           Version
# ----------------- -------
# annotated-doc     0.0.4
# annotated-types   0.8.0
# anyio             4.14.2
# click             8.4.2
# colorama          0.4.6
# fastapi           0.139.2
# greenlet          3.5.4
# h11               0.16.0
# idna              3.18
# pip               24.0
# psycopg2-binary   2.9.12
# pydantic          2.13.4
# pydantic_core     2.46.4
# python-dotenv     1.2.2
# SQLAlchemy        2.0.51
# starlette         1.3.1
# typing_extensions 4.16.0
# typing-inspection 0.4.2
# uvicorn           0.51.0








# ✅ Step 5 — Configure .gitignore

# Make sure it ignores things like:
# .venv/
# __pycache__/
# .env
# .pytest_cache/






# Step 6 — Create a PostgreSQL Database

# Notice: Database, not table.
# Example: url_shortener_db
# No tables yet. Just an empty database.

# Step 6.1 — Open pgAdmin 4
# Open pgAdmin 4.
# Wait until the dashboard loads. On the left side, you should see something like:
# Servers
# └── PostgreSQL 17 (Your version may be PostgreSQL 16 or 17.)

# Step 6.2 — Expand Your Server
# Click the arrow (>) next to: Servers
# Then click the arrow next to your PostgreSQL server. It may ask for your PostgreSQL password. Enter it.
# Now you'll see something like:
# Servers
# └── PostgreSQL 17
#     ├── Databases
#     ├── Login/Group Roles
#     ├── Tablespaces

# Step 6.3 — Create a New Database
# Right-click on: Databases
# Choose: Create -> Database...
# A new window will open. 

# Step 6.4 — Fill the Database Details
# You'll be on the General tab.
# Database Name: url_shortener_db
# Owner (Leave it as): postgres
# Do not change anything else.

# Step 6.5 — Save
# Click: Save
# That's it. You have created your 2nd project database.

# Step 6.6 — Verify
# Expand:
# Databases

# You should now see:
# Databases
# ├── postgres
# ├── backend_journey
# ├── guesswise
# └── url_shortener_db
# The database exists.

# What NOT to Do
# Do NOT create:
# Leave it completely empty. We want SQLAlchemy to create the tables later.







# Step 7 — Configure .env
# Something like: DATABASE_URL=...
# No secrets in the code.

# Now go to your project folder.
# Create a file named: .env

# If it already exists, open it.
# Add this line: DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/url_shortener_db
# Replace: YOUR_PASSWORD → your PostgreSQL password.
# Example: DATABASE_URL=postgresql://postgres:mysecret***@localhost:5432/url_shortener_db

# Let's Understand This URL
# postgresql:// -> The database driver/protocol.
# postgres -> The PostgreSQL username.
# YOUR_PASSWORD -> The password for that user.
# localhost -> The database is running on your own computer.
# 5432 -> The default PostgreSQL port.
# url_shortener_db -> The database we just created.







# Step 8 — Create the Database Connection
# This is the first real backend file.

# database.py
# Its only responsibility: Read .env, Create SQLAlchemy Engine, Create Session, Expose get_db().
# Nothing else.

# Why do we need database.py -> Imagine every file that needs the database creates its own connection:
# router.py
# connect_to_database()

# service.py
# connect_to_database()

# repository.py
# connect_to_database()

# Soon you'll have the same code copied everywhere. Professional projects avoid this.
# Instead, one file is responsible for database configuration, and the rest of the project uses it.

# That's why we have:
# app/
# └── database/
#   └── database.py

# Its only job is: Read .env -> Create Engine -> Create Session Factory -> Provide Database Sessions.
# Nothing more.

# What we'll build today
# By the end of this step, database.py should do four things:
# 1. Read DATABASE_URL from .env
# 2. Create the SQLAlchemy Engine
# 3. Create the Session Factory
# 4. Create get_db() for FastAPI
# No models, No tables, No CRUD, No business logic.

# Step 8.1 — Imports

# First, open: app/database/database.py
# Add only these imports:
# from dotenv import load_dotenv
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# import os

# Why each import?
# load_dotenv -> Loads variables from the .env file into Python. Without it: os.getenv("DATABASE_URL") would return None.
# create_engine -> Creates SQLAlchemy's connection engine. Think of it as the application's gateway to PostgreSQL.
# sessionmaker -> Creates database sessions. Every request will eventually use one session.
# os -> Allows us to read environment variables.

# Step 8.2 — Load the .env File

# Now add only these two lines below the imports.
# load_dotenv()
# DATABASE_URL = os.getenv("DATABASE_URL")

# So now your file becomes:
# from dotenv import load_dotenv
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# import os

# load_dotenv()
# DATABASE_URL = os.getenv("DATABASE_URL")

# Let's Understand These Two Lines
# Line 1 -> load_dotenv()
# It tells Python: "Go find the .env file and load all the variables into the environment."
# Without this line, os.getenv("DATABASE_URL") would return: None
# because Python doesn't automatically read .env files.

# Line 2 -> DATABASE_URL = os.getenv("DATABASE_URL")
# This asks the operating system: "Give me the value stored in the environment variable named DATABASE_URL."

# If your .env contains: DATABASE_URL=postgresql://postgres:1234@localhost:5432/url_shortener_db
# then DATABASE_URL will contain exactly: "postgresql://postgres:1234@localhost:5432/url_shortener_db"
# Notice something important: We are not hardcoding the password in our Python code.
# That's a professional practice because:
# Different developers can have different passwords.
# Production servers have different database credentials.
# Secrets stay outside the source code.

# Step 8.3 — Create the SQLAlchemy Engine

# This is the first place where our application will know how to talk to PostgreSQL.
# Add only one line below DATABASE_URL:
# engine = create_engine(DATABASE_URL)

# Step 8.4 — What is sessionmaker?

# Before we write any code, I want to explain why we need it.
# Imagine you walk into a bank. You don't own the bank. You don't get permanent access to the bank's database.
# Instead: Customer -> Gets a Token -> Performs Transactions -> Returns the Token
# A database session works in a similar way.

# What is a Session -> A session is your application's temporary conversation with the database.
# Example:  Open Session -> Read Data -> Insert Data -> Update Data -> Commit / Rollback -> Close Session
# Every request in FastAPI should get its own session. 
# why -> Because if two requests share the same session, they can interfere with each other.

# Imagine two users.
# User A ----------------\
#                          \
#                           Database
#                          /
# User B ----------------/

# If they shared the same session: User A could accidentally affect User B's transaction. One failed request could corrupt another. It wouldn't be thread-safe.

# Instead:
# User A → Session A → Database
# User B → Session B → Database
# Each request gets its own session.

# So what does sessionmaker do -> It doesn't create a session immediately. It creates a factory that knows how to create sessions whenever we need one. 

# Think of it like this: 
# Engine
#     │
#     ▼
# Session Factory
#     │
#     ▼
# Session 1
# Session 2
# Session 3
# Session 4
# The factory keeps making new sessions when FastAPI asks for them.

# Why not just write: Session()
# Because Python doesn't know:
# Which engine?
# Which database?
# Which settings?
# So first we configure the factory.

# Now write only ONE line: SessionLocal = sessionmaker(bind=engine)

# Why is it called SessionLocal?
# This is a very common naming convention in FastAPI and SQLAlchemy projects.
# It tells us: "This is the session factory for this application's local database."
# You could technically name it: banana = sessionmaker(bind=engine)
# and Python wouldn't complain. But nobody does that. Good names make code readable.


# Full file:

# import os
# from dotenv import load_dotenv
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# load_dotenv()
# DATABASE_URL = os.getenv("DATABASE_URL")
# if DATABASE_URL is None:
#     raise ValueError("DATABASE_URL is not set in the .env file.")
# engine = create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(
#     autocommit=False,
#     autoflush=False,
#     bind=engine
# )
# def get_db():
#     """
#     Provide a database session for each request.
#     """
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# This file does only four things:
# Reads the .env
# Creates the SQLAlchemy Engine
# Creates the Session Factory
# Provides get_db() so FastAPI can give each request its own database session and automatically close it afterward.

# Why autocommit=False -> We want to decide when data is saved.
# Example: db.add(url), db.commit()
# We control the commit ourselves. That's much safer.

# Why autoflush=False -> SQLAlchemy won't automatically send pending changes to the database before every query.

# Why yield -> This is FastAPI's dependency pattern.
# The flow is: Request comes in -> Create Session -> Use Session -> Request finishes -> Automatically close Session
# No memory leaks, No forgotten connections.








# Step 9 — Create main.py
# Just enough to verify the application runs.

# Example flow:
# Run FastAPI -> Open Swagger -> See API -> Done
# No routers yet.

# Now we're creating the entry point of our application.
# Think of main.py as the main gate of the project. Every request starts here.

# Later, it will send requests to: Client → main.py → Router → Service → Repository → Database
# But for now, main.py has only one responsibility: Start the FastAPI application.

# Create main.py:

# from fastapi import FastAPI
# app = FastAPI(
#     title="URL Shortener API",
#     version="1.0.0",
#     description="A URL Shortener API built with FastAPI and PostgreSQL."
# )
# @app.get("/")
# def root():
#     return {
#         "message": "Welcome to URL Shortener API 🚀"
#     }

# Let's Understand It

# 1. from fastapi import FastAPI
# Imports the FastAPI class. Without this, we can't create an API application.

# 2. app = FastAPI(...)
# This creates our application object.
# Think of it like: Flask → app = Flask(__name__)
# FastAPI → app = FastAPI() Everything (routes, middleware, docs) will attach to this app.

# 3. title= , version= , description =.
# These are metadata. They don't affect functionality.
# They appear in Swagger UI. Professional APIs usually fill these in.

# 4.@app.get("/")
# This is our first route.
# It means: GET request to "/" → Execute root()

# 5. return {"message": "Welcome to URL Shortener API 🚀"}
# FastAPI automatically converts the Python dictionary into JSON.
# Response: {"message": "Welcome to URL Shortener API 🚀"}
# No json.dumps() required.


# Now Let's Run It
# Open terminal inside the project.
# Run: python -m uvicorn main:app --reload
# Remember why we use: python -m uvicorn instead of uvicorn Because on Windows, sometimes uvicorn isn't added to PATH, while python -m uvicorn always works inside the active virtual environment.

# If everything is correct, you'll see something like: INFO: Uvicorn running on http://127.0.0.1:8000
# Now open: http://127.0.0.1:8000
# You should see: {"message": "Welcome to URL Shortener API 🚀"}

# Then open: http://127.0.0.1:8000/docs

# You should see Swagger UI with:
# URL Shortener API
# Version 1.0.0
# One endpoint: GET /

# ------------------- OR -----------------
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

# Then you can simply press the Run button in VS Code or execute: python main.py
# instead of: python -m uvicorn main:app --reload




# Step 10 — Verify Everything Works
# Start the server.
# Visit: http://127.0.0.1:8000/docs
# If Swagger opens successfully: backend foundation is complete.