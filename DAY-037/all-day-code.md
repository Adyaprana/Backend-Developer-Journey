# 📅 Backend Developer Journey — Day 37

## 🎯 Goal Achieved

* ✅ Created `Character` model using `@dataclass`
* ✅ Created `Question` model using `@dataclass`
* ✅ Created Repository Interface
* ✅ Implemented `JsonRepository`
* ✅ Loaded JSON data
* ✅ Converted JSON → Python Objects
* ✅ Tested everything from `main.py`

---

# 📁 Project Structure

```text
GuessWise/

├── main.py
│
├── models/
│   ├── character.py
│   └── question.py
│
├── repository/
│   ├── repository.py
│   └── json_repository.py
│
└── data/
    ├── characters.json
    └── questions.json
```

---

# 📄 File: models/character.py

```python
from dataclasses import dataclass


@dataclass
class Character:
    id: int
    name: str
    category: str
    attributes: dict[str, bool]
```

---

# 📄 File: models/question.py

```python
from dataclasses import dataclass


@dataclass
class Question:
    id: int
    text: str
    attribute: str
```

---

# 📄 File: repository/repository.py

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

---

# 📄 File: repository/json_repository.py

```python
import json

from models.character import Character
from models.question import Question
from repository.repository import Repository


class JsonRepository(Repository):

    def get_characters(self) -> list[Character]:
        with open("data/characters.json", "r") as file:
            data = json.load(file)

        characters: list[Character] = []

        for item in data:
            character = Character(**item)
            characters.append(character)

        return characters

    def get_questions(self) -> list[Question]:
        with open("data/questions.json", "r") as file:
            data = json.load(file)

        questions: list[Question] = []

        for item in data:
            question = Question(**item)
            questions.append(question)

        return questions
```

---

# 📄 File: main.py

```python
from repository.json_repository import JsonRepository

repository = JsonRepository()

characters = repository.get_characters()
questions = repository.get_questions()

print("Characters:")
for character in characters:
    print(character)

print("\nQuestions:")
for question in questions:
    print(question)
```

---

# 📄 File: data/characters.json

```json
[
    {
        "id": 1,
        "name": "Virat Kohli",
        "category": "character",
        "attributes": {
            "real": true,
            "alive": true,
            "male": true,
            "indian": true,
            "cricketer": true
        }
    }
]
```

---

# 📄 File: data/questions.json

```json
[
    {
        "id": 1,
        "text": "Is your character real?",
        "attribute": "real"
    }
]
```

---

# 🧠 Concepts Learned Today

* Python `@dataclass`
* Type Hints
* Repository Pattern
* Abstract Base Class (`ABC`)
* `@abstractmethod`
* JSON Parsing
* JSON → Python Dictionary
* Dictionary → Dataclass Object (`**item`)
* Object-Oriented Design
* Separation of Concerns
* Layered Architecture

---

# 🏗️ Architecture After Day 37

```text
main.py
    │
    ▼
JsonRepository
    │
    ▼
characters.json / questions.json
    │
    ▼
Character / Question Objects
```

---

# ✅ Day 37 Milestone

Your project now has a fully working **Data Access Layer**.

The application can:

* Read JSON files
* Convert JSON into Python objects
* Return strongly typed objects
* Keep the game independent of the data source

This architecture is ready for future migration to PostgreSQL without changing the game logic.
