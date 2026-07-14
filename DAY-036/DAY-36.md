# DAY 36 — GuessWise: Project Initialization + Architecture Design

> **Project:** GuessWise — Akinator-inspired CLI Guessing Game
>
> **Phase:** Project Initialization + Design (No code written yet)
>
> **Path:** `C:\A_MY THINGS\001\Backend-Developer-Journey\Project\GuessWise`
>
> **Status:** ✅ Day 36 Complete — Design phase done, coding starts Day 37

---

# 🎯 What Day 36 Was About

Day 36 was not about writing code.

It was about **thinking before coding** — the professional approach that separates good developers from average ones.

Before you write a single line of implementation:

```
You need to know:   What are you building?
You need to know:   How is the data structured?
You need to know:   How do the layers connect?
You need to know:   What changes when you switch from JSON to PostgreSQL?
You need to know:   What stays the same?
```

Every decision made today saves hours of refactoring later.

---

# ✅ Day 36 Completion Checklist

```
✅ Project initialized
✅ Folder structure created in VS Code
✅ Virtual environment (.venv) created and activated
✅ Documentation started (GuessWise.md)
✅ High-level architecture designed
✅ Repository pattern decided
✅ Data flow designed
✅ Character model concept designed
✅ Question model concept designed
✅ JSON design discussed and finalized
✅ PostgreSQL migration strategy planned

🎉 Day 36 officially complete.
   Planning and design phase finished before implementation code begins.
```

---

# 📁 Project Location

```
Root folder:     C:\A_MY THINGS\001\Backend-Developer-Journey\
Project folder:  C:\A_MY THINGS\001\Backend-Developer-Journey\Project\GuessWise\
```

**Note on repository and README:**

GuessWise currently lives inside the existing `Backend-Developer-Journey` folder, which is already a Git repository. No separate `git init` needed right now. No separate `.gitignore` needed right now.

When GuessWise is pushed as its own repository on GitHub (Day 42), that is when we add:

```
README.md        (rename GuessWise.md → README.md at that point)
.gitignore       (add proper Python .gitignore)
LICENSE
requirements.txt (filled with actual dependencies)
```

For now: GuessWise.md serves as the design document and will become README.md later.

---

# 📁 Folder Structure Created

Exactly as visible in VS Code:

```
GuessWise/
│
├── data/
│   ├── characters.json
│   └── questions.json
│
├── engines/
│   ├── __init__.py
│   ├── character_engine.py
│   └── question_engine.py
│
├── models/
│   ├── __init__.py
│   ├── character.py
│   └── question.py
│
├── repository/
│   ├── __init__.py
│   ├── repository.py
│   └── json_repository.py
│
├── tests/
│
├── utils/
│   ├── __init__.py
│   ├── display.py
│   └── validation.py
│
├── .venv/               ← Virtual environment (not committed)
├── requirements.txt     ← To install Python packages
├── game.py
├── GuessWise.md         ← Design document 
├── main.py
└── structure.scss       ← Folder structure notes
```

**Why `__init__.py` in every package?**

```
Python needs __init__.py to recognize a folder as a package.
Without it: import engines.character_engine would fail.
With it:    Python knows engines/ is a module you can import from.
```

---

# 🖥 Environment Setup

```bash
# Virtual environment created and activated:
python -m venv .venv
.venv\Scripts\activate

# Confirmed:
Python 3.12.3
```

---

# 🏗 Architecture Design (Phase 1)

## The Core Problem This Architecture Solves

**Without good architecture:**

```
Day 40: "Switch from JSON to PostgreSQL"
→ You open game.py
→ It has 50 lines of json.load() mixed with game logic
→ You rewrite everything
→ You break the game
→ 3 hours wasted
```

**With the Repository Pattern:**

```
Day 40: "Switch from JSON to PostgreSQL"
→ Create postgres_repository.py
→ Implement same 2 methods: load_characters(), load_questions()
→ Change one line in main.py: repository = PostgresRepository()
→ Game works. Nothing else changed.
→ 30 minutes.
```

**This is what "professional architecture" means.**

---

## The Layers

```
┌──────────────────────────────────────────┐
│           PRESENTATION LAYER             │
│                                          │
│  main.py      → Entry point, CLI menu    │
│  display.py   → All print statements     │
│  validation.py → Input validation        │
│                                          │
│  Rule: No business logic here.           │
│  Only: "what does the user see/type?"    │
└─────────────────────┬────────────────────┘
                      │
┌─────────────────────▼────────────────────┐
│            BUSINESS LAYER                │
│                                          │
│  game.py              → Game loop        │
│  character_engine.py  → Filtering        │
│  question_engine.py   → Question flow    │
│                                          │
│  Rule: No SQL here. No JSON here.        │
│  Only: "what does the game DO?"          │
└─────────────────────┬────────────────────┘
                      │
┌─────────────────────▼────────────────────┐
│              DATA LAYER                  │
│                                          │
│  repository.py         → Abstract base   │
│  json_repository.py    → JSON impl       │
│  postgres_repository.py → PostgreSQL impl│
│                                          │
│  Rule: No game logic here.               │
│  Only: "how do we get/save data?"        │
└─────────────────────┬────────────────────┘
                      │
┌─────────────────────▼────────────────────┐
│               STORAGE                    │
│                                          │
│  data/characters.json  (Version 1)       │
│  data/questions.json   (Version 1)       │
│  PostgreSQL database   (Version 2)       │
└──────────────────────────────────────────┘
```

---

## The Repository Pattern Explained

```python
# repository.py (the CONTRACT — abstract base class)
class Repository:
    def load_characters(self) -> list:
        raise NotImplementedError

    def load_questions(self) -> list:
        raise NotImplementedError


# json_repository.py (Version 1 implementation)
class JsonRepository(Repository):
    def load_characters(self) -> list:
        with open("data/characters.json") as f:
            return json.load(f)

    def load_questions(self) -> list:
        with open("data/questions.json") as f:
            return json.load(f)


# postgres_repository.py (Version 2 implementation — Day 40)
class PostgresRepository(Repository):
    def load_characters(self) -> list:
        return session.query(Character).all()

    def load_questions(self) -> list:
        return session.query(Question).all()


# main.py
repository = JsonRepository()        # Day 36-39
# repository = PostgresRepository()  # Day 40+ (one line change!)

game = Game(repository)
game.start()
```

**The Game class never knows whether data comes from JSON or PostgreSQL.**
**This is the core principle: separate "what" from "how".**

---

# 📊 Data Design (Phase 2)

## Game Menu Design

```
===== GuessWise =====

1. Character (Person — real or fictional)
2. Animal
3. Object
4. Movie
5. Place
6. Exit

Choose a category: _
```

Why categories? They shrink the search space. Fewer characters to filter = fewer questions needed to guess.

---

## Question Flow (Decision Tree Concept)

```
Character selected:

Is your character real? [y/n]
           │
    ┌──────┴──────┐
    YES            NO
    │              │
Is alive?      Fictional Universe?
    │              │
 Dead?         Anime / Marvel / DC?
    │
 Profession?
    │
 Country?
    │
 Political role?
```

This is essentially a **binary decision tree**. In the future, the engine will pick the question that divides remaining characters most evenly (information gain). For Version 1, questions are asked in a fixed order.

---

## characters.json — Final Design

```json
[
  {
    "id": 1,
    "name": "Virat Kohli",
    "category": "character",
    "properties": {
      "real": true,
      "male": true,
      "alive": true,
      "indian": true,
      "cricketer": true,
      "actor": false,
      "musician": false,
      "fictional": false,
      "married": true
    }
  },
  {
    "id": 2,
    "name": "Naruto",
    "category": "character",
    "properties": {
      "real": false,
      "male": true,
      "alive": true,
      "indian": false,
      "cricketer": false,
      "actor": false,
      "musician": false,
      "fictional": true,
      "married": false
    }
  },
  {
    "id": 3,
    "name": "A.R. Rahman",
    "category": "character",
    "properties": {
      "real": true,
      "male": true,
      "alive": true,
      "indian": true,
      "cricketer": false,
      "actor": false,
      "musician": true,
      "fictional": false,
      "married": true
    }
  },
  {
    "id": 4,
    "name": "Hermione Granger",
    "category": "character",
    "properties": {
      "real": false,
      "male": false,
      "alive": true,
      "indian": false,
      "cricketer": false,
      "actor": false,
      "musician": false,
      "fictional": true,
      "married": false
    }
  },
  {
    "id": 5,
    "name": "Priyanka Chopra",
    "category": "character",
    "properties": {
      "real": true,
      "male": false,
      "alive": true,
      "indian": true,
      "cricketer": false,
      "actor": true,
      "musician": false,
      "fictional": false,
      "married": true
    }
  }
]
```

**Why `properties` is nested (not top-level)?**

```
Top-level (bad for PostgreSQL migration):
{
  "name": "Virat Kohli",
  "real": true,
  "male": true,
  ...
}

When you migrate to PostgreSQL:
  Every property needs its own column.
  Adding a new property = ALTER TABLE.
  Breaks everything.

Nested properties (good for PostgreSQL migration):
{
  "name": "Virat Kohli",
  "properties": {"real": true, "male": true}
}

When you migrate to PostgreSQL:
  CREATE TABLE character_properties (character_id, property, value)
  Adding a new property = INSERT a new row.
  Nothing breaks.

Our JSON design already thinks about the database.
```

---

## questions.json — Final Design

```json
[
  {
    "id": 1,
    "question": "Is your character a real person?",
    "property": "real"
  },
  {
    "id": 2,
    "question": "Is your character male?",
    "property": "male"
  },
  {
    "id": 3,
    "question": "Is your character still alive?",
    "property": "alive"
  },
  {
    "id": 4,
    "question": "Is your character Indian?",
    "property": "indian"
  },
  {
    "id": 5,
    "question": "Is your character a cricketer?",
    "property": "cricketer"
  },
  {
    "id": 6,
    "question": "Is your character an actor?",
    "property": "actor"
  },
  {
    "id": 7,
    "question": "Is your character a musician?",
    "property": "musician"
  },
  {
    "id": 8,
    "question": "Is your character fictional (from a book, movie, or game)?",
    "property": "fictional"
  },
  {
    "id": 9,
    "question": "Is your character married?",
    "property": "married"
  }
]
```

**How a question maps to a character property:**

```
Question:  "Is your character Indian?"
Property:  "indian"

User answers "yes"
→ CharacterEngine filters: keep characters where properties["indian"] == True
→ Virat Kohli: properties["indian"] = true  ✅ stays
→ Naruto: properties["indian"] = false       ❌ removed

User answers "no"
→ Keep characters where properties["indian"] == False
→ Naruto stays, Virat Kohli removed
```

---

## Future-Proof Question Design (Version 3+)

```json
{
  "id": 1,
  "text": "Is your character real?",
  "property": "real",
  "type": "boolean"
}
```

```json
{
  "id": 15,
  "text": "What continent is your character from?",
  "property": "continent",
  "type": "choice",
  "choices": ["Asia", "Europe", "Americas", "Africa", "Australia"]
}
```

Not needed now. But our design doesn't prevent it. Version 1 uses boolean only.

---

# 🧠 Key Concepts Decided Today

## Separation of Data and Behavior

```
Character object = WHAT the character IS (data)
  name: "Virat Kohli"
  properties: {real: True, indian: True, cricketer: True}

Question object = WHAT to ASK the user (behavior description)
  question: "Is your character Indian?"
  property: "indian"

Character never knows how questions are asked.
Question never knows about characters.
The ENGINE connects them during the game loop.
```

## Why Game Shouldn't Read JSON Directly

```
Bad (tightly coupled):
  class Game:
      def start(self):
          with open("data/characters.json") as f:   ← JSON reading in game
              self.characters = json.load(f)

Good (loosely coupled):
  class Game:
      def __init__(self, repository):
          self.characters = repository.load_characters()   ← game doesn't know where data comes from

Version 1: repository = JsonRepository()
Version 2: repository = PostgresRepository()
Game.start() doesn't change at all.
```

## PostgreSQL Migration Plan (Already Designed)

```
Version 1 tables are already reflected in the JSON structure:

JSON structure:         Future PostgreSQL tables:
─────────────────       ──────────────────────────
characters.json    →    characters (id, name, category)
  └── properties   →    character_properties (character_id, property, value)
questions.json     →    questions (id, question, property)
```

The transition from JSON to PostgreSQL on Day 40 will be smooth because the data was designed with the database in mind from the start.

---

# 🔁 Data Flow Diagram

```
Program Start
      │
      ▼
main.py loads
      │
      ▼
Repository.load_characters()   ← JSON (now) or PostgreSQL (later)
Repository.load_questions()
      │
      ▼
Character objects created
Question objects created
      │
      ▼
Game.start()
      │
      ▼
Show menu → User picks category
      │
      ▼
QuestionEngine gets next question
      │
      ▼
Display question → User answers yes/no
      │
      ▼
CharacterEngine.filter(property, answer)
→ Remove characters that don't match
      │
      ▼
CharacterEngine.count() == 1?
      │
   ┌──┴──┐
  YES    NO
   │      │
Guess   Ask next question
   │
   ▼
"Is your character [name]?"
   │
User confirms → Game wins
   │
User denies → Game loses
```

---

# 📅 What's Coming: Day 37

Tomorrow the real coding begins. No more planning. Implementation starts.

## Day 37 Goals

```
1. Character model  →  models/character.py
   - Python dataclass
   - name, category, properties
   - matches() method
   - display() method

2. Question model   →  models/question.py
   - Python dataclass
   - id, question text, property
   - ask() method

3. Repository interface  →  repository/repository.py
   - Abstract base class
   - load_characters() method
   - load_questions() method

4. JSON Repository  →  repository/json_repository.py
   - Reads characters.json
   - Reads questions.json
   - Returns Character and Question objects

5. Test in main.py
   - Load characters
   - Load questions
   - Print them
   - Confirm: data layer works
```

**By end of Day 37:**

The game won't play yet. But it will be able to load structured data into Python objects — which is the foundation that all game logic sits on top of.

```
Day 37: Data loads correctly ✅
Day 38: Questions asked + filtering works ✅
Day 39: Full game playable ✅
Day 40: PostgreSQL replaces JSON ✅
Day 41: Admin CRUD operations ✅
Day 42: GitHub release ✅
```

---

# 🧠 Software Engineering Lessons From Day 36

```
1. Always design before coding.
   A clear architecture saves hours of refactoring.

2. The Repository Pattern separates data access from business logic.
   When you change storage (JSON → PostgreSQL), only the repository changes.
   The game logic stays untouched.

3. Data design determines database design.
   The JSON structure we chose maps directly to PostgreSQL tables.
   No surprises on migration day.

4. __init__.py makes a folder a Python package.
   Without it, imports fail.

5. Virtual environments isolate project dependencies.
   Never install packages globally.

6. Nested properties are more flexible than flat properties.
   Adding new character attributes doesn't break existing code.

7. A professional project separates:
   What the user sees (presentation)
   What the game does (business logic)
   Where data comes from (data layer)
   Never mix these three.
```

---

*Day 36 Complete. Architecture designed. Folder structure created. Coding starts tomorrow.* ✅
