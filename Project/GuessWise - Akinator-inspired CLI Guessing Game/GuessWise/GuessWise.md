````markdown
# 🎯 GuessWise

> A command-line Akinator-inspired guessing game built from scratch in Python to learn professional backend development.

## 📖 About

GuessWise is a backend-focused project where the computer tries to guess the character, animal, object, or fictional personality that the user is thinking of by asking a series of questions.

This project is being developed incrementally, following real-world software engineering principles such as clean architecture, modular design, and separation of concerns.

The goal is not only to build a game but also to learn how professional backend applications are designed from scratch.

---

## 🚀 Current Version

**Version:** `v1.0 (In Development)`

### Current Features

- Project initialization
- Modular project structure
- JSON-based data storage
- Repository pattern (planned)
- Object-Oriented Design (planned)

---

## 🛠️ Tech Stack

- Python 3
- JSON
- Git & GitHub

### Planned Technologies

- PostgreSQL
- SQLAlchemy
- FastAPI
- Docker
- Redis
- React / Next.js

---

## 📂 Project Structure

```text
guesswise/

├── main.py
├── game.py
├── README.md
├── requirements.txt
├── .gitignore

├── models/
│   ├── __init__.py
│   ├── character.py
│   └── question.py

├── repository/
│   ├── __init__.py
│   ├── repository.py
│   └── json_repository.py

├── engines/
│   ├── __init__.py
│   ├── character_engine.py
│   └── question_engine.py

├── utils/
│   ├── __init__.py
│   ├── display.py
│   └── validation.py

├── data/
│   ├── characters.json
│   └── questions.json

└── tests/
````

---

## 🏗️ Software Architecture

```text
User
   │
   ▼
Game
   │
   ▼
Question Engine
   │
   ▼
Character Engine
   │
   ▼
Repository Interface
   │
   ├── JSON Repository
   └── PostgreSQL Repository (Future)
```

The game logic never directly accesses the data source. This makes it easy to replace JSON with PostgreSQL in future versions without changing the core application logic.

---

## 🛣️ Roadmap

### Version 1

* CLI Game
* JSON Storage
* Character Filtering
* Guessing Engine

### Version 2

* PostgreSQL Integration
* SQLAlchemy ORM

### Version 3

* FastAPI REST API

### Version 4

* Authentication
* Admin Panel
* CRUD Operations

### Version 5

* React / Next.js Frontend

### Version 6

* Learning Engine

### Version 7

* AI-powered Question Selection

---

## 📚 Learning Goals

This project is designed to strengthen practical knowledge of:

* Python
* Object-Oriented Programming
* File Handling
* JSON
* Software Architecture
* Repository Pattern
* SQLAlchemy
* PostgreSQL
* FastAPI
* Clean Code
* Modular Programming

---

## 🤝 Contributing

This project is currently being developed as part of my Backend Developer Journey.

Contributions, suggestions, and feedback are always welcome.

---

## 📄 License

This project is licensed under the MIT License.

```
```
