
# ✅ 1. Game Menu

# --------CLI--------------
# ===== GuessWise =====

# 1 Character
# 2 Animal
# 3 Object
# 4 Movie
# 5 Place
# 6 Exit

# This keeps the search space smaller and makes the game faster.



# ✅ 2. Character Questions

# Character
#       │
#       ▼
# Real ?
#       │
#  ┌────┴────┐
#  │         │
# Yes        No
#  │         │
# Alive?   Fictional
#  │
# Dead?
#  │
# Profession?
#  │
# Country?
#  │
# Political Party?
#  │
# Prime Minister?

# Excellent thinking.
# This is actually similar to a decision tree, which Akinator-like games use.
# Later we'll make the engine smart enough to choose the best next question.




# ✅ 3. Why Game Shouldn't Read JSON

# when i migrate to sql we not need to change game part only the repository part game logic will be same always
# That is called Separation of Concerns.
# Game
#    │
# Repository
#    │
# JSON

# Later becomes
# Game
#    │
# Repository
#    │
# PostgreSQL

# Game doesn't care.
# This is professional architecture.






#  ✅ 4. Character JSON

# Instead of making every property a top-level key, group them together.
[
  {
    "id": 1,
    "name": "Virat Kohli",
    "category": "character",
    "properties": {
      "real": True,
      "male": True,
      "alive": True,
      "indian": True,
      "cricketer": True,
      "married": True
    }
  }
]
# Later in PostgreSQL, it becomes:
# characters
# -----------
# id
# name
# category

# and
# character_properties
# --------------------
# character_id
# property
# value

# OR
# questions
# ---------
# id
# question
# property
# Notice how our design already thinks about SQL.


# Questions JSON --> 
[
    {
        "id":1,
        "question":"Is your character real?",
        "property":"real"
    },
    {
        "id":2,
        "question":"Is your character male?",
        "property":"male"
    }
]

# Even Better (Future-Proof)
# Eventually we may want five answers.

# YES
# NO
# PROBABLY
# PROBABLY NOT
# DON'T KNOW

# So later our JSON could evolve into:
{
    "id":1,
    "text":"Is your character real?",
    "property":"real",
    "type":"boolean"
}

# or

{
    "id":15,
    "text":"What continent is your character from?",
    "property":"continent",
    "type":"choice"
}
# Now our engine can support different question types.





# The Character object only contain properties (facts), and the Question object maps a question to one property

# Character
#     │
#     └── properties
#          ├── real = true
#          ├── indian = true
#          └── cricketer = true
# Question
#     │
#     ├── "Is your character real?"
#     └── property = "real"

# A Character represents data, not questions
# Character
# ---------
# Name : Virat Kohli
# Properties:
# - real
# - indian
# - male
# - cricketer
# - alive
# It should never know how those facts are asked to the user.

# Question object maps one question to one property.
# Question
# ---------
# Question : Is your character real?
# Property : real
# The engine asks the question.
# If the answer is "Yes", it filters characters where:
# real = True

# This is called Separation of Data and Behavior.



# AFTER BOTH Phase:
# ✅ Day 36 Status

# Here's everything i planned for Day 36:

# ✅ Project initialized
# ✅ Folder structure created
# ✅ Virtual environment created
# ✅ Documentation started
# ✅ High-level architecture designed
# ✅ Repository pattern decided
# ✅ Data flow designed
# ✅ Character model concept designed
# ✅ Question model concept designed
# ✅ JSON design discussed
# ✅ PostgreSQL migration strategy planned
# 🎉 Day 36 is officially complete.

# This is a milestone because you've finished the planning and design phase before writing implementation code.