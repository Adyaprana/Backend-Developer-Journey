# DAY 37 — GuessWise: Models, Repository Pattern + LeetCode Prefix Sum

> **Project:** GuessWise — Data Access Layer Complete
>
> **Path:** `C:\A_MY THINGS\001\Backend-Developer-Journey\Project\GuessWise`
>
> **LeetCode:** #724 Find Pivot Index ✅ (Prefix Sum pattern)
>
> **Status:** ✅ Day 37 Complete — Data layer working, first real code written

---

# 🎯 What Was Built Today

```
✅ Character model using @dataclass
✅ Question model using @dataclass
✅ Repository Interface (Abstract Base Class)
✅ JsonRepository implementation
✅ characters.json + questions.json populated
✅ JSON → Python Objects working
✅ Tested from main.py
✅ LeetCode #724 solved (Brute Force + Prefix Sum)
```

---

# 📁 Project State After Day 37

```
GuessWise/
│
├── main.py                      ← Entry point — loads and prints data
│
├── models/
│   ├── __init__.py
│   ├── character.py             ← ✅ Written today
│   └── question.py              ← ✅ Written today
│
├── repository/
│   ├── __init__.py
│   ├── repository.py            ← ✅ Written today (abstract interface)
│   └── json_repository.py      ← ✅ Written today (JSON implementation)
│
└── data/
    ├── characters.json          ← ✅ Populated today
    └── questions.json           ← ✅ Populated today
```

---

# SECTION 1 — WHAT IS A MODEL?

## The Core Concept

A **model** is simply a data container — a Python class that represents a real-world thing.

```
Bank app:      Account (id, owner, balance)
School app:    Student (id, name, age, branch)
Amazon app:    Product (id, name, price, stock)
GuessWise:     Character (id, name, category, attributes)
```

A model is **not** game logic. It is **not** a database query. It just holds information.

## Why Not Just Use a Dictionary?

```python
# Dictionary approach:
character = {
    "id": 1,
    "name": "Virat Kohli",
    "category": "character",
    "attributes": {"real": True, "indian": True}
}

# Access: character["name"]
# Typo risk: character["naem"]  → KeyError (caught only at runtime)
# No autocomplete in VS Code
# No type hints

# Object approach:
character = Character(id=1, name="Virat Kohli", ...)
# Access: character.name
# Typo risk: character.naem  → AttributeError (caught at runtime)
# Autocomplete works in VS Code
# Type hints enforced
```

Professional Python projects always convert raw JSON into objects before using it. It makes the code safer, more readable, and easier to maintain.

## The Memory Model

```
JSON file = Hard drive (slow, permanent storage)
Character object = RAM (fast, in-memory)

Load JSON once → Create objects → Work only with objects

500 characters in memory ≈ few KB
Reading JSON file 500 times = unnecessary disk I/O
```

---

# SECTION 2 — @dataclass EXPLAINED

## The Problem It Solves

Without `@dataclass`, every model class needs repetitive boilerplate:

```python
# WITHOUT @dataclass — lots of manual work
class Character:
    def __init__(self, id, name, category, attributes):
        self.id = id
        self.name = name
        self.category = category
        self.attributes = attributes

    def __repr__(self):
        return f"Character(id={self.id}, name={self.name}, ...)"

    def __eq__(self, other):
        return (self.id == other.id and
                self.name == other.name and
                self.category == other.category)
```

For 10 models (Character, Question, Animal, GameState, Player...) that's 30+ methods of identical boilerplate.

## The Solution

```python
# WITH @dataclass — Python generates everything automatically
from dataclasses import dataclass

@dataclass
class Character:
    id: int
    name: str
    category: str
    attributes: dict[str, bool]

# Python automatically creates:
# __init__()     → so you can write Character(1, "Virat", ...)
# __repr__()     → so print(character) shows readable output
# __eq__()       → so character1 == character2 compares values
```

## What @dataclass Actually Is

`@dataclass` is a **decorator** — a function that upgrades your class.

```
Your Character class
        │
        ▼
   @dataclass runs
        │
        ▼
Python adds __init__, __repr__, __eq__
        │
        ▼
Upgraded Character class (with all methods)
```

Think of it as a class supercharger. You define the fields; Python generates the plumbing.

## What Python Generates

```python
from dataclasses import dataclass

@dataclass
class Character:
    id: int
    name: str
    category: str
    attributes: dict[str, bool]

# Python secretly creates this (you never see it, but it exists):
# def __init__(self, id: int, name: str, category: str, attributes: dict):
#     self.id = id
#     self.name = name
#     self.category = category
#     self.attributes = attributes
#
# def __repr__(self):
#     return f"Character(id={self.id!r}, name={self.name!r}, ...)"
#
# def __eq__(self, other):
#     if not isinstance(other, Character):
#         return NotImplemented
#     return (self.id, self.name, self.category, self.attributes) == \
#            (other.id, other.name, other.category, other.attributes)

# Usage:
c = Character(1, "Virat Kohli", "character", {"real": True})
print(c)
# Character(id=1, name='Virat Kohli', category='character', attributes={'real': True})

a = Character(1, "Virat Kohli", "character", {"real": True})
b = Character(1, "Virat Kohli", "character", {"real": True})
print(a == b)   # True (compares values, not memory addresses)
```

---

# SECTION 3 — THE MODELS

## models/character.py

```python
from dataclasses import dataclass


@dataclass
class Character:
    id: int
    name: str
    category: str
    attributes: dict[str, bool]
```

**Design decisions:**

```
id: int
  → Unique identifier. Integer for JSON version.
  → In PostgreSQL version: will be SERIAL PRIMARY KEY.

name: str
  → Character's name. String.

category: str
  → "character", "animal", "object", "movie", "place"
  → Keeps search space small.

attributes: dict[str, bool]
  → All facts about this character.
  → Keys: "real", "male", "indian", "cricketer", etc.
  → Values: True or False only.
  → dict[str, bool] = dictionary with string keys and boolean values
```

**Why attributes as a dict, not flat fields?**

```python
# FLAT (bad for future migrations):
@dataclass
class Character:
    id: int
    name: str
    real: bool
    male: bool
    indian: bool
    cricketer: bool
    # Adding new attribute = changing the class = breaking everything

# NESTED (good for future migrations):
@dataclass
class Character:
    id: int
    name: str
    attributes: dict[str, bool]
    # Adding new attribute = just add a key to the dict
    # Class never changes
    # PostgreSQL migration: character_properties (character_id, key, value)
```

---

## models/question.py

```python
from dataclasses import dataclass


@dataclass
class Question:
    id: int
    text: str
    attribute: str
```

**Design decisions:**

```
id: int
  → Unique identifier.

text: str
  → The question shown to the user.
  → "Is your character real?"

attribute: str
  → The key this question targets in Character.attributes.
  → "real" → looks up character.attributes["real"]
  → This is how Question connects to Character — through the key.
```

**How Question and Character connect (through the engine, not directly):**

```
Question:  text="Is your character real?",  attribute="real"
                                                   │
                        ┌──────────────────────────┘
                        │
Character.attributes:  {"real": True, "male": True, "indian": True}
                              ↑
                    attribute = "real" → look up this key
                    value = True → character IS real

User answers "yes":
  Keep characters where attributes["real"] == True

User answers "no":
  Keep characters where attributes["real"] == False
```

**Important design principle:**

```
Character knows nothing about questions.
Question knows nothing about characters.
They are connected only by the string key (attribute name).

This is called LOOSE COUPLING — one of the most important
principles in backend engineering.
```

---

# SECTION 4 — THE REPOSITORY PATTERN

## Why the Game Must NOT Read JSON Directly

```python
# BAD — tightly coupled
class Game:
    def start(self):
        with open("data/characters.json") as f:   # ← JSON in game logic
            self.characters = json.load(f)

# What happens on Day 40 when we switch to PostgreSQL?
# Open game.py → find all json.load() calls → rewrite them
# Risk: break game logic while changing data layer
# Might also need to change question_engine.py, character_engine.py...
# Hours of bug-fixing


# GOOD — loosely coupled (Repository Pattern)
class Game:
    def __init__(self, repository):
        self.characters = repository.get_characters()  # ← game doesn't know WHERE

# Day 40: switch to PostgreSQL
# Change one line in main.py: repository = PostgresRepository()
# Game.py → untouched
# character_engine.py → untouched
# question_engine.py → untouched
# 10 minutes, not 3 hours
```

## The Repository as a USB Cable

```
Phone (Game) doesn't know or care about electricity source.
Phone only knows: USB port (Repository interface).

Wall socket    → USB cable → Phone
Power bank     → USB cable → Phone
Car charger    → USB cable → Phone

JSON file      → Repository → Game
SQLite         → Repository → Game
PostgreSQL     → Repository → Game
MongoDB        → Repository → Game

The Game always says: repository.get_characters()
It never knows what's behind the repository.
```

## repository/repository.py (The Contract)

```python
from abc import ABC, abstractmethod

from models.character import Character
from models.question import Question


class Repository(ABC):

    @abstractmethod
    def get_characters(self) -> list[Character]:
        pass

    @abstractmethod
    def get_questions(self) -> list[Question]:
        pass
```

**What is ABC?**

```
ABC = Abstract Base Class
It means: "This class is a template, not an implementation."
You CANNOT do: repository = Repository()  → TypeError

You CAN do:
  repository = JsonRepository()      ← concrete implementation
  repository = PostgresRepository()  ← concrete implementation
```

**What is @abstractmethod?**

```
It means: "Every subclass MUST implement this method."
If JsonRepository forgets to implement get_characters():
  → TypeError at class definition time
  → Python catches the mistake immediately
  → Not at runtime when game is running
```

**Why `get_` not `load_`?**

```
load_characters() suggests the caller cares HOW data is retrieved.
get_characters()  says "give me characters" — implementation detail irrelevant.

From Game's perspective: "I need characters, I don't care where they come from."
get_ is the cleaner naming convention.
```

---

## repository/json_repository.py (The Implementation)

```python
import json

from models.character import Character
from models.question import Question
from repository.repository import Repository


class JsonRepository(Repository):

    def get_characters(self) -> list[Character]:
        with open("data/characters.json", "r") as file:
            data = json.load(file)

        characters: list[Character] = []

        for item in data:
            character = Character(**item)
            characters.append(character)

        return characters

    def get_questions(self) -> list[Question]:
        with open("data/questions.json", "r") as file:
            data = json.load(file)

        questions: list[Question] = []

        for item in data:
            question = Question(**item)
            questions.append(question)

        return questions
```

**The magic of `Character(**item)`:**

```python
# item from JSON:
item = {
    "id": 1,
    "name": "Virat Kohli",
    "category": "character",
    "attributes": {"real": True, "male": True}
}

# Character(**item) is equivalent to:
Character(id=1, name="Virat Kohli", category="character", attributes={"real": True, "male": True})

# ** unpacks the dictionary into keyword arguments.
# The keys must match the @dataclass field names exactly.
# This is why our JSON keys are: id, name, category, attributes
# (Same names as in the dataclass definition)
```

**Complete data flow:**

```
main.py calls: repository.get_characters()
                        │
                        ▼
        open("data/characters.json")
                        │
                        ▼
           data = json.load(file)
           # data is a list of dicts
                        │
                        ▼
              for item in data:
              # item is one dict
                        │
                        ▼
            character = Character(**item)
            # dict → typed Python object
                        │
                        ▼
         characters.append(character)
                        │
                        ▼
           return characters
           # list[Character] returned
                        │
                        ▼
   main.py has: [Character(...), Character(...), ...]
```

---

# SECTION 5 — DATA FILES

## data/characters.json

```json
[
    {
        "id": 1,
        "name": "Virat Kohli",
        "category": "character",
        "attributes": {
            "real": true,
            "alive": true,
            "male": true,
            "indian": true,
            "cricketer": true,
            "actor": false,
            "musician": false,
            "fictional": false
        }
    },
    {
        "id": 2,
        "name": "Naruto",
        "category": "character",
        "attributes": {
            "real": false,
            "alive": true,
            "male": true,
            "indian": false,
            "cricketer": false,
            "actor": false,
            "musician": false,
            "fictional": true
        }
    },
    {
        "id": 3,
        "name": "A.R. Rahman",
        "category": "character",
        "attributes": {
            "real": true,
            "alive": true,
            "male": true,
            "indian": true,
            "cricketer": false,
            "actor": false,
            "musician": true,
            "fictional": false
        }
    },
    {
        "id": 4,
        "name": "Hermione Granger",
        "category": "character",
        "attributes": {
            "real": false,
            "alive": true,
            "male": false,
            "indian": false,
            "cricketer": false,
            "actor": false,
            "musician": false,
            "fictional": true
        }
    },
    {
        "id": 5,
        "name": "Priyanka Chopra",
        "category": "character",
        "attributes": {
            "real": true,
            "alive": true,
            "male": false,
            "indian": true,
            "cricketer": false,
            "actor": true,
            "musician": false,
            "fictional": false
        }
    }
]
```

## data/questions.json

```json
[
    {
        "id": 1,
        "text": "Is your character a real person?",
        "attribute": "real"
    },
    {
        "id": 2,
        "text": "Is your character male?",
        "attribute": "male"
    },
    {
        "id": 3,
        "text": "Is your character still alive?",
        "attribute": "alive"
    },
    {
        "id": 4,
        "text": "Is your character Indian?",
        "attribute": "indian"
    },
    {
        "id": 5,
        "text": "Is your character a cricketer?",
        "attribute": "cricketer"
    },
    {
        "id": 6,
        "text": "Is your character an actor?",
        "attribute": "actor"
    },
    {
        "id": 7,
        "text": "Is your character a musician?",
        "attribute": "musician"
    },
    {
        "id": 8,
        "text": "Is your character fictional?",
        "attribute": "fictional"
    }
]
```

---

# SECTION 6 — MAIN.PY (TESTING THE DATA LAYER)

```python
from repository.json_repository import JsonRepository

repository = JsonRepository()

characters = repository.get_characters()
questions  = repository.get_questions()

print("Characters:")
for character in characters:
    print(character)

print("\nQuestions:")
for question in questions:
    print(question)
```

**Expected output:**

```
Characters:
Character(id=1, name='Virat Kohli', category='character', attributes={'real': True, 'alive': True, 'male': True, 'indian': True, 'cricketer': True, 'actor': False, 'musician': False, 'fictional': False})
Character(id=2, name='Naruto', category='character', attributes={...})
Character(id=3, name='A.R. Rahman', category='character', attributes={...})
Character(id=4, name='Hermione Granger', category='character', attributes={...})
Character(id=5, name='Priyanka Chopra', category='character', attributes={...})

Questions:
Question(id=1, text='Is your character a real person?', attribute='real')
Question(id=2, text='Is your character male?', attribute='male')
...
```

**This output confirms:**

```
✅ JSON is being read correctly
✅ Dictionaries are being converted to typed Python objects
✅ @dataclass __repr__ shows readable output
✅ The data layer works independently of game logic
✅ Architecture is clean — main.py knows nothing about JSON internals
```

---

# SECTION 7 — KEY CONCEPTS LEARNED TODAY

## @dataclass

```python
from dataclasses import dataclass

@dataclass
class Character:
    id: int
    name: str
    category: str
    attributes: dict[str, bool]

# Auto-generates: __init__, __repr__, __eq__
# Reduces boilerplate significantly
# Standard Python for data container classes
```

## Abstract Base Class (ABC)

```python
from abc import ABC, abstractmethod

class Repository(ABC):        # Cannot be instantiated directly
    @abstractmethod
    def get_characters(self): # Must be implemented by subclasses
        pass
```

## **kwargs unpacking

```python
item = {"id": 1, "name": "Virat", "category": "character", "attributes": {}}
character = Character(**item)
# Equivalent to: Character(id=1, name="Virat", category="character", attributes={})
```

## Type Hints

```python
def get_characters(self) -> list[Character]:
    characters: list[Character] = []
    ...
    return characters
```

## Separation of Concerns

```
models/       → WHAT data looks like (structure)
repository/   → WHERE data comes from (access)
game.py       → WHAT the game does (logic)
main.py       → WHERE it all starts (entry point)
```

---

# SECTION 8 — LEET CODE #724: FIND PIVOT INDEX

## Problem

Find the pivot index — where left sum equals right sum (pivot element excluded from both).

```
[1, 7, 3, 6, 5, 6]
         ↑
    index 3 is pivot

Left:  1 + 7 + 3 = 11
Right: 5 + 6 = 11
```

## Brute Force — O(n²)

```python
class Solution(object):
    def pivotIndex(self, nums):
        for i in range(len(nums)):
            l_sum = sum(nums[:i])       # Recalculate left from scratch
            r_sum = sum(nums[i + 1:])   # Recalculate right from scratch
            if l_sum == r_sum:
                return i
        return -1
```

**Why it's slow:**

```
For each index, sum() scans the entire left and right subarrays.
At index 3: left sum recalculates 1+7+3 (already computed before)
At index 4: left sum recalculates 1+7+3+6 (one more element)

Repeated work. O(n) work × O(n) iterations = O(n²) total.
```

## Prefix Sum — O(n) ✅ Submitted

```python
class Solution(object):
    def pivotIndex(self, nums):
        l_sum = 0
        r_sum = sum(nums)         # Total sum = initial right sum

        for i in range(len(nums)):
            r_sum -= nums[i]      # Remove pivot from right
            if l_sum == r_sum:    # Check if balanced
                return i
            l_sum += nums[i]      # Move pivot to left

        return -1
```

**Why order matters:**

```
WRONG order:
  l_sum += nums[i]   ← add pivot to left first
  r_sum -= nums[i]   ← then remove from right
  if l_sum == r_sum  ← pivot is now in LEFT, not excluded!

CORRECT order:
  r_sum -= nums[i]   ← remove pivot from right first (now excluded)
  if l_sum == r_sum  ← pivot is in neither sum (correct!)
  l_sum += nums[i]   ← move pivot to left for NEXT iteration
```

**Dry run:**

```
nums = [1, 7, 3, 6, 5, 6]
total = 28

i=0: r=28-1=27, l=0  → 0≠27 → l=1
i=1: r=27-7=20, l=1  → 1≠20 → l=8
i=2: r=20-3=17, l=8  → 8≠17 → l=11
i=3: r=17-6=11, l=11 → 11==11 → return 3 ✅
```

## Prefix Sum Pattern — Why It Matters

```
This pattern appears everywhere in interviews:

LeetCode #560  — Subarray Sum Equals K
LeetCode #303  — Range Sum Query
LeetCode #1480 — Running Sum of 1D Array
LeetCode #238  — Product of Array Except Self

The key insight is always the same:
  Instead of recalculating from scratch,
  maintain a running value and update it incrementally.
```

**Submitted:** ✅ Accepted | 747/747 test cases | Runtime: 7ms | Memory: 13.24MB

---

# SECTION 9 — ARCHITECTURE AFTER DAY 37

```
main.py
    │
    ▼ creates
JsonRepository (implements Repository interface)
    │
    ▼ reads
characters.json / questions.json
    │
    ▼ converts
Character objects / Question objects (via @dataclass + **kwargs)
    │
    ▼ returns
list[Character] / list[Question]
    │
    ▼ received by
main.py (prints them for now, game will use them from Day 38)
```

**What's NOT in this layer:**

```
❌ No game logic in repository
❌ No JSON reading in game logic
❌ No printing in repository
❌ No business decisions anywhere except game.py (coming Day 38)
```

---

# ✅ Day 37 Task Summary

| Task | Status |
|------|--------|
| Understand what a model is | ✅ Done |
| Learn `@dataclass` deeply | ✅ Done |
| Create `Character` model | ✅ Done |
| Create `Question` model | ✅ Done |
| Create Repository Interface (ABC) | ✅ Done |
| Create JSON Repository | ✅ Done |
| Populate characters.json | ✅ Done |
| Populate questions.json | ✅ Done |
| Test from `main.py` | ✅ Done |
| LeetCode #724 Brute Force | ✅ Done |
| LeetCode #724 Prefix Sum | ✅ Accepted (7ms) |

---

# 📅 What's Coming: Day 38

Tomorrow the **game logic** begins.

```
Day 38 goals:

1. CharacterEngine (engines/character_engine.py)
   - Store remaining characters
   - filter(attribute, answer) → removes non-matching characters
   - count() → how many characters remain
   - guess() → returns the last remaining character

2. QuestionEngine (engines/question_engine.py)
   - Store questions list
   - next_question() → returns next question or None
   - validate_answer() → checks if input is y/n

3. Game loop (game.py)
   - Load characters + questions via repository
   - Loop: ask question → filter characters
   - Stop when 1 character remains → guess
   - Handle: no characters left, questions exhausted

By end of Day 38: Game is playable end-to-end.
```

---

*Day 37 Complete. Data layer working. First production code written. Game logic starts tomorrow.* ✅

