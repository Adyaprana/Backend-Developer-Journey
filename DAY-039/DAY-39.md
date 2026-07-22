# DAY 39 — GuessWise: Full Game Loop, Generic Engine + LeetCode Third Maximum

> **Project:** GuessWise — End-to-End Playable CLI Game (Version 1 Complete)
>
> **Path:** `C:\A_MY THINGS\001\Backend-Developer-Journey\Project\GuessWise`
>
> **LeetCode:** #414 Third Maximum Number ✅ (0ms · Beats 100%)
>
> **Status:** ✅ Day 39 Complete — GuessWise Version 1 is fully playable

---

# 🎯 What Was Built Today

```
✅ Generic play_game() replaces duplicated character_mode()/animal_mode()
✅ select_category() — filters characters AND questions by category
✅ filter_characters() — core filtering algorithm (list comprehension)
✅ show_remaining_candidates() — live feedback after each answer
✅ play_again() — restart loop with category memory
✅ 80 characters across 3 categories (character, animal, object)
✅ 150 questions across 3 categories
✅ tools/update_attributes.py — data migration utility
✅ LeetCode #414 Third Maximum Number (0ms, beats 100%)
```

**GuessWise Version 1 is now a complete, playable game from start to finish.**

---

# 📁 Final Project State (Phase 4 Complete)

```
GuessWise/
│
├── main.py                      ← Entry point (3 lines)
├── game.py                      ← ✅ Complete game logic (all methods)
│
├── models/
│   ├── __init__.py
│   ├── character.py             ← @dataclass with id, name, category, attributes
│   └── question.py              ← @dataclass with id, category, text, attribute
│
├── repository/
│   ├── __init__.py
│   ├── repository.py            ← Abstract base class (ABC)
│   └── json_repository.py      ← JSON implementation
│
├── engines/
│   ├── __init__.py
│   ├── character_engine.py      ← (stub — logic moved into Game for now)
│   └── question_engine.py       ← (stub — logic moved into Game for now)
│
├── utils/
│   ├── __init__.py
│   ├── display.py               ← (stub)
│   └── validation.py            ← (stub)
│
├── tools/
│   └── update_attributes.py     ← ✅ Data migration utility
│
└── data/
    ├── characters.json          ← 80 characters (ids 1–80)
    └── questions.json           ← 150 questions (50 per category)
```

---

# SECTION 1 — THE COMPLETE CODE

## main.py

```python
from game import Game

game = Game()
game.start()
```

**Why main.py has only 3 lines:**

```
The job of main.py is ONLY to start the application.
All logic belongs elsewhere.

This is the Single Entry Point principle.
When you read main.py, you know: "Game starts here."
When you need to debug: you go to game.py, not main.py.

FastAPI follows the same idea:
  main.py: app = FastAPI(); uvicorn.run(app)
  Everything else: routers, models, services, database.py
```

---

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

**Every design decision explained:**

```
@dataclass
→ Python generates __init__, __repr__, __eq__ automatically.
→ Without it: 20 lines of boilerplate per model.
→ Standard Python for data containers since 3.7.

id: int
→ Unique identifier.
→ In JSON version: manually assigned (1, 2, 3...).
→ In PostgreSQL version (Day 40): SERIAL PRIMARY KEY, auto-generated.

name: str
→ Display name of the character.
→ str = unlimited text. No length constraint at this layer.

category: str
→ "character", "animal", "object"
→ Used by select_category() to partition the character list.
→ One string key connects characters to their questions.

attributes: dict[str, bool]
→ All facts about the character as key-value pairs.
→ Key: attribute name (matches question.attribute).
→ Value: True or False only.
→ Why dict and not flat fields?
   Flat: character.real, character.male, character.cricketer...
         Adding one new attribute = change the class = potential breakage.
   Dict: character.attributes["real"], character.attributes["male"]
         Adding one new attribute = add one JSON key.
         Class never changes. Data changes. Clean separation.
```

---

## models/question.py

```python
from dataclasses import dataclass

@dataclass
class Question:
    id: int
    category: str
    text: str
    attribute: str
```

**Every field explained:**

```
id: int
→ Unique identifier per question within a category group.

category: str
→ "character", "animal", "object"
→ Matches the category field in Character.
→ This is how Question connects to Character — through category + attribute.

text: str
→ What the user sees on screen.
→ "Is your character a real person?"

attribute: str
→ The KEY that connects this question to Character.attributes.
→ Question.attribute = "real"
   Character.attributes["real"] = True
→ When user answers "Yes":
   filter_characters("real", True)
   → keep characters where attributes.get("real") == True
```

**Why Question doesn't have a direct reference to Character:**

```
Loose Coupling: Question and Character are independent objects.
They share only a string key (attribute name).

If Question held a reference to Character:
  Circular dependency risk.
  Testing question logic requires loading characters.
  Changing Character format breaks Question.

With string-key connection:
  Question can be loaded, tested, and used without knowing Character exists.
  This is how professional systems are designed.
```

---

## repository/repository.py

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

**What ABC (Abstract Base Class) does:**

```python
# Without ABC:
repository = Repository()   # This would work (but shouldn't!)
repository.get_characters() # Returns None — no implementation!

# With ABC:
repository = Repository()   # TypeError: Can't instantiate abstract class
# Forces you to use a concrete implementation (JsonRepository, PostgresRepository)

# ABC says: "This is a CONTRACT, not an implementation."
# Anyone who inherits MUST implement all @abstractmethod methods.
```

**Why this is the most important file in the project:**

```
This file defines the INTERFACE — the contract.
It says: "Whatever gives data to GuessWise must provide these two methods."

Game.start() calls:
  self.repository.get_characters()
  self.repository.get_questions()

Game doesn't care if repository is:
  JsonRepository  (reads files)
  PostgresRepository (runs SQL)
  MockRepository  (returns test data)
  APIRepository   (calls an external API)

As long as it implements these two methods, Game works unchanged.
This is the Repository Pattern — the core architectural decision of the project.
```

---

## repository/json_repository.py

```python
import json

from models.character import Character
from models.question import Question
from repository.repository import Repository


class JsonRepository(Repository):

    def get_characters(self) -> list[Character]:
        with open("data/characters.json", "r") as file:
            data = json.load(file)
            characters = []
            for item in data:
                character = Character(**item)
                characters.append(character)
            return characters
            
    def get_questions(self) -> list[Question]:
        with open("data/questions.json", "r") as file:
            data = json.load(file)

            questions = []
            for group in data:
                category = group["category"]

                for item in group["questions"]:
                    questions.append(
                        Question(
                            id=item["id"],
                            category=category,
                            text=item["text"],
                            attribute=item["attribute"]
                        )
                    )
            return questions
```

**Detailed breakdown of get_characters():**

```python
with open("data/characters.json", "r") as file:
# Opens the file. "r" = read mode.
# "with" = context manager: file closes automatically, even if error occurs.

data = json.load(file)
# Reads the entire JSON file and parses it into Python objects.
# JSON array → Python list of dicts

for item in data:
# item is one character dict:
# {"id": 1, "name": "Virat Kohli", "category": "character", "attributes": {...}}

character = Character(**item)
# **item unpacks the dict as keyword arguments:
# Character(id=1, name="Virat Kohli", category="character", attributes={...})
# The dict keys MUST match the @dataclass field names exactly.
# This is why JSON keys are: id, name, category, attributes
```

**Detailed breakdown of get_questions():**

```python
# questions.json is a LIST of GROUPS (not a flat list)
# [
#   {
#     "category": "character",
#     "questions": [
#       {"id": 1, "text": "...", "attribute": "..."},
#       ...
#     ]
#   },
#   {
#     "category": "animal",
#     "questions": [...]
#   }
# ]

for group in data:
    category = group["category"]        # "character", "animal", "object"
    
    for item in group["questions"]:     # inner loop: each question
        questions.append(
            Question(
                id=item["id"],
                category=category,      # inherited from the outer group
                text=item["text"],
                attribute=item["attribute"]
            )
        )

# Why nested structure instead of flat?
# Flat: every question would duplicate its category field.
# Grouped: category defined once per group. DRY principle.
# 
# Result: Question objects all have category embedded,
# even though JSON stores category at the group level.
```

---

## game.py — The Complete File

```python
from repository.json_repository import JsonRepository


class Game:
    def __init__(self):
        self.repository = JsonRepository()

    def start(self):
        self.all_characters = self.repository.get_characters()
        self.characters = self.all_characters.copy()
        self.questions = self.repository.get_questions()
        
        print("Game Started")
        print(f"Loaded {len(self.characters)} characters")
        print(f"Loaded {len(self.questions)} questions")
        self.show_menu()
        
    def show_menu(self):
        while True:
            print("===================================")
            print("        🎯 GuessWise               ")
            print("===================================")

            print("1. Character")
            print("2. Animal")
            print("3. Object")
            print("4. Exit")
            choice = input("Enter your choice (1-4): ").strip()
            if choice == "1":
                self.select_category("character")
                self.play_game()

            elif choice == "2":
                self.select_category("animal")
                self.play_game()

            elif choice == "3":
                self.select_category("object")
                self.play_game()

            elif choice == "4":
                print("Game Exit")
                break
            else:
                print("Invalid choice! Please enter a number from 1 to 4.")
                continue

    def play_game(self):
        
        question_index = 0
        while True:
            if question_index >= len(self.current_questions):
                print("🤔 I couldn't uniquely identify your answer.")
                print("\nPossible Matches:")
                self.show_remaining_candidates()

                if self.play_again():
                    self.select_category(self.current_category)
                    return self.play_game()
                return

            print("\n=========================")
            print("🎯 GuessWise")
            print("=========================")
            print(f"Category : {self.current_category.title()}")
            print(f"Remaining Candidates : {len(self.characters)}")
            
            print(f"Question {question_index + 1}")
            question = self.current_questions[question_index]
            print(question.text)
            print("1. Yes")
            print("2. No")
            print("3. Probably")
            print("4. Probably Not")
            print("5. Don't Know")
            answers = {
                "1": "Yes",
                "2": "No",
                "3": "Probably",
                "4": "Probably Not",
                "5": "Don't Know"
            }
            choice = input("Enter your choice (1-5): ").strip()

            if choice == "1":
                self.filter_characters(question.attribute, True)

            elif choice == "2":
                self.filter_characters(question.attribute, False)               

            elif choice in ["3", "4", "5"]:
                print(f"You selected: {answers[choice]}")
            else:
                print("Invalid choice! Please enter a number from 1 to 5.")

            self.show_remaining_candidates()

            if len(self.characters) == 1:
                print("\n🎉 I guessed your answer!")
                print(f"It's: {self.characters[0].name}")

                if self.play_again():
                    self.select_category(self.current_category)
                    return self.play_game()
                return
            
            elif len(self.characters) == 0:
                print("\n❌ No matching character found.")
                
                if self.play_again():
                    self.select_category(self.current_category)
                    return self.play_game()
                return
            question_index += 1

    def select_category(self, category: str):
        self.current_category = category

        self.characters = [
            character
            for character in self.all_characters
            if character.category == category
        ]

        self.current_questions = [
            question
            for question in self.questions
            if question.category == category
        ]

    def filter_characters(self, attribute: str, expected_value: bool):
        self.characters = [
            character
            for character in self.characters
            if character.attributes.get(attribute, False) == expected_value
        ]

    def show_remaining_candidates(self):
        print("\nRemaining Candidates:")
        for character in self.characters:
            print("-", character.name)

    def play_again(self) -> bool:
        while True:
            print("\n-----------------------")
            print("Play Again?")
            print("-----------------------")
            print("1. Yes")
            print("2. No")

            choice = input("Enter your choice: ").strip()

            if choice == "1":
                return True

            elif choice == "2":
                return False
            print("Invalid choice!")
```

---

# SECTION 2 — EVERY METHOD EXPLAINED DEEPLY

## `__init__` — Dependency Injection

```python
def __init__(self):
    self.repository = JsonRepository()
```

**What happens here:**

```
When you write: game = Game()
Python calls __init__() automatically.

self.repository = JsonRepository()
→ Creates one JsonRepository object.
→ Stores it as an instance attribute so ALL methods can use it.
→ Game never opens JSON files directly. Only through self.repository.

Why this matters:
  On Day 40, this line changes to:
    self.repository = PostgresRepository()
  
  NOTHING ELSE IN THE FILE CHANGES.
  The game logic stays identical.
  Only the data source switches.
  This is the entire point of the Repository Pattern.
```

---

## `start()` — Application Startup

```python
def start(self):
    self.all_characters = self.repository.get_characters()
    self.characters = self.all_characters.copy()
    self.questions = self.repository.get_questions()
    
    print("Game Started")
    print(f"Loaded {len(self.characters)} characters")
    print(f"Loaded {len(self.questions)} questions")
    self.show_menu()
```

**Why `self.all_characters` AND `self.characters` (two lists):**

```
self.all_characters = self.repository.get_characters()
→ The MASTER list. Never modified. Contains all 80 characters.

self.characters = self.all_characters.copy()
→ The WORKING list. Gets filtered during the game.
→ .copy() creates a SHALLOW COPY (new list, same object references).
→ Filtering self.characters never touches self.all_characters.

When play_again() returns True:
  select_category(self.current_category)
  This method reads from self.all_characters and rebuilds self.characters.
  Fresh start. Master list unchanged.

If we only had one list:
  After playing once, the list is empty (filtered down to 1 character).
  "Play Again" would start with 1 character, not 80.
  Game would be broken.
```

**Why `start()` calls `show_menu()` at the end:**

```
Single Responsibility:
  start() = load data + verify it loaded
  show_menu() = handle user interaction

If start() also had the menu loop, it would do two things.
Functions that do two things are harder to test and maintain.
```

---

## `show_menu()` — Main Navigation

```python
def show_menu(self):
    while True:
        print("===================================")
        print("        🎯 GuessWise               ")
        print("===================================")

        print("1. Character")
        print("2. Animal")
        print("3. Object")
        print("4. Exit")
        choice = input("Enter your choice (1-4): ").strip()
        if choice == "1":
            self.select_category("character")
            self.play_game()

        elif choice == "2":
            self.select_category("animal")
            self.play_game()

        elif choice == "3":
            self.select_category("object")
            self.play_game()

        elif choice == "4":
            print("Game Exit")
            break
        else:
            print("Invalid choice! Please enter a number from 1 to 4.")
            continue
```

**Why `while True` + `break`:**

```
The menu must repeat until the user chooses Exit.

while True:     → Run forever
    ...
    elif choice == "4":
        break   → Exit the loop when user wants to quit

Alternative: while choice != "4"
But this requires initializing choice before the loop (choice = "").
while True + break is cleaner for "run-until-exit" patterns.
```

**Why call `select_category()` before `play_game()`:**

```
select_category("character") does two things:
  1. Sets self.current_category = "character"
  2. Filters self.characters to only "character" type
  3. Filters self.current_questions to only "character" questions

play_game() then works on these pre-filtered lists.
play_game() itself doesn't know what category is selected.
It just uses whatever is in self.characters and self.current_questions.

This separation means:
  play_game() is reusable across all categories.
  No if/elif inside play_game() checking the category.
```

**The OLD approach (Day 38) that was replaced:**

```python
# DAY 38 — two separate methods (DUPLICATED LOGIC)
if choice == "1":
    self.character_mode()
if choice == "2":
    self.animal_mode()

# character_mode() and animal_mode() had identical code
# with just different data source — VIOLATION of DRY principle.

# DAY 39 — Generic solution (SINGLE METHOD)
if choice == "1":
    self.select_category("character")
    self.play_game()
if choice == "2":
    self.select_category("animal")
    self.play_game()

# play_game() is the same for all categories.
# Only the setup (select_category) differs.
# DRY: Don't Repeat Yourself.
```

---

## `select_category()` — Category Setup

```python
def select_category(self, category: str):
    self.current_category = category

    self.characters = [
        character
        for character in self.all_characters
        if character.category == category
    ]

    self.current_questions = [
        question
        for question in self.questions
        if question.category == category
    ]
```

**What happens in detail:**

```
Input: category = "character"

Step 1:
  self.current_category = "character"
  → Stores the current category for use in play_again() later.

Step 2 (list comprehension):
  self.characters = [
      character
      for character in self.all_characters    ← loop over all 80
      if character.category == "character"    ← keep only matching ones
  ]
  → Result: list of all characters with category == "character" (ids 1–80)

Step 3 (same pattern for questions):
  self.current_questions = [
      question
      for question in self.questions          ← loop over all 150
      if question.category == "character"     ← keep only matching ones
  ]
  → Result: list of 50 questions for "character" category
```

**List comprehension explained:**

```python
# List comprehension is a one-line for loop that builds a list.

# Equivalent to:
self.characters = []
for character in self.all_characters:
    if character.category == category:
        self.characters.append(character)

# Compressed to:
self.characters = [character for character in self.all_characters if character.category == category]

# Read as:
# "Give me all characters, for each character in all_characters, if category matches."

# List comprehensions:
# ✅ Faster than equivalent for loop + append (Python optimizes them)
# ✅ More Pythonic — experienced Python developers write them naturally
# ✅ In one line instead of three
# ✅ No need to manually create empty list and append
```

---

## `play_game()` — The Game Loop

This is the most important method. It runs the entire question-answer loop.

```python
def play_game(self):
    
    question_index = 0
    while True:
        # ── CASE 1: QUESTIONS EXHAUSTED ────────────────────────
        if question_index >= len(self.current_questions):
            print("🤔 I couldn't uniquely identify your answer.")
            print("\nPossible Matches:")
            self.show_remaining_candidates()

            if self.play_again():
                self.select_category(self.current_category)
                return self.play_game()
            return

        # ── DISPLAY QUESTION ───────────────────────────────────
        print("\n=========================")
        print("🎯 GuessWise")
        print("=========================")
        print(f"Category : {self.current_category.title()}")
        print(f"Remaining Candidates : {len(self.characters)}")
        
        print(f"Question {question_index + 1}")
        question = self.current_questions[question_index]
        print(question.text)
        print("1. Yes")
        print("2. No")
        print("3. Probably")
        print("4. Probably Not")
        print("5. Don't Know")
        answers = {
            "1": "Yes",
            "2": "No",
            "3": "Probably",
            "4": "Probably Not",
            "5": "Don't Know"
        }
        choice = input("Enter your choice (1-5): ").strip()

        # ── PROCESS ANSWER ─────────────────────────────────────
        if choice == "1":
            self.filter_characters(question.attribute, True)

        elif choice == "2":
            self.filter_characters(question.attribute, False)               

        elif choice in ["3", "4", "5"]:
            print(f"You selected: {answers[choice]}")
            # Uncertain answers: don't filter (keep all candidates)
        else:
            print("Invalid choice! Please enter a number from 1 to 5.")

        # ── SHOW CANDIDATES ────────────────────────────────────
        self.show_remaining_candidates()

        # ── CASE 2: EXACTLY ONE CHARACTER REMAINS ──────────────
        if len(self.characters) == 1:
            print("\n🎉 I guessed your answer!")
            print(f"It's: {self.characters[0].name}")

            if self.play_again():
                self.select_category(self.current_category)
                return self.play_game()
            return
        
        # ── CASE 3: ZERO CHARACTERS REMAIN ─────────────────────
        elif len(self.characters) == 0:
            print("\n❌ No matching character found.")
            
            if self.play_again():
                self.select_category(self.current_category)
                return self.play_game()
            return

        question_index += 1
```

**How question_index works:**

```
question_index = 0  → start from first question

Each loop iteration:
  Show question at index question_index
  Get user's answer
  Filter (or not, if "Probably"/"Don't Know")
  Show remaining candidates
  Check if game is over
  question_index += 1  → move to next question

When question_index >= len(self.current_questions):
  All 50 questions exhausted with no single match found.
  Show "Possible Matches" and ask to play again.
```

**The three exit conditions:**

```
Exit 1: All questions exhausted
  question_index >= len(self.current_questions)
  "I couldn't uniquely identify your answer."
  Show remaining candidates (could be 2, 5, 10...)

Exit 2: Exactly 1 character remains
  len(self.characters) == 1
  "🎉 I guessed! It's: [name]"

Exit 3: Zero characters remain
  len(self.characters) == 0
  "❌ No matching character found."
  (User may have answered incorrectly, or data is wrong)
```

**Why "Probably" and "Don't Know" don't filter:**

```
Real Akinator allows uncertainty. If the user isn't sure, we shouldn't
narrow down the candidates based on uncertain information.

choice "1" = Yes      → filter_characters(attr, True)
choice "2" = No       → filter_characters(attr, False)
choice "3" = Probably → print message, but NO filtering
choice "4" = Prob Not → print message, but NO filtering
choice "5" = Don't Know → print message, but NO filtering

In a more advanced version (future):
  "Probably" could filter with weighted scoring.
  "Probably Not" could down-rank but not eliminate.
  Version 1 keeps it simple: binary filtering on Yes/No only.
```

**The play_again() pattern:**

```python
if self.play_again():
    self.select_category(self.current_category)   # reset to same category
    return self.play_game()                       # recursive call
return                                            # exit game
```

```
self.current_category was stored by select_category() earlier.
When play_again() = True:
  1. select_category(same category) resets self.characters from all_characters
  2. play_game() is called again (recursive)
  3. "return self.play_game()" is important:
     Without "return", play_game() would continue from where it was.
     With "return", the current call exits and new call takes over.
```

---

## `filter_characters()` — The Core Algorithm

```python
def filter_characters(self, attribute: str, expected_value: bool):
    self.characters = [
        character
        for character in self.characters
        if character.attributes.get(attribute, False) == expected_value
    ]
```

**This is the heart of the entire game.**

```
Parameters:
  attribute:      "real"    (the attribute key to check)
  expected_value: True      (what the user said — yes = True, no = False)

Logic:
  For each character in the current working list:
    Look up character.attributes.get("real", False)
    If that value == True (what user said)
    → Keep this character
    Otherwise
    → Remove it (by not including in the new list)

The result replaces self.characters with the filtered version.
```

**Tracing an example:**

```
Before filter:
  self.characters = [Virat Kohli, Naruto, MS Dhoni, Hermione, Batman, ...]
  (say 80 characters, category = "character")

Question: "Is your character a real person?"
User answers: "1" (Yes)

filter_characters("real", True)

For each character:
  Virat Kohli:   attributes["real"] = True  → True == True  → KEEP ✅
  Naruto:        attributes["real"] = False → False == True → DROP ❌
  MS Dhoni:      attributes["real"] = True  → True == True  → KEEP ✅
  Hermione:      attributes["real"] = False → False == True → DROP ❌
  Batman:        attributes["real"] = False → False == True → DROP ❌

After filter:
  self.characters = [Virat Kohli, MS Dhoni, Sachin, SRK, Obama, ...]
  (only the real people remain)
```

**Why `.get(attribute, False)` instead of `[attribute]`:**

```python
# Direct access — RISKY
character.attributes[attribute]
# If attribute doesn't exist in this character's dict → KeyError!
# Game crashes.

# .get() with default — SAFE
character.attributes.get(attribute, False)
# If attribute doesn't exist → returns False (safe default)
# Game continues normally.

# When would an attribute be missing?
# If you added a new question but forgot to update old character data.
# .get() makes the code robust against incomplete data.
```

**The filter replaces, not appends:**

```python
self.characters = [...]  # new list assigned to self.characters
# Old list is garbage collected by Python.
# self.characters now points to the filtered list.
# This is why "Play Again" needs select_category() —
# to restore self.characters from self.all_characters.
```

---

## `show_remaining_candidates()` — Live Feedback

```python
def show_remaining_candidates(self):
    print("\nRemaining Candidates:")
    for character in self.characters:
        print("-", character.name)
```

**Why this is important for user experience:**

```
Without this feedback:
  User answers 3 questions, doesn't know if anything changed.
  Is the game working? Did my answer matter?
  Frustrating experience.

With this feedback:
  User answers "Yes, my character is real."
  Game immediately shows: "Remaining: Virat Kohli, MS Dhoni, Obama..."
  User can see: "Ok, the game eliminated Naruto and Harry Potter."
  Satisfying, transparent, game-like.

Real Akinator shows the probability of each guess after each question.
Version 1 shows the remaining candidates list (simpler but informative).
```

---

## `play_again()` — Clean Return Value

```python
def play_again(self) -> bool:
    while True:
        print("\n-----------------------")
        print("Play Again?")
        print("-----------------------")
        print("1. Yes")
        print("2. No")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            return True

        elif choice == "2":
            return False
        print("Invalid choice!")
```

**Why return `bool` instead of a string:**

```
Returns True or False — Python's boolean type.
The caller (play_game) uses it as:

if self.play_again():     → evaluates True/False directly
    ...                   → Python's if works naturally with bool

If it returned a string:
if self.play_again() == "yes":    → fragile, extra comparison
if self.play_again() == "1":      → what does "1" mean? Less readable

Return type annotation `-> bool` serves as documentation:
"This method returns a boolean."
Type checkers (mypy, Pylance) can verify this automatically.
```

**Why `while True` (retry on invalid input):**

```
If user enters "abc" or "3":
  print("Invalid choice!")
  Loop continues — user gets another chance.
  
Without while True:
  Invalid input → method returns None → if None → False → game exits.
  User is forced out of the game by a typo. Bad UX.

With while True:
  Invalid input → "Invalid choice!" → ask again.
  User always has a chance to make a valid choice.
```

---

# SECTION 3 — DATA FILES (Full Structure)

## data/characters.json (Structure)

The final characters.json contains **80 characters** in 3 categories:

```
Character category (ids 1–80):
  Cricketers:  Virat Kohli, MS Dhoni, Sachin Tendulkar, Rohit Sharma
  Footballers: Cristiano Ronaldo, Lionel Messi, Neymar Jr, Kylian Mbappe
  Tennis:      Novak Djokovic, Rafael Nadal, Roger Federer, Serena Williams
  Tech:        Elon Musk, Bill Gates, Steve Jobs, Mark Zuckerberg, Jeff Bezos,
               Sundar Pichai, Satya Nadella, Tim Cook
  Scientists:  Albert Einstein, Isaac Newton, Nikola Tesla, Marie Curie,
               Charles Darwin, Stephen Hawking
  Indian:      APJ Abdul Kalam, Mahatma Gandhi, Subhas Chandra Bose,
               Bhagat Singh, Narendra Modi, Barack Obama, Abraham Lincoln,
               Nelson Mandela
  Musicians:   Taylor Swift, Ed Sheeran, Michael Jackson, Ariana Grande
  Bollywood:   Shah Rukh Khan, Aamir Khan, Deepika Padukone
  Hollywood:   Emma Watson, Tom Cruise, Leonardo DiCaprio, Robert Downey Jr
  Marvel/DC:   Spider-Man, Iron Man, Captain America, Thor, Hulk,
               Batman, Superman, Wonder Woman, Joker, Harley Quinn
  Anime:       Naruto Uzumaki, Sasuke Uchiha, Monkey D. Luffy, Goku, Vegeta
  Animated:    Pikachu, Mickey Mouse, Donald Duck, Elsa, Anna
  Harry Potter: Harry Potter, Hermione Granger, Ron Weasley, Albus Dumbledore
  Video Games: Mario, Luigi, Link, Kratos, Sonic, Lara Croft,
               Master Chief, Geralt of Rivia
  Mythology:   Zeus, Thor (Mythology), Hercules

Animal category (ids 81–115):
  Big Cats:    Lion, Tiger
  Wild:        Elephant, Wolf, Fox, Bear, Deer, Rabbit, Monkey, Chimpanzee
               Panda, Koala, Kangaroo, Giraffe, Zebra
  Domestic:    Dog, Cat, Horse, Cow, Buffalo, Goat, Sheep
  Reptiles:    Crocodile, Alligator, Snake
  Birds:       Eagle, Owl, Parrot, Penguin
  Aquatic:     Dolphin, Shark, Whale, Octopus
  Other:       Frog, Turtle

Object category (ids 116–150):
  Furniture:   Chair, Table, Sofa, Bed
  Electronics: Laptop, Keyboard, Mouse, Monitor, Phone, Television,
               Camera, Headphones, Watch, Clock, Fan, Refrigerator, Microwave
  Stationery:  Pen, Pencil, Book, Notebook, Backpack
  Kitchen:     Bottle, Cup, Spoon, Fork, Knife, Plate
  Bedroom:     Pillow, Blanket
  Structural:  Door, Window, Lamp
  Transport:   Bicycle
  Misc:        Umbrella
```

---

## Each Character Has 51 Attributes

```json
{
  "id": 1,
  "name": "Virat Kohli",
  "category": "character",
  "attributes": {
    "fictional": false,
    "real": true,
    "alive": true,
    "human": true,
    "male": true,
    "female": false,
    "indian": false,
    "cricketer": false,
    "actor": false,
    "musician": false,
    "politician": false,
    "scientist": false,
    "writer": false,
    "singer": false,
    "sportsperson": false,
    "footballer": false,
    "tennis_player": false,
    "award_winner": false,
    "asian": false,
    "european": false,
    "american": false,
    "over_50": false,
    "movies": false,
    "television": false,
    "glasses": false,
    "beard": false,
    "bald": false,
    "black_hair": false,
    "married": false,
    "has_children": false,
    "usa": false,
    "uk": false,
    "comic_character": false,
    "magic": false,
    "superpowers": false,
    "animated": false,
    "anime": false,
    "video_game": false,
    "royalty": false,
    "historical": false,
    "freedom_fighter": false,
    "youtuber": false,
    "influencer": false,
    "billionaire": false,
    "ceo": false,
    "entrepreneur": false,
    "teacher": false,
    "doctor": false,
    "engineer": false,
    "criminal": false,
    "world_famous": false
  }
}
```

**⚠️ Important note:** The attributes are all `false` in the raw file. This is because the `tools/update_attributes.py` creates the structure, but **actual values need to be filled in manually or through an admin tool (Day 41).** The game structure is complete; attribute accuracy is a data quality task.

---

## data/questions.json (Structure)

```json
[
  {
    "category": "character",
    "questions": [
      {"id": 1, "text": "Is your character a real person?", "attribute": "real"},
      {"id": 2, "text": "Is your character male?", "attribute": "male"},
      {"id": 3, "text": "Is your character still alive?", "attribute": "alive"},
      {"id": 4, "text": "Is your character Indian?", "attribute": "indian"},
      {"id": 5, "text": "Is your character a cricketer?", "attribute": "cricketer"},
      ... 50 questions total
    ]
  },
  {
    "category": "animal",
    "questions": [
      {"id": 1, "text": "Is it a mammal?", "attribute": "mammal"},
      {"id": 2, "text": "Is it a wild animal?", "attribute": "wild"},
      ... 50 questions total
    ]
  },
  {
    "category": "object",
    "questions": [
      {"id": 1, "text": "Is it electronic?", "attribute": "electronic"},
      {"id": 2, "text": "Can it fit in your pocket?", "attribute": "portable"},
      ... 50 questions total
    ]
  }
]
```

**Why nested structure (category group > questions) instead of flat list:**

```
Flat (bad):
[
  {"id": 1, "category": "character", "text": "...", "attribute": "..."},
  {"id": 2, "category": "character", "text": "...", "attribute": "..."},
  ... 150 entries, each repeating "category": "character" 50 times
]

Nested (good):
[
  {
    "category": "character",   ← defined once
    "questions": [
      {"id": 1, ...},           ← no category duplication
      ...50 questions
    ]
  }
]

DRY principle: "Don't Repeat Yourself"
"character" appears once in the nested version, 50 times in the flat version.
```

---

# SECTION 4 — THE DATA MIGRATION TOOL

## tools/update_attributes.py

```python
import json
from pathlib import Path

# ─────────────────────────────────────────────
# File Paths
# ─────────────────────────────────────────────

BASE_DIR = Path(__file__).resolve().parent.parent

CHARACTER_FILE = BASE_DIR / "data" / "characters.json"
QUESTION_FILE  = BASE_DIR / "data" / "questions.json"

# ─────────────────────────────────────────────
# Load Questions
# ─────────────────────────────────────────────

with open(QUESTION_FILE, "r", encoding="utf-8") as file:
    question_groups = json.load(file)

category_attributes = {}

for group in question_groups:
    category   = group["category"]
    attributes = [question["attribute"] for question in group["questions"]]
    category_attributes[category] = attributes

# ─────────────────────────────────────────────
# Load Characters
# ─────────────────────────────────────────────

with open(CHARACTER_FILE, "r", encoding="utf-8") as file:
    characters = json.load(file)

# ─────────────────────────────────────────────
# Add Missing Attributes
# ─────────────────────────────────────────────

updated = 0

for character in characters:
    category           = character["category"]
    required_attributes = category_attributes.get(category, [])
    attributes         = character.setdefault("attributes", {})

    for attribute in required_attributes:
        if attribute not in attributes:
            attributes[attribute] = False
            updated += 1

# ─────────────────────────────────────────────
# Save
# ─────────────────────────────────────────────

with open(CHARACTER_FILE, "w", encoding="utf-8") as file:
    json.dump(characters, file, indent=2)

print("=" * 40)
print("Migration Complete")
print("=" * 40)
print(f"Characters       : {len(characters)}")
print(f"Attributes Added : {updated}")
print("characters.json updated successfully.")
```

**What this tool does and why it matters:**

```
Problem:
  You have 80 characters in characters.json.
  You add 5 new questions to questions.json.
  Now those 5 new attributes are missing from all 80 characters.
  filter_characters() uses .get(attribute, False) as fallback.
  But the actual data doesn't have the keys — inconsistent.

Solution:
  Run update_attributes.py once.
  It reads ALL attributes from questions.json.
  It checks every character in characters.json.
  If any attribute is missing → adds it with default value False.
  Saves the updated file.

This is a DATA MIGRATION TOOL — the same concept used in:
  Django: migrations
  SQLAlchemy: Alembic
  Backend projects: schema migration scripts

Running it is safe:
  Only adds missing keys (never overwrites existing values).
  Existing True/False values for filled-in characters are preserved.
```

**New Python concepts used:**

```python
BASE_DIR = Path(__file__).resolve().parent.parent

# Path(__file__): path to update_attributes.py itself
# .resolve(): get absolute path (no relative ../ issues)
# .parent: go up one folder (to tools/)
# .parent again: go up one more (to GuessWise root)
# / "data" / "characters.json": path joining (works on Windows + Mac + Linux)
# 
# This is BETTER than hardcoding paths:
#   open("../data/characters.json")  → breaks if script is run from different directory
#   Path(__file__).resolve()...       → works from ANY directory

character.setdefault("attributes", {})
# setdefault(key, default):
#   If "attributes" key exists → return its value
#   If "attributes" key does NOT exist → create it with {} and return {}
# Safe way to ensure a key exists before doing attribute lookups.

if attribute not in attributes:
    attributes[attribute] = False
    updated += 1
# "not in" checks if key exists in dictionary.
# Only add if missing (never overwrite existing real values).
# Track count for reporting.
```

---

# SECTION 5 — THE COMPLETE GAME FLOW

## Full Play Session Trace

```
$ python main.py

Game Started
Loaded 80 characters
Loaded 150 questions

===================================
        🎯 GuessWise
===================================
1. Character
2. Animal
3. Object
4. Exit

Enter your choice (1-4): 1   [user picks Character]

=========================
🎯 GuessWise
=========================
Category : Character
Remaining Candidates : 80
Question 1
Is your character a real person?
1. Yes
2. No
3. Probably
4. Probably Not
5. Don't Know

Enter your choice (1-5): 1   [user says Yes]

Remaining Candidates:
- Virat Kohli
- MS Dhoni
- Sachin Tendulkar
- Elon Musk
- Bill Gates
- Taylor Swift
... (all real people)

=========================
Category : Character
Remaining Candidates : 45
Question 2
Is your character male?
...

Enter your choice (1-5): 1   [Yes]

Remaining Candidates:
- Virat Kohli
- MS Dhoni
- Elon Musk
...

=========================
Category : Character  
Remaining Candidates : 38
Question 3
Is your character still alive?
...

Enter your choice (1-5): 1   [Yes]

...

[Several more questions later, 1 character remains]

🎉 I guessed your answer!
It's: Virat Kohli

-----------------------
Play Again?
-----------------------
1. Yes
2. No

Enter your choice: 2   [No]

[Game returns to main menu]

===================================
        🎯 GuessWise
===================================
Enter your choice (1-4): 4   [Exit]

Game Exit
```

---

# SECTION 6 — CONCEPTS LEARNED (DAYS 36–39 SUMMARY)

```
Day 36: Architecture Design
  → Repository Pattern
  → Layered architecture (presentation/business/data)
  → JSON design for future PostgreSQL migration

Day 37: Models + Data Layer
  → @dataclass (auto-generates __init__, __repr__, __eq__)
  → Abstract Base Class (ABC) + @abstractmethod
  → **kwargs dict unpacking: Character(**item)
  → JsonRepository: reads JSON → typed Python objects

Day 38: Game Class + CLI Menu
  → Instance attributes (self.x) for state sharing across methods
  → Method decomposition (show_menu vs character_mode)
  → Dictionary mapping: {"1": "Yes", "2": "No"} replaces if/elif chains
  → Input validation with while True + break

Day 39: Generic Engine + Full Game Loop
  → Generic play_game() replacing category-specific methods (DRY principle)
  → select_category() — two-list design (all_characters + characters)
  → filter_characters() — list comprehension filtering algorithm
  → .get(key, default) — safe dict access
  → show_remaining_candidates() — live UX feedback
  → play_again() — bool return type + recursive call pattern
  → update_attributes.py — data migration tool
  → Path(__file__).resolve() — portable file paths
  → .setdefault() — safe key initialization
```

---

# SECTION 7 — LEETCODE #414: THIRD MAXIMUM NUMBER

## Problem

Given an integer array, return the **third distinct maximum**. If there is no third maximum, return the **maximum**.

```
[3, 2, 1] → 1   (third maximum exists: 3 > 2 > 1 → return 1)
[1, 2]    → 2   (no third maximum → return maximum = 2)
[2, 2, 3, 1] → 1 (distinct: 3, 2, 1 → third = 1)
```

## Approach 1: Sorting — O(n log n)

```python
class Solution(object):
    def thirdMax(self, nums):
        unique = list(set(nums))      # remove duplicates
        unique.sort(reverse=True)     # sort descending: [3, 2, 1]
        
        if len(unique) >= 3:
            return unique[2]           # third element (index 2)
        else:
            return unique[0]           # not enough → return maximum
```

**Why `set()` first:**

```
set() removes duplicates.
[2, 2, 3, 1] → {1, 2, 3}
list({1, 2, 3}) → [1, 2, 3]
After sort descending: [3, 2, 1]
unique[2] = 1 → correct third maximum.

Without set(): [2, 2, 3, 1] sorted desc = [3, 2, 2, 1]
unique[2] = 2 → wrong! (that's the second maximum, not third)
```

## Approach 2: One-Pass with Three Trackers — O(n) ✅ Submitted

```python
class Solution(object):
    def thirdMax(self, nums):
        first = None
        second = None
        third = None

        for num in nums:
            # Skip duplicates
            if num == first or num == second or num == third:
                continue

            # Update top three in order
            if first is None or num > first:
                third = second
                second = first
                first = num

            elif second is None or num > second:
                third = second
                second = num

            elif third is None or num > third:
                third = num

        if third is None:
            return first   # no third maximum exists → return maximum
        return third
```

**Dry run — `[3, 2, 1]`:**

```
Initial: first=None, second=None, third=None

num=3:
  Not duplicate.
  first is None → update:
    third = second = None
    second = first = None
    first = 3
  State: first=3, second=None, third=None

num=2:
  Not duplicate (2 ≠ 3, 2 ≠ None, 2 ≠ None).
  2 > first=3? No.
  second is None → update:
    third = second = None
    second = 2
  State: first=3, second=2, third=None

num=1:
  Not duplicate.
  1 > 3? No. 1 > 2? No.
  third is None → update:
    third = 1
  State: first=3, second=2, third=1

Return third = 1 ✅
```

**Dry run — `[1, 2]`:**

```
After processing: first=2, second=1, third=None
third is None → return first = 2 ✅
```

**Dry run — `[2, 2, 3, 1]`:**

```
num=2: first=2
num=2: duplicate (2 == first=2) → skip
num=3: 3 > 2 → first=3, second=2, third=None
num=1: 1 < 3, 1 < 2, third is None → third=1
Return third = 1 ✅
```

**Why `None` instead of `-infinity`:**

```python
# Common alternative: use -infinity
first = float('-inf')

# Problem: if all numbers are -infinity, this breaks.
# Also: how do you tell "not set yet" from "legitimately set to -inf"?

# Using None:
first = None
# if first is None: → clearly "not set yet"
# if num > first when first=None: → never happens (we check None first)

# The "is None" check handles the "not initialized" state cleanly.
# None is Python's explicit "no value" — more readable than -inf.
```

**Result:** ✅ Accepted | 34/34 test cases | Runtime: 0ms | Beats 100% | Memory: 12.62MB, Beats 99.42%

## Complexity

```
Sorting approach:     Time O(n log n)   Space O(n)  — extra set/list
One-pass approach:    Time O(n)         Space O(1)  — only 3 variables
```

---

# ✅ Day 39 Task Summary

| Task | Status |
|------|--------|
| Generic play_game() method | ✅ Done |
| select_category() with dual list | ✅ Done |
| filter_characters() list comprehension | ✅ Done |
| show_remaining_candidates() | ✅ Done |
| play_again() with bool return | ✅ Done |
| 80 characters, 3 categories | ✅ Done |
| 150 questions (50 per category) | ✅ Done |
| tools/update_attributes.py | ✅ Done |
| Full end-to-end game playable | ✅ Done |
| LeetCode #414 Sorting approach | ✅ Done |
| LeetCode #414 One-pass O(1) | ✅ Accepted (0ms, 100%) |

---

# 📅 What's Coming: Days 40–42

```
Day 40: PostgreSQL Migration
  → Create postgres_repository.py
  → Implement same get_characters() and get_questions()
  → Change one line in main.py: JsonRepository → PostgresRepository
  → Game code unchanged


```

---

*Day 39 Complete. GuessWise Version 1 is fully playable. PostgreSQL migration starts tomorrow.* ✅
