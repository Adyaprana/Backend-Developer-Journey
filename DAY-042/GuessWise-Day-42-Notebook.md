# 🚀 DAY 42 — GuessWise CLI v1.0 (Final Architecture & Knowledge Manager)

> "Today was the biggest architectural upgrade of the entire GuessWise CLI project."

---

# 📅 Day Objective

Today the goal was **NOT** to add more features.

Instead, the goal was to transform GuessWise from a **simple question-answer game** into an application that actually contains a small **decision engine**, just like Akinator.

This was also the final day of the CLI version.

Today's work focused on:

- Building the Knowledge Manager
- Refactoring Question Engine
- Improving Architecture
- Removing duplicated responsibilities
- Making the Game class much smaller
- Completing GuessWise CLI v1.0

---

# 📌 Where We Started

At the beginning of Day 42 our architecture looked like this:

```text
Game
 │
 ├── CharacterEngine
 │
 ├── QuestionEngine
 │
 └── Repository
```

The project worked...

but one important problem still existed.

---

# ❌ Problem 1

Game was deciding everything.

It was responsible for

- asking questions
- filtering characters
- deciding question order

That means the Game class was becoming too intelligent.

Game should only control the flow.

It should NEVER contain business logic.

---

# ❌ Problem 2

Question Engine still worked like this:

Question 1

↓

Question 2

↓

Question 3

↓

Question 4

↓

...

Every game asked the exact same sequence of questions.

This is NOT how Akinator works.

---

# ❌ Problem 3

Question selection wasn't intelligent.

Questions were simply taken one after another.

No matter what the player answered...

the next question never changed.

That meant the game wasn't actually "thinking."

---

# ❌ Problem 4

KnowledgeManager Version 1

The first implementation looked like this:

```python
KnowledgeManager(
    characters,
    questions
)
```

Inside it we stored

```python
self.characters
self.questions
```

---

This created a major bug.

Suppose the game starts with

35 candidates

Player answers

YES

CharacterEngine filters them

↓

18 candidates remain

BUT...

KnowledgeManager still had

35 candidates.

It never updated.

So it kept selecting questions using outdated data.

---

# Why This Was Wrong

The Knowledge Manager should NEVER own the character list.

The Character Engine already owns that data.

If two classes store the same information...

they eventually become different.

That is called

**Data Duplication**

and eventually causes

**Data Inconsistency.**

---

# ✅ Solution

Instead of passing

```python
characters
questions
```

we now pass

```python
CharacterEngine
QuestionEngine
```

```python
self.knowledge_manager = KnowledgeManager(
    self.character_engine,
    self.question_engine
)
```

Now the Knowledge Manager no longer owns the data.

It asks the engines whenever it needs information.

---

# Dependency Injection

This is another software engineering concept.

Instead of creating objects itself...

Knowledge Manager receives them.

```python
KnowledgeManager(
    character_engine,
    question_engine
)
```

This is called

**Dependency Injection (DI).**

---

# Why DI is Better

Old design

```text
KnowledgeManager

↓

Own copy of characters
```

New design

```text
KnowledgeManager

↓

CharacterEngine

↓

Latest Remaining Characters
```

Now there is only ONE source of truth.

That makes the project easier to maintain.

---

# New Architecture

```text
Game
 │
 ▼
KnowledgeManager
 │
 ├───────────────┐
 ▼               ▼
CharacterEngine  QuestionEngine
```

Notice something...

Game no longer needs to know

- where characters are stored
- where questions are stored

It only communicates with the Knowledge Manager.

That is much cleaner.

---

# Single Responsibility Principle

Today we improved SRP again.

Game

✅ Runs the game

CharacterEngine

✅ Filters characters

QuestionEngine

✅ Stores remaining questions

KnowledgeManager

✅ Chooses the smartest question

Repository

✅ Loads data

Each class now has ONE reason to change.

That is exactly what the Single Responsibility Principle teaches.

---

# Knowledge Manager Becomes the Brain

Instead of this

```text
Game

↓

Question Engine

↓

Question
```

we now have

```text
Game

↓

Knowledge Manager

↓

Best Question
```

This small change completely changes the architecture.

The Game no longer decides what to ask.

The Knowledge Manager becomes the brain of GuessWise.

---

# What We Learned

Today introduced several important concepts:

- Dependency Injection
- Data Consistency
- Data Duplication
- Single Source of Truth
- Better Responsibility Separation
- Knowledge Manager Architecture
- Decision Engine Design
- Software Refactoring

These concepts are used in real backend systems every day.

---

# 🚀 DAY-42 Part 2 — Building the Decision Engine

---

# Knowledge Manager Algorithm

The biggest feature added today was the algorithm that selects the next question.

Instead of asking questions one by one...

GuessWise now tries to choose the **best possible question**.

This is the first step toward building an Akinator-like engine.

---

# The Old System

Previously...

Question Engine controlled everything.

```text
Question 1

↓

Question 2

↓

Question 3

↓

Question 4
```

Every game looked identical.

No intelligence.

No decision making.

---

# The New System

Now...

Knowledge Manager asks

> "Which question will eliminate the most candidates?"

Instead of

> "Which question comes next?"

That is a huge architectural difference.

---

# Choosing the Best Question

For every remaining question...

Knowledge Manager checks

```python
for question in questions:
```

Then...

for every remaining character

```python
for character in characters:
```

it counts

```text
True

False
```

---

Example

Remaining Characters

```text
Virat
Sachin
Messi
Batman
Iron Man
```

Question

```text
Is Real?
```

Result

```text
True = 3

False = 2
```

Difference

```text
1
```

Very good question.

---

Another Question

```text
Is Male?
```

```text
True = 5

False = 0
```

Difference

```text
5
```

Terrible question.

It doesn't eliminate anyone.

---

# Score Calculation

We used

```python
score = abs(
    true_count - false_count
)
```

---

Suppose

```text
True = 10

False = 10
```

Difference

```text
0
```

Perfect.

Exactly half the candidates disappear.

---

Suppose

```text
True = 19

False = 1
```

Difference

```text
18
```

Very bad.

Almost nobody gets eliminated.

---

The smaller the score...

the better the question.

---

# Why Absolute Value?

Imagine

```text
True = 8

False = 12
```

Difference

```text
-4
```

or

```text
4
```

Both represent the same split.

So we use

```python
abs()
```

to remove the sign.

---

# Removing Asked Questions

Originally...

Knowledge Manager kept selecting

```text
Forest?

Forest?

Forest?
```

again and again.

Why?

Because the question was never removed.

---

Today we fixed it.

After selecting the best question

```python
self.question_engine.remove(
    best_question
)
```

Now

```text
Question

↓

Asked

↓

Removed

↓

Never Asked Again
```

This completely fixed the repeated-question bug.

---

# Refactoring Question Engine

This was another huge improvement.

Old Question Engine

```python
current_question()

next_question()

current_index
```

It assumed questions are sequential.

That design no longer worked.

---

Today we redesigned it.

New Question Engine

```python
remaining()

remove()

finished()

count()

reset()
```

Notice

No indexes.

No current question.

Knowledge Manager decides everything.

Question Engine simply stores questions.

---

# Why This Is Better

Old Design

```text
Question Engine

↓

Question Order
```

New Design

```text
Question Engine

↓

Question Storage

Knowledge Manager

↓

Question Selection
```

Each class has only one responsibility.

---

# Character Engine

Character Engine already handled

- filtering
- guessing
- counting

Today we kept it exactly the same.

That is actually a good sign.

Good software does NOT require changing every class whenever a feature is added.

Character Engine was already designed correctly.

---

# Processing Answers

Originally

Game handled

```python
if choice == "1":
```

```python
elif choice == "2":
```

This is business logic.

Game should not know how answers affect characters.

---

Today we introduced

```python
KnowledgeManager.process_answer()
```

Now

Game simply forwards the user's answer.

```python
self.knowledge_manager.process_answer(
    question,
    choice
)
```

Knowledge Manager decides what to do.

---

# Encapsulation

Before

```text
Game

↓

Filtering Logic
```

Now

```text
Game

↓

Knowledge Manager

↓

Character Engine
```

Filtering logic is hidden.

Game only knows

"I received an answer."

This is called

**Encapsulation.**

---

# Better Flow

Current Flow

```text
User

↓

Game

↓

Knowledge Manager

↓

Character Engine

↓

Remaining Characters
```

Game never touches filtering anymore.

This makes the architecture much cleaner.

---

# Concepts Learned Today

Today introduced

- Decision Algorithms
- Score-based Selection
- Refactoring
- Dynamic Question Selection
- Encapsulation
- Responsibility Separation
- Removing Sequential Logic
- Dependency Injection
- Single Source of Truth
- Software Architecture Evolution

These are concepts used in real production backend systems.

---



## GuessWise CLI v1.0

Every major change made during Day 42.

### Files Modified

-   `game.py`
-   `engines/knowledge_manager.py`
-   `engines/question_engine.py`

------------------------------------------------------------------------

## game.py

**Purpose**

-   Added `KnowledgeManager`
-   Delegated question selection
-   Delegated answer processing
-   Removed sequential question logic
-   Added CLI v1.0 title
-   Added `No useful questions remain.` safeguard

**Main Flow**

``` text
Game
 ↓
KnowledgeManager.best_question()
 ↓
Display Question
 ↓
KnowledgeManager.process_answer()
 ↓
CharacterEngine.filter()
```

## Code

```python
from repository.postgres_repository import PostgresRepository
from engines.character_engine import CharacterEngine
from engines.question_engine import QuestionEngine
from engines.knowledge_manager import KnowledgeManager


class Game:
    def __init__(self):
        self.repository = PostgresRepository()

    def start(self):
        self.all_characters = self.repository.get_characters()
        self.questions = self.repository.get_questions()

        print("Game Started")
        print(f"Loaded {len(self.all_characters)} characters")
        print(f"Loaded {len(self.questions)} questions")

        self.show_menu()
        
    
    def show_menu(self):
        while True:
            print("===================================")
            print("      🎯 GuessWise CLI v1.0        ")
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
        
        while True:
            if self.question_engine.finished():
                print("🤔 I couldn't uniquely identify your answer.")
                print("\nPossible Matches:")
                print("\nRemaining Candidates:")
                for character in self.character_engine.remaining():
                    print("-", character.name)

                if self.play_again():
                    self.select_category(self.current_category)
                    return self.play_game()
                return

            print("\n=========================")
            print("🎯 GuessWise:",self.current_category.title())
            print("=========================")
            print(f"Category : {self.current_category.title()}")
            print(f"Remaining Candidates : {self.character_engine.count()}")
            
            asked = 50 - self.question_engine.count() + 1
            print(f"Question {asked}")
            question = self.knowledge_manager.best_question()
            if question is None:
                print("No useful questions remain.")
                break
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
            
            if choice in ["1", "2"]:
                self.knowledge_manager.process_answer(
                    question,
                    choice
                )

            elif choice in ["3", "4", "5"]:
                print(f"You selected: {answers[choice]}")

            else:
                print("Invalid choice! Please enter a number from 1 to 5.")
                continue

            print("\nRemaining Candidates:")
            for character in self.character_engine.remaining():
                print("-", character.name)

            if self.character_engine.has_guess():
                print("\n🎉 I guessed your answer!")
                guess = self.character_engine.guess()
                print(f"It's: {guess.name}")

                if self.play_again():
                    self.select_category(self.current_category)
                    return self.play_game()
                return
            
            elif self.character_engine.count() == 0:
                print("\n❌ No matching character found.")
                
                if self.play_again():
                    self.select_category(self.current_category)
                    return self.play_game()
                return

    def select_category(self, category: str):
        self.current_category = category

        characters = [
            character
            for character in self.all_characters
                if character.category == category
        ]
        self.character_engine = CharacterEngine(characters)

        questions = [
            question
            for question in self.questions
            if question.category == category
        ]
        self.question_engine = QuestionEngine(questions)
        self.knowledge_manager = KnowledgeManager(
            self.character_engine,
            self.question_engine
        )

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

------------------------------------------------------------------------

## engines/knowledge_manager.py

**Purpose**

KnowledgeManager became the brain of GuessWise.

Responsibilities:

-   Read remaining characters
-   Read remaining questions
-   Choose best question
-   Remove asked question
-   Process answers

Algorithm:

``` python
score = abs(true_count - false_count)
```

Skip useless questions:

``` python
if true_count == 0 or false_count == 0:
    continue
```
## Code

``` python
"""
Knowledge Manager

Responsible for selecting
the best next question.

The Game never decides
which question to ask.
"""


from engines.character_engine import CharacterEngine
from engines.question_engine import QuestionEngine
from models.question import Question


class KnowledgeManager:
    """Chooses the best question."""

    def __init__(
        self,
        character_engine: CharacterEngine,
        question_engine: QuestionEngine
    ):
        self.character_engine = character_engine
        self.question_engine = question_engine

    def best_question(self) -> Question:
        """Choose the best remaining question."""

        characters = self.character_engine.remaining()
        questions = self.question_engine.remaining()

        best_question = None
        best_score = float("inf")

        for question in questions:

            true_count = 0
            false_count = 0

            for character in characters:
                value = character.attributes.get(
                    question.attribute,
                    False
                )

                if value:
                    true_count += 1
                else:
                    false_count += 1
            
            if true_count == 0 or false_count == 0:
                continue
            score = abs(true_count - false_count)

            if score < best_score:
                best_score = score
                best_question = question

        if best_question:
            self.question_engine.remove(best_question)

        return best_question



    def process_answer(
        self,
        question: Question,
        answer: str
    ):
        """Process the user's answer."""

        if answer == "1":
            self.character_engine.filter(
                question.attribute,
                True
            )

        elif answer == "2":
            self.character_engine.filter(
                question.attribute,
                False
            )
        else:
            pass
```
------------------------------------------------------------------------

## engines/question_engine.py

QuestionEngine no longer manages indexes.

Old:

-   current_question()
-   next_question()

New:

-   remaining()
-   remove()
-   finished()
-   count()
-   reset()
## Code

``` python
"""
Question Engine

Responsible for managing
the remaining questions.
"""

from models.question import Question


class QuestionEngine:
    """Stores and manages remaining questions."""

    def __init__(self, questions: list[Question]):
        self.questions = questions.copy()

    def remaining(self) -> list[Question]:
        """Return all remaining questions."""
        return self.questions

    def remove(self, question: Question):
        """Remove a question after it has been asked."""
        if question in self.questions:
            self.questions.remove(question)

    def finished(self) -> bool:
        """Return True if there are no more questions."""
        return len(self.questions) == 0

    def count(self) -> int:
        """Return number of remaining questions."""
        return len(self.questions)

    def reset(self, questions: list[Question]):
        """Reset the question list."""
        self.questions = questions.copy()

```
------------------------------------------------------------------------

---

# 🚀 DAY-42 Part 3 — Final Polish, Version 1.0 Release & Lessons Learned

---

# Final Architecture

After eight days of continuous refactoring, GuessWise finally reached its Version 1.0 architecture.

```text
                          User
                            │
                            ▼
                         Game.py
                            │
                            ▼
                  Knowledge Manager
                  ├──────────────────┐
                  ▼                  ▼
          Character Engine     Question Engine
                  │                  │
                  └─────────┬────────┘
                            ▼
                  PostgreSQL Repository
                            │
                            ▼
                      PostgreSQL Database
```

This architecture is much closer to how real backend applications are designed.

Each layer has one responsibility.

Each class communicates only with the layer below it.

---

# Evolution of the Project

The project did not reach this architecture immediately.

It evolved gradually.

## Version 0

Everything inside one file.

```text
main.py

↓

Everything
```

Problems

- Massive file
- Hard to maintain
- Hard to understand
- No reusable code

---

## Version 0.5

Separated Models

```text
Models

↓

Game
```

Better than before.

Still tightly coupled.

---

## Version 0.6

Repository Pattern

```text
Game

↓

Repository

↓

JSON
```

Game no longer cared where data came from.

Huge improvement.

---

## Version 0.7

Character Engine

```text
Game

↓

Character Engine
```

Filtering logic moved out of Game.

Game became smaller.

---

## Version 0.8

Question Engine

Question management moved out of Game.

Game became even cleaner.

---

## Version 0.9

PostgreSQL

Project moved from JSON storage to a relational database.

Benefits

- Better scalability
- Normalized data
- Faster querying
- Professional backend architecture

---

## Version 1.0

Knowledge Manager

The final missing piece.

Now the project contains a real decision engine.

This is the biggest architectural achievement of the CLI version.

---

# JSON → PostgreSQL

Originally

```text
JSON Files

↓

Load Everything
```

Now

```text
PostgreSQL

↓

Repository

↓

Game
```

Advantages

- Permanent storage
- Normalized schema
- No duplicated attributes
- Better scalability
- Easier future expansion

This is exactly how many backend applications store their data.

---

# Database Normalization

Instead of storing

```text
Virat

real = True

male = True

alive = True

...

Sachin

real = True

male = True

alive = True
```

again and again,

we created

```text
Attributes Table

↓

real

male

alive

fictional

...
```

Characters now simply reference these attributes.

Benefits

- Less duplication
- Easier updates
- Better consistency
- Professional relational design

---

# Repository Pattern

One of the biggest lessons of this project.

Game never reads

```python
characters.json
```

or

```sql
SELECT *
```

Instead

Game asks

```python
repository.get_characters()
```

Repository decides

whether the data comes from

- JSON
- PostgreSQL
- API
- CSV
- MongoDB

Game never changes.

That is the real power of abstraction.

---

# What I Learned During GuessWise

## Python

- Classes
- Objects
- Dataclasses
- Type Hints
- Modules
- Packages
- Imports

---

## Object-Oriented Programming

- Encapsulation
- Abstraction
- Composition
- Responsibility Separation

---

## Software Engineering

- SOLID Principles
- Repository Pattern
- Layered Architecture
- Dependency Injection
- Refactoring
- Separation of Concerns

---

## Database

- PostgreSQL
- SQLAlchemy ORM
- Relationships
- Foreign Keys
- Normalization
- Seeding
- Repository Integration

---

## Backend Development

- Project Structure
- Data Layer
- Business Layer
- Engine Layer
- Game Layer

This project feels much closer to a real backend application than a simple Python project.

---

# Biggest Lessons

One of the biggest things I learned is that writing code is not the difficult part.

Designing software is.

Good software is built by asking questions like

- Which class should own this responsibility?
- Should this class know about this data?
- Am I duplicating information?
- Can this code be reused?
- What happens if requirements change?

Those questions matter much more than writing another function.

---

# GuessWise CLI v1.0

Final Features

- ✅ Character Category
- ✅ Animal Category
- ✅ Object Category
- ✅ PostgreSQL Database
- ✅ SQLAlchemy ORM
- ✅ Repository Pattern
- ✅ Character Engine
- ✅ Question Engine
- ✅ Knowledge Manager
- ✅ Dynamic Question Selection
- ✅ Modular Architecture
- ✅ Clean Code
- ✅ Layered Design

The project successfully reached all the goals planned for Version 1.

---

# Future Vision — GuessWise v2

The CLI version is complete.

The next version will transform GuessWise into a full-stack application.

Planned features

- FastAPI Backend
- REST API
- React / Next.js Frontend
- User Authentication
- Admin Dashboard
- Statistics
- Leaderboards
- Better Decision Algorithm (Entropy / Information Gain)
- Machine Learning Based Knowledge Engine
- AI-assisted Question Selection
- Cloud Database
- Docker Deployment
- CI/CD Pipeline

Version 2 will build on the architecture created in Version 1 rather than replacing it.

---

# Final Thoughts

GuessWise started as a simple command-line guessing game.

By the end of this journey, it became a well-structured backend project demonstrating professional software engineering practices.

More importantly, this project was never just about building a game.

It was about learning **how to think like a backend engineer**:

- designing before coding,
- separating responsibilities,
- building reusable components,
- and writing code that can grow over time.

GuessWise CLI v1.0 marks the completion of that first milestone.

The next milestone begins with GuessWise v2.

---

# ✅ Day 42 Summary

Today I completed the final version of GuessWise CLI.

Major achievements:

- Built the Knowledge Manager (decision engine)
- Replaced sequential question selection with dynamic question selection
- Refactored Question Engine to manage remaining questions instead of indexes
- Moved answer-processing logic from `Game` to `KnowledgeManager`
- Applied Dependency Injection between engines
- Eliminated repeated-question bugs
- Achieved a cleaner, layered architecture
- Finalized GuessWise CLI v1.0
- Prepared the project for future expansion into a FastAPI + React application

---

# 🏁 End of GuessWise CLI v1.0

**Project Status:** ✅ Completed

**Version:** 1.0

**Duration:** Day 35 → Day 42

*"Every great software project starts with simple code, but becomes valuable through thoughtful architecture and continuous refactoring."*

