# DAY 35 — REST + SQL PRACTICE + PROJECT PLANNING

> **Original Plan:** Rest + Solve 5 HackerRank SQL problems
>
> **What Actually Happened:** Solved 14 SQL problems total, completed the entire SQL LeetCode What I Study, and made a strategic decision to build a real project instead of doing boring revision.
>
> **Week:** W5 → W6 Transition
>
> **Status:** ✅ Planning Complete — Development Starts Day 36

---

# 📊 SQL Progress — 14 Problems Completed

Before Day 35 even started, the SQL practice was already far ahead of the roadmap. All planned HackerRank problems were replaced by a complete LeetCode SQL streak.

| # | Problem | Concept Learned |
|---|---------|----------------|
| ✅ 175 | Combine Two Tables | LEFT JOIN |
| ✅ 595 | Big Countries | WHERE + OR |
| ✅ 584 | Find Customer Referee | IS NULL |
| ✅ 577 | Employee Bonus | LEFT JOIN + IS NULL |
| ✅ 181 | Employees Earning More Than Their Managers | Self JOIN |
| ✅ 596 | Classes With at Least 5 Students | GROUP BY + HAVING |
| ✅ 586 | Customer Placing the Largest Number of Orders | ORDER BY + LIMIT |
| ✅ 570 | Managers with at Least 5 Direct Reports | Self JOIN + HAVING |
| ✅ 1070 | Product Sales Analysis III | Subquery + JOIN |
| ✅ 511 | Game Play Analysis I | MIN() |
| ✅ 1045 | Customers Who Bought All Products | COUNT(DISTINCT) + Scalar Subquery |
| ✅ 610 | Triangle Judgement | CASE WHEN |
| ✅ 1527 | Patients With a Condition | LIKE + Wildcards |
| ✅ **619** | **Biggest Single Number** | **MAX() + Aggregate Subquery + NULL Handling** |

**14 SQL problems solved. Every major SQL concept covered. SQL practice officially complete.**

---

# LeetCode 619 — Biggest Single Number (Today's Final Problem)

```sql
-- ═══════════════════════════════════════════════════════════════
-- LeetCode #619 — Biggest Single Number
-- Difficulty: Easy | Status: ✅ Accepted (18/18 test cases)
-- Runtime: 201ms | Memory: 0.00 MB | Beats memory: 100%
-- Topic: GROUP BY + HAVING + MAX() + Subquery + NULL Handling
-- ═══════════════════════════════════════════════════════════════

DROP TABLE IF EXISTS MyNumbers;

CREATE TABLE MyNumbers (num INT);

INSERT INTO MyNumbers VALUES
(8),(8),(3),(3),(1),(4),(5),(6),(6);

-- SOLUTION
SELECT MAX(num) AS num
FROM (
    SELECT num
    FROM MyNumbers
    GROUP BY num
    HAVING COUNT(*) = 1
) AS unique_numbers;

-- Step 1: GROUP BY num → count occurrences
-- Step 2: HAVING COUNT(*) = 1 → keep only unique numbers (1, 4, 5)
-- Step 3: MAX() → find the largest one = 5
-- Bonus: If no unique numbers exist, MAX() returns NULL automatically
-- (ORDER BY + LIMIT 1 would return no rows instead of NULL — wrong!)

-- Expected: 5
```

**Why `MAX()` instead of `ORDER BY DESC LIMIT 1`:**

```
ORDER BY + LIMIT 1 on an empty result → returns ZERO rows
MAX() on an empty result              → returns NULL

The problem says: "If there is no single number, return NULL."
MAX() handles this correctly. LIMIT does not.
```

---

# 🔄 Why I'm Changing the Plan

## The Original Plan for Days 36–42

```
Days 36–42 (Week 6): Python Revision
  → Revisit Python basics
  → Practice OOP
  → Practice decorators, generators
  → Solve DSA problems
```

## The Problem With Boring Revision

Reading notes you already know feels meaningless.

Solving random LeetCode problems without a goal feels disconnected.

After 5 weeks of intense learning — Python, HTTP, Git, SQL, SQLAlchemy — the brain needs to **apply** knowledge, not just re-read it.

## The Better Approach

> **Instead of revising Python by reading, revise Python by building.**

Build a real project that forces you to use:

```
Variables           → Character properties, question text
Data Types          → Strings, booleans, integers, lists, dicts
Functions           → Game logic, filtering, display
Loops               → Question loop, filtering loop
Conditions          → Matching attributes, answer validation
Lists               → Character lists, question lists
Tuples              → Immutable config values
Dictionaries        → Character attribute storage
Sets                → Unique answers tracking
Classes             → Character, Question, Game, Repository
Objects             → Every character and question is an object
JSON                → Data storage in Version 1
File Handling       → Reading JSON files
SQL                 → Character/question database in Version 2
PostgreSQL          → Production database backend
SQLAlchemy          → ORM connecting Python to PostgreSQL
Architecture        → Layered design, Repository Pattern
Clean Code          → Single responsibility, readable names
```

**One project. Every concept used naturally. No boring revision.**

---

# ✦ MONTH 2 CHECKPOINT — DAY 42

The roadmap milestone at Day 42 shows exactly what needs to be achieved:

```
✅ Write Python classes, decorators, generators without help
✅ Write complex SQL JOIN queries
✅ Understand async/await in Python
✅ Know all HTTP methods and status codes by heart
✅ Explain OOP (4 pillars) in an interview right now
✅ Design a basic database schema on paper
✅ Have 2+ projects on GitHub with README
✅ Can use SQLAlchemy to connect Python to PostgreSQL
```

A revision exercise doesn't tick these boxes. A **real project does.**

The GuessWise project will touch all of these by Day 42:

```
OOP (4 pillars)      → Character, Game, Engine, Repository classes
Database schema      → characters, questions, attributes tables designed today
GitHub with README   → Full project pushed to GitHub on Day 42
SQLAlchemy + PG      → Version 2 replaces JSON with PostgreSQL
```

---

# 🎯 The Project: GuessWise

## What Is It?

An **Akinator-inspired CLI guessing game** — the classic "think of a character and I'll guess who it is."

```
User thinks of a character (e.g. Virat Kohli)

Game asks:
  → Is your character real? [y/n] y
  → Is your character male? [y/n] y
  → Is your character Indian? [y/n] y
  → Is your character a cricketer? [y/n] y

Game has only 1 character left → Virat Kohli

Game says: "Is your character Virat Kohli?"

User: Yes!

Game wins.
```

## Why This Project?

```
It's simple enough to finish in 7 days.
It's complex enough to teach real architecture.
It requires OOP, JSON, SQL, SQLAlchemy — everything from the last 5 weeks.
It produces a GitHub portfolio project that looks professional.
It is something you can demo in an interview.
```

---

# 📁 Project Architecture

## The Concept: Separation of Concerns

The most important backend principle: **every layer only does one thing.**

```
┌─────────────────────────────────────┐
│         PRESENTATION LAYER          │
│   main.py — CLI entry point         │
│   display.py — all print statements │
└──────────────────┬──────────────────┘
                   │
┌──────────────────▼──────────────────┐
│          BUSINESS LAYER             │
│   game.py — game loop control       │
│   question_engine.py — asks Q's     │
│   character_engine.py — filters     │
└──────────────────┬──────────────────┘
                   │
┌──────────────────▼──────────────────┐
│            DATA LAYER               │
│   repository.py — abstract base     │
│   json_repository.py — reads JSON   │
│   postgres_repository.py — reads DB │
└──────────────────┬──────────────────┘
                   │
┌──────────────────▼──────────────────┐
│              STORAGE                │
│   data/characters.json (Version 1)  │
│   PostgreSQL database  (Version 2)  │
└─────────────────────────────────────┘
```

## Final Folder Structure

```
GuessWise/
│
├── src/
│   ├── main.py                    ← Entry point
│   ├── game.py                    ← Game loop
│   │
│   ├── engines/
│   │   ├── character_engine.py    ← Filtering logic
│   │   └── question_engine.py     ← Question + validation
│   │
│   ├── repository/
│   │   ├── repository.py          ← Abstract base
│   │   ├── json_repository.py     ← JSON implementation
│   │   └── postgres_repository.py ← PostgreSQL implementation
│   │
│   ├── models/
│   │   ├── character.py           ← Character class
│   │   └── question.py            ← Question class
│   │
│   ├── utils/
│   │   ├── display.py             ← All print/UI
│   │   └── validation.py          ← Input validation
│   │
│   └── config.py                  ← Constants, paths, settings
│
├── data/
│   ├── characters.json
│   └── questions.json
│
├── tests/
├── docs/
├── README.md
├── requirements.txt
└── .gitignore
```

---

# 🗂 Data Design

## characters.json

```json
[
  {
    "name": "Virat Kohli",
    "real": true,
    "male": true,
    "indian": true,
    "cricketer": true,
    "fictional": false,
    "musician": false,
    "actor": false,
    "athlete": true
  },
  {
    "name": "Naruto",
    "real": false,
    "male": true,
    "indian": false,
    "cricketer": false,
    "fictional": true,
    "musician": false,
    "actor": false,
    "athlete": false
  },
  {
    "name": "A.R. Rahman",
    "real": true,
    "male": true,
    "indian": true,
    "cricketer": false,
    "fictional": false,
    "musician": true,
    "actor": false,
    "athlete": false
  }
]
```

## questions.json

```json
[
  {
    "question": "Is your character a real person?",
    "property": "real"
  },
  {
    "question": "Is your character male?",
    "property": "male"
  },
  {
    "question": "Is your character Indian?",
    "property": "indian"
  },
  {
    "question": "Is your character a cricketer?",
    "property": "cricketer"
  },
  {
    "question": "Is your character fictional?",
    "property": "fictional"
  },
  {
    "question": "Is your character a musician?",
    "property": "musician"
  }
]
```

---

# 🏗 Version 2 Database Schema

When the project moves from JSON to PostgreSQL:

```sql
CREATE TABLE characters (
    id   SERIAL      PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE attributes (
    id           SERIAL       PRIMARY KEY,
    character_id INTEGER      REFERENCES characters(id) ON DELETE CASCADE,
    key          VARCHAR(50)  NOT NULL,
    value        BOOLEAN      NOT NULL
);

CREATE TABLE questions (
    id       SERIAL      PRIMARY KEY,
    text     TEXT        NOT NULL,
    property VARCHAR(50) NOT NULL
);
```

---

# 🔑 The Repository Pattern

The most important architectural concept in this project.

```
WITHOUT Repository Pattern:

game.py contains:
  with open("characters.json") as f:
      characters = json.load(f)

Problem:
  When you switch to PostgreSQL,
  you rewrite game.py.
  Business logic and data logic are mixed.


WITH Repository Pattern:

game.py contains:
  characters = repository.load_characters()

json_repository.py contains:
  def load_characters():
      with open("characters.json") as f:
          return json.load(f)

postgres_repository.py contains:
  def load_characters():
      return session.query(Character).all()

Game never changes.
Only the repository implementation swaps.
THIS IS HOW PROFESSIONAL BACKENDS ARE BUILT.
```

---

# 📅 Day-by-Day Plan

| Day | Goal | Deliverable |
|-----|------|-------------|
| **35** | Planning + Architecture | This document ✅ |
| **36** | Project structure + Models + JSON loading | Characters and questions load correctly |
| **37** | Question Engine + Input validation + CLI | Game asks questions, validates answers |
| **38** | Character Engine + Filtering + Guess logic | Game plays end-to-end |
| **39** | Refactor + Error handling + Polish | Stable, clean Version 1 |
| **40** | PostgreSQL + SQLAlchemy + postgres_repository | Database replaces JSON, game unchanged |
| **41** | Admin CRUD + Add/Delete/Update characters | Full admin CLI operations |
| **42** | Tests + README + GitHub release | v1.0 on GitHub, LinkedIn post |

---

# 🧠 OOP Classes Overview

```python
class Character:
    """Represents one character in the game."""
    name: str
    attributes: dict   # {"real": True, "male": True, "indian": True}

    def matches(self, property: str, answer: bool) -> bool:
        """Returns True if character's property matches the answer."""

    def display(self) -> str:
        """Returns formatted display string."""


class Question:
    """Represents one yes/no question."""
    text: str
    property: str      # The attribute key this question targets

    def ask(self) -> str:
        """Returns the question text for display."""


class Repository:
    """Abstract base — defines the interface for data access."""
    def load_characters(self) -> list[Character]: ...
    def load_questions(self)  -> list[Question]: ...


class JsonRepository(Repository):
    """Loads data from JSON files."""
    def load_characters(self) -> list[Character]: ...
    def load_questions(self)  -> list[Question]: ...


class CharacterEngine:
    """Filters characters based on answers."""
    remaining: list[Character]

    def filter(self, property: str, answer: bool) -> None: ...
    def count(self) -> int: ...
    def guess(self) -> Character: ...


class QuestionEngine:
    """Manages the question flow."""
    questions: list[Question]
    current_index: int

    def next_question(self) -> Question | None: ...
    def validate_answer(self, answer: str) -> bool: ...


class Game:
    """Controls the entire game flow."""
    character_engine: CharacterEngine
    question_engine: QuestionEngine

    def start(self) -> None: ...
    def play(self) -> None: ...
    def guess(self) -> None: ...
    def restart(self) -> None: ...
```

---

# 🎯 Filtering Algorithm

```
Start: All characters loaded (e.g. 20 characters)

Loop:
  1. Get next question from QuestionEngine
  2. Display question to user
  3. Get yes/no answer
  4. CharacterEngine.filter(property, answer)
     → Remove all characters where attribute ≠ answer
  5. CharacterEngine.count()
     → If 1 remaining: guess()
     → If 0 remaining: "I give up! Who were you thinking of?"
     → If questions exhausted: guess best remaining

Guess:
  "Is your character [name]?"
  → Yes: "I win! 🎉"
  → No: "I give up! 🤔"
```

---

# 📋 Coding Standards for This Project

```
Language:    Python 3.10+
Style:       PEP 8
Line length: Maximum 100 characters
Types:       Type hints on all functions
Docstrings:  Every class and method
Constants:   All in config.py (no magic strings/numbers)
Commits:     Conventional Commits (feat:, fix:, refactor:)
Branches:    feature/models, feature/game, feature/database
```

---

# 🎯 Success Criteria at Day 42

By the end of Day 42, GuessWise v1.0 should:

```
✅ Play a complete game from start to finish in the terminal
✅ Correctly filter characters based on yes/no answers
✅ Store data in JSON (Version 1) AND PostgreSQL (Version 2)
✅ Follow layered architecture — game never knows where data comes from
✅ Have zero hardcoded strings in business logic
✅ Have a complete README with screenshots
✅ Be pushed to GitHub with a proper release tag (v1.0)
✅ Demonstrate OOP, JSON, SQLAlchemy, Repository Pattern
✅ Be something you can talk about in a backend interview
```

---

# 📝 Reflection on Week 5

## What Was Accomplished (Days 29–35)

```
Day 29: SQL basics — CREATE TABLE, SELECT, INSERT, UPDATE, DELETE
Day 30: SQL JOINs — INNER, LEFT, RIGHT, FULL OUTER, SELF JOIN
Day 31: Aggregations — GROUP BY, HAVING, ORDER BY, LIMIT, subqueries
Day 32: Database design — Primary Keys, Foreign Keys, indexes, e-commerce schema
Day 33: Transactions — BEGIN, COMMIT, ROLLBACK, ACID, N+1 problem
Day 34: SQLAlchemy ORM — models, sessions, CRUD, relationships, FastAPI integration
Day 35: 14 LeetCode SQL problems ✅ + project planning ✅
```

## SQL Concepts Mastered

```
✅ SELECT, WHERE, GROUP BY, HAVING, ORDER BY, LIMIT, OFFSET
✅ All aggregate functions: COUNT, SUM, AVG, MAX, MIN
✅ All JOIN types: INNER, LEFT, RIGHT, FULL OUTER, SELF
✅ Subqueries: in WHERE, FROM (derived table), SELECT (scalar)
✅ CASE WHEN, LIKE, IS NULL, BETWEEN, IN
✅ Transactions: BEGIN, COMMIT, ROLLBACK, SAVEPOINT, ACID
✅ Database design: PKs, FKs, UNIQUE, NOT NULL, indexes
✅ SQLAlchemy: models, sessions, CRUD, relationships, FastAPI integration
✅ 14 LeetCode database problems solved ⭐
```

---

# 🚀 Looking Ahead: Week 6 (Days 36–42)

Week 6 is no longer revision week. It is **build week.**

```
The next 7 days will produce:
  → A complete CLI application (GuessWise)
  → Two storage backends (JSON and PostgreSQL)
  → Clean layered architecture
  → Professional GitHub repository
  → A project you can demo in interviews
  → Natural revision of every Python and SQL concept from the last 5 weeks
```

The original roadmap said revision. The new plan says build.

**Building is better than revising. Always.**

---

*Day 35 Complete. Planning done. Code starts tomorrow.* ✅

