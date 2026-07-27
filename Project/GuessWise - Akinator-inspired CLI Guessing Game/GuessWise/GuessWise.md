# 🎯 GuessWise --- Akinator Inspired Intelligent Guessing Engine

> **GuessWise is a production-style backend project built to learn
> software engineering by developing a complete guessing engine from
> scratch.**
>
> From a simple JSON file to a layered architecture using PostgreSQL,
> SQLAlchemy, Repository Pattern, and multiple engines, this project
> represents my backend development journey.

![Python](https://img.shields.io/badge/Python-3.12-blue)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-red)
![Architecture](https://img.shields.io/badge/Clean-Architecture-success)
![Status](https://img.shields.io/badge/Version-v1.0-brightgreen)
![License](https://img.shields.io/badge/License-MIT-green)

------------------------------------------------------------------------

# 🌟 Project Vision

GuessWise is much more than a CLI game.

It was intentionally built as a learning project to practice how
professional backend systems evolve:

-   Build a working prototype
-   Refactor into clean architecture
-   Separate responsibilities
-   Introduce a database
-   Replace implementations without changing business logic
-   Design software that can grow

The long-term vision is to evolve GuessWise into a full-stack AI-powered
guessing platform.

------------------------------------------------------------------------

# ✨ Features

## Gameplay

-   Character category
-   Animal category
-   Object category
-   Dynamic question selection
-   Smart candidate filtering
-   Intelligent guessing

## Backend

-   Repository Pattern
-   SQLAlchemy ORM
-   PostgreSQL
-   Dependency Injection
-   Clean Architecture
-   Modular Design
-   Layered Application

------------------------------------------------------------------------

# 🏛 Final Architecture

``` text
                           User
                             │
                             ▼
                           Game
                             │
                             ▼
                    Knowledge Manager
                   ┌─────────┴─────────┐
                   ▼                   ▼
          Character Engine     Question Engine
                   │                   │
                   └─────────┬─────────┘
                             ▼
                  PostgreSQL Repository
                             │
                             ▼
                        PostgreSQL
```

------------------------------------------------------------------------

# 📂 Project Structure

``` text
GuessWise
│
├── database/
│   ├── database.py
│   ├── models.py
│   ├── create_tables.py
│   ├── seed.py
│   └── run_seed.py
│
├── repository/
│   ├── repository.py
│   ├── json_repository.py
│   └── postgres_repository.py
│
├── engines/
│   ├── character_engine.py
│   ├── question_engine.py
│   └── knowledge_manager.py
│
├── models/
├── data/
├── game.py
├── main.py
└── README.md
```

------------------------------------------------------------------------

# 🧠 Core Components

## Game

Coordinates the entire application and communicates with the user.

## Character Engine

Maintains the remaining candidates and filters them based on answers.

## Question Engine

Stores the remaining questions and removes those already asked.

## Knowledge Manager

Acts as the decision engine by selecting the most informative question
from the remaining candidates.

## Repository

Abstracts data access so the rest of the application is independent of
storage.

------------------------------------------------------------------------

# 🗄 Database Design

``` text
Characters
     │
     ├────────────┐
     ▼            ▼
CharacterAttributes
     ▲            │
     │            ▼
 Attributes <── Questions
```

Normalized tables eliminate duplicated attribute names and support
future expansion.

------------------------------------------------------------------------

# 🚀 Development Timeline

## Day 35--39

-   Planned the project
-   Implemented CLI
-   Stored data in JSON
-   Built filtering logic

## Day 40

-   Refactored into Character Engine
-   Refactored into Question Engine
-   Reduced responsibilities inside Game

## Day 41

-   Migrated JSON to PostgreSQL
-   Designed normalized database
-   Implemented SQLAlchemy models
-   Built PostgreSQL repository
-   Seeded the database

## Day 42

-   Introduced Knowledge Manager
-   Dynamic question selection
-   Improved architecture
-   Finalized GuessWise CLI v1.0

------------------------------------------------------------------------

# 📚 Software Engineering Concepts

-   Object-Oriented Programming
-   SOLID Principles
-   Single Responsibility Principle
-   Separation of Concerns
-   Repository Pattern
-   Dependency Injection
-   Layered Architecture
-   Database Normalization
-   SQLAlchemy ORM
-   PostgreSQL
-   Refactoring
-   Clean Code

------------------------------------------------------------------------

# 💻 Installation

``` bash
git clone <repo-url>
cd GuessWise

python -m venv .venv

# Windows
.venv\Scripts\activate

pip install -r requirements.txt

python -m database.create_tables
python -m database.run_seed

python main.py
```

------------------------------------------------------------------------

# 🔮 Future Roadmap

## Version 2

-   FastAPI REST API
-   React / Next.js frontend
-   JWT Authentication
-   Admin Dashboard
-   Docker

## Version 3

-   Entropy / Information Gain
-   Machine Learning
-   Self-learning knowledge base
-   Multiplayer mode
-   Analytics

------------------------------------------------------------------------

# 📈 What This Project Demonstrates

-   Backend application design
-   Clean architecture
-   Professional refactoring
-   Repository abstraction
-   Database modelling
-   ORM usage
-   Decision engine implementation

------------------------------------------------------------------------

# 👨‍💻 About the Developer

**Adyaprana Pradhan**

This project is part of my **Backend Developer Journey**, where I build
increasingly complex backend systems to master software engineering
through practical projects.

------------------------------------------------------------------------

# 🤝 Contributing

Contributions, suggestions, and improvements are welcome. Feel free to
fork the repository, open an issue, or submit a pull request.

------------------------------------------------------------------------

# 📄 License

Licensed under the MIT License.

------------------------------------------------------------------------

⭐ If you enjoyed this project, consider giving it a **Star** on GitHub!
