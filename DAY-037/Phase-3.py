# Today's Roadmap

# We'll do this in order:
# STEP 1 → Understand what a Model is
# STEP 2 → Learn @dataclass
# STEP 3 → Build Character model
# STEP 4 → Build Question model
# STEP 5 → Repository Interface
# STEP 6 → JSON Repository
# STEP 7 → Read JSON
# STEP 8 → Convert JSON → Objects
# STEP 9 → Test from main.py



# STEP 1 — What is a Model?

# What is a Character?

# Is it a function -> No.
# Is it game logic -> No.
# It is data.
# Think about a student management system.

# A student has:
# ID
# Name
# Age
# Branch

# A bank application has:
# Account
# Balance
# Owner

# An Amazon application has:
# Product
# Price
# Stock

# Our game has: Character

# A Character is simply a container for information.
# For example:
# Name: Virat Kohli
# Category: Character
# Attributes:
# real
# alive
# male
# indian
# cricketer

# Why do we create a Character class?

# Imagine later you write:
# character.name
# instead of
# character["name"]

# Which is cleaner?
# The object approach.
# Professional Python projects almost always convert raw JSON into objects before using it.
# That's what we're going to learn.


# What should the Character object contain?

# The entire character into memory.
# Suppose characters.json contains:

{
    "id": 1,
    "name": "Virat Kohli",
    "category": "character",
    "attributes": {
        "real": True,
        "alive": True,
        "male": True,
        "indian": True,
        "cricketer": True
    }
}

# After loading it, the Character object should already contain everything:
# Character
# ----------
# id = 1
# name = "Virat Kohli"
# category = "character"
# attributes = {
#     "real": True,
#     "alive": True,
#     "male": True,
#     "indian": True,
#     "cricketer": True
# }

# So if later we write: character.name
# Python immediately returns: Virat Kohli

# It doesn't need to search the JSON again.
# Why is this better?
# Imagine we have 500 characters.
# If every time we needed the name we searched the JSON file again, it would be much slower.

# Instead, we:
# Read the JSON once.
# Convert it into Python objects.
# Work only with those objects.
# This is how many backend applications work.

# Think of it like this
# The JSON file is like a hard drive.
# The Character object is like RAM (memory).
# We load the data from disk into memory once, then work with it there because it's much faster.

# ✅ Correct Character Model Design
# Our Character object will contain:

# Character
# id
# name
# category
# attributes



# But when we were using a database like PostgreSQL.
# Then Character object contain the id and by help of it we get value for all names and attributes.

# characters table
# id | name
# -------------
# 1  | Virat Kohli
# Then the id is used to fetch the rest of the data from the database.


# 🎯 Day 37 — Step 1 Complete
# ✅ What a model is.
# ✅ Why we create a Character class.
# ✅ Why the object stores all its data.
# ✅ Why we load JSON only once.






# Day 37 — Step 2: Understanding @dataclass
# Goal: Understand why we use @dataclass, not just how.

# First, what problem does it solve?
# Imagine you create a normal Character class.
# Without @dataclass, you have to write everything yourself.

class Character:
    def __init__(self, id, name, category, attributes):
        self.id = id
        self.name = name
        self.category = category
        self.attributes = attributes

# Now suppose you want to print the object.
# character = Character(1, "Virat Kohli", "character", {})
# print(character)

# Output: <__main__.Character object at 0x000001A5C92F8D60>

# 😐 That's not useful.
# Now imagine you create 20 models.
# Character
# Question
# Animal
# Object
# GameState
# Player
# Answer
# Repository
# ...

# Every class needs:
# __init__()
# __repr__()
# __eq__()

# You'll keep writing the same code.
# Python developers noticed this repetition.

# So they introduced...
#  @dataclass
# A dataclass automatically creates this boilerplate code for you.

# Instead of writing:
class Character:
    def __init__(self, id, name, category, attributes):
        self.id = id
        self.name = name
        self.category = category
        self.attributes = attributes

# You simply write:
from dataclasses import dataclass
@dataclass
class Character:
    id: int
    name: str
    category: str
    attributes: dict

# That's it.
# Python generates the rest automatically.

# What does @ mean?
# This is an important question.
# Many beginners think: "Is @ some special syntax?"

# Actually...
# @dataclass is a decorator.

# Think of it like this:

# Character Class
        # │
        # ▼
# @dataclass
        # │
        # ▼
# Python automatically adds useful methods

# It's like upgrading your class.
# What methods does it create?

# Let's say we write:
# from dataclasses import dataclass
# @dataclass
# class Character:
    # id: int
    # name: str

# Python automatically creates:

# __init__()
# So you can do:

# character = Character(1, "Virat Kohli")
# without writing __init__() yourself.
# It also creates: __repr__()

# Now:
# print(character)
# prints: Character(id=1, name='Virat Kohli')
# instead of: <__main__.Character object at 0x000001A5C92F8D60>

# Much nicer.
# It also creates: __eq__()

# Meaning:
a = Character(1, "Virat Kohli")
b = Character(1, "Virat Kohli")

print(a == b)

# Output: True
# Without @dataclass, Python would compare memory addresses instead.
# Why do backend developers love dataclasses?
# Because many backend classes are just data containers.

# Examples:
# User
# Product
# Order
# Character
# Question
# Student
# Book
# Employee

# These classes mainly store data.
# Dataclasses reduce boilerplate.
# Will we always use dataclasses?
# No.

# Later, when we reach SQLAlchemy, you'll write:
# class Character(Base):

# instead of
# @dataclass

# because SQLAlchemy provides its own model system.
# But for Version 1 (JSON-based GuessWise), @dataclass is an excellent choice.

# Think like an engineer
# Ask yourself:

# Does my class mainly store data?
# If the answer is Yes, a dataclass is often a good fit.

# If the class has lots of behavior and complex logic, a regular class might be better.




# Step 3 Begins

# Now we're finally ready to write the first production code of GuessWise.

# We'll create:
# models/
    # character.py

# Before writing any code, we'll answer one more design question:

# What should the data types be?

# Think carefully.
# id = ?
# name = ?
# category = ?
# attributes = ?

# Should they be:

# id: int
# name: str
# category: str
# attributes: dict[str, bool]

# or something else?
# I want you to decide the types first. Once you answer that, we'll write your very first production-ready Python class together.



# try writing models/character.py yourself.

# Use this checklist instead of copying:

# Import dataclass.
# Create the Character class.
# Add the @dataclass decorator.
# Add four fields:
# id
# name
# category
# attributes
# Use the data types we discussed.

# Don't worry about docstrings, comments, or methods yet



# Why didn't we write
# def __init__(...)

# Because @dataclass secretly creates it for us.
# Imagine Python automatically generates:
# def __init__(self, id, name, category, attributes):
#     self.id = id
#     self.name = name
#     self.category = category
#     self.attributes = attributes

# You don't have to write it.
# That's the magic of dataclasses.

# models/character.py
from dataclasses import dataclass
@dataclass
class Character:
    id: int
    name: str
    category: str
    attributes: dict[str, bool]

# models/question.py
from dataclasses import dataclass
@dataclass
class Question:
    id: int
    text: str
    attribute: str

# If the answer is Yes, we keep that character.
# If the answer is No, we remove it.
# Everything connects beautifully.

# Important Design Lesson
# Notice our two models:

# Character:
# id
# name
# category
# attributes
# Stores facts.

# Question:
# id
# text
# attribute
# Stores questions.

# The Question object doesn't know anything about characters.
# The Character object doesn't know anything about questions.

# Who connects them?
# The Game Engine.
# This is called loose coupling.
# It's one of the most important ideas in backend engineering.



