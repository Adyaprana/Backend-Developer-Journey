# 🚀 Backend Developer Journey — Project 1 (URL Shortener API)

# Day 55 — Service Layer (Business Logic)

# Yesterday was a huge milestone.
# We proved that: Python Script → Repository → PostgreSQL
# works perfectly. Today we're building the brain of our application.


# Where should the short code be generated?
# Imagine this: https://google.com becomes aB9xQ2

# Where should that happen?
# Option A -> Router
# Option B -> Repository
# Option C -> Service

# Answer: Service 
# Why --> Because generating a short code is business logic.
# The Repository should only know: "Save this object."
# It should never know: "How do I generate a unique short code?"

# Think Like a Real Company
# Imagine tomorrow your manager says: "Instead of 6 characters, we want 8."
# Should you edit: Repository -> No.
# Should you edit: Router -> No.
# You only edit: Service
# because that's where the business rule lives.



# Responsibilities
# Let's lock these in.

# Router Responsible for:
# HTTP requests
# HTTP responses
# Validation

# Service Responsible for:
# Business rules
# Generating short codes
# Deciding what happens
# Calling repositories

# Repository Responsible for:
# Database CRUD
# SQLAlchemy
# PostgreSQL


# Application Flow
# This is now our architecture:
# Client → URLCreate (Schema) → Router → URLService → URLRepository → PostgreSQL
#                                               ↓
#                                      Business Logic
#                                               ↓
# Client ← URLResponse (Schema) ← URLService ← URLRepository ← PostgreSQL
# This is the flow we'll follow for the rest of the project.


# Today's Build Order
# Create URLService
#         ↓
# Generate Short Code
#         ↓
# Create SQLAlchemy Model
#         ↓
# Call Repository
#         ↓
# Return Saved Object





# Step 1 — Create the Service File
# Create: app/services/url_service.py





# Step 2 — Before Coding
# I want you to make one design decision. Our short codes will be random.
# Examples: Ab12Cd, xY9LmP, Qw8RtK, 

# Question: What characters should we allow?
# Option A -> abcdefghijklmnopqrstuvwxyz
# Option B -> ABCDEFGHIJKLMNOPQRSTUVWXYZ
# Option C -> 0123456789
# Option D -> All of the above

# Answer: Option D
# abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789
# Why -> More possible combinations.
# A 6-character code using 62 possible characters gives: 62^6 ≈ 56.8 billion combinations
# That's more than enough for Version 1.

# One More Design Question 
# How long should the short code be?
# We currently have: String(10) in the database.
# But that's the maximum length, not the required length.
# Should Version 1 generate:
# 6 characters?
# 8 characters?
# 10 characters?

# recommendation -> 6 characters.
# Reasons: Easy to type, Easy to share, 56+ billion possible combinations.
# Similar to many URL shorteners. If we ever need more, we can change one constant in the Service.


# Short Code Strategy — Version 1
# Algorithm: Random Generation
# Character Set: A-Z, a-z, 0-9
# Length: 6 Characters
# Possible Combinations: 62^6 ≈ 56.8 Billion

# Reason:
# ✔ Easy to type
# ✔ Easy to share
# ✔ Huge number of combinations
# ✔ Can be increased later if needed


# Today we're going to write our first real business logic.
# The Service will:

# Receive original_url
#         ↓
# Generate random 6-character code
#         ↓
# Create ShortenedURL model
#         ↓
# Call Repository
#         ↓
# Return saved object

# Notice something beautiful The Service doesn't know: SQL queries, HTTP requests.
# It only knows business rules. That's exactly how we wanted to design this project.


# Let's remember our architecture.
# Client → URLCreate (Schema) → Router → URLService → URLRepository → PostgreSQL
#                                        ↓
#                               Business Logic

# Today we're only building the URLService.

# What should the Service do?
# Our service has 4 responsibilities.

# Receive original_url
#         ↓
# Generate a random short code
#         ↓
# Create a ShortenedURL model
#         ↓
# Ask Repository to save it
# Notice something...
# The Service doesn't know SQL, The Service doesn't know HTTP, The Service only knows business rules.








# Step 1 — Create url_service.py
# Create:
# app/
# └── services/
#       └── url_service.py







# Step 2 — Write the Imports
# import random
# import string
# from sqlalchemy.orm import Session
# from app.models.shortened_url import ShortenedURL
# from app.repositories.url_repository import URLRepository

# Why these imports?

# random -> We'll randomly choose characters.
# Example: random.choice(...)

# string -> Python already gives us: string.ascii_letters
# which is: abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ and string.digits which is: 0123456789
# So instead of typing all 62 characters ourselves, Python already has them.

# Session -> The Service doesn't create sessions. It receives one.

# ShortenedURL -> Because the Service creates the database model.

# URLRepository -> Because the Service delegates saving to the Repository.





# Step 3 — Create the Class
# class URLService:
#     """
#     Handles business logic for URL shortening.
#     """





# Step 4 — Generate the Short Code
# Now the first business logic.

    # @staticmethod
    # def generate_short_code(length: int = 6) -> str:
    #     """
    #     Generate a random short code.
    #     """
    #     characters = string.ascii_letters + string.digits

    #     return "".join(
    #         random.choice(characters)
    #         for _ in range(length)
    #     )

# Let's Understand This
# This line: characters = string.ascii_letters + string.digits
# becomes: abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789
# Exactly what we decided. Then: random.choice(characters) means: Pick one random character.
# This part: for _ in range(length) means: Repeat 6 times.
# Then: "".join(...) joins them together.
# Example: a, B, 3, x, P, 7 -> aB3xP7


# Step 5 — Create the Main Business Method
# Now write:

    # def create_short_url(
    #     self,
    #     db: Session,
    #     original_url: str
    # ) -> ShortenedURL:
    #     """
    #     Create and save a shortened URL.
    #     """
    #     short_code = self.generate_short_code()
    #     url = ShortenedURL(
    #         original_url=original_url,
    #         short_code=short_code
    #     )
    #     repository = URLRepository()
    #     return repository.create(db, url)


# Receive original URL
#         ↓
# Generate a short code
#         ↓
# Create a ShortenedURL object
#         ↓
# Create a Repository
#         ↓
# Ask Repository to save it
#         ↓
# Return the saved object
# That's exactly what the Service should do.



# You found a bug in our current implementation before we even ran it. 
# Let's understand the problem Imagine this.
# Today we generate: Ab12Cd We save it.
# Database:
# original_url	short_code
# google.com	Ab12Cd
# Tomorrow another user shortens:
# github.com Our random generator again generates: Ab12Cd
# Now we have:
# original_url	short_code
# google.com	Ab12Cd
# github.com	Ab12Cd ❌
# Now imagine someone opens: ourdomain.com/Ab12Cd
# Which URL should it open? -> Google, GitHub
# Impossible. That's why: unique=True
# exists on short_code.
# What happens right now?
# Our database says:
# short_code = mapped_column(
#     String(10),
#     unique=True
# )
# If we accidentally generate the same code,
# PostgreSQL says: UNIQUE constraint violation
# The insert fails. So our application crashes. So yes...
# Our current service has a bug. And you found it before testing.
# That's exactly what happens in design reviews at software companies.
# How do real companies solve it?
# The flow becomes:
# Generate Code
#       ↓
# Ask Repository:
# "Does this code already exist?"
#       ↓
#         Yes ─────► Generate Again
#          │
#          No
#          │
#          ▼
# Save to Database

# Notice something. The Repository already knows how to search the database.
# The Service decides: "Keep generating until you find a unique one."
# Each layer keeps its responsibility. 

# Here's how we'll fix it We'll add one more repository method.
# def get_by_short_code(...)

# Flow:
# Generate Code
#       ↓
# Repository.get_by_short_code()
#       ↓
# Exists?
#       │
#  ┌────┴────┐
#  │         │
# Yes       No
#  │         │
# Generate   Save
# Again
# This is why architecture matters
# Notice how easy the fix is.
# We don't touch:
# Router ✅
# Schema ✅
# Database Model ✅

# We only add:
# Repository
# Service

# Exactly the two layers responsible for this. That's the benefit of clean architecture.

# Why shouldn't the Repository generate the short code?
# Answer: Because generating a short code is a business rule, not a database operation.
# The Repository should only perform CRUD operations.
# The Service decides: how the code is generated, how long it should be, whether it needs to be unique, and when to retry.
# The Repository simply answers questions like: "Does this short code already exist?"


# Recommendation: I actually want to change our plan a little.
# Instead of writing the "simple" URLService first and fixing it later...
# Let's build it correctly from the beginning.
# We'll implement:

# Generate Code
#       ↓
# Repository → Check Database
#       ↓
# Unique?
#       │
#  ┌────┴────┐
#  │         │
# No        Yes
#  │         │
# Generate   Save
# Again
# This adds maybe 10–15 lines of code, but now our URL Shortener won't have a hidden bug.


# "We have unique=True, but we also need a condition: if the generated code already exists, generate another one; otherwise, store it in the database."
# That's the complete solution.


# Our Final Flow This is what we'll implement:

# Receive Original URL
#         ↓
# Generate Random Code
#         ↓
# Repository → Check if Code Exists
#         ↓
# Exists?
#    ┌───────────┐
#    │           │
#  Yes          No
#    │           │
# Generate     Save to Database
# Another Code


# Notice the Responsibilities 

# Service Responsible for: Generate Code, Repeat Until Unique, Call Repository
# Repository Responsible for: Check Database, Save Data
# The Repository never says: "Generate another code."
# It simply answers: "Yes, this code exists." or "No, it doesn't."
# This is called Single Responsibility Principle (SRP).



# Another Thing The database still has: unique=True
# We should never remove it. Even after adding our check.
# Imagine this:
# User A → Generates Ab12Cd
# User B → Generates Ab12Cd
# Both check the database at the same time Both see "Code doesn't exist"
# Both try to insert Without the database constraint: Duplicate data could be stored.
# With: unique=True -> PostgreSQL guarantees that only one insert succeeds.
# This is called a database constraint, and it's the final safety net.

# So we'll have two layers of protection
# Application Layer: Generate Code → Check Exists → Generate Again if Needed
# This prevents most duplicates.

# Database Layer: UNIQUE Constraint
# This guarantees correctness, even if two requests happen at the same time.
# Professional systems usually have both.




# Real Companies Do This Too Think of it like entering a username on a website.
# When you type: john123
# The website immediately checks: "Is this username already taken?"
# If yes: Username already exists.
# But even after that check, the database still has a UNIQUE constraint on the username column.
# Why -> Because two people could click Register at the exact same moment.
# The application check improves the user experience. The database constraint guarantees correctness.


# Interview Question

# Q: If we already have unique=True, why do we still check in the Service before saving?
# Answer: Because the application check prevents most duplicate attempts and provides a better user experience by generating a new code before trying to save. However, the database UNIQUE constraint is still required as the final guarantee against race conditions or concurrent requests.

# Step 1 — Update the Repository
# First, our Repository needs a way to answer one question: "Does this short code already exist?"
# Add this method inside URLRepository:

# from typing import Optional
# def get_by_short_code(
#     self,
#     db: Session,
#     short_code: str
# ) -> Optional[ShortenedURL]:
#     """
#     Return a URL by its short code.
#     """
#     return (
#         db.query(ShortenedURL)
#         .filter(ShortenedURL.short_code == short_code)
#         .first()
#     )

# Responsibility The Repository doesn't decide anything.
# It simply answers: Question: Does "Ab12Cd" exist?
# Answer:
# ✔ Yes → Return ShortenedURL
# ❌ No → Return None
# That's it.


# Step 2 — Build the Service
# Now replace url_service.py with this:

# import random
# import string

# from sqlalchemy.orm import Session

# from app.models.shortened_url import ShortenedURL
# from app.repositories.url_repository import URLRepository


# class URLService:
#     """
#     Handles business logic for URL shortening.
#     """

#     CODE_LENGTH = 6

#     def __init__(self):
#         self.repository = URLRepository()

#     def generate_short_code(self) -> str:
#         """
#         Generate a unique short code.
#         """

#         characters = string.ascii_letters + string.digits

#         return "".join(
#             random.choice(characters)
#             for _ in range(self.CODE_LENGTH)
#         )

#     def create_short_url(
#         self,
#         db: Session,
#         original_url: str
#     ) -> ShortenedURL:

#         while True:

#             short_code = self.generate_short_code()

#             existing_url = self.repository.get_by_short_code(
#                 db,
#                 short_code
#             )

#             if existing_url is None:
#                 break

#         url = ShortenedURL(
#             original_url=original_url,
#             short_code=short_code
#         )

#         return self.repository.create(db, url)

# Let's Understand the Flow
# Receive URL
#       ↓
# Generate Code
#       ↓
# Repository → Check Database
#       ↓
# Exists?
#  ┌─────────────┐
#  │             │
# Yes           No
#  │             │
# Generate      Save
# Again
# This is now a correct Version 1 implementation.

# Why while True 
# Some people get scared seeing it. Here it's actually perfect. Flow:
# Generate -> Check Database -> Unique? -> Repeat if Not Unique -> Save if Unique
# The loop exits as soon as we find a unique code.
# Why CODE_LENGTH? Instead of: generate_short_code(6) everywhere,
# we have: CODE_LENGTH = 6 If tomorrow we decide: 6 → 8
# we change one line. That's called avoiding magic numbers.
# Architecture Review
# Our application now looks like this:

# Client -> URLCreate (Schema) -> Router -> URLService -> Generate Code -> URLRepository -> # Check Database -> Unique -> Save -> PostgreSQL -> URLResponse (Schema) -> Client


# Q1. What is Business Logic?
# Answer: Business logic is the set of rules that define how the application behaves.
# Example: Generate a short code, Ensure it is unique, Decide whether to retry.
# These are business rules, not database operations.


# Q2. Why is short code generation in the Service instead of the Repository?
# Answer: Generating a short code is a business rule. The Repository should only perform database operations like saving or retrieving data.

# Q3. Why do we check if a short code already exists?
# Answer: To avoid assigning the same short code to two different URLs.
# Even though the probability is low, duplicates are still possible with random generation.

# Q4. Why do we still keep unique=True in the database?
# Answer: Because application-level checks cannot prevent race conditions.
# The database constraint is the final guarantee that duplicate short codes cannot be stored.

# Q5. Why use a constant like CODE_LENGTH?
# Answer: It avoids magic numbers and makes future changes easier. If the required code length changes, only one value needs to be updated.



# Our backend now has a proper layered architecture:

# app/
# │
# ├── database/
# │     ├── base.py
# │     └── database.py
# │
# ├── models/
# │     └── shortened_url.py
# │
# ├── schemas/
# │     └── url.py
# │
# ├── repositories/
# │     └── url_repository.py
# │
# ├── services/
# │     └── url_service.py
# │
# ├── routers/        ← Empty (Tomorrow)
# │
# └── utils/


# 🎤 Interview Questions

# Q1. What is the Service Layer?
# Answer: # The Service layer contains business logic. It decides what should happen in the application and coordinates other layers like the Repository.

# Q2. What is the difference between Service and Repository?
# Answer:  Service → Business rules and application behavior.
#          Repository → Database operations.

# Q3. Why generate the short code in the Service?
# Answer: Because generating a short code is a business rule. The Repository should only handle data storage and retrieval.

# Q4. What is a race condition?
# Answer: A race condition occurs when two or more operations happen at nearly the same time and interfere with each other. In our project, two requests could generate the same short code before either one is saved, which is why the database's UNIQUE constraint is still necessary.

# Q5. Why avoid magic numbers?
# Answer: Magic numbers make code harder to maintain. Using a named constant like CODE_LENGTH makes the purpose clear and allows changes in one place.