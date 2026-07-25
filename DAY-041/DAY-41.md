# DAY 41 — GuessWise: PostgreSQL Migration, SQLAlchemy ORM + LeetCode Array Concatenation

> **Project:** GuessWise — JSON replaced by PostgreSQL (full migration complete)
>
> **Path:** `C:\A_MY THINGS\001\Backend-Developer-Journey\Project\GuessWise`
>
> **LeetCode:** #1929 Concatenation of Array ✅ (0ms · Beats 100%)
>
> **Status:** ✅ Day 41 Complete - GuessWise now runs on a real production database

---

# 🎯 What Was Built Today

```
✅ database/database.py      — SQLAlchemy engine + session + Base
✅ database/models.py        — 4 ORM models (Character, Attribute, CharacterAttribute, Question)
✅ database/create_tables.py — Creates all tables from Python classes
✅ database/seed.py          — Seeder class: reads JSON, populates PostgreSQL
✅ database/run_seed.py      — One-command database setup
✅ repository/postgres_repository.py — PostgresRepository implementing the interface
✅ game.py                   — ONE LINE CHANGED: JsonRepository → PostgresRepository
✅ LeetCode #1929 solved (3 approaches: Two Loops, One Loop, Pythonic)
```

**The entire game works identically. Only the data source changed.**

---

# 📁 Final Project State After Day 41

```
GuessWise/
│
├── main.py                          ← unchanged (3 lines)
├── game.py                          ← ONE LINE CHANGED
│
├── models/                          ← Game models (unchanged)
│   ├── character.py                 ← @dataclass: id, name, category, attributes
│   └── question.py                  ← @dataclass: id, category, text, attribute
│
├── repository/
│   ├── repository.py                ← ABC interface (unchanged)
│   ├── json_repository.py          ← Version 1 (still works)
│   └── postgres_repository.py      ← ✅ NEW — reads from PostgreSQL
│
├── engines/
│   ├── character_engine.py          ← unchanged
│   └── question_engine.py          ← unchanged
│
├── database/                        ← ✅ ENTIRE NEW LAYER
│   ├── __init__.py
│   ├── database.py                  ← Engine, SessionLocal, Base
│   ├── models.py                    ← ORM Models (4 classes)
│   ├── create_tables.py             ← Creates all tables
│   ├── seed.py                      ← Seeder class
│   └── run_seed.py                  ← Entry point for setup
│
├── tools/
│   └── update_attributes.py
│
└── data/
    ├── characters.json              ← still used by Seeder
    └── questions.json               ← still used by Seeder
```

---

# SECTION 1 — WHY MIGRATE FROM JSON TO POSTGRESQL?

## The Problem With JSON

Until Day 40, GuessWise stored all data in two JSON files:

```
characters.json  → 80 characters, each with 51 attributes
questions.json   → 150 questions across 3 categories
```

This worked fine for a local CLI tool, but it fails as soon as the application needs to grow:

```
JSON limitations:
  ❌ Cannot query efficiently (no WHERE, no JOIN, no INDEX)
  ❌ Cannot support multiple concurrent users
  ❌ Cannot build an admin dashboard easily
  ❌ Cannot add/delete/update a single character without reading the whole file
  ❌ Cannot scale beyond a single machine
  ❌ No referential integrity (nothing prevents broken data)
  ❌ Every "query" loads the entire file into memory

PostgreSQL advantages:
  ✅ Efficient queries with WHERE, JOIN, INDEX
  ✅ Handles thousands of concurrent connections
  ✅ Admin dashboards can query it directly
  ✅ Update a single row without touching the rest
  ✅ Scales to millions of records
  ✅ Foreign keys enforce data integrity
  ✅ Only loads the data you ask for
```

## The Key Principle: Swap the Storage, Keep the Game

The Repository Pattern was built for exactly this moment:

```
Before Day 41:
  game.py: self.repository = JsonRepository()

After Day 41:
  game.py: self.repository = PostgresRepository()

Everything else: UNCHANGED.
  game.py (besides that one line)  → unchanged
  character_engine.py              → unchanged
  question_engine.py               → unchanged
  models/character.py              → unchanged
  models/question.py               → unchanged
  main.py                          → unchanged
```

**One line changed. The entire backend swapped. This is why architecture matters.**

---

# SECTION 2 — THE NEW DATABASE LAYER

## database/database.py — The Connection Configuration

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase


DATABASE_URL = "postgresql+psycopg2://postgres:postgres123@localhost:5432/guesswise"

engine = create_engine(
    DATABASE_URL,
    echo=False
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)


class Base(DeclarativeBase):
    pass
```

**Every line explained:**

```python
DATABASE_URL = "postgresql+psycopg2://postgres:postgres123@localhost:5432/guesswise"

# Breaking this down:
# postgresql    → database type (tells SQLAlchemy: generate PostgreSQL SQL syntax)
# +psycopg2     → the driver that physically sends SQL over the network
# postgres      → PostgreSQL username
# postgres123   → PostgreSQL password (NEVER commit this to GitHub!)
# @localhost    → host (our own machine)
# :5432         → port (PostgreSQL's default)
# /guesswise    → database name in PostgreSQL
```

```python
engine = create_engine(DATABASE_URL, echo=False)

# create_engine() doesn't immediately connect to PostgreSQL.
# It creates a CONNECTION FACTORY — a configuration object.
# Actual connection happens only when the first query is executed (lazy).

# echo=False: don't print SQL statements to console (set True for debugging)
# In development: echo=True shows every SQL query SQLAlchemy generates
# In production: echo=False to avoid flooding logs
```

```python
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

# sessionmaker() creates a Session FACTORY — not a session itself.
# Every time you call SessionLocal(), you get a new session.

# A Session is like a conversation with PostgreSQL:
#   session = SessionLocal()    → open the conversation
#   session.query(...)          → ask a question
#   session.add(obj)            → stage a change
#   session.commit()            → save permanently
#   session.close()             → end the conversation

# autoflush=False:  don't auto-flush before queries (more control)
# autocommit=False: changes must be explicitly committed (safer)
```

```python
class Base(DeclarativeBase):
    pass

# Base is the parent class for ALL database models.
# Every table you create inherits from Base.
# Base knows about all models and can create their tables.

# class Character(Base):  ← Character table
# class Attribute(Base):  ← Attribute table
# etc.

# DeclarativeBase (SQLAlchemy 2.0+ style) is cleaner than
# the old declarative_base() function.
```

---

## Why We Created a Separate `database/` Folder

```
Before Day 41:
  No database folder. Data came from JSON files.

After Day 41:
  database/
    database.py      — connection configuration
    models.py        — table definitions (ORM models)
    create_tables.py — creates tables in PostgreSQL
    seed.py          — populates tables from JSON
    run_seed.py      — runs everything with one command

Single Responsibility Principle at the FOLDER level:
  database/ = everything about PostgreSQL setup and schema
  repository/ = everything about getting/saving data
  models/ = game-level data shapes
  engines/ = game logic
```

---

## database/models.py - The Four ORM Models

This file contains the most complex design decision of the entire project: **database normalization using an association table**.

```python
from sqlalchemy import (
    String,
    Boolean,
    ForeignKey
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from database.database import Base
```

### The Database Schema

```
Before (JSON structure — flat attributes):
  Character: {name, category, attributes: {real: true, male: true, ...}}

After (normalized relational schema):

characters table:           attributes table:
┌────┬──────────────┬──────────┐    ┌────┬───────────┐
│ id │ name         │ category │    │ id │ name      │
├────┼──────────────┼──────────┤    ├────┼───────────┤
│  1 │ Virat Kohli  │ character│    │  1 │ real      │
│  2 │ Naruto       │ character│    │  2 │ male      │
└────┴──────────────┴──────────┘    │  3 │ alive     │
                                    │  4 │ indian    │
character_attributes (junction):    └────┴───────────┘
┌──────────────┬──────────────┬───────┐
│ character_id │ attribute_id │ value │
├──────────────┼──────────────┼───────┤
│      1       │      1       │  True │  (Virat, real, True)
│      1       │      2       │  True │  (Virat, male, True)
│      1       │      4       │  True │  (Virat, indian, True)
│      2       │      1       │ False │  (Naruto, real, False)
└──────────────┴──────────────┴───────┘

questions table:
┌────┬───────────┬──────────────────────────────┬──────────────┐
│ id │ category  │ text                         │ attribute_id │
├────┼───────────┼──────────────────────────────┼──────────────┤
│  1 │ character │ Is your character real?      │      1       │
│  2 │ character │ Is your character male?      │      2       │
└────┴───────────┴──────────────────────────────┴──────────────┘
```

### The Complete models.py

```python
from sqlalchemy import (
    String,
    Boolean,
    ForeignKey
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from database.database import Base


class Character(Base):
    __tablename__ = "characters"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(100))

    category: Mapped[str] = mapped_column(String(50))

    attributes: Mapped[list["CharacterAttribute"]] = relationship(
        back_populates="character",
        cascade="all, delete-orphan"
    )


class Attribute(Base):
    __tablename__ = "attributes"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(
        String(100),
        unique=True
    )

    questions: Mapped[list["Question"]] = relationship(
        back_populates="attribute"
    )

    characters: Mapped[list["CharacterAttribute"]] = relationship(
        back_populates="attribute"
    )


class CharacterAttribute(Base):
    __tablename__ = "character_attributes"

    character_id: Mapped[int] = mapped_column(
        ForeignKey("characters.id"),
        primary_key=True
    )

    attribute_id: Mapped[int] = mapped_column(
        ForeignKey("attributes.id"),
        primary_key=True
    )

    value: Mapped[bool] = mapped_column(Boolean)

    character: Mapped["Character"] = relationship(
        back_populates="attributes"
    )

    attribute: Mapped["Attribute"] = relationship(
        back_populates="characters"
    )


class Question(Base):
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(primary_key=True)

    category: Mapped[str] = mapped_column(String(50))

    text: Mapped[str] = mapped_column(String(255))

    attribute_id: Mapped[int] = mapped_column(
        ForeignKey("attributes.id")
    )

    attribute: Mapped["Attribute"] = relationship(
        back_populates="questions"
    )
```

### Every Design Decision Explained

**Why `Mapped[int]` and `mapped_column()` instead of `Column(Integer)`?**

```python
# OLD SQLAlchemy 1.x style:
id = Column(Integer, primary_key=True)

# NEW SQLAlchemy 2.0 style (what we use):
id: Mapped[int] = mapped_column(primary_key=True)

# The new style:
# ✅ Has Python type hints → Pylance autocomplete works
# ✅ Type-safe → mypy can catch bugs before runtime
# ✅ Cleaner syntax
# ✅ SQLAlchemy 2.0+ recommended approach
```

**Why does `Attribute.name` have `unique=True`?**

```python
name: Mapped[str] = mapped_column(String(100), unique=True)

# If "male" already exists in the attributes table,
# we cannot insert another row named "male".
# This enforces: each attribute name exists exactly once.

# Without unique=True:
#   Virat's "male" → row 1
#   Sachin's "male" → row 2
#   Dhoni's "male" → row 3
#   ... duplicates everywhere, normalization defeated

# With unique=True:
#   "male" exists once, all characters reference it.
```

**Why is `CharacterAttribute` a separate table (not just columns in Character)?**

```python
# If we stored attributes as columns on Character:
class Character(Base):
    real   = Column(Boolean)
    male   = Column(Boolean)
    indian = Column(Boolean)
    # ... 51 more columns

# Adding a new attribute "youtuber" = ALTER TABLE characters ADD COLUMN youtuber BOOLEAN
# This requires a database migration for every new attribute.
# Dangerous in production. Tables get wide and fragile.

# With CharacterAttribute (association table):
# Adding "youtuber" = INSERT INTO attributes (name) VALUES ('youtuber')
#                   + INSERT INTO character_attributes for each character
# No schema change. Just new rows. Safe.
```

**Why `cascade="all, delete-orphan"` on Character.attributes?**

```python
attributes: Mapped[list["CharacterAttribute"]] = relationship(
    back_populates="character",
    cascade="all, delete-orphan"
)

# cascade="all, delete-orphan" means:
# If you delete a Character, ALL their CharacterAttribute rows are also deleted.
# No orphan rows left behind.

# Without cascade:
#   DELETE FROM characters WHERE id = 1;
#   The character_attributes rows for character_id=1 remain.
#   Orphan data. Inconsistency.

# With cascade:
#   Delete character → character_attributes auto-deleted.
#   Clean database.
```

**Why does Question have `attribute_id` instead of `attribute` (string)?**

```python
# Old JSON version:
# questions.json: {"text": "Is your character real?", "attribute": "real"}

# New database version:
attribute_id: Mapped[int] = mapped_column(ForeignKey("attributes.id"))
attribute: Mapped["Attribute"] = relationship(back_populates="questions")

# Why FK instead of string?
# Normalization: "real" is stored once in attributes table.
# Question references it by ID.
# Typo prevention: attributes.id = 1, cannot have "rael" typo.
# Referential integrity: cannot create a question for a non-existent attribute.
```

**The Mapped type annotations explained:**

```python
# Mapped[int]       → this column stores Python int / SQL INTEGER
# Mapped[str]       → this column stores Python str / SQL VARCHAR
# Mapped[bool]      → this column stores Python bool / SQL BOOLEAN
# Mapped[list["X"]] → this is a one-to-many relationship returning a list of X
# Mapped["X"]       → this is a many-to-one relationship returning one X

# The string in quotes ("CharacterAttribute") is a FORWARD REFERENCE.
# Python reads the file top to bottom.
# At the point where Character is defined, CharacterAttribute doesn't exist yet.
# Using a string tells SQLAlchemy: "resolve this name later, not now."
```

---

## database/create_tables.py — Code-First Table Creation

```python
from database.database import Base, engine

# Import all models so SQLAlchemy knows about them
from database.models import (
    Character,
    Attribute,
    CharacterAttribute,
    Question
)


def create_tables():
    Base.metadata.create_all(engine)
    print("✅ Tables created successfully!")


if __name__ == "__main__":
    create_tables()
```

**Why import all models before calling `create_all()`?**

```
Base.metadata tracks every class that inherits from Base.
But Python only registers a class when it imports it.

If you call Base.metadata.create_all() without importing the models,
Base has no idea they exist → no tables are created.

The import chain:
  create_tables.py imports Character, Attribute, CharacterAttribute, Question
  These classes inherit from Base
  Base.metadata now knows all four tables
  create_all() creates all four

This is why the "import all models" comments exist in production code.
Without them, it's a common silent bug.
```

**What `Base.metadata.create_all(engine)` does in SQL:**

```sql
-- SQLAlchemy generates and executes:
CREATE TABLE IF NOT EXISTS characters (
    id       SERIAL  PRIMARY KEY,
    name     VARCHAR(100),
    category VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS attributes (
    id   SERIAL       PRIMARY KEY,
    name VARCHAR(100) UNIQUE
);

CREATE TABLE IF NOT EXISTS character_attributes (
    character_id INTEGER REFERENCES characters(id),
    attribute_id INTEGER REFERENCES attributes(id),
    value        BOOLEAN,
    PRIMARY KEY (character_id, attribute_id)
);

CREATE TABLE IF NOT EXISTS questions (
    id           SERIAL       PRIMARY KEY,
    category     VARCHAR(50),
    text         VARCHAR(255),
    attribute_id INTEGER REFERENCES attributes(id)
);
```

**You never write this SQL. SQLAlchemy writes it from your Python classes.**

This is called **Code-First Development**: Python classes define the schema, not SQL files.

**Run command:**

```bash
# Must use -m flag (runs as a module so imports work correctly)
python -m database.create_tables

# Why -m and not: python database/create_tables.py?
# Without -m: Python doesn't set up the package correctly
# "from database.database import..." would fail with ModuleNotFoundError
# With -m: Python treats database/ as a package, imports work correctly
```

---

## database/seed.py — The Seeder Class

This is the most complex file in the database layer. It reads JSON and populates all four PostgreSQL tables.

```python
import json

from sqlalchemy.orm import Session

from database.database import SessionLocal
from database.models import (
    Character,
    Attribute,
    CharacterAttribute,
    Question
)

class Seeder:

    def __init__(self):
        self.db: Session = SessionLocal()

    def seed(self):
        self.seed_characters()
        self.seed_questions()

        self.db.commit()
        self.db.close()

        print("✅ Database Seeded Successfully")

    def seed_characters(self):

        with open("data/characters.json", "r") as file:
            data = json.load(file)

        for item in data:
            self.insert_character(item)
    
    def insert_character(self, item):

        character = Character(
            id=item["id"],
            name=item["name"],
            category=item["category"]
        )

        self.db.add(character)
        self.db.flush()

        self.insert_attributes(
            character.id,
            item["attributes"]
        )

    def insert_attributes(
        self,
        character_id,
        attributes
    ):
        for name, value in attributes.items():

            attribute = (
                self.db.query(Attribute)
                .filter_by(name=name)
                .first()
            )
            if attribute is None:
                attribute = Attribute(
                    name=name
                )
                self.db.add(attribute)
                self.db.flush()

            character_attribute = CharacterAttribute(
                character_id=character_id,
                attribute_id=attribute.id,
                value=value
            )

            self.db.add(character_attribute)


    def seed_questions(self):

        with open("data/questions.json", "r") as file:
            data = json.load(file)
        for group in data:
            category = group["category"]

            for item in group["questions"]:
                self.insert_question(
                    category,
                    item
                )
    
    def insert_question(
        self,
        category,
        item
    ):
        attribute = (
            self.db.query(Attribute)
            .filter_by(name=item["attribute"])
            .first()
        )

        if attribute is None:
            raise ValueError(
                f"Attribute '{item['attribute']}' not found."
            )

        question = Question(
            category=category,
            text=item["text"],
            attribute_id=attribute.id
        )

        self.db.add(question)
```

### Every Method Explained

**`__init__`:**

```python
def __init__(self):
    self.db: Session = SessionLocal()

# Opens a database session for the entire seeding operation.
# All inserts use this one session.
# Committed once at the end of seed().
# This is efficient: one transaction for all 80+ characters.
```

**`seed()`:**

```python
def seed(self):
    self.seed_characters()
    self.seed_questions()
    self.db.commit()    # Save ALL changes at once
    self.db.close()     # Release the connection
    print("✅ Database Seeded Successfully")

# Why commit at the end, not after each character?
# Transaction performance: 1 COMMIT for 80 characters vs 80 COMMITs.
# If anything fails partway through → entire seed is rolled back.
# No partial data. Either everything is seeded or nothing is.
# ACID atomicity in action.
```

**`insert_character(item)`:**

```python
def insert_character(self, item):
    character = Character(
        id=item["id"],
        name=item["name"],
        category=item["category"]
    )
    self.db.add(character)
    self.db.flush()             # ← CRITICAL: generate character.id NOW
    
    self.insert_attributes(
        character.id,           # ← now we have the ID
        item["attributes"]
    )
```

```
Why db.flush() before insert_attributes()?

Without flush():
  character = Character(id=1, name="Virat", category="character")
  self.db.add(character)
  # character.id = ??? (PostgreSQL hasn't generated it yet)
  self.insert_attributes(character.id, ...)  # character.id is None!
  # CharacterAttribute(character_id=None) → INSERT fails

With flush():
  character = Character(...)
  self.db.add(character)
  self.db.flush()   # Sends INSERT to PostgreSQL (no commit yet)
  # PostgreSQL generates id=1, returns it
  # character.id = 1  ← now available
  self.insert_attributes(character.id, ...)  # character.id = 1 ✅

flush() = "execute this SQL but keep the transaction open"
commit() = "permanently save everything"
```

**`insert_attributes(character_id, attributes)`:**

```python
def insert_attributes(self, character_id, attributes):
    for name, value in attributes.items():
        # attributes = {"real": True, "male": True, "indian": True, ...}
        # name = "real", value = True
        # name = "male", value = True
        # ... 51 iterations per character

        # STEP 1: Check if this attribute already exists
        attribute = (
            self.db.query(Attribute)
            .filter_by(name=name)
            .first()
        )

        # STEP 2: Create if missing (normalization)
        if attribute is None:
            attribute = Attribute(name=name)
            self.db.add(attribute)
            self.db.flush()    # Get attribute.id immediately

        # STEP 3: Link character to attribute with value
        character_attribute = CharacterAttribute(
            character_id=character_id,
            attribute_id=attribute.id,
            value=value
        )
        self.db.add(character_attribute)
```

```
Why check if attribute exists before creating?

80 characters × 51 attributes = 4,080 attribute values
But there are only ~54 unique attribute names.

Without the check:
  "real" would be inserted 80 times.
  "male" would be inserted 80 times.
  ...
  Attributes table has 4,080 rows instead of 54.
  UNIQUE constraint on name → crash on 2nd insert of "real".

With the check:
  First character (Virat) → "real" doesn't exist → INSERT → attribute.id=1
  Second character (Naruto) → "real" exists, attribute.id=1 → reuse
  CharacterAttribute: (naruto_id, 1, False)
  54 unique attributes. 4,080 character_attribute rows. Correct.
```

**`seed_questions()`:**

```python
def seed_questions(self):
    with open("data/questions.json", "r") as file:
        data = json.load(file)
    for group in data:
        category = group["category"]
        for item in group["questions"]:
            self.insert_question(category, item)
```

**`insert_question(category, item)`:**

```python
def insert_question(self, category, item):
    # Find the Attribute this question targets
    attribute = (
        self.db.query(Attribute)
        .filter_by(name=item["attribute"])
        .first()
    )

    if attribute is None:
        raise ValueError(
            f"Attribute '{item['attribute']}' not found."
        )
    # This would mean: a question references an attribute that wasn't
    # seeded for any character. Data inconsistency. Stop immediately.

    question = Question(
        category=category,
        text=item["text"],
        attribute_id=attribute.id  # FK to attributes table
    )
    self.db.add(question)
```

```
Why is questions seeded AFTER characters?

Questions reference attribute_id (FK to attributes table).
Attributes are created during character seeding.
If questions were seeded first:
  attribute.id doesn't exist yet → ValueError → crash.

Correct order:
  1. seed_characters() → creates characters + attributes
  2. seed_questions()  → references attributes that now exist
```

**The duplicate ID bug (and how it was fixed):**

```
Original questions.json structure had IDs 1-50 for each category:
  character questions: id 1, 2, 3 ... 50
  animal questions:    id 1, 2, 3 ... 50  ← DUPLICATE PRIMARY KEYS!
  object questions:    id 1, 2, 3 ... 50  ← DUPLICATE PRIMARY KEYS!

PostgreSQL error: duplicate key value violates unique constraint "questions_pkey"

Fix: global unique IDs across all categories:
  character questions: id  1 to  50
  animal questions:    id 51 to 100
  object questions:    id 101 to 150

Primary Keys must be globally unique within a table.
```

---

## database/run_seed.py — The One-Command Setup

```python
from database.database import Base, engine
from database.models import (
    Character,
    Attribute,
    CharacterAttribute,
    Question
)
from database.seed import Seeder


def main():
    print("Creating database tables...")
    Base.metadata.create_all(engine)

    print("Seeding database...")
    seeder = Seeder()
    seeder.seed()

    print("✅ Database setup completed successfully!")


if __name__ == "__main__":
    main()
```

**Run with:**

```bash
python -m database.run_seed
```

**Output:**

```
Creating database tables...
✅ Tables created successfully!
Seeding database...
✅ Database Seeded Successfully
✅ Database setup completed successfully!
```

**What this does in sequence:**

```
1. Create tables (if they don't exist):
   characters, attributes, character_attributes, questions

2. Open Seeder session

3. Read characters.json
   For each character:
     Insert Character row
     For each attribute:
       Check if Attribute name exists → create if not
       Insert CharacterAttribute row (character + attribute + value)

4. Read questions.json
   For each question:
     Find Attribute by name
     Insert Question row with attribute_id

5. Commit everything
6. Close session
```

---

# SECTION 3 — THE POSTGRESQL REPOSITORY

## repository/postgres_repository.py — The Bridge

This class is the translation layer between PostgreSQL/SQLAlchemy and the game.

```python
from sqlalchemy.orm import Session

from database.database import SessionLocal
from database.models import (
    Character as DBCharacter,     # Alias: database model
    Question as DBQuestion        # Alias: database model
)

from models.character import Character    # Game model
from models.question import Question      # Game model
from repository.repository import Repository

class PostgresRepository(Repository):

    def __init__(self):
        self.db: Session = SessionLocal()

    def get_characters(self) -> list[Character]:
        db_characters = (
            self.db.query(DBCharacter)
            .all()
        )

        characters = []

        for db_character in db_characters:

            # Convert database relationships into the dictionary
            # the game expects
            attributes = {}

            for character_attribute in db_character.attributes:
                attributes[
                    character_attribute.attribute.name
                ] = character_attribute.value

            game_character = Character(
                id=db_character.id,
                name=db_character.name,
                category=db_character.category,
                attributes=attributes
            )

            characters.append(game_character)

        return characters
    
    def get_questions(self) -> list[Question]:
        db_questions = (
            self.db.query(DBQuestion)
            .all()
        )
        questions = []
        for db_question in db_questions:

            game_question = Question(
                id=db_question.id,
                category=db_question.category,
                text=db_question.text,
                attribute=db_question.attribute.name   # Follow relationship
            )

            questions.append(game_question)

        return questions
```

### Every Design Decision Explained

**Why `Character as DBCharacter`?**

```python
from database.models import Character as DBCharacter
from models.character import Character

# Both classes are called Character.
# Without aliasing:
#   from database.models import Character
#   from models.character import Character
#   → Second import overwrites the first!
#   → Only game Character is available. DBCharacter disappears.

# With aliasing:
#   DBCharacter = database model (SQLAlchemy, for querying)
#   Character   = game model (dataclass, for game logic)
#   No conflict. Both accessible.
```

**`get_characters()` — the full translation chain:**

```
Step 1: db.query(DBCharacter).all()
  → SELECT * FROM characters;
  Returns: [DBCharacter(id=1, name="Virat"), DBCharacter(id=2, ...), ...]

Step 2: for character_attribute in db_character.attributes:
  → SQLAlchemy automatically executes:
    SELECT * FROM character_attributes WHERE character_id = 1;
    Then for each row: SELECT * FROM attributes WHERE id = ?;
  → No manual JOIN. Relationship navigates automatically.

Step 3: Build the attributes dict:
  attributes["real"]   = True
  attributes["male"]   = True
  attributes["indian"] = True
  ...

Step 4: Create game Character:
  Character(
    id=1,
    name="Virat Kohli",
    category="character",
    attributes={"real": True, "male": True, "indian": True, ...}
  )

This is IDENTICAL to what JsonRepository returns.
Game doesn't notice the storage changed.
```

**`get_questions()` — the attribute name resolution:**

```python
game_question = Question(
    id=db_question.id,
    category=db_question.category,
    text=db_question.text,
    attribute=db_question.attribute.name   # ← follows FK relationship
)

# db_question.attribute_id = 1
# db_question.attribute     → SQLAlchemy loads Attribute(id=1, name="real")
# db_question.attribute.name = "real"

# Game Question.attribute = "real"   (the string key)
# This is what filter() uses: character.attributes.get("real", False)
# Exact match. Works identically to JSON version.
```

---

## game.py — The One-Line Change

```python
# BEFORE Day 41:
from repository.json_repository import JsonRepository

class Game:
    def __init__(self):
        self.repository = JsonRepository()   # ← reads JSON files


# AFTER Day 41:
from repository.postgres_repository import PostgresRepository

class Game:
    def __init__(self):
        self.repository = PostgresRepository()  # ← reads PostgreSQL
```

**Everything else in game.py: unchanged.**

```
start()            → unchanged
show_menu()        → unchanged
play_game()        → unchanged
select_category()  → unchanged
play_again()       → unchanged
```

This is the entire point of the Repository Pattern: **swap storage with one line.**

---

# SECTION 4 — THE COMPLETE ARCHITECTURE (AFTER DAY 41)

```
python main.py
      │
      ▼
Game.__init__()
  self.repository = PostgresRepository()
      │
      ▼
Game.start()
  self.all_characters = self.repository.get_characters()
  self.questions = self.repository.get_questions()
      │
      ▼
PostgresRepository.get_characters()
  self.db.query(DBCharacter).all()
      │
      ▼ (SQLAlchemy generates JOIN automatically)
SELECT characters.*, attributes.name, character_attributes.value
FROM characters
JOIN character_attributes ON characters.id = character_attributes.character_id
JOIN attributes ON character_attributes.attribute_id = attributes.id
      │
      ▼
PostgreSQL executes query, returns rows
      │
      ▼
PostgresRepository builds dict: {"real": True, "male": True, ...}
Creates game Character objects
      │
      ▼
Game.show_menu()
Game.select_category("character")
  self.character_engine = CharacterEngine(characters)
  self.question_engine  = QuestionEngine(questions)
      │
      ▼
Game.play_game()
  question_engine.current_question()
  character_engine.filter(attribute, bool)
  character_engine.has_guess()
  character_engine.guess()
```

---

# SECTION 5 — DATABASE NORMALIZATION EXPLAINED

## What Is Normalization?

Normalization is the process of organizing database tables to reduce redundancy and improve data integrity.

## First Normal Form (1NF) — Atomic Values

```
❌ Violates 1NF (multiple values in one cell):
  characters table:
  id | name  | attributes
  1  | Virat | real=true,male=true,indian=true,...

✅ Satisfies 1NF (each cell has one value):
  characters table:           character_attributes table:
  id | name  | category       character_id | attribute_id | value
  1  | Virat | character       1           | 1            | true
                               1           | 2            | true
```

## Why the CharacterAttribute Table?

```
Option A: Attributes as columns on Character (denormalized):
  characters table:
  id | name  | real | male | alive | indian | cricketer | ... 51 columns

Problems:
  → Adding "youtuber" attribute = ALTER TABLE (schema change, dangerous!)
  → Every row stores NULL for attributes that don't apply
  → Hard to query "all characters with real=true"

Option B: CharacterAttribute junction table (normalized):
  character_attributes:
  character_id | attribute_id | value
  1            | 1            | true   (Virat, real, true)
  1            | 2            | true   (Virat, male, true)

Benefits:
  → Adding "youtuber" = INSERT one row into attributes, done
  → No schema change
  → Easy to query: WHERE attribute.name='real' AND value=true
  → Unlimited attributes without touching Character schema
```

## Domain Model vs Persistence Model

```
Domain Model (game layer):
  models/character.py
  @dataclass Character:
    id: int
    name: str
    category: str
    attributes: dict[str, bool]   ← simple Python dict
  
  Used by: CharacterEngine, QuestionEngine, Game
  Never touches SQLAlchemy.

Persistence Model (database layer):
  database/models.py
  class Character(Base):
    id: Mapped[int]
    name: Mapped[str]
    category: Mapped[str]
    attributes: Mapped[list[CharacterAttribute]]  ← SQLAlchemy relationship
  
  Used by: PostgresRepository
  Never used by Game, CharacterEngine, QuestionEngine.

Repository performs the conversion:
  Persistence Model → Domain Model

This separation is called:
  Domain Model vs Persistence Model
  Business Logic vs Data Access
  Clean Architecture
```

---

# SECTION 6 — CONCEPTS LEARNED TODAY

## ORM (Object Relational Mapper)

```
Without ORM:
  cursor.execute("SELECT * FROM characters WHERE id = %s", (1,))
  row = cursor.fetchone()
  character = {"id": row[0], "name": row[1], ...}

With ORM:
  character = session.query(Character).filter_by(id=1).first()
  print(character.name)   # Python attribute access

ORM maps: Python class → database table
           Python instance → database row
           Python attribute → database column
```

## SQLAlchemy Relationships

```python
# Relationship navigates between tables automatically.
# No manual JOIN queries.

character.attributes         # → loads all CharacterAttribute rows for this character
question.attribute           # → loads the Attribute this question points to
question.attribute.name      # → follows TWO relationships in one expression

SQLAlchemy generates:
  SELECT * FROM character_attributes WHERE character_id = ?;
  SELECT * FROM attributes WHERE id = ?;
```

## flush() vs commit()

```
flush():
  → Sends SQL to PostgreSQL immediately
  → Transaction is still OPEN (can be rolled back)
  → PostgreSQL generates IDs (SERIAL) right now
  → Use when: you need a generated ID before committing

commit():
  → Permanently saves everything in the transaction
  → Transaction is CLOSED
  → Cannot be rolled back after this
  → Use when: all work is complete and correct

Pattern:
  INSERT character → flush() → get character.id
  INSERT character_attribute (using character.id) → flush()
  INSERT next character → flush() ...
  COMMIT at end → everything saved in one transaction
```

## Engine vs Session

```
Engine:
  → Created once per application startup
  → Configuration object: knows how to connect to PostgreSQL
  → Think: "the road to the database"

Session:
  → Created per operation or per request
  → Active conversation with PostgreSQL
  → Think: "a single trip down the road"
  → Always close after use (release the connection)

engine = create_engine(...)        # Once
session = SessionLocal()           # Per request
session.query(...).all()           # Work
session.commit()                   # Save
session.close()                    # Release
```

## Dependency Inversion Principle (DIP)

```
Game.start() calls: self.repository.get_characters()

"Game depends on Repository interface, not on PostgreSQL"

Game → Repository (abstract) ← PostgresRepository

The Game doesn't care whether data comes from:
  JSON, PostgreSQL, MongoDB, Redis, API, or in-memory list.

This is Dependency Inversion:
  High-level modules (Game) don't depend on low-level modules (PostgreSQL).
  Both depend on abstractions (Repository interface).
```

---

# SECTION 7 — IMPORTANT THINGS TO KNOW

```
 1. SQLAlchemy 2.0 uses Mapped[T] and mapped_column() — cleaner than Column().

 2. DeclarativeBase is the modern way to create Base (instead of declarative_base()).

 3. Base.metadata.create_all() creates tables only if they don't exist.
    Use drop_all() first if you need to rebuild from scratch.

 4. db.flush() generates IDs without committing. Use before needing generated IDs.
    db.commit() saves permanently. Don't call until all work is done.

 5. Forward references in Mapped["ClassName"] avoid circular import issues.
    Python resolves these string references after all classes are loaded.

 6. Import aliasing (as DBCharacter) prevents name collision when both
    game and database have a class called Character.

 7. Always run Python packages with python -m module.name, not python path/to/file.py.
    The -m flag sets up the package system correctly so imports work.

 8. Primary Keys must be globally unique within a table.
    Questions from different categories must have different IDs.

 9. Foreign Key values appear unrelated to the row's own ID — that is correct.
    attribute_id in Question references attributes.id, not questions.id.

10. Seeding characters before questions is required.
    Questions reference attribute_id. Attributes are created during character seeding.
    Wrong order → AttributeError.

11. The Seeder checks if an Attribute exists before creating.
    This is normalization: "real" exists once, all 80 characters reference it.
    Without the check: UNIQUE constraint violation on second insert.

12. cascade="all, delete-orphan" automatically deletes CharacterAttribute rows
    when the parent Character is deleted. Prevents orphan data.

13. Domain Model (models/) is for game logic.
    Persistence Model (database/models.py) is for SQLAlchemy.
    Repository converts one to the other. Never mix them.

14. Repository Pattern makes storage swappable with one line.
    JsonRepository → PostgresRepository → future MongoRepository.
    Game never changes.

15. Code-First Development: Python classes define the schema, not SQL files.
    Base.metadata.create_all() generates all CREATE TABLE statements.
```

---

# SECTION 8 — INTERVIEW QUESTIONS

## Q1. What is SQLAlchemy ORM?

SQLAlchemy ORM maps Python classes to database tables. Instead of writing SQL strings, you work with Python objects. SQLAlchemy generates the SQL automatically. A Python class becomes a table, a class instance becomes a row, and class attributes become columns.

## Q2. What is the difference between Engine and Session?

The Engine is created once and knows how to connect to PostgreSQL — it is the configuration object that manages connection pooling. The Session is created per operation and represents an active transaction — it is where you execute queries, add objects, and commit or roll back changes.

## Q3. What is the difference between `flush()` and `commit()`?

`flush()` sends SQL to the database and generates IDs (SERIAL/sequences) but keeps the transaction open. It is used when you need a generated ID before the transaction is complete. `commit()` permanently saves all changes in the transaction and closes it. You cannot roll back after a commit.

## Q4. What is database normalization?

Normalization organizes tables to reduce data duplication. Instead of storing "male", "real", "alive" as columns on every character row, we store them once in an attributes table and use a junction table (character_attributes) to link characters to attributes with a boolean value. This means adding a new attribute requires only inserting a new row, not altering the table schema.

## Q5. What is an association table (junction table)?

An association table is the standard way to implement a many-to-many relationship. A character can have many attributes, and an attribute can apply to many characters. The `character_attributes` table stores `(character_id, attribute_id, value)` — each row is one fact about one character. This avoids wide tables and makes attributes extensible without schema changes.

## Q6. Why are there two Character classes?

`models/character.py` (domain model) is a simple `@dataclass` used by the game. `database/models.py` (persistence model) is a SQLAlchemy class representing the characters table with relationships and foreign keys. The Repository converts persistence models to domain models so the game never directly touches SQLAlchemy — separation of concerns.

## Q7. Why does the Game class change with just one line?

Because of the Repository Pattern and Dependency Inversion Principle. The Game only depends on the `Repository` abstract interface, which defines two methods: `get_characters()` and `get_questions()`. Whether those methods read from JSON files, PostgreSQL, or MongoDB is irrelevant to the Game. Swapping the implementation is one line: `self.repository = PostgresRepository()`.

## Q8. What is Code-First Development?

Code-First means Python classes define the database schema, not SQL files. `Base.metadata.create_all(engine)` reads all registered SQLAlchemy models and generates the corresponding `CREATE TABLE` SQL automatically. The Python code is the single source of truth for the database structure.

---

# SECTION 9 — LEETCODE #1929: CONCATENATION OF ARRAY

## Problem

Given array `nums` of length `n`, create an array of length `2n` where the original appears twice.

```
nums = [1, 2, 1]  →  [1, 2, 1, 1, 2, 1]
```

## Approach 1 — Two Loops (Manual)

```python
class Solution(object):
    def getConcatenation(self, nums):
        ans = []
        for i in range(len(nums)):
            ans.append(nums[i])      # First copy
        for i in range(len(nums)):
            ans.append(nums[i])      # Second copy
        return ans
```

**Why two loops instead of one:** The simplest mental model. First loop fills positions 0 to n-1. Second loop fills positions n to 2n-1. Clean, readable, obvious intent.

## Approach 2 — One Loop with Index Assignment ✅ Submitted (0ms, beats 100%)

```python
class Solution(object):
    def getConcatenation(self, nums):
        ans = [0] * (2 * len(nums))   # Pre-allocate 2n slots
        for i in range(len(nums)):
            ans[i]          = nums[i]  # First half
            ans[i + len(nums)] = nums[i]  # Second half
        return ans
```

**Why pre-allocate with `[0] * (2n)`:**

```
ans = []          → empty list, has no indexes yet
ans[i] = value    → IndexError! Index i doesn't exist.

ans = [0] * (2*n) → list of 2n zeros, all indexes 0 to 2n-1 exist
ans[i] = value    → replaces the zero at position i. Works.

Two ways to fill a list:
  append()      → grows the list (use when size unknown)
  index assign  → fills existing positions (use when size known)
```

**Why `i + len(nums)` and not `i + n`:**

```python
# In Python, n is not a built-in variable.
# len(nums) gives you n dynamically.
# i + len(nums) places the element in the second half.

# For nums = [1,2,1], len(nums) = 3:
# i=0: ans[0]=1, ans[3]=1
# i=1: ans[1]=2, ans[4]=2
# i=2: ans[2]=1, ans[5]=1
# Result: [1, 2, 1, 1, 2, 1] ✅
```

## Approach 3 — Pythonic

```python
# Method 1: list concatenation
class Solution(object):
    def getConcatenation(self, nums):
        return nums + nums

# Method 2: list repetition
class Solution(object):
    def getConcatenation(self, nums):
        return nums * 2
```

**Why `nums * 2` works:**

```python
# Python's list multiplication creates a new list with the contents repeated.
[1, 2, 3] * 2  →  [1, 2, 3, 1, 2, 3]

# This is identical to: nums + nums
# Both create a new list. Neither modifies the original.
```

**When to use which:**

```
Interview: use Approach 2 (index assignment)
  → Demonstrates understanding of index arithmetic
  → Shows you know the difference between append and index assign
  → Clearly shows how first and second halves map

Coding contest: use Approach 3 (nums * 2)
  → Faster to type
  → Fewer characters
  → Same O(n) time complexity

Never: one is not better than the other in complexity.
All three: Time O(n), Space O(n).
```

**Result:** ✅ Accepted | 92/92 test cases | Runtime: 0ms | Beats 100%

---

# SECTION 10 — DEBUGGING PROBLEMS SOLVED TODAY

## Problem 1: ModuleNotFoundError sqlalchemy

```
Error: No module named 'sqlalchemy'
Cause: SQLAlchemy installed globally, not in virtual environment.
Fix:   Activate .venv first, then:
       python -m pip install sqlalchemy psycopg2-binary
```

## Problem 2: "database is not a package"

```
Error: ModuleNotFoundError: No module named 'database.database'
Cause: Running file directly: python database/create_tables.py
       Python doesn't recognise database/ as a package.
Fix:   Use: python -m database.create_tables
       The -m flag runs it as a module, package imports work.
```

## Problem 3: Duplicate Primary Key on Questions

```
Error: duplicate key value violates unique constraint "questions_pkey"
Cause: questions.json had IDs 1-50 for each category.
       Character questions: 1-50. Animal questions: 1-50. Object: 1-50.
       PostgreSQL PRIMARY KEY must be globally unique.
Fix:   Assigned global IDs: character 1-50, animal 51-100, object 101-150.
```

## Problem 4: attribute_id doesn't match question.id (not a bug)

```
Confusion: Question id=5, attribute_id=8. Why don't they match?
Answer: Foreign Keys reference another table's ID, not the row's own ID.
        question.id = 5 means "this is the 5th question"
        question.attribute_id = 8 means "this question targets attribute #8"
        attribute #8 might be "actor". Completely unrelated numbers. Correct.
```

## Problem 5: Seeder crashes on re-run (tables have data)

```
Error: UNIQUE constraint violation or PRIMARY KEY conflict on re-seed.
Cause: Characters/Attributes already exist from previous seed.
Fix:   Drop tables first, then recreate and reseed:
       Base.metadata.drop_all(engine)
       Base.metadata.create_all(engine)
       Seeder().seed()
       Or: Add IF NOT EXISTS checks to Seeder.
```

---

# ✅ Day 41 Task Summary

| Task | Status |
|------|--------|
| Create database/database.py | ✅ Done |
| Create database/models.py (4 tables) | ✅ Done |
| Create database/create_tables.py | ✅ Done |
| Create database/seed.py (Seeder class) | ✅ Done |
| Create database/run_seed.py | ✅ Done |
| Create postgres_repository.py | ✅ Done |
| Update game.py (one line change) | ✅ Done |
| Run migration successfully | ✅ Done |
| Verify game works with PostgreSQL | ✅ Done |
| LeetCode #1929 (all 3 approaches) | ✅ Done |

---

# 📅 What's Coming: Day 42

```
Day 42 — GitHub Release + Month 2 Checkpoint

  → Rename GuessWise.md to README.md
  → Create .gitignore
  → Push GuessWise as standalone GitHub repository
  → Tag v1.0
  → LinkedIn announcement post

Month 2 Checkpoint goals:
  ✅ Write Python classes, decorators, generators without help
  ✅ Write complex SQL JOIN queries
  ✅ Understand async/await in Python
  ✅ Know all HTTP methods and status codes by heart
  ✅ Explain OOP (4 pillars) in an interview right now
  ✅ Design a basic database schema on paper
  ✅ Have 2+ projects on GitHub with README (PENDING → Day 42)
  ✅ Can use SQLAlchemy to connect Python to PostgreSQL
```

---

# REVISION SHEET

```
═══════════════════════════════════════════════════════════
GUESSWISE DAY 41 — POSTGRESQL MIGRATION
═══════════════════════════════════════════════════════════

DATABASE_URL FORMAT:
  postgresql+psycopg2://user:password@host:5432/dbname

KEY OBJECTS:
  engine      = create_engine(URL)   → connection factory (once)
  SessionLocal = sessionmaker(...)   → session factory
  session     = SessionLocal()       → one conversation with DB

BASE:
  class Base(DeclarativeBase): pass
  All ORM models inherit from Base
  Base.metadata.create_all(engine) → creates all tables

ORM MODEL SYNTAX (SQLAlchemy 2.0):
  class MyTable(Base):
      __tablename__ = "my_table"
      id: Mapped[int] = mapped_column(primary_key=True)
      name: Mapped[str] = mapped_column(String(100))
      fk: Mapped[int] = mapped_column(ForeignKey("other.id"))

RELATIONSHIP:
  items = relationship("Item", back_populates="parent")
  parent = relationship("Parent", back_populates="items")
  Navigates between related objects automatically.

FLUSH vs COMMIT:
  flush()  → generates IDs, transaction still open
  commit() → saves permanently, transaction closed

SEEDER PATTERN:
  insert parent → flush() → get parent.id
  insert child(parent_id) → flush()
  commit at end

REPOSITORY PATTERN:
  class Repo(ABC):
      @abstractmethod
      def get_data(): pass

  class JsonRepo(Repo):    ← reads JSON
  class PostgresRepo(Repo): ← reads PostgreSQL

  One line in game.py switches storage.

NORMALIZATION:
  Don't duplicate attribute names across 80 characters.
  Store once in attributes table.
  Reference via character_attributes junction table.

RUN COMMANDS:
  python -m database.create_tables  ← create tables
  python -m database.run_seed       ← create + seed

INTERVIEW VOCABULARY:
  ORM, Engine, Session, flush/commit, Mapped
  Normalization, Foreign Key, Association Table
  Many-to-Many, Junction Table, Cascade
  Domain Model, Persistence Model, Repository Pattern
  Dependency Inversion, Loose Coupling, Code-First
```

---

## LeetCode Solved This Day

| Problem | Difficulty | Topic | Status | Runtime |
|---------|-----------|-------|--------|---------|
| #1929 Concatenation of Array | Easy | Array Construction, Index Assignment | ✅ Accepted 92/92 | 0ms, Beats 100% |

---

*Day 41 Complete. GuessWise migrated from JSON to PostgreSQL. Architecture complete. GitHub release next.* ✅

