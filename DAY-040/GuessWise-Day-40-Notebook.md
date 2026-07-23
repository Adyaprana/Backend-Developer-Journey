# GuessWise --- Day 40 Development Notes

> **Project:** GuessWise (CLI Akinator Clone)\
> **Day:** 40\
> **Goal:** Refactor the project by introducing Engine classes while
> keeping the game behavior unchanged.

## Objective

Today focused on **refactoring**, not adding new features. The goal was
to move responsibilities out of `Game` into dedicated engine classes
while preserving the existing behavior.

## Folder Changes

``` text
GuessWise/
├── engines/
│   ├── __init__.py
│   ├── character_engine.py
│   └── question_engine.py
```

### Why `__init__.py`?

-   Marks the folder as a Python package.
-   Allows imports like:

``` python
from engines.character_engine import CharacterEngine
```

The file is empty because it only identifies the directory as a package.

## CharacterEngine

Responsibilities:

-   Store candidates
-   Filter candidates
-   Count remaining candidates
-   Return remaining candidates
-   Return the final guess

Implemented methods:

-   `__init__()`
-   `remaining()`
-   `filter()`
-   `count()`
-   `has_guess()`
-   `guess()`

The engine contains **business logic only**. It does not print, read
JSON, or ask for user input.

## QuestionEngine

Responsibilities:

-   Store questions
-   Return current question
-   Move to the next question
-   Reset navigation
-   Detect when all questions have been used

Implemented methods:

-   `__init__()`
-   `current_question()`
-   `next_question()`
-   `reset()`
-   `finished()`
-   `question_number()`

## Game Refactor

### Before

`Game` managed:

-   Question index
-   Character filtering
-   Candidate storage
-   Remaining candidates
-   Guess detection

### After

`Game` now:

-   Loads data
-   Shows menus
-   Accepts input
-   Coordinates `CharacterEngine`
-   Coordinates `QuestionEngine`

## Important Code Changes

### Character Engine

``` python
self.character_engine.filter(question.attribute, True)
```

``` python
self.character_engine.count()
```

``` python
guess = self.character_engine.guess()
```

### Question Engine

``` python
question = self.question_engine.current_question()
```

``` python
self.question_engine.next_question()
```

``` python
self.question_engine.finished()
```

## Architecture

``` text
main.py
    │
    ▼
Game
 │
 ├── JsonRepository
 ├── CharacterEngine
 └── QuestionEngine
```

## Design Principles

-   Single Responsibility Principle (SRP)
-   Separation of Concerns
-   Composition
-   Encapsulation
-   Modular Programming
-   Refactoring

## Why This Matters

Instead of one large `Game` class doing everything, each class now has a
clear responsibility.

If the filtering algorithm changes, only `CharacterEngine` changes.

If question navigation changes, only `QuestionEngine` changes.

If the data source changes from JSON to PostgreSQL, only the repository
changes.

This makes the project easier to maintain, test, and extend.


## Day 40 Summary

✅ Introduced `CharacterEngine`

✅ Introduced `QuestionEngine`

✅ Refactored `Game`

✅ Improved project architecture

✅ Prepared the project for future SQLAlchemy, PostgreSQL, and FastAPI
integration.

## Architecture Review

``` text
GuessWise
│
├── main.py
│
├── game.py
│
├── repository/
│      │
│      ├── repository.py
│      └── json_repository.py
│
├── models/
│      ├── character.py
│      └── question.py
│
├── engines/
│      ├── character_engine.py
│      └── question_engine.py
│
└── data/
       ├── characters.json
       └── questions.json
```