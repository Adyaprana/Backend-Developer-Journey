# DAY-35.md

# 🎯 Project Planning Day (Before Coding Starts)

> **Project Name:** GuessWise (Akinator-inspired CLI Guessing Game)
>
> **Version:** v1.0 Planning
>
> **Roadmap Days:** 35 → 42
>
> **Author:** Adyaprana Pradhan
>
> **Status:** Planning Complete → Development Starts Day 36

---

# 📌 Overview

Instead of spending Week 6 revising Python by solving random problems, this week will be converted into a real software engineering sprint.

The goal is to build an Akinator-inspired guessing game completely from scratch while applying everything learned in the last five weeks.

This project is **not** intended to copy Akinator's AI.

Instead, it is meant to teach:

* Software Architecture
* Python Project Structure
* Object-Oriented Programming
* JSON Data Handling
* SQLAlchemy
* PostgreSQL
* Repository Pattern
* CRUD Operations
* Backend Thinking

Every version should be built as if it were going into production.

---

# 🎯 Main Goal

Create a terminal application where

* User thinks of a character
* Game asks intelligent questions
* User answers
* Characters are filtered
* Game eventually guesses the character

---

# 🚀 Learning Goals

By completing this project you should naturally revise

* Variables
* Data Types
* Functions
* Loops
* Conditions
* Lists
* Tuples
* Dictionaries
* Sets
* Classes
* Objects
* JSON
* File Handling
* SQL
* PostgreSQL
* SQLAlchemy
* Software Architecture
* Repository Pattern
* OOP

without doing boring revision.

---

# 🚀 Project Versions

---

## Version 1

CLI

Storage

JSON

Learning

* Python
* OOP
* JSON
* Architecture

---

## Version 2

Storage

PostgreSQL

Learning

* SQLAlchemy
* CRUD
* Repository Pattern

---

## Version 3

FastAPI

REST API

Learning

* Backend Development
* HTTP
* JSON Responses

---

## Version 4

React / Next.js

Learning

* Frontend
* API Integration

---

## Version 5

Authentication

Learning

* JWT
* Login
* Register
* User Profiles

---

## Version 6

Learning Engine

Game remembers

* New Characters
* New Questions

---

## Version 7

AI Powered

Smarter Question Selection

OpenAI / Local LLM

---

# 🎯 Current Scope

Only

Version 1

and

Version 2

---

# ❌ Out Of Scope

No AI

No Machine Learning

No Authentication

No React

No Docker

No FastAPI

No Cloud Deployment

---

# 📁 Final Folder Structure

```
GuessWise/

│

├── src/

│   ├── main.py

│   ├── game.py

│

│   ├── engines/

│   │

│   ├── character_engine.py

│   ├── question_engine.py

│

│

│   ├── repository/

│   │

│   ├── repository.py

│   ├── json_repository.py

│   ├── postgres_repository.py

│

│

│   ├── models/

│   │

│   ├── character.py

│   ├── question.py

│

│

│   ├── utils/

│   │

│   ├── display.py

│   ├── validation.py

│

│

│   ├── config.py

│

│

├── data/

│

├── characters.json

├── questions.json

│

├── tests/

│

├── docs/

│

├── README.md

├── requirements.txt

└── LICENSE
```

---

# 🏗 High Level Architecture

```
User

↓

Game

↓

Question Engine

↓

Character Engine

↓

Repository

↓

JSON

or

PostgreSQL
```

Notice

Game

never knows

where data comes from.

That is one of the biggest backend principles.

---

# 🧠 Software Layers

## Presentation Layer

Handles

* CLI
* User Input
* Printing

Files

```
main.py

display.py
```

---

## Business Layer

Contains

All Game Logic

Files

```
game.py

character_engine.py

question_engine.py
```

---

## Data Layer

Loads

Stores

Updates

Characters

Questions

Files

```
repository.py

json_repository.py

postgres_repository.py
```

---

## Models

Represents

Objects

```
Character

Question
```

---

# 🧠 OOP Design

---

## Character

Represents

One Character

Properties

```
name

attributes
```

Methods

```
matches()

display()
```

---

## Question

Represents

One Question

Properties

```
text

property
```

Methods

```
ask()
```

---

## Repository

Responsible For

Loading Data

Methods

```
load_characters()

load_questions()
```

---

## CharacterEngine

Responsible For

Filtering Characters

Methods

```
filter()

remaining()

guess()
```

---

## QuestionEngine

Responsible For

Asking Questions

Input Validation

Methods

```
next_question()

validate()

ask()
```

---

## Game

Controls

Entire Game

Methods

```
start()

play()

guess()

restart()
```

---

# 🧠 Programming Principles

Each class

Only one responsibility.

Never mix

Printing

Database

Game Logic

Everything separated.

---

# 🎯 Repository Pattern

Instead of

```
Game

↓

JSON
```

Use

```
Game

↓

Repository

↓

JSON

or

↓

PostgreSQL
```

Tomorrow

Game

doesn't change.

Only Repository changes.

Professional Architecture.

---

# 📊 Data Flow

```
Start Game

↓

Load Characters

↓

Load Questions

↓

Initialize Remaining Characters

↓

Ask Question

↓

User Answers

↓

Character Engine Filters

↓

Remaining > 1 ?

↓

YES

↓

Ask Next Question

↓

Remaining == 1

↓

Guess Character

↓

Correct ?

↓

Game Over
```

---

# 🎯 Filtering Algorithm

Pseudo Code

```
remaining = all_characters

for every question

    ask question

    answer = user input

    remove characters

    if only one remains

        guess

    else

        continue
```

---

# 🧠 Future Smart Question Algorithm

Current

Questions

Fixed Order

Future

Choose question

that divides

remaining characters

almost equally.

Example

```
20 Characters

↓

Question

↓

10 Yes

10 No

↓

Excellent Question
```

Better than

```
19 Yes

1 No
```

---

# 📄 JSON Structure

## characters.json

```json
[
  {
    "name": "Virat Kohli",
    "real": true,
    "male": true,
    "indian": true,
    "cricketer": true
  }
]
```

---

## questions.json

```json
[
  {
    "question": "Is your character real?",
    "property": "real"
  }
]
```

---

# 🧠 Version 2 Database Design

Tables

```
characters

questions

attributes
```

Later

```
users

games

history
```

---

# 🎯 Coding Standards

Follow

PEP8

Maximum

79-100 characters

Use

Type Hints

Everywhere

Example

```python
def load_characters() -> list:
```

---

Use

Docstrings

Every Function

Example

```python
"""
Loads characters
from repository.
"""
```

---

Never

Hardcode

Magic Numbers

Instead

```
MAX_QUESTIONS

DEFAULT_PATH
```

inside

config.py

---

# 🧪 Testing Strategy

Every module

Should be tested

Separately

Character

Question

Repository

Game

---

# 🔀 Git Workflow

```
main

↓

feature/models

↓

feature/game

↓

feature/database

↓

merge
```

Even if working alone,

practice using branches.

---

# 📝 Commit Format

```
feat:

fix:

refactor:

docs:

test:
```

Examples

```
feat: add character model

feat: add filtering algorithm

fix: input validation bug

docs: update README
```

---

# 🎯 Daily Plan

---

# ✅ Day 35

Planning

Architecture

Folder Structure

Flowchart

JSON Design

Repository Pattern

Milestone

No Coding

---

# ✅ Day 36

Create Repository

Project Structure

Character Class

Question Class

Load JSON

Verify Data Loading

---

# ✅ Day 37

Question Engine

Input Validation

Question Flow

CLI Improvements

---

# ✅ Day 38

Character Engine

Filtering Algorithm

Guess Logic

Game Working

---

# ✅ Day 39

Refactor

Bug Fixes

Improve CLI

Error Handling

Documentation

---

# ✅ Day 40

Replace JSON

↓

PostgreSQL

↓

SQLAlchemy

Repository Updated

No Game Logic Changes

---

# ✅ Day 41

CRUD

Add Character

Delete Character

Update Character

Search Character

---

# ✅ Day 42

Testing

Documentation

README

Screenshots

GitHub Release

LinkedIn Post

v1.0 Release

---

# 🎯 Milestones

Day 36

✅ Data Loads

---

Day 37

✅ Questions Work

---

Day 38

✅ Game Playable

---

Day 39

✅ Stable Version

---

Day 40

✅ PostgreSQL Connected

---

Day 41

✅ Admin CRUD

---

Day 42

✅ Production Ready CLI

---

# 📈 Future Roadmap

```
CLI

↓

SQLite

↓

PostgreSQL

↓

FastAPI

↓

Authentication

↓

REST API

↓

React

↓

Learning Engine

↓

AI

↓

Deployment
```

---

# 🎯 Success Criteria

By Day 42

I should be able to

* Build a modular Python application
* Design software architecture
* Work with JSON and PostgreSQL
* Use SQLAlchemy ORM
* Apply OOP principles
* Implement CRUD operations
* Follow clean project structure
* Write maintainable code
* Push a production-quality repository to GitHub

---

# 🏁 End of Planning

Planning is complete.

Development officially starts on **Day 36**.

From this point onward, every day has a clear deliverable, and by Day 42 the project should reach **Version 1.0** with a modular CLI architecture, PostgreSQL integration, and professional documentation ready for GitHub.
