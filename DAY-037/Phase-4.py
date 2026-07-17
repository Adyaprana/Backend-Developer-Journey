# The Repository Pattern.
# Repository have the access of the data. The game should not know where the data comes from. It also helps us migrate the database without changing the game logic.



# Imagine This
# Suppose today your project looks like this:

# Game
#  │
#  ▼
# JSON File
# So the Game directly does: open("characters.json")

# Everything works.
# Six months later your says: "This shoud moving to PostgreSQL."

# Now every place that reads JSON has to change.

# Maybe:
# game.py
# question_engine.py
# character_engine.py
# admin.py

# Everything breaks.
# Big problem.



# Instead we build this
    #             Game
    #               │
    #               ▼
    #         Repository
    #          /       \
    #         /         \
    #  JSON Repository   PostgreSQL Repository

# Now the Game says: repository.get_characters()
# The Game doesn't care if the repository reads from: JSON, SQLite, PostgreSQL, MongoDB, API, Cloud
# It doesn't matter.

# Think of a Mobile Charger
# The phone doesn't know if electricity comes from: Wall Socket, Power Bank, Laptop USB, Car Charger
# It only knows: USB Cable
# The USB cable is the interface.
# The repository is exactly like that.



# We have:
# repository/
# │
# ├── repository.py
# └── json_repository.py
# What is the difference?

# repository.py
# This is NOT the JSON repository.
# This is NOT PostgreSQL.
# It only says: "Any repository must provide these methods."

# Like a contract. 
# Imagine I say: Every bird must fly.
# I'm not talking about an eagle.
# I'm not talking about a sparrow.
# I'm talking about all birds.
# The repository is the same idea.

# So...
# What methods should every repository have?
# Think about our game.
# What does the Game need?

# Maybe: Load Characters
# Maybe: Load Questions
# Later: Save Characters
# Later: Save Questions
# Maybe: Add Character
# Maybe: Delete Character
# Maybe: Update Character



# JSON Repository

# This one actually writes: 
open("characters.json")
# PostgreSQL Repository
# This one actually writes:
# SELECT *
# FROM characters;
# Notice Something Amazing

# The Game still writes:
# repository.get_characters()

# Exactly the same code.
# Nothing changes.

# This is called Abstraction

# The Game only knows:
# Repository It never knows JSON or PostgreSQL


# For now:
# The Game needs:
# Game
#  │
#  ▼
# Repository
#  │
#  ├── Give me all characters
#  └── Give me all questions

# That's it.
# The game is read-only.

# It never:
# Adds a character 
# Deletes a character 
# Updates a character 

# What Should i use load_ or get_?
# This is a good design discussion.

# Option 1:
# load_characters()
# load_questions()

# Option 2:
# get_characters()
# get_questions()

# # I recommend:

# get_characters()
# get_questions()

# Because from the Game's perspective:
# characters = repository.get_characters()

# reads naturally.
# The Game doesn't care how they're loaded.

# Maybe they're:
# Read from JSON
# Read from PostgreSQL
# Read from Redis
# Cached in memory
# The Game simply says: "Give me the characters."


# Version 1 Repository Interface

# So our interface becomes: Repository
# get_characters()
# get_questions()

# Very small.
# Very clean.
# Very professional.


# Why not more methods?

# Repository
# get_characters()
# get_questions()
# save_characters()
# save_questions()
# delete()
# update()
# insert()
# find()
# ...
# before they even need them. This is called over-engineering. Professional developers avoid it.



# repository/repository.py
from abc import ABC, abstractmethod

# from models.character import Character
# from models.question import Question


# class Repository(ABC):

#     @abstractmethod
#     def get_characters(self) -> list[Character]:
#         pass

#     @abstractmethod
#     def get_questions(self) -> list[Question]:
#         pass

# What is ABC?
# It means: This class is only a blueprint.
# Nobody should create: Repository()
# Instead they'll create: JsonRepository() Later PostgresRepository()


# What is @abstractmethod?
# It says: Every repository must have this method.
# So JSON Repository must implement:
# get_characters() and get_questions()
# Later PostgreSQL Repository must also implement the same methods.


# repository/
#     json_repository.py

# Its job is only to read data from JSON files.
# Nothing else.

# import json
# from models.character import Character
# from models.question import Question
# from repository.repository import Repository
# class JsonRepository(Repository):

#     def get_characters(self) -> list[Character]:
#         with open("data/characters.json", "r") as file:

#     def get_questions(self) -> list[Question]:
#         pass

# When we call: repository.get_characters()

# It should:
# Open JSON
#     ↓
# Read JSON
#     ↓
# Convert into Character objects
#     ↓
# Return list[Character]

# Step 1 - What does json.load() return?

# Suppose your characters.json is:
# [
#     {
#         "id": 1,
#         "name": "Virat Kohli",
#         "category": "character",
#         "attributes": {
#             "real": true,
#             "male": true
#         }
#     },
#     {
#         "id": 2,
#         "name": "Lion",
#         "category": "animal",
#         "attributes": {
#             "real": true,
#             "male": true
#         }
#     }
# ]

# When you do: data = json.load(file)
# data becomes:
# [
#     {...},
#     {...}
# ]
# Not one dictionary-> A list of dictionaries.

# Step 2 - How do we visit every dictionary?
# You've already learned this in Python.
# for item in data:

# First iteration:
# item =
# {
#     "id":1,
#     "name":"Virat Kohli",
#     ...
# }

# Second iteration:
# item =
# {
#     "id":2,
#     "name":"Lion",
#     ...
# }
# Now we have one dictionary at a time.

# Step 3 - Convert ONE dictionary
# We already learned this.
# character = Character(**item)
# Now character is no longer a dictionary.
# It is a real object.

# Step 4 - Where do we keep all the objects?
# If we have:
# Virat Kohli
# Lion
# Spider-Man
# Batman
# Should we overwrite the variable every time?
# character = ...
# No.
# We need a list.
# So first create:
# characters = []

# Step 5 - Add every object
# You've already learned lists.
# characters.append(character)

# Step 6 - Finally return them
# At the end:
# return characters

# Put it together
# Now look at the complete flow.

# data = json.load(file)
# characters = []
# for item in data:
#     character = Character(**item)
#     characters.append(character)
# return characters




# import json

# from models.character import Character
# from models.question import Question
# from repository.repository import Repository

# class JsonRepository(Repository):

#     def get_characters(self) -> list[Character]:
#         with open("data/characters.json", "r") as file:
#             data = json.load(file)
#             characters = []
#             for item in data:
#                 character = Character(**item)
#                 characters.append(character)
#             return characters
            
#     def get_questions(self) -> list[Question]:
#         with open("data/questions.json", "r") as file:
#             data = json.load(file)
#             questions = []
#             for item in data:
#                 question = Question(**item)
#                 questions.append(question)
#             return questions



# Main.py -->

# Create a JsonRepository
# Load all characters
# Load all questions
# Print them

# Step 1 — Import the Repository
# First, import your repository.
# file is located here:
# repository/
#     json_repository.py
# Inside it, the class is:
# class JsonRepository
# (Hint: It's similar to how you imported Character.)

# Step 2 — Create an Object
# After importing: repository = JsonRepository()

# Question: Why do we write: JsonRepository() instead of Repository()
# Answer: Because Repository is only the blueprint (interface).

# JsonRepository is the actual implementation.

# Step 3 — Load Characters
# Now ask the repository: characters = repository.get_characters()
# Notice how nice this reads.
# main.py doesn't know anything about JSON.

# It simply asks: "Repository, give me the characters."
# That's clean architecture.

# Step 4 — Print Them
# For now, just do:
# print(characters)

# Because Character is a dataclass, Python will print something like:
# [
#     Character(
#         id=1,
#         name='Virat Kohli',
#         ...
#     )
# ]

# Much better than raw dictionaries.

# Step 5 — Do the Same for Questions
# Exactly the same: questions = repository.get_questions()
# Then: print(questions)


# This is the first time the project has a real entry point (main.py).

# from repository.json_repository import JsonRepository
# repository = JsonRepository()
# characters = repository.get_characters()
# print(characters)
# questions = repository.get_questions()
# print(questions)

# Code Review
# Import -> from repository.json_repository import JsonRepository
# Create Repository -> repository = JsonRepository()
# Get Characters -> characters = repository.get_characters()
# Print -> print(characters)

# main.py
#    │
#    ▼
# JsonRepository()
#    │
#    ▼
# Open characters.json
#    │
#    ▼
# json.load()
#    │
#    ▼
# Python Dictionary
#    │
#    ▼
# Character(**item)
#    │
#    ▼
# Character Object
#    │
#    ▼
# Return list[Character]
#    │
#    ▼
# print()


# Day 37
# | Task                        | Status |
# | --------------------------- | ------ |
# | Learn `@dataclass`          | ✅ Done |
# | Create `Character` model    | ✅ Done |
# | Create `Question` model     | ✅ Done |
# | Create Repository Interface | ✅ Done |
# | Create JSON Repository      | ✅ Done |
# | Read JSON files             | ✅ Done |
# | Convert JSON → Objects      | ✅ Done |
# | Test from `main.py`         | ✅ Done |


