> Backend Developer Journey
> Day: 38

# Goal

Today we transformed GuessWise from a data-loading project into an interactive CLI application.

## What I built

- Game class
- Game flow
- Main menu
- Character mode
- Question display
- User answer collection
- Input validation
- Better architecture

---

# Project Flow

```
main.py
    |
    v
Game.start()
    |
    +--> Load Characters
    |
    +--> Load Questions
    |
    +--> Show Menu
             |
             +--> Character Mode
                        |
                        +--> Display Question
                        |
                        +--> Get Answer
                        |
                        +--> Print Selected Answer
```
---

# File Paths -> C:\A_MY THINGS\001\Backend-Developer-Journey\Project

## game.py

```python
from repository.json_repository import JsonRepository


class Game:
    def __init__(self):
        self.repository = JsonRepository()

    def start(self):
        self.characters = self.repository.get_characters()
        self.questions = self.repository.get_questions()

        print("Game Started")
        print(f"Loaded {len(self.characters)} characters")
        print(f"Loaded {len(self.questions)} questions")

        self.show_menu()

    def show_menu(self):
        while True:
            print("===================================")
            print("        🎯 GuessWise")
            print("===================================")

            print("1. Character")
            print("2. Animal")
            print("3. Object")
            print("4. Exit")

            choice = input("\\nEnter your choice (1-4): ").strip()

            if choice == "1":
                self.character_mode()

            elif choice == "2":
                print("Animal Mode")

            elif choice == "3":
                print("Object Mode")

            elif choice == "4":
                print("Game Exit")
                break

            else:
                print("Invalid choice! Please enter a number from 1 to 4.")

    def character_mode(self):
        while True:
            print("\\n=========================")
            print("Character Mode")
            print("=========================")
            print("\\nQuestion 1\\n")

            question = self.questions[0]
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

            choice = input("\\nEnter your choice (1-5): ").strip()

            if choice in answers:
                print(f"You selected: {answers[choice]}")
                break

            print("Invalid choice! Please enter a number from 1 to 5.")
```
---

## game.py

```python
from game import Game

game = Game()
game.start()

```
# 🎮 GuessWise: Architecture & Game Flow Design

## 🧠 Why We Created the `Game` Class
The `Game` class controls the overall application flow. To ensure clean code, it follows the **Separation of Concerns** principle:

* **What it does:** Coordinates the execution and states of the application.
* **What it does NOT do:** 
  * Read raw JSON files.
  * Execute SQL queries.
  * Store low-level database logic.

---

## 🗄️ Why Use the Repository Pattern?
The `Game` class should never know the technical details of where its data comes from. 

* **Today:** We use a **JSON Repository**.
* **Tomorrow:** We can switch to a **PostgreSQL Repository**.
* **The Benefit:** The core game engine code remains completely unchanged, regardless of storage backend updates.

---

## 💾 Why Use `self.characters`?
Local variables disappear as soon as a function finishes executing. 

* **Persistence:** `self.characters` belongs to the instance of the `Game` object.
* **Reusability:** It saves the data so it can be reused across future methods like:
  * `ask_question()`
  * `filter_characters()`
  * `guess_character()`

---

## 🛠️ Method Breakdown & Modular Design

### `show_menu()`
Has exactly **one responsibility**: Display the main user interface menu and process the initial numeric selection.

### `character_mode()`
Keeps character-specific quiz logic cleanly separated from the core main menu. This modular design makes the game engine significantly easier to extend with future modes (like Animal or Object modes).

---

## 🗺️ Why Use Dictionary Mapping?

Instead of building massive, messy conditional logic like this:
```python
if choice == "1":
    print("Yes")
```

We map user inputs directly to data tables:
```python
answers = {
    "1": "Yes",
    "2": "No",
    "3": "Probably",
    "4": "Probably Not",
    "5": "Don't Know"
}
```

### Key Benefits:
* Much cleaner layout.
* Easier to maintain and expand.
* Completely eliminates long, repetitive `if`/`elif` code chains.

---

## 🖥️ Expected Console Output

```text
Game Started
Loaded 1 characters
Loaded 1 questions

===================================
🎯 GuessWise
===================================
1. Character
2. Animal
3. Object
4. Exit

Enter your choice (1-4): 1

=========================
Character Mode
=========================

Question 1

Is your character real?

1. Yes
2. No
3. Probably
4. Probably Not
5. Don't Know

Enter your choice (1-5): 1

You selected: Yes
```

---

## 🎓 Concepts Learned
* **Layered Architecture** & **Repository Pattern**
* **Separation of Concerns (SoC)**
* **Single Responsibility Principle (SRP)**
* **Dataclasses** (used previously)
* **Object-Oriented Programming (OOP)**
* **Method Decomposition** & **Input Validation**
* **CLI Design** & **Dictionary Lookup Mapping**

---
