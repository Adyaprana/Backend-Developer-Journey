# 🚀 GuessWise - Day 41
## PostgreSQL Migration & Repository Pattern

> **Project:** GuessWise CLI  
> **Day:** 41  
> **Goal:** Replace the JSON data source with PostgreSQL without changing the Game logic.

---

# 🎯 Day Goal

Until Day 40, GuessWise was completely dependent on JSON files.

```
Game
 │
 ├── characters.json
 └── questions.json
```

Although the architecture was improving (Repository Pattern, CharacterEngine, QuestionEngine), the actual data still came from JSON files.

Today's goal was to migrate the entire project to PostgreSQL while keeping the rest of the game unchanged.

This is exactly how real software evolves.

Instead of rewriting the application, we replace only the data source.

---

# 📚 What I Learned Today

- PostgreSQL integration with Python
- SQLAlchemy ORM
- Database Normalization
- ORM Relationships
- One-to-Many Relationship
- Many-to-Many Relationship
- Association Table
- Repository Pattern in real projects
- Database Seeding
- Separating Database Models from Game Models
- Converting ORM objects into Domain objects
- Dependency Inversion

---

# 🏗 Previous Architecture

```
                Game
                  │
                  ▼
          JsonRepository
                  │
                  ▼
          characters.json
          questions.json
```

Problems:

- Everything depended on JSON.
- No real database.
- Cannot scale.
- Cannot support online multiplayer.
- Cannot easily edit data.
- Difficult to build an admin dashboard.
- Impossible to query efficiently.

---

# 🏗 New Architecture

```
                 Game
                   │
                   ▼
          PostgresRepository
                   │
                   ▼
             SQLAlchemy ORM
                   │
                   ▼
             PostgreSQL Database
```

The Game doesn't know where the data comes from.

It simply asks

```python
repository.get_characters()
repository.get_questions()
```

This is the beauty of the Repository Pattern.

---

# 🗂 New Folder Created

```
database/

│
├── __init__.py
├── database.py
├── models.py
├── seed.py
├── create_tables.py
└── run_seed.py
```

Each file has one responsibility.

---

# database.py

Responsible for connecting Python to PostgreSQL.

---

## Code

```python
DATABASE_URL = (
    "postgresql+psycopg2://postgres:password@localhost:5432/guesswise"
)
```

This tells SQLAlchemy

- database type
- username
- password
- host
- database name

---

Then

```python
engine = create_engine(...)
```

creates the connection engine.

Think of it as

```
Python
   │
   ▼
Engine
   │
   ▼
PostgreSQL
```

---

Then

```python
SessionLocal = sessionmaker(...)
```

creates database sessions.

A Session is like opening a conversation with PostgreSQL.

```
Session
 │
 ├── Read
 ├── Insert
 ├── Update
 └── Delete
```

Without a session nothing can happen.

---

Finally

```python
class Base(DeclarativeBase):
    pass
```

Every database model inherits from Base.

Example

```python
class Character(Base):
```

Without Base SQLAlchemy cannot create tables.

---

# models.py

Today I learned something very important.

These models are NOT my game models.

These are ORM models.

There are now two completely different kinds of models.

---

## Game Models

Located in

```
models/
```

Example

```python
Character
Question
```

These are used only by the game.

---

## Database Models

Located in

```
database/models.py
```

Example

```python
Character
Attribute
CharacterAttribute
Question
```

These exist only for PostgreSQL.

---

The Repository converts

```
Database Model
        │
        ▼
 Game Model
```

The Game never directly touches SQLAlchemy.

---

# Character Table

```python
class Character(Base):
```

Represents

```
characters
```

table.

Columns

```
id
name
category
```

---

Relationship

```python
attributes = relationship(...)
```

This means

```
Character

↓

CharacterAttribute
```

Instead of storing attributes directly, we store references.

---

# Attribute Table

Instead of

```
real
male
alive
actor
```

being repeated thousands of times,

we created

```
attributes
```

table.

Example

```
id    name

1     real

2     male

3     alive
```

Why?

Normalization.

---

Without normalization

```
Virat

real
male
alive

Sachin

real
male
alive
```

The same words appear hundreds of times.

---

With normalization

```
Attribute Table

1 real
2 male
3 alive
```

Characters simply reference these IDs.

Much smaller.

Much cleaner.

---

# CharacterAttribute Table

This is today's biggest concept.

It is called an

Association Table

or

Junction Table.

Instead of

```
Character

↓

real = True
male = True
```

we store

```
character_id

attribute_id

value
```

Example

```
Virat

↓

real

↓

True
```

One row.

---

Another row

```
Virat

↓

male

↓

True
```

Another row.

---

This design can store unlimited attributes without changing the Character table.

Very scalable.

---

# Question Table

Questions no longer store

```
attribute = "male"
```

Instead

```
attribute_id
```

points to

```
Attribute Table
```

Example

```
Question

↓

attribute_id = 2

↓

male
```

Again

Normalization.

---

# Why Question IDs Repeat

Originally

```
Character Questions

1...

50

Animal Questions

1...

50

Object Questions

1...

50
```

This caused duplicate primary keys.

Solution

Every question received a globally unique ID.

Example

```
Character

1-50

Animal

51-100

Object

101-150
```

Primary Keys must always be unique.

---

# Creating Tables

Today I learned

```
Base.metadata.create_all(engine)
```

SQLAlchemy automatically creates every table.

No SQL needed.

It generated

```
characters

attributes

character_attributes

questions
```

directly from Python classes.

This is called

Code First Development.


# Repository Pattern with PostgreSQL

One of today's biggest achievements was implementing the Repository Pattern with a real database.

Previously

```
Game
 │
 ▼
JsonRepository
 │
 ▼
JSON Files
```

Today

```
Game
 │
 ▼
PostgresRepository
 │
 ▼
SQLAlchemy ORM
 │
 ▼
PostgreSQL
```

The Game class never changed.

Only the Repository changed.

That is exactly why Repository Pattern exists.

The Game only knows

```python
self.repository.get_characters()
self.repository.get_questions()
```

It doesn't care whether the data comes from

- JSON
- PostgreSQL
- MongoDB
- API
- Redis

This is called **Dependency Inversion Principle (DIP)**.

---

# Why Repository Pattern is Powerful

Imagine tomorrow I decide to move everything into MongoDB.

Without Repository Pattern

```
Game

↓

Rewrite everything
```

With Repository Pattern

```
Game

↓

No change

↓

Create MongoRepository
```

The Game still works.

Only one class changes.

This is one of the biggest software engineering concepts I learned today.

---

# PostgresRepository

Today I created

```
repository/

└── postgres_repository.py
```

Its responsibility is

- Read from PostgreSQL
- Convert database models into game models
- Return usable objects to the Game

It never prints anything.

It never filters characters.

It never asks questions.

It only retrieves data.

Single Responsibility Principle.

---

# get_characters()

Today I built

```python
def get_characters():
```

It performs

```
PostgreSQL

↓

SQLAlchemy Objects

↓

Game Character Objects
```

---

## Step 1

Read every character

```python
db_characters = (
    self.db.query(DBCharacter)
    .all()
)
```

Equivalent SQL

```sql
SELECT *
FROM characters;
```

---

## Step 2

Read every relationship

```python
for character_attribute in db_character.attributes:
```

Thanks to SQLAlchemy relationships

```
Character

↓

CharacterAttribute

↓

Attribute
```

everything is automatically connected.

I don't manually write JOIN queries.

SQLAlchemy does it.

---

## Step 3

Convert into dictionary

```python
attributes[
    character_attribute.attribute.name
] = character_attribute.value
```

Example

```
attribute.name

↓

male
```

value

↓

```
True
```

Dictionary becomes

```python
{
    "male": True,
    "real": True
}
```

Exactly what my Game expects.

---

## Step 4

Create Game Character

```python
Character(
    ...
)
```

Notice

This is NOT

Database Character.

This is

Game Character.

This conversion keeps the database layer independent from the Game layer.

---

# get_questions()

Exactly the same process.

Database

↓

ORM

↓

Game Question

---

SQLAlchemy relationship

```python
db_question.attribute.name
```

automatically converts

```
attribute_id

↓

Attribute Table

↓

attribute.name
```

No SQL JOINs written manually.

SQLAlchemy follows relationships automatically.

---

# Seeding the Database

Today I built

```
seed.py
```

Its responsibility

Move JSON data into PostgreSQL.

---

Workflow

```
characters.json

↓

Seeder

↓

Character Table

↓

Attribute Table

↓

CharacterAttribute Table
```

---

Questions

```
questions.json

↓

Seeder

↓

Questions Table
```

---

# Why Seeder Exists

Without Seeder

Every time

I create a new database

I would manually insert

150 Characters

150 Questions

154 Attributes

Impossible.

Seeder automates everything.

One command

↓

Entire database is rebuilt.

---

# insert_character()

This function

- creates Character
- saves it
- inserts attributes

instead of putting everything into one huge function.

Benefits

- reusable
- readable
- easier debugging

---

# insert_attributes()

This function taught me Normalization.

First

Search

```python
attribute = (
    self.db.query(Attribute)
    .filter_by(name=name)
    .first()
)
```

If

```
male
```

already exists

Don't create another one.

Reuse it.

If not

Create it.

This avoids duplicate rows.

---

Then

Create

```
CharacterAttribute
```

This links

Character

↓

Attribute

↓

Value

instead of storing attributes inside Character.

---

# insert_question()

Instead of storing

```
attribute = "male"
```

Questions now store

```
attribute_id
```

which references

```
Attribute Table
```

Again

Normalization.

---

# create_tables.py

One command

```python
Base.metadata.create_all(engine)
```

created

```
characters

attributes

character_attributes

questions
```

automatically.

No SQL written manually.

---

# run_seed.py

Today I also built

```
run_seed.py
```

Purpose

Run the complete setup with one command.

```
python -m database.run_seed
```

Output

```
Create Tables

↓

Seed Database

↓

Done
```

One command.

Complete database.

---

# Biggest Concepts I Learned Today

## 1. ORM

Instead of SQL

```sql
SELECT *
FROM characters;
```

I write

```python
self.db.query(Character).all()
```

Python objects instead of SQL strings.

---

## 2. Relationships

Instead of writing JOIN queries

I use

```python
character.attributes

question.attribute
```

SQLAlchemy automatically joins tables.

---

## 3. Normalization

Don't duplicate data.

Store it once.

Reference it everywhere.

---

## 4. Association Tables

Many-to-Many relationships require a junction table.

Today I implemented

```
CharacterAttribute
```

---

## 5. Repository Pattern

The Game no longer knows

where data comes from.

Huge architecture improvement.

---

## 6. Layered Architecture

Today the project became

```
Presentation Layer

↓

Game

↓

Business Layer

↓

CharacterEngine
QuestionEngine

↓

Repository Layer

↓

PostgresRepository

↓

Database Layer

↓

SQLAlchemy

↓

PostgreSQL
```

Every layer has one responsibility.

---

# Comparison

## Before Day 41

```
Game

↓

JsonRepository

↓

JSON Files
```

Everything depended on files.

---

## After Day 41

```
Game

↓

Repository Interface

↓

PostgresRepository

↓

SQLAlchemy

↓

PostgreSQL
```

The Game became completely independent of the storage system.

---

# What I Can Explain in an Interview Now

- What is SQLAlchemy ORM?
- Difference between ORM Models and Domain Models.
- What is Normalization?
- Why use a Junction Table?
- What is a Many-to-Many relationship?
- What is an Association Table?
- What is the Repository Pattern?
- Why use Repository Pattern?
- Why separate Game Models and Database Models?
- What is Dependency Inversion Principle?
- How SQLAlchemy Relationships work.
- How to seed a PostgreSQL database from JSON.
- Why PostgreSQL is better than JSON for scalable applications.

---

# Day 41 Summary

Today was one of the biggest milestones of the GuessWise project.

I successfully migrated the application from a JSON-based storage system to a fully normalized PostgreSQL database using SQLAlchemy ORM without changing the Game logic.

I learned how to design relational databases, create ORM models, define relationships, normalize data, build a Repository Pattern, seed a database automatically, and separate the database layer from the business layer.

The Game now communicates only with a Repository, making it independent of the underlying storage technology.

This architecture is significantly more scalable, maintainable, and closer to real-world backend systems used in production.

---

# End of Day 41

**Project Status**

```
GuessWise CLI
        │
        ├── Game Engine ✅
        ├── Character Engine ✅
        ├── Question Engine ✅
        ├── Repository Pattern ✅
        ├── PostgreSQL Migration ✅
        ├── SQLAlchemy ORM ✅
        ├── Database Normalization ✅
        ├── Automatic Seeder ✅
        └── Clean Layered Architecture ✅
```

**Next Milestone (Day 42)**

```
Knowledge Manager

↓

Dynamic Question Selection

↓

GuessWise becomes Akinator-like instead of asking fixed questions.
```

# 🚀 GuessWise - Day 41 (Part 3)
## Deep Concepts, Debugging Notes & Important Learnings

> This part contains everything I learned while building, debugging, and understanding the PostgreSQL migration. These are the concepts that are easy to forget later, so I documented them here.

---

# 💡 Why We Didn't Change the Game Class

One of the biggest achievements today was that **the Game class barely changed**.

Before:

```python
self.repository = JsonRepository()
```

After:

```python
self.repository = PostgresRepository()
```

Everything else worked exactly the same.

Why?

Because the Game only depends on the Repository interface.

```
Game

↓

Repository Interface

↓

JsonRepository

OR

PostgresRepository
```

This is called **Loose Coupling**.

The Game doesn't care where the data comes from.

---

# 💡 Why We Created Two Different Character Classes

At first this was confusing.

We already had

```
models/

Character
```

Then we created another

```
database/models.py

Character
```

Why?

Because they have different jobs.

---

## Game Character

```
models/character.py
```

Purpose

```
Used by the game.
```

Contains

```
id

name

category

attributes (dictionary)
```

The engines use this object.

---

## Database Character

```
database/models.py
```

Purpose

```
Represents a PostgreSQL table.
```

Contains

```
Columns

Relationships

Foreign Keys
```

Only SQLAlchemy uses this object.

---

This separation is called

```
Domain Model

vs

Persistence Model
```

Professional backend applications almost always separate them.

---

# 💡 Why We Used

```python
Character as DBCharacter
```

Instead of

```python
Character
```

Both classes have the same name.

```
Game Character

Database Character
```

Without aliasing

Python wouldn't know which one we mean.

So

```python
from database.models import Character as DBCharacter
```

means

```
Database Character

↓

DBCharacter
```

Now the code becomes much easier to understand.

---

Exactly the same for

```python
Question as DBQuestion
```

---

# 💡 Why Question.attribute_id Doesn't Match Question.id

When I first saw

```
Question

id = 5

attribute_id = 8
```

I thought something was wrong.

It wasn't.

These IDs belong to different tables.

Example

Question Table

```
id

5

↓

Question Number
```

Attribute Table

```
id

8

↓

actor
```

Question 5

asks

```
actor?
```

Therefore

```
attribute_id = 8
```

Perfectly correct.

Foreign Keys point into another table.

They are NOT supposed to match the row's own ID.

---

# 💡 Why Attribute IDs Look Random

During seeding

every new attribute is inserted only once.

Example

```
real

male

alive

actor
```

They receive IDs based on insertion order.

Questions simply reference those IDs.

Therefore

```
attribute_id

2

5

18

24
```

is completely normal.

---

# 💡 Why We Check Before Creating an Attribute

Instead of

```python
Attribute(
    name="male"
)
```

every time,

we first search

```python
attribute = (
    self.db.query(Attribute)
    .filter_by(name=name)
    .first()
)
```

Why?

Imagine

```
Virat

male

Sachin

male

Dhoni

male
```

Without checking

Database becomes

```
male

male

male

male

male
```

Thousands of duplicate rows.

Instead

we create

```
male
```

once.

Everyone references that row.

This is Normalization.

---

# 💡 Why We Used db.flush()

One of today's most important SQLAlchemy concepts.

Suppose

```python
character = Character(...)
```

At this moment

```
character.id

?

Unknown
```

The ID doesn't exist yet.

We need the ID immediately because

```
CharacterAttribute

↓

character_id
```

depends on it.

So we call

```python
self.db.flush()
```

Flush sends the INSERT to PostgreSQL immediately,

without committing the transaction.

Now

```
character.id

↓

Available
```

and we can create relationships.

---

Difference

```
flush()

↓

Generate IDs

↓

Continue working
```

```
commit()

↓

Save everything permanently
```

Never confuse these two.

---

# 💡 Engine vs Session

Today I finally understood the difference.

---

Engine

```
Connection Factory
```

Responsible for

```
Connecting to PostgreSQL.
```

Think

```
Road

↓

PostgreSQL
```

---

Session

```
Conversation
```

Responsible for

```
Reading

Writing

Updating

Deleting
```

Think

```
Engine

↓

Open Session

↓

Work

↓

Commit

↓

Close
```

Every database operation happens inside a Session.

---

# 💡 Why We Used create_tables.py

Instead of opening pgAdmin

and manually creating

```
characters

questions

attributes

character_attributes
```

we let SQLAlchemy create everything.

One command

```python
Base.metadata.create_all(engine)
```

generated the whole database.

This is called

```
Code First
```

The Python code becomes the source of truth.

---

# 💡 Why We Ran

```bash
python -m database.create_tables
```

Instead of

```bash
python database/create_tables.py
```

Python packages work correctly only when executed as modules.

Using

```
-m
```

tells Python

```
Run this as a package.
```

That is why imports like

```python
from database.database import ...
```

worked correctly.

---

# 💡 Why Repository Converts Database Objects

The database returns

```
DBCharacter
```

The Game expects

```
Character
```

Repository performs the conversion.

```
DBCharacter

↓

Dictionary

↓

Character
```

The Game never sees SQLAlchemy.

Huge architecture improvement.

---

# 💡 Why We Still Return Dictionaries for Attributes

Database stores

```
CharacterAttribute
```

Game expects

```python
{
    "male": True,
    "alive": False
}
```

Repository converts

```
Rows

↓

Dictionary
```

The rest of the project remains unchanged.

---

# 💡 Complete Data Flow

This is the entire architecture after Day 41.

```
characters.json

↓

Seeder

↓

PostgreSQL

↓

SQLAlchemy

↓

PostgresRepository

↓

Character Objects

↓

CharacterEngine

↓

Game

↓

Player
```

Questions follow exactly the same path.

---

# 🐞 Debugging Problems I Solved Today

## Problem 1

```
ModuleNotFoundError

No module named sqlalchemy
```

Reason

Package installed globally,

not inside the virtual environment.

Solution

```bash
python -m pip install sqlalchemy psycopg2-binary
```

inside the activated venv.

---

## Problem 2

```
database is not a package
```

Reason

Running files directly.

Solution

Run

```bash
python -m database.create_tables
```

instead.

---

## Problem 3

```
Duplicate Primary Key
```

Reason

Questions used IDs

```
1-50

1-50

1-50
```

for each category.

Solution

Global IDs

```
Character

1-50

Animal

51-100

Object

101-150
```

---

## Problem 4

```
attribute_id

doesn't match

question.id
```

Reason

Foreign Keys point to another table.

Not a bug.

---

## Problem 5

```
No module named sqlalchemy
```

Even though pip showed SQLAlchemy installed.

Reason

Installed globally,

not inside the project's virtual environment.

Solution

Activate

```
.venv
```

and install packages again.

---

## Problem 6

Seeder crashed because tables already contained data.

Solution

Drop

↓

Recreate Tables

↓

Seed Again

Clean database.

---

# 🎯 What Changed Compared to Yesterday

Yesterday

```
Game

↓

JsonRepository

↓

JSON Files
```

Today

```
Game

↓

Repository Interface

↓

PostgresRepository

↓

SQLAlchemy ORM

↓

PostgreSQL
```

This is a major architectural milestone.

---

# 📝 Commands Used Today

## Install Packages

python -m pip install sqlalchemy psycopg2-binary

## Create Tables

python -m database.create_tables

## Seed Database

python -m database.run_seed

## PostgreSQL Service

Start PostgreSQL server

## Verify Tables

Open pgAdmin
Refresh
View characters
View attributes
View character_attributes
View questions

# 🧠 Interview Questions I Can Answer

- Why use PostgreSQL instead of JSON?
- What is SQLAlchemy ORM?
- What is an ORM?
- What is a Session?
- What is an Engine?
- Difference between flush() and commit().
- What is Normalization?
- What is a Foreign Key?
- What is a Many-to-Many relationship?
- Why use an Association Table?
- What is Repository Pattern?
- Why separate Domain Models from Database Models?
- Why use SQLAlchemy Relationships?
- What is Dependency Inversion?
- Why execute Python packages with `python -m`?
- Why seed a database instead of inserting rows manually?

---

# 🏆 Day 41 Final Reflection

Today was one of the most important learning days in the GuessWise project.

I transformed the project from a file-based application into a database-backed application using PostgreSQL and SQLAlchemy while preserving the existing game logic.

More importantly, I learned *why* software is designed this way. I now understand the purpose of repositories, database normalization, ORM models, relationships, sessions, foreign keys, association tables, and dependency inversion.

Instead of just making the project work, I learned how professional backend applications separate responsibilities, protect business logic from database changes, and build systems that can evolve over time.

This day marks the transition of GuessWise from a simple Python CLI project into a backend application with a scalable architecture.

