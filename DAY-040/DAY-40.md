# DAY 40 — GuessWise: Engine Classes, Refactoring + LeetCode In-Place Marking

> **Project:** GuessWise — Architecture Refactor (CharacterEngine + QuestionEngine)
>
> **Path:** `C:\A_MY THINGS\001\Backend-Developer-Journey\Project\GuessWise`
>
> **LeetCode:** #448 Find All Numbers Disappeared in an Array ✅ (28ms · Beats 85.87%)
>
> **Status:** ✅ Day 40 Complete — Engine classes extracted, architecture fully modular

---

# 🎯 What Was Built Today

```
✅ CharacterEngine class — owns all character filtering logic
✅ QuestionEngine class — owns all question navigation logic
✅ Game refactored — now coordinates engines instead of doing their work
✅ select_category() now creates engine instances (not raw lists)
✅ play_game() now calls engine methods instead of inline code
✅ All game behavior preserved — zero functionality change, only architecture
✅ LeetCode #448 solved (Brute Force + HashSet + Index Marking O(1) space)
```

**Today was a REFACTORING day — the game plays identically to Day 39, but the code is now properly separated into single-responsibility classes.**

---

# 📁 Project State After Day 40

```
GuessWise/
│
├── main.py                          ← unchanged (3 lines)
├── game.py                          ← ✅ REFACTORED — now coordinates engines
│
├── models/
│   ├── __init__.py
│   ├── character.py                 ← unchanged
│   └── question.py                  ← unchanged
│
├── repository/
│   ├── __init__.py
│   ├── repository.py                ← unchanged
│   └── json_repository.py          ← unchanged
│
├── engines/
│   ├── __init__.py                  ← ✅ NEW (empty — marks as Python package)
│   ├── character_engine.py          ← ✅ NEW — filtering logic extracted here
│   └── question_engine.py          ← ✅ NEW — navigation logic extracted here
│
├── tools/
│   └── update_attributes.py
│
└── data/
    ├── characters.json
    └── questions.json
```

---

# SECTION 1 — WHY REFACTOR? THE PROBLEM WITH DAY 39

## Day 39 Game.play_game() — Too Many Responsibilities

In Day 39, `game.py` did everything:

```python
# DAY 39 — Game was doing ALL of this internally:

# ❌ Tracking question index (question_index = 0)
# ❌ Getting current question (self.current_questions[question_index])
# ❌ Checking if questions are exhausted (question_index >= len(...))
# ❌ Moving to next question (question_index += 1)
# ❌ Filtering characters (self.characters = [c for c in ...])
# ❌ Counting remaining (len(self.characters))
# ❌ Checking if guess ready (len(self.characters) == 1)
# ❌ Getting the guess (self.characters[0])
# ❌ Showing candidates (for c in self.characters: print("-", c.name))
```

**This violates the Single Responsibility Principle (SRP):**

```
A class should have ONLY ONE reason to change.

Game.py was changing for:
  → Bug in question navigation?     Edit game.py
  → Bug in filtering algorithm?     Edit game.py
  → Change how candidates display?  Edit game.py
  → Change guess logic?             Edit game.py

Every change touches the same 200-line file.
Risk of introducing new bugs increases with every edit.
Testing is harder because everything is tangled together.
```

## The Solution: Extract Engine Classes

```
BEFORE (Day 39):

     Game
      │
      ├── question_index = 0
      ├── question_index += 1
      ├── current_questions[question_index]
      ├── question_index >= len(questions)
      ├── self.characters = [filter list comprehension]
      ├── len(self.characters) == 1
      ├── self.characters[0]
      └── for c in self.characters: print(...)

AFTER (Day 40):

     Game
      │
      ├── CharacterEngine   ← owns everything about characters
      │    ├── .filter()
      │    ├── .count()
      │    ├── .has_guess()
      │    ├── .guess()
      │    └── .remaining()
      │
      └── QuestionEngine    ← owns everything about questions
           ├── .current_question()
           ├── .next_question()
           ├── .finished()
           ├── .reset()
           └── .question_number()

Game now says WHAT to do.
Engines decide HOW to do it.
```

---

# SECTION 2 — THE COMPLETE CODE

## main.py (Unchanged)

```python
from game import Game

game = Game()
game.start()
```

**Still 3 lines. main.py is the entry point, nothing more.**

---

## models/character.py (Unchanged)

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

## models/question.py (Unchanged)

```python
from dataclasses import dataclass


@dataclass
class Question:
    id: int
    category: str
    text: str
    attribute: str
```

---

## repository/repository.py (Unchanged)

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

## repository/json_repository.py (Unchanged)

```python
import json

from models.character import Character
from models.question import Question
from repository.repository import Repository


class JsonRepository(Repository):

    def get_characters(self) -> list[Character]:
        with open("data/characters.json", "r") as file:
            data = json.load(file)
            characters = []
            for item in data:
                character = Character(**item)
                characters.append(character)
            return characters

    def get_questions(self) -> list[Question]:
        with open("data/questions.json", "r") as file:
            data = json.load(file)

            questions = []
            for group in data:
                category = group["category"]

                for item in group["questions"]:
                    questions.append(
                        Question(
                            id=item["id"],
                            category=category,
                            text=item["text"],
                            attribute=item["attribute"]
                        )
                    )
            return questions
```

---

## engines/__init__.py (New — Empty)

```python
# Empty file.
# Marks the engines/ directory as a Python package.
# Required so Python allows: from engines.character_engine import CharacterEngine
```

**Why is an empty file important?**

```
Python needs __init__.py to recognise a folder as a package.
Without it: ImportError when trying to import from engines/
With it:    from engines.character_engine import CharacterEngine  ← works

Python 3.3+ introduced "namespace packages" (no __init__.py needed)
but explicit __init__.py is still the professional standard —
it makes the package boundary clear and allows package-level code later.
```

---

## engines/character_engine.py (NEW — Core Filtering Logic)

```python
"""
Character Engine

Responsible for:
- Storing candidates
- Filtering candidates
- Returning remaining candidates
"""

from models.character import Character


class CharacterEngine:
    """Handles all character filtering."""

    def __init__(self, characters: list[Character]):
        self.characters = characters

    def remaining(self) -> list[Character]:
        """Return all remaining candidates."""
        return self.characters

    def filter(self, attribute: str, expected_value: bool):
        """Filter candidates by attribute."""
        self.characters = [
            character
            for character in self.characters
            if character.attributes.get(attribute, False) == expected_value
        ]

    def count(self) -> int:
        """Return the number of remaining candidates."""
        return len(self.characters)

    def has_guess(self) -> bool:
        """Return True if exactly one candidate remains."""
        return len(self.characters) == 1

    def guess(self) -> Character:
        """Return the final guessed character."""
        return self.characters[0]
```

### Every Method Explained in Detail

**`__init__(self, characters: list[Character])`**

```python
def __init__(self, characters: list[Character]):
    self.characters = characters
```

```
Parameters:
  characters: list[Character]
  → The list of Character objects for this game session.
  → Passed in at creation time (from select_category()).
  → NOT loaded here — loading is the Repository's job.
  → CharacterEngine only RECEIVES data, never fetches it.

self.characters = characters
  → Stores the list as an instance attribute.
  → This is the WORKING list — it will be filtered down over time.
  → Starts as (e.g.) all 80 characters, ends as 1 (the guess).

Type hint: list[Character]
  → Documents what type is expected.
  → Pylance/mypy can catch bugs if wrong type is passed.
  → Acts as documentation for anyone reading the code.
```

**`remaining(self) -> list[Character]`**

```python
def remaining(self) -> list[Character]:
    """Return all remaining candidates."""
    return self.characters
```

```
Returns the current working list.
Used by Game to display remaining candidates after each filter.

Why a method instead of accessing self.characters directly?
  Encapsulation: Game doesn't need to know how candidates are stored.
  If we change the internal storage (e.g., dict instead of list),
  only this method changes. Game.play_game() stays the same.

Example usage in Game:
  for character in self.character_engine.remaining():
      print("-", character.name)
```

**`filter(self, attribute: str, expected_value: bool)`**

```python
def filter(self, attribute: str, expected_value: bool):
    """Filter candidates by attribute."""
    self.characters = [
        character
        for character in self.characters
        if character.attributes.get(attribute, False) == expected_value
    ]
```

```
This is the CORE ALGORITHM of the entire GuessWise game.

Parameters:
  attribute: str
    → The attribute name to check. E.g., "real", "male", "indian"
    → Comes from question.attribute (the bridge between Question and Character)

  expected_value: bool
    → True if user answered "Yes", False if user answered "No"

Algorithm (list comprehension):
  For each character in the CURRENT self.characters list:
    Look up character.attributes.get(attribute, False)
    → .get() safe access: returns False if key missing (no KeyError crash)
    Compare the result to expected_value
    → True == True   → character matches "Yes" answer → KEEP
    → False == True  → character doesn't match       → DROP
    → True == False  → character doesn't match       → DROP
    → False == False → character matches "No" answer → KEEP

Result: self.characters is replaced with the filtered list.

Example trace:
  Before: characters = [Virat Kohli, Naruto, MS Dhoni, Hermione]
  Call:   filter("real", True)  (user said character is real)

  Virat Kohli:  attributes.get("real") = True  → True == True  → KEEP
  Naruto:       attributes.get("real") = False → False == True → DROP
  MS Dhoni:     attributes.get("real") = True  → True == True  → KEEP
  Hermione:     attributes.get("real") = False → False == True → DROP

  After:  characters = [Virat Kohli, MS Dhoni]

Why .get(attribute, False) instead of [attribute]:
  character.attributes["real"]         → KeyError if "real" missing
  character.attributes.get("real", False) → returns False safely

  If a character was added to JSON without all attributes updated,
  .get() handles it gracefully. The game doesn't crash.
  Default False means: "assume this character doesn't have this attribute"
  which is the safe conservative assumption.
```

**`count(self) -> int`**

```python
def count(self) -> int:
    """Return the number of remaining candidates."""
    return len(self.characters)
```

```
Returns how many characters remain after filtering.
Used by Game to:
  1. Display "Remaining Candidates: X" header
  2. Check if count == 0 (no match found)

Before this refactor, Game had:
  len(self.characters)   ← directly accessing internal state

After refactor:
  self.character_engine.count()  ← asking the engine

The difference: Game no longer needs to know HOW candidates are stored.
It just asks "how many are left?" and trusts the engine's answer.
```

**`has_guess(self) -> bool`**

```python
def has_guess(self) -> bool:
    """Return True if exactly one candidate remains."""
    return len(self.characters) == 1
```

```
Returns True when exactly one character remains — the game can guess.

Why a named method instead of count() == 1 in Game?
  Readability:
    BEFORE: if len(self.characters) == 1:
    AFTER:  if self.character_engine.has_guess():

  The AFTER version reads like English: "if the engine has a guess..."
  The BEFORE version requires the reader to mentally parse the logic.

  This is called "intention-revealing naming" — 
  name the method after WHAT it means, not HOW it works.

  Tomorrow, if the guess logic changes (e.g., guess when 2 remain
  if confidence is high), only has_guess() changes.
  Game.play_game() stays the same.
```

**`guess(self) -> Character`**

```python
def guess(self) -> Character:
    """Return the final guessed character."""
    return self.characters[0]
```

```
Returns the single remaining character when has_guess() is True.

Usage in Game:
  if self.character_engine.has_guess():
      guess = self.character_engine.guess()
      print(f"It's: {guess.name}")

The return type annotation -> Character serves as:
  1. Documentation: this returns a Character object
  2. Type checking: Pylance warns if caller expects wrong type
  3. Auto-complete: guess.name, guess.category work in VS Code

Contract: always call has_guess() before calling guess().
If called when 0 or 2+ characters remain, IndexError on characters[0].
In production, we'd add a guard:
  if not self.characters:
      raise ValueError("No candidates remaining — cannot guess.")
But for Version 1, the caller (Game) is responsible for the contract.
```

---

## engines/question_engine.py (NEW — Navigation Logic)

```python
"""
Question Engine

Responsible for question navigation.

Responsibilities:
- Store questions.
- Return the current question.
- Move to the next question.
- Reset question order.

The Game class should never manage question indexes directly.
"""

from models.question import Question


class QuestionEngine:
    """Handles question navigation."""

    def __init__(self, questions: list[Question]):
        self.questions = questions
        self.current_index = 0

    def current_question(self) -> Question:
        """Return the current question."""
        return self.questions[self.current_index]

    def next_question(self):
        """Move to the next question."""
        self.current_index += 1

    def reset(self):
        """Reset to the first question."""
        self.current_index = 0

    def finished(self) -> bool:
        """Return True if there are no more questions."""
        return self.current_index >= len(self.questions)

    def question_number(self) -> int:
        """Return the current question number (1-based)."""
        return self.current_index + 1
```

### Every Method Explained in Detail

**`__init__(self, questions: list[Question])`**

```python
def __init__(self, questions: list[Question]):
    self.questions = questions
    self.current_index = 0
```

```
Parameters:
  questions: list[Question]
  → The filtered question list for the current category.
  → Passed from select_category() via Game.
  → QuestionEngine stores these and navigates through them.

self.questions = questions
  → Stores the full question list. Never modified.

self.current_index = 0
  → The pointer to the current question.
  → Starts at 0 (first question).
  → Incremented by next_question().
  → Reset by reset().
  → The engine OWNS this index. Game never touches it directly.

Before refactor, Game tracked this:
  question_index = 0           ← local variable in play_game()
  question_index += 1          ← updated inside the loop
  question_index >= len(...)   ← checked in the loop

After refactor, QuestionEngine owns it:
  self.current_index = 0       ← engine owns the state
  self.current_index += 1      ← only engine modifies it
  Game calls: engine.finished()  ← engine checks the condition

This is ENCAPSULATION: internal state hidden, accessed through methods.
```

**`current_question(self) -> Question`**

```python
def current_question(self) -> Question:
    """Return the current question."""
    return self.questions[self.current_index]
```

```
Returns the Question object at the current position.

Before refactor in Game:
  question = self.current_questions[question_index]

After refactor in Game:
  question = self.question_engine.current_question()

The second version:
  → Game doesn't need to know about question_index
  → Game doesn't need to know that questions are stored in a list
  → Game just asks "give me the current question"

The engine knows HOW. Game knows WHAT it needs.
```

**`next_question(self)`**

```python
def next_question(self):
    """Move to the next question."""
    self.current_index += 1
```

```
Advances the internal pointer by 1.
Called by Game at the END of each loop iteration.

Before refactor:
  question_index += 1   ← Game tracked this itself

After refactor:
  self.question_engine.next_question()   ← Engine handles it

In the future:
  If we want to skip questions, or ask questions in a smarter order,
  only next_question() changes. Game doesn't need to know.
```

**`reset(self)`**

```python
def reset(self):
    """Reset to the first question."""
    self.current_index = 0
```

```
Resets the pointer back to question 0.
Used when play_again() returns True — start fresh.

In Day 39, "Play Again" worked by calling select_category() again,
which created a NEW QuestionEngine (resetting automatically).
reset() provides an alternative if we want to keep the same engine
but restart from the first question.

Both approaches are valid. select_category() creates a new instance,
reset() reuses the existing one. Day 40 uses select_category().
```

**`finished(self) -> bool`**

```python
def finished(self) -> bool:
    """Return True if there are no more questions."""
    return self.current_index >= len(self.questions)
```

```
Returns True when all questions have been asked.

Before refactor in Game:
  if question_index >= len(self.current_questions):
      print("🤔 I couldn't uniquely identify...")

After refactor in Game:
  if self.question_engine.finished():
      print("🤔 I couldn't uniquely identify...")

Reads like English: "if the question engine is finished..."
The BEFORE version required knowing about question_index and len().
The AFTER version hides that implementation detail.

Edge case: what if questions list is empty?
  current_index = 0, len(questions) = 0
  0 >= 0 → True → finished() immediately
  Game shows "couldn't identify" right away. Correct behavior.
```

**`question_number(self) -> int`**

```python
def question_number(self) -> int:
    """Return the current question number (1-based)."""
    return self.current_index + 1
```

```
Returns human-readable question number (1-based, not 0-based).

Why +1?
  Arrays are 0-indexed: first question is at index 0.
  Humans count from 1: "Question 1", "Question 2", not "Question 0".

Before refactor in Game:
  print(f"Question {question_index + 1}")

After refactor in Game:
  print(f"Question {self.question_engine.question_number()}")

The engine does the +1. Game never sees the raw index.
```

---

## game.py (REFACTORED — the main change of Day 40)

```python
from repository.json_repository import JsonRepository
from engines.character_engine import CharacterEngine
from engines.question_engine import QuestionEngine


class Game:
    def __init__(self):
        self.repository = JsonRepository()

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
            print("        🎯 GuessWise               ")
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
            # ── CASE 1: ALL QUESTIONS USED ──────────────────────────
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

            # ── DISPLAY CURRENT QUESTION ────────────────────────────
            print("\n=========================")
            print("🎯 GuessWise")
            print("=========================")
            print(f"Category : {self.current_category.title()}")
            print(f"Remaining Candidates : {self.character_engine.count()}")

            print(f"Question {self.question_engine.question_number()}")
            question = self.question_engine.current_question()
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

            # ── PROCESS ANSWER ───────────────────────────────────────
            if choice == "1":
                self.character_engine.filter(
                    question.attribute,
                    True
                )

            elif choice == "2":
                self.character_engine.filter(
                    question.attribute,
                    False
                )

            elif choice in ["3", "4", "5"]:
                print(f"You selected: {answers[choice]}")
            else:
                print("Invalid choice! Please enter a number from 1 to 5.")

            # ── SHOW REMAINING CANDIDATES ────────────────────────────
            print("\nRemaining Candidates:")
            for character in self.character_engine.remaining():
                print("-", character.name)

            # ── CASE 2: EXACTLY ONE REMAINS ─────────────────────────
            if self.character_engine.has_guess():
                print("\n🎉 I guessed your answer!")
                guess = self.character_engine.guess()
                print(f"It's: {guess.name}")

                if self.play_again():
                    self.select_category(self.current_category)
                    return self.play_game()
                return

            # ── CASE 3: ZERO REMAIN ──────────────────────────────────
            elif self.character_engine.count() == 0:
                print("\n❌ No matching character found.")

                if self.play_again():
                    self.select_category(self.current_category)
                    return self.play_game()
                return

            # ── ADVANCE TO NEXT QUESTION ─────────────────────────────
            self.question_engine.next_question()

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

---

# SECTION 3 — BEFORE vs AFTER: THE REFACTOR IN DETAIL

## select_category() — Before vs After

**Day 39 (stored raw lists):**

```python
def select_category(self, category: str):
    self.current_category = category

    self.characters = [                  # ← raw list stored on self
        character
        for character in self.all_characters
        if character.category == category
    ]

    self.current_questions = [           # ← raw list stored on self
        question
        for question in self.questions
        if question.category == category
    ]
```

**Day 40 (creates engine instances):**

```python
def select_category(self, category: str):
    self.current_category = category

    characters = [
        character
        for character in self.all_characters
        if character.category == category
    ]
    self.character_engine = CharacterEngine(characters)   # ← engine object

    questions = [
        question
        for question in self.questions
        if question.category == category
    ]
    self.question_engine = QuestionEngine(questions)      # ← engine object
```

**What changed and why:**

```
Day 39:
  self.characters = [...]             ← raw list, Game manages it
  self.current_questions = [...]      ← raw list, Game manages it

  Consequence: Game needs methods like:
    filter_characters()
    show_remaining_candidates()
  Game grows with every new feature.

Day 40:
  self.character_engine = CharacterEngine([...])   ← engine manages the list
  self.question_engine = QuestionEngine([...])     ← engine manages navigation

  Consequence: Game just holds TWO objects.
  Every operation delegates to an engine.
  Game stays small and focused.

This is COMPOSITION:
  "Prefer composition over inheritance"
  Instead of Game inheriting from some BaseGame with filtering methods,
  Game CONTAINS engine objects that handle their specific domains.
```

## play_game() — Before vs After Comparison

```python
# DAY 39 play_game() — Game doing everything itself
def play_game(self):
    question_index = 0                      # Game tracks index itself
    while True:
        if question_index >= len(self.current_questions):  # Game checks
            ...
        print(f"Question {question_index + 1}")            # Game formats
        question = self.current_questions[question_index]  # Game accesses

        if choice == "1":
            self.filter_characters(question.attribute, True)   # Game method

        for character in self.characters:   # Game accesses characters directly
            print("-", character.name)

        if len(self.characters) == 1:       # Game checks count
            guess = self.characters[0]      # Game gets guess

        question_index += 1                 # Game increments index


# DAY 40 play_game() — Game coordinates, engines execute
def play_game(self):
    while True:
        if self.question_engine.finished():     # Engine tells Game
            ...
        print(f"Question {self.question_engine.question_number()}")  # Engine formats
        question = self.question_engine.current_question()           # Engine returns

        if choice == "1":
            self.character_engine.filter(question.attribute, True)   # Engine does

        for character in self.character_engine.remaining():   # Engine returns list
            print("-", character.name)

        if self.character_engine.has_guess():          # Engine knows
            guess = self.character_engine.guess()      # Engine returns

        self.question_engine.next_question()   # Engine advances
```

**The transformation:**

```
Day 39: Game KNOWS how questions are stored (list + index)
Day 40: Game ASKS the engine what to do next

Day 39: Game KNOWS how filtering works (list comprehension)
Day 40: Game ASKS the engine to filter

Day 39: Game calculates "Question N" by adding 1 to index
Day 40: Game asks engine for question_number()

This is the difference between:
  "Doing it yourself"        (Day 39)
  "Delegating to an expert"  (Day 40)
```

---

# SECTION 4 — DESIGN PRINCIPLES APPLIED

## Single Responsibility Principle (SRP)

```
CharacterEngine:
  One responsibility: manage the character candidate list.
  Changes when: filtering algorithm changes, guess logic changes.
  Does NOT change when: question navigation changes, menu changes.

QuestionEngine:
  One responsibility: navigate through the question list.
  Changes when: question ordering changes, skip logic added.
  Does NOT change when: filtering changes, display changes.

Game:
  One responsibility: coordinate the application flow.
  Changes when: menu structure changes, user flow changes.
  Does NOT change when: filtering algorithm changes, question ordering changes.

Repository:
  One responsibility: load data from storage.
  Changes when: storage format changes (JSON → PostgreSQL).
  Does NOT change when: game logic changes, filtering changes.
```

## Encapsulation

```
CharacterEngine encapsulates:
  → The list of characters (self.characters)
  → The filtering algorithm
  → The guess detection logic

External code never:
  → Access engine.characters directly (use engine.remaining())
  → Count with len(engine.characters) (use engine.count())
  → Check engine.characters[0] (use engine.guess())

Why this matters:
  If we change storage from list to dict:
    Before: every caller that wrote len(self.characters) breaks
    After:  only count() inside CharacterEngine changes

  Encapsulation = protection against the cost of change.
```

## Composition vs Inheritance

```
Game does NOT inherit from CharacterEngine or QuestionEngine.
Game CONTAINS CharacterEngine and QuestionEngine.

class Game:
    def __init__(self):
        ...
        # self.character_engine is set in select_category()
        # self.question_engine  is set in select_category()

This is composition:
  Game HAS A character engine.
  Game HAS A question engine.

As opposed to inheritance:
  Game IS A character engine. (wrong — Game is not a filtering engine)

"Favour composition over inheritance" — Gang of Four (Design Patterns)
Composition is more flexible and easier to swap out.
```

## Separation of Concerns

```
Each concern belongs to exactly one class:

CONCERN                → CLASS
─────────────────────────────────────────
Load JSON data         → JsonRepository
Define character shape → Character model
Define question shape  → Question model
Filter candidates      → CharacterEngine
Navigate questions     → QuestionEngine
Coordinate flow        → Game
Start the program      → main.py

No class does two concerns.
No concern lives in two classes.
```

---

# SECTION 5 — ARCHITECTURE DIAGRAM

```
main.py
    │
    ▼
Game
 │
 ├── __init__()
 │    └── self.repository = JsonRepository()
 │
 ├── start()
 │    ├── self.all_characters = repository.get_characters()
 │    ├── self.questions = repository.get_questions()
 │    └── show_menu()
 │
 ├── show_menu()
 │    └── select_category(category) → play_game()
 │
 ├── select_category(category)
 │    ├── filter all_characters → CharacterEngine(filtered_list)
 │    └── filter questions → QuestionEngine(filtered_list)
 │
 ├── play_game()
 │    ├── question_engine.finished()?     → exit
 │    ├── question_engine.question_number() → display
 │    ├── question_engine.current_question() → ask
 │    ├── character_engine.filter(attr, bool) → update
 │    ├── character_engine.remaining()    → display
 │    ├── character_engine.has_guess()?   → guess + exit
 │    ├── character_engine.count() == 0?  → no match + exit
 │    └── question_engine.next_question() → advance
 │
 └── play_again() → bool
      └── True: select_category(current_category) → play_game()


CharacterEngine
 ├── __init__(characters: list[Character])
 ├── remaining() → list[Character]
 ├── filter(attribute: str, expected_value: bool)
 ├── count() → int
 ├── has_guess() → bool
 └── guess() → Character


QuestionEngine
 ├── __init__(questions: list[Question])
 ├── current_question() → Question
 ├── next_question()
 ├── reset()
 ├── finished() → bool
 └── question_number() → int


JsonRepository
 ├── get_characters() → list[Character]
 └── get_questions() → list[Question]
      ├── reads data/characters.json
      └── reads data/questions.json
           → Character(**item)   [dict unpacking]
           → Question(id, category, text, attribute)
```

---

# SECTION 6 — WHAT CHANGES AND WHAT STAYS WHEN ADDING FEATURES

## "I want to change the filtering algorithm"

```
Day 39: Edit game.py → filter_characters() method
Day 40: Edit character_engine.py → filter() method

Result: Game.py stays unchanged. Test CharacterEngine in isolation.
```

## "I want to ask questions in a smarter order"

```
Day 40: Edit question_engine.py → next_question() method
  Currently: self.current_index += 1  (sequential)
  Future:    find question that splits remaining chars most evenly
             (information gain / decision tree approach)

Result: Game.py stays unchanged. CharacterEngine stays unchanged.
```

## "I want to switch from JSON to PostgreSQL"

```
Day 40: Create postgres_repository.py → implement get_characters() and get_questions()
Change one line in game.py:
  Before: self.repository = JsonRepository()
  After:  self.repository = PostgresRepository()

Result: All engine files unchanged. All model files unchanged.
        Only one line in game.py changes.
```

## "I want to add a FastAPI endpoint"

```
Future: Create routes/game_routes.py
  @app.post("/start-game")
  def start_game():
      engine = CharacterEngine(repository.get_characters())
      ...
      return engine.remaining()

Result: CharacterEngine and QuestionEngine work exactly the same
        in both CLI and API contexts. Code reuse.
```

---

# SECTION 7 — COMPLETE GAME SESSION (With Engine Methods)

```
$ python main.py

Game Started
Loaded 80 characters
Loaded 150 questions

===================================
        🎯 GuessWise
===================================
1. Character
2. Animal
3. Object
4. Exit
Enter your choice (1-4): 1
[select_category("character") called]
[CharacterEngine created with 80 characters]
[QuestionEngine created with 50 questions]

=========================
🎯 GuessWise
=========================
Category : Character
Remaining Candidates : 80          ← character_engine.count()
Question 1                          ← question_engine.question_number()
Is your character a real person?    ← question_engine.current_question().text
1. Yes
2. No
3. Probably
4. Probably Not
5. Don't Know
Enter your choice (1-5): 1
[character_engine.filter("real", True)]

Remaining Candidates:
- Virat Kohli                       ← character_engine.remaining()
- MS Dhoni
- Elon Musk
- Bill Gates
...
[question_engine.next_question()]

=========================
Category : Character
Remaining Candidates : 45
Question 2
Is your character male?
...
Enter your choice (1-5): 1
[character_engine.filter("male", True)]
...

[Several questions later]

Remaining Candidates:
- Virat Kohli
[character_engine.has_guess() → True]

🎉 I guessed your answer!
It's: Virat Kohli                   ← character_engine.guess().name

-----------------------
Play Again?
-----------------------
1. Yes
2. No
Enter your choice: 2

[Returns to show_menu()]
```

---

# SECTION 8 — LEETCODE #448: FIND ALL NUMBERS DISAPPEARED IN AN ARRAY

## Problem

Given array `nums` of size `n` where `1 <= nums[i] <= n`, return all integers in `[1, n]` that don't appear in `nums`.

```
nums = [4,3,2,7,8,2,3,1]   n = 8
Expected: 1,2,3,4,5,6,7,8
Present:  1,2,3,4,7,8  (5 and 6 missing)
Output: [5, 6]
```

## Approach 1 — Brute Force O(n²)

```python
class Solution(object):
    def findDisappearedNumbers(self, nums):
        answer = []
        for number in range(1, len(nums) + 1):
            if number not in nums:      # list search = O(n) each time
                answer.append(number)
        return answer
```

**Why O(n²):** `number not in nums` is O(n) for a list. Called n times → O(n²).

## Approach 2 — HashSet O(n) time, O(n) space ✅ Submitted

```python
class Solution(object):
    def findDisappearedNumbers(self, nums):
        seen = set(nums)               # O(n) build, O(1) lookup
        answer = []
        for number in range(1, len(nums) + 1):
            if number not in seen:     # O(1) per check
                answer.append(number)
        return answer
```

**Submitted:** ✅ Accepted | 35/35 test cases | Runtime: 28ms | Beats 85.87%

## Approach 3 — Index Marking O(n) time, O(1) space (Optimal)

```python
class Solution(object):
    def findDisappearedNumbers(self, nums):
        answer = []

        # First Pass: mark visited numbers using the array itself
        for i in range(len(nums)):
            index = abs(nums[i]) - 1       # value → index (0-based)
            if nums[index] > 0:            # only negate if positive
                nums[index] = -nums[index] # negative = "this number exists"

        # Second Pass: positive value = its number is missing
        for i in range(len(nums)):
            if nums[i] > 0:
                answer.append(i + 1)       # index → missing number

        return answer
```

**Complete dry run on `[4,3,2,7,8,2,3,1]`:**

```
FIRST PASS (marking):

i=0: nums[0]=4  → index=abs(4)-1=3  → nums[3]=7>0  → nums[3]=-7
     Array: [4,3,2,-7,8,2,3,1]

i=1: nums[1]=3  → index=abs(3)-1=2  → nums[2]=2>0  → nums[2]=-2
     Array: [4,3,-2,-7,8,2,3,1]

i=2: nums[2]=-2 → index=abs(-2)-1=1 → nums[1]=3>0  → nums[1]=-3
     Array: [4,-3,-2,-7,8,2,3,1]

i=3: nums[3]=-7 → index=abs(-7)-1=6 → nums[6]=3>0  → nums[6]=-3
     Array: [4,-3,-2,-7,8,2,-3,1]

i=4: nums[4]=8  → index=abs(8)-1=7  → nums[7]=1>0  → nums[7]=-1
     Array: [4,-3,-2,-7,8,2,-3,-1]

i=5: nums[5]=2  → index=abs(2)-1=1  → nums[1]=-3<0 → skip (already marked)
     Array: [4,-3,-2,-7,8,2,-3,-1]

i=6: nums[6]=-3 → index=abs(-3)-1=2 → nums[2]=-2<0 → skip (already marked)
     Array: [4,-3,-2,-7,8,2,-3,-1]

i=7: nums[7]=-1 → index=abs(-1)-1=0 → nums[0]=4>0  → nums[0]=-4
     Array: [-4,-3,-2,-7,8,2,-3,-1]

SECOND PASS (find positives):

i=0: nums[0]=-4 → negative → skip
i=1: nums[1]=-3 → negative → skip
i=2: nums[2]=-2 → negative → skip
i=3: nums[3]=-7 → negative → skip
i=4: nums[4]=8  → POSITIVE → missing number = 4+1 = 5  ← answer
i=5: nums[5]=2  → POSITIVE → missing number = 5+1 = 6  ← answer
i=6: nums[6]=-3 → negative → skip
i=7: nums[7]=-1 → negative → skip

Return: [5, 6] ✅
```

**Why `abs()` is critical:**

```
After first few iterations, array contains negative values:
  nums = [4,-3,-2,-7,8,2,-3,-1]

Now we read nums[2] = -2.
We want to use this to find an index.

WITHOUT abs():
  index = nums[2] - 1 = -2 - 1 = -3
  Python allows negative indexing: nums[-3] = nums[len-3]
  → WRONG INDEX. Bug.

WITH abs():
  index = abs(nums[2]) - 1 = abs(-2) - 1 = 2 - 1 = 1
  → CORRECT INDEX. Works.
```

**Why check `if nums[index] > 0` before negating:**

```
nums = [2, 2, ...]   (duplicate 2)

First 2: mark index 1 → nums[1] = -2
Second 2: mark index 1 again → nums[1] = -(-2) = 2 (UNMARKED!)

The mark disappears! 2 would be reported as missing. Bug.

Fix: only negate if value is STILL POSITIVE:
  if nums[index] > 0:
      nums[index] = -nums[index]   ← mark once, stay marked

Second time we see duplicate:
  nums[index] = -2 (already negative) → 0 > 0 is False → skip
  Mark preserved. Correct.
```

**The key insight (interview pattern):**

```
When problem says: 1 <= nums[i] <= n

Ask yourself: "Can each VALUE act as an INDEX?"

If yes: you can use the array itself as a visited set.
  → No extra HashSet needed
  → O(1) space (excluding output)
  → Same O(n) time as HashSet approach

This "index marking" pattern also appears in:
  LeetCode #442 — Find All Duplicates in an Array
  LeetCode #41  — First Missing Positive (advanced)
```

## Complexity Comparison

```
Approach             │ Time     │ Space  │ Notes
─────────────────────┼──────────┼────────┼────────────────────────
Brute Force          │ O(n²)    │ O(1)   │ list search = slow
HashSet              │ O(n)     │ O(n)   │ extra set = extra memory
Index Marking        │ O(n)     │ O(1)   │ optimal — uses array itself
```

---

# ✅ Day 40 Task Summary

| Task | Status |
|------|--------|
| Create engines/__init__.py | ✅ Done |
| Create CharacterEngine with all methods | ✅ Done |
| Create QuestionEngine with all methods | ✅ Done |
| Refactor game.py to use engines | ✅ Done |
| Refactor select_category() to create engines | ✅ Done |
| Refactor play_game() to call engine methods | ✅ Done |
| Verify game behavior unchanged | ✅ Done |
| LeetCode #448 Brute Force | ✅ Done |
| LeetCode #448 HashSet | ✅ Accepted (28ms) |
| LeetCode #448 Index Marking O(1) space | ✅ Done |

---

# 📅 What's Coming: Days 41–42

```
Day 41: Admin CRUD
  → CLI tool to add new characters
  → CLI tool to delete characters by name
  → CLI tool to update character attributes
  → Works through the Repository layer (same pattern)

Day 42: GitHub Release
  → Rename GuessWise.md → README.md
  → Create proper .gitignore
  → Push GuessWise as standalone GitHub repository
  → Tag v1.0
  → LinkedIn announcement post
```

---

*Day 40 Complete. Engine classes extracted. Architecture fully modular. GuessWise is ready for PostgreSQL migration and future FastAPI integration.* ✅