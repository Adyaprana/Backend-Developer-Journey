# DAY 42 — GuessWise CLI v1.0: Knowledge Manager, Decision Engine & Final Release

> **Project:** GuessWise — Akinator-inspired CLI Game (Version 1.0 Complete)
>
> **Path:** `C:\A_MY THINGS\001\Backend-Developer-Journey\Project\GuessWise`
>
> **LeetCode:** #1480 Running Sum of 1d Array ✅ (0ms · Beats 100%)
>
> **Status:** ✅ Day 42 Complete — GuessWise CLI v1.0 officially released

---

# 🎯 What Was Built Today

```
✅ engines/knowledge_manager.py  — The Brain: dynamic question selection
✅ engines/question_engine.py    — Refactored: storage only, no index logic
✅ game.py                       — Refactored: delegates everything to KnowledgeManager
✅ GuessWise CLI v1.0 released   — Final architecture complete
✅ LeetCode #1480 solved         — Running Sum, Prefix Sum pattern
```

**Day 42 was the most important architectural day of the entire project.** GuessWise went from a game that asked questions in a fixed order to one that actively chooses the best next question — the first step toward building a real Akinator-style decision engine.

---

# 📁 Final Project State — GuessWise v1.0

```
GuessWise/
│
├── main.py                          ← Entry point (3 lines, unchanged)
├── game.py                          ← ✅ REFACTORED — delegates to KnowledgeManager
│
├── models/
│   ├── character.py                 ← @dataclass (unchanged)
│   └── question.py                  ← @dataclass (unchanged)
│
├── repository/
│   ├── repository.py                ← ABC interface (unchanged)
│   ├── json_repository.py          ← Version 1 (kept for reference)
│   └── postgres_repository.py      ← Active repository
│
├── engines/
│   ├── character_engine.py          ← Filtering (unchanged)
│   ├── question_engine.py          ← ✅ REFACTORED — storage only
│   └── knowledge_manager.py        ← ✅ NEW — the brain
│
├── database/
│   ├── database.py
│   ├── models.py
│   ├── seed.py
│   └── run_seed.py
│
└── data/
    ├── characters.json
    └── questions.json
```

---

# SECTION 1 — THE PROBLEM WITH DAY 41

## What Was Wrong Before Today

At the start of Day 42, GuessWise had this architecture:

```
Game
 │
 ├── CharacterEngine
 ├── QuestionEngine
 └── PostgresRepository
```

It worked — but it had four serious problems.

---

**Problem 1: Game was doing too much**

```python
# In Day 41 game.py:
question = self.question_engine.current_question()   # Game decided the question
...
if choice == "1":
    self.character_engine.filter(question.attribute, True)   # Game filtered
elif choice == "2":
    self.character_engine.filter(question.attribute, False)  # Game filtered
self.question_engine.next_question()    # Game advanced the index
```

Game was doing:
- Deciding which question to show
- Processing the user's answer
- Filtering characters
- Managing question navigation

That is four responsibilities in one class. Single Responsibility Principle violated.

---

**Problem 2: Questions asked in fixed sequential order**

```
Question 1 → Question 2 → Question 3 → ... → Question 50
```

Every game session asked the SAME questions in the SAME order. No matter what answers the user gave, the next question never changed. This is NOT how Akinator works.

---

**Problem 3: No intelligence — questions not selected based on candidates**

A question like "Is your character male?" is useless when all remaining candidates are male. Asking it eliminates nobody. The game wasted questions.

---

**Problem 4: Data Duplication Bug**

In the first KnowledgeManager attempt:

```python
KnowledgeManager(characters, questions)  # Passed RAW data
self.characters = characters             # Own copy
```

CharacterEngine filters → candidates reduce from 80 to 30.
But KnowledgeManager still had 80 characters (its own copy).
It kept selecting questions based on stale data.

This is called **Data Inconsistency** — two classes holding the same data that gets out of sync.

---

## The Solutions Applied Today

```
Problem 1: Game doing too much
  → Extract KnowledgeManager to own question selection and answer processing

Problem 2: Fixed question order
  → KnowledgeManager picks the BEST question from remaining questions, not next in sequence

Problem 3: No intelligence
  → Score algorithm: choose question that splits remaining candidates most evenly

Problem 4: Data duplication
  → KnowledgeManager receives CharacterEngine + QuestionEngine (not raw data)
    It always reads from engines (single source of truth)
```

---

# SECTION 2 — THE COMPLETE CODE

## main.py (Unchanged)

```python
from game import Game

game = Game()
game.start()
```

Still 3 lines. Still the entry point and nothing more.

---

## engines/question_engine.py — REFACTORED

**Day 41 version (index-based):**

```python
class QuestionEngine:
    def __init__(self, questions):
        self.questions = questions
        self.current_index = 0          # ← tracked sequence

    def current_question(self):
        return self.questions[self.current_index]

    def next_question(self):
        self.current_index += 1         # ← sequential only

    def finished(self):
        return self.current_index >= len(self.questions)

    def question_number(self):
        return self.current_index + 1
```

**Day 42 version (storage-based):**

```python
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

**Every design decision explained:**

```
questions.copy() in __init__:
  Creates a shallow copy of the list.
  Changes to self.questions don't affect the original.
  Without .copy(): deleting from self.questions would also delete
  from the list passed by the caller. Bug.

remaining() → list[Question]:
  Returns the current pool of unasked questions.
  KnowledgeManager calls this to get candidates for scoring.

remove(question):
  Removes a specific question object (not by index, by object identity).
  Called by KnowledgeManager AFTER selecting best_question().
  Guards with "if question in self.questions" to prevent KeyError.

finished() → bool:
  Returns True when no questions remain.
  Game calls this to detect the "couldn't guess" exit condition.

count() → int:
  Returns number of remaining questions.
  Used to display "Question X/50" counter.

reset(questions):
  Rebuilds the list for play_again() flow.
  Takes a fresh list and copies it.
```

**Why NO `current_index` or `current_question()` or `next_question()`:**

```
Old design: QuestionEngine decided ORDER (sequential).
New design: QuestionEngine stores what's LEFT.
           KnowledgeManager decides which ONE to pick.

Responsibility is now split correctly:
  QuestionEngine = storage
  KnowledgeManager = selection strategy
```

---

## engines/character_engine.py (Unchanged)

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

CharacterEngine was already designed correctly. No changes needed.

**This is a sign of good architecture** — when a new feature is added, the correctly designed parts don't change.

---

## engines/knowledge_manager.py — THE BRAIN (NEW)

```python
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

---

### `__init__` — Dependency Injection

```python
def __init__(
    self,
    character_engine: CharacterEngine,
    question_engine: QuestionEngine
):
    self.character_engine = character_engine
    self.question_engine = question_engine
```

**What Dependency Injection means:**

```
KnowledgeManager does NOT create CharacterEngine or QuestionEngine.
It RECEIVES them from outside (Game creates them, passes them in).

This is Dependency Injection:
  "Don't create your dependencies. Receive them."

Benefits:
  1. Single Source of Truth
     When CharacterEngine filters characters, KnowledgeManager
     automatically sees the updated list (same object in memory).
     No stale data. No duplication.

  2. Testability
     In tests, you can pass a MockCharacterEngine with fake data.
     KnowledgeManager works the same way.

  3. Flexibility
     Tomorrow: pass a different engine with AI-based scoring.
     KnowledgeManager.best_question() doesn't change at all.
```

**The bug this fixes:**

```python
# BAD (Day 41 first attempt):
KnowledgeManager(characters, questions)
# KnowledgeManager owns a COPY of characters.
# CharacterEngine filters → reduces candidates.
# KnowledgeManager still has the original 80. OUT OF SYNC.

# GOOD (Day 42):
KnowledgeManager(character_engine, question_engine)
# KnowledgeManager holds REFERENCES to the engines.
# CharacterEngine filters → candidates reduce.
# KnowledgeManager calls character_engine.remaining() → gets UPDATED list.
# ALWAYS in sync. Single source of truth.
```

---

### `best_question()` — The Decision Algorithm

This is the most important method in the entire project.

```python
def best_question(self) -> Question:
    """Choose the best remaining question."""

    characters = self.character_engine.remaining()  # LIVE data, always current
    questions = self.question_engine.remaining()    # Unasked questions pool

    best_question = None
    best_score = float("inf")   # Start with the worst possible score

    for question in questions:           # Check every remaining question

        true_count = 0
        false_count = 0

        for character in characters:     # Check every remaining candidate
            value = character.attributes.get(
                question.attribute,      # The attribute this question targets
                False                   # Default if attribute missing
            )

            if value:
                true_count += 1         # This character would answer Yes
            else:
                false_count += 1        # This character would answer No

        # SKIP useless questions:
        if true_count == 0 or false_count == 0:
            continue
        # true_count == 0: everyone answers No → question eliminates nobody if answered No
        # false_count == 0: everyone answers Yes → question eliminates nobody if answered Yes
        # Either way: question can only eliminate ALL candidates on one answer
        # and NONE on the other. Not useful for narrowing.

        # SCORE: closer to 0 = better split
        score = abs(true_count - false_count)

        if score < best_score:
            best_score = score
            best_question = question

    # Remove the selected question from the pool
    # (so it's never asked again)
    if best_question:
        self.question_engine.remove(best_question)

    return best_question
```

**The algorithm explained with a concrete example:**

```
Remaining candidates: 20 characters

Question A: "Is your character real?"
  Characters where real=True:  12
  Characters where real=False:  8
  score = abs(12 - 8) = 4

Question B: "Is your character male?"
  Characters where male=True:  19
  Characters where male=False:  1
  score = abs(19 - 1) = 18

Question C: "Is your character Indian?"
  Characters where indian=True:  10
  Characters where indian=False: 10
  score = abs(10 - 10) = 0   ← PERFECT

  If user says Yes → 10 candidates remain
  If user says No  → 10 candidates remain
  Either way: half eliminated.

Question D: "Is your character a footballer?"
  Characters where footballer=True:  0
  Characters where footballer=False: 20
  → SKIP (true_count == 0, useless question right now)

WINNER: Question C (score = 0)
Game asks: "Is your character Indian?"
```

**Why `float("inf")` as initial best_score:**

```python
best_score = float("inf")

# Any real score will be less than infinity.
# So the first valid question always becomes best_question.

# Alternative: best_score = len(characters) + 1
# Also works, but float("inf") is more semantically clear.
# It says: "I haven't found a good score yet. Any real score beats this."
```

**Why `.get(attribute, False)` not `[attribute]`:**

```python
value = character.attributes.get(question.attribute, False)

# character.attributes["real"]           → KeyError if "real" missing!
# character.attributes.get("real", False) → returns False safely

# When would an attribute be missing?
# If a new question was added to questions.json
# but update_attributes.py wasn't re-run.
# .get() makes best_question() robust against data quality issues.
```

**Why remove the question AFTER selecting it:**

```python
if best_question:
    self.question_engine.remove(best_question)
return best_question
```

```
If we removed BEFORE returning:
  best_question = question
  self.question_engine.remove(best_question)
  return best_question
  → Works, but remove() happens before we know if we'll use it.

If we forgot to remove:
  The game keeps asking the SAME question every turn!
  KnowledgeManager finds the same "best" question again next time.
  Infinite loop of the same question. Bug.

Correct: select → remove → return.
```

---

### `process_answer()` — Delegated Filtering

```python
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
        pass   # "Probably", "Probably Not", "Don't Know" — no filtering
```

**Before Day 42 (Game did this directly):**

```python
# In game.py Day 41:
if choice == "1":
    self.character_engine.filter(question.attribute, True)
elif choice == "2":
    self.character_engine.filter(question.attribute, False)
```

**After Day 42 (Game delegates to KnowledgeManager):**

```python
# In game.py Day 42:
if choice in ["1", "2"]:
    self.knowledge_manager.process_answer(question, choice)
```

**Why this matters:**

```
Before: Game knows about attributes, filtering logic, and answer mapping.
        Game is doing business logic.

After:  Game forwards the choice. KnowledgeManager decides what to do.
        Game only controls the flow.

This is Encapsulation:
  KnowledgeManager hides HOW filtering works.
  Game only knows WHAT happened ("user answered").
  Game doesn't need to know what True or False means for filtering.
```

---

## game.py — REFACTORED

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
            # ── EXIT 1: All questions exhausted ────────────────────────
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

            # ── DISPLAY ─────────────────────────────────────────────────
            print("\n=========================")
            print("🎯 GuessWise:", self.current_category.title())
            print("=========================")
            print(f"Category : {self.current_category.title()}")
            print(f"Remaining Candidates : {self.character_engine.count()}")

            asked = 50 - self.question_engine.count() + 1
            print(f"Question {asked}")

            # ── GET BEST QUESTION ────────────────────────────────────────
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

            # ── PROCESS ANSWER ───────────────────────────────────────────
            if choice in ["1", "2"]:
                self.knowledge_manager.process_answer(question, choice)

            elif choice in ["3", "4", "5"]:
                print(f"You selected: {answers[choice]}")

            else:
                print("Invalid choice! Please enter a number from 1 to 5.")
                continue

            # ── SHOW REMAINING ───────────────────────────────────────────
            print("\nRemaining Candidates:")
            for character in self.character_engine.remaining():
                print("-", character.name)

            # ── EXIT 2: Exactly one remains ──────────────────────────────
            if self.character_engine.has_guess():
                print("\n🎉 I guessed your answer!")
                guess = self.character_engine.guess()
                print(f"It's: {guess.name}")

                if self.play_again():
                    self.select_category(self.current_category)
                    return self.play_game()
                return

            # ── EXIT 3: Zero remain ──────────────────────────────────────
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

        # Create KnowledgeManager with REFERENCES to the engines
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

---

### The Key Change in select_category()

**Day 41:**

```python
def select_category(self, category: str):
    self.current_category = category
    self.character_engine = CharacterEngine(characters)
    self.question_engine = QuestionEngine(questions)
    # No KnowledgeManager — Game handled logic directly
```

**Day 42:**

```python
def select_category(self, category: str):
    self.current_category = category
    self.character_engine = CharacterEngine(characters)
    self.question_engine = QuestionEngine(questions)

    # KnowledgeManager receives REFERENCES (not copies)
    self.knowledge_manager = KnowledgeManager(
        self.character_engine,
        self.question_engine
    )
```

**Why create KnowledgeManager in select_category() and not __init__:**

```
__init__ runs once. select_category() runs every time a category is selected.

Each category needs fresh engines with fresh data.
KnowledgeManager must receive the NEW engines for the new category.

If created in __init__: it would hold references to old engines.
If created in select_category(): it always holds fresh, category-specific engines.
```

### The "Question N" Counter

```python
asked = 50 - self.question_engine.count() + 1
print(f"Question {asked}")
```

**Why this formula:**

```
Questions start at 50 for each category.
count() decreases as questions are removed.

Before any question is asked: count() = 50
  asked = 50 - 50 + 1 = 1  → "Question 1"

After first question asked: count() = 49
  asked = 50 - 49 + 1 = 2  → "Question 2"

After tenth question asked: count() = 40
  asked = 50 - 40 + 1 = 11 → "Question 11"

Why not just track question_number in the engine?
Because questions are no longer sequential.
The engine doesn't know what number we're on.
Game tracks it by watching how many questions remain.
```

---

# SECTION 3 — THE DECISION ALGORITHM EXPLAINED DEEPLY

## The Problem: Why Fixed Order is Wrong

Suppose we have 5 remaining candidates:

```
Virat Kohli  — real=T, male=T, cricketer=T, actor=F, musician=F
Sachin       — real=T, male=T, cricketer=T, actor=F, musician=F
Priyanka     — real=T, male=F, cricketer=F, actor=T, musician=F
AR Rahman    — real=T, male=T, cricketer=F, actor=F, musician=T
Naruto       — real=F, male=T, cricketer=F, actor=F, musician=F
```

If the next question in fixed order is "Is your character male?" (male=T for 4 of 5):

```
User answers YES: 4 candidates remain (useless)
User answers NO:  1 candidate remains (great if correct)
```

Expected: eliminates 3-4 on average. Very inefficient question here.

Better question: "Is your character a real person?" (4 real, 1 fictional):

```
User answers YES: 4 candidates remain
User answers NO:  1 candidate remains
```

Even better: "Is your character a cricketer?" (2 cricketers, 3 non-cricketers):

```
User answers YES: 2 candidates remain
User answers NO:  3 candidates remain
```

score = abs(2-3) = 1 ← excellent split!

---

## The Scoring Matrix

```
Candidates remaining: n

Perfect question:  true_count = n/2,  false_count = n/2  → score = 0
Worst question:    true_count = n,    false_count = 0    → score = n (skip!)
Good question:     score near 0
Bad question:      score near n/2 or higher

The algorithm selects min(score) across all remaining questions.
```

## Why Skip Questions Where true_count == 0 or false_count == 0

```
true_count == 0: Every candidate answers "No" to this question.
  If user says No: 0 candidates eliminated.
  If user says Yes: ALL candidates eliminated (impossible — user must be one of them).
  Either way: this question provides no useful information.
  
false_count == 0: Every candidate answers "Yes".
  Same logic in reverse.

These questions burn a turn without reducing candidates.
Skipping them is essential for an efficient game.
```

---

# SECTION 4 — ARCHITECTURE EVOLUTION (ALL 8 DAYS)

## Day 35 — Planning

```
No code. Just design decisions.
Repository Pattern selected.
Layered architecture designed.
JSON as initial storage.
```

## Day 36 — Project Structure

```
Folder structure created.
Virtual environment.
characters.json, questions.json designed.
```

## Version 0.5 — Day 37 (Models + Repository)

```
Data Layer:
  models/character.py  (@dataclass)
  models/question.py   (@dataclass)
  repository/          (ABC + JsonRepository)

Architecture:
  main.py → JsonRepository → Character/Question objects
```

## Version 0.6 — Day 38 (Game Class)

```
Game class added.
show_menu() + character_mode() created.
dictionary answer mapping.
```

## Version 0.7 — Day 39 (Full Game Loop)

```
Generic play_game() replaces duplicated category methods.
select_category() with dual list design.
filter_characters() list comprehension.
80 characters + 150 questions loaded.
```

## Version 0.8 — Day 40 (Engine Classes)

```
CharacterEngine extracted from Game.
QuestionEngine (index-based) extracted.
Game now delegates to engines.
Single Responsibility improved.
```

## Version 0.9 — Day 41 (PostgreSQL Migration)

```
database/ layer added.
SQLAlchemy ORM models.
Seeder class.
PostgresRepository.
ONE LINE CHANGED in game.py.
Game behavior: identical.
```

## Version 1.0 — Day 42 (Today)

```
KnowledgeManager — The Brain.
QuestionEngine refactored (storage only).
Dynamic question selection.
Dependency Injection between engines.
Single source of truth.
Score-based algorithm.
GuessWise CLI v1.0 released.
```

---

# SECTION 5 — DESIGN PRINCIPLES DEMONSTRATED

## Single Responsibility Principle

```
Game              → Controls application flow. One reason to change:
                    "How does the user navigate the game?"

CharacterEngine   → Filters candidates. One reason to change:
                    "How are candidates filtered?"

QuestionEngine    → Stores remaining questions. One reason to change:
                    "How are unasked questions managed?"

KnowledgeManager  → Selects best question + processes answers. One reason to change:
                    "How does the selection algorithm work?"

Repository        → Loads data. One reason to change:
                    "Where does data come from?"
```

## Dependency Inversion Principle

```
High-level module (Game) does NOT depend on low-level modules
(CharacterEngine, QuestionEngine, PostgreSQL).

Game depends only on abstractions:
  self.repository         → Repository (ABC)
  self.character_engine   → CharacterEngine (interface)
  self.question_engine    → QuestionEngine (interface)
  self.knowledge_manager  → KnowledgeManager (interface)

Low-level modules depend on same abstractions.
```

## Open/Closed Principle

```
KnowledgeManager.best_question() uses score-based algorithm.
Later: replace with entropy/information-gain algorithm.

You don't modify KnowledgeManager.
You EXTEND it (override best_question() in a subclass).

class SmartKnowledgeManager(KnowledgeManager):
    def best_question(self):
        # Better entropy-based algorithm here
        ...

game.knowledge_manager = SmartKnowledgeManager(...)
# Game.play_game() works identically. No changes needed.
```

## Composition Over Inheritance

```
KnowledgeManager HAS CharacterEngine and QuestionEngine.
KnowledgeManager IS NOT a CharacterEngine.
KnowledgeManager IS NOT a QuestionEngine.

This is Composition:
  Objects work together by holding references to each other.
  More flexible than inheritance.
  Engines can be replaced independently.
```

## Encapsulation

```
Game.play_game() does NOT know:
  → How characters are filtered
  → Which question is best
  → How scores are calculated
  → What True/False means for filtering

It only knows:
  → knowledge_manager.best_question() → gives me a question
  → knowledge_manager.process_answer(question, choice) → handles the logic
  → character_engine.remaining() → gives me the candidates

The HOW is hidden. The WHAT is exposed.
```

---

# SECTION 6 — FULL ARCHITECTURE DIAGRAM

```
                          User
                            │
                            ▼
                         Game.py
                            │
                     ┌──────┴──────┐
                     │  select_    │
                     │  category() │
                     └──────┬──────┘
                            │ creates
              ┌─────────────┼──────────────┐
              ▼             ▼              ▼
   CharacterEngine   QuestionEngine  KnowledgeManager
        │                  │               │
        │ owns:            │ owns:         │ uses:
        │ self.characters  │ self.questions│ char_engine.remaining()
        │                  │               │ question_engine.remaining()
        │                  │               │ question_engine.remove()
        │                  │               │ char_engine.filter()
        │                  │               │
        └──────────────────┴───────────────┘
                            │
                            ▼
               PostgresRepository
                            │
                            ▼
                      PostgreSQL DB
                  (characters, attributes,
                   character_attributes, questions)
```

---

# SECTION 7 — COMPLETE GAME SESSION (Day 42 Version)

```
$ python main.py

Game Started
Loaded 80 characters
Loaded 150 questions

===================================
      🎯 GuessWise CLI v1.0
===================================
1. Character
2. Animal
3. Object
4. Exit
Enter your choice (1-4): 1
[select_category("character")]
[CharacterEngine: 80 characters]
[QuestionEngine: 50 questions]
[KnowledgeManager: receives both engines]

=========================
🎯 GuessWise: Character
=========================
Category : Character
Remaining Candidates : 80
Question 1
[knowledge_manager.best_question() evaluates all 50 questions]
[Finds: "Is your character real?" score=12 (42 real, 38 fictional)]
Is your character a real person?
1. Yes ... 5. Don't Know
Enter your choice (1-5): 1
[knowledge_manager.process_answer(question, "1")]
[character_engine.filter("real", True)]

Remaining Candidates:
- Virat Kohli
- MS Dhoni
- Elon Musk
... (42 real characters)

=========================
Category : Character
Remaining Candidates : 42
Question 2
[best_question() re-evaluates with 42 remaining]
[Different question selected based on remaining set]
Is your character Indian?
...
Enter your choice (1-5): 1

[More questions follow, each dynamically selected...]

...

Remaining Candidates:
- Virat Kohli

🎉 I guessed your answer!
It's: Virat Kohli

-----------------------
Play Again?
-----------------------
1. Yes
2. No
Enter your choice: 2
```

---

# SECTION 8 — WHAT CHANGED FROM DAY 41 TO DAY 42

| File | Day 41 | Day 42 |
|------|--------|--------|
| `game.py` | Direct filtering, sequential questions | Delegates to KnowledgeManager |
| `question_engine.py` | Index-based (current_question, next_question) | Storage-based (remaining, remove) |
| `character_engine.py` | Unchanged | Unchanged (correctly designed) |
| `knowledge_manager.py` | Didn't exist | NEW — decision engine |

---

# SECTION 9 — CONCEPTS LEARNED TODAY

```
Dependency Injection:
  Don't create dependencies inside a class.
  Receive them from outside.
  KnowledgeManager receives CharacterEngine + QuestionEngine.

Single Source of Truth:
  Don't duplicate data between classes.
  KnowledgeManager reads from engines — never stores its own copy.

Encapsulation:
  Hide HOW behind a clean WHAT interface.
  Game never touches filtering logic.
  KnowledgeManager hides it.

Dynamic Question Selection:
  Score = abs(true_count - false_count)
  Lower score = better split = better question.
  Skip questions where all candidates give same answer.

Separation of Concerns (evolved):
  QuestionEngine = storage (what questions remain?)
  KnowledgeManager = strategy (which question is best?)
  CharacterEngine = filtering (who still matches?)
  Game = flow (what happens next?)

Composition:
  KnowledgeManager HAS engines. It IS NOT an engine.
  Composition is more flexible than inheritance.

Software Evolution:
  Good systems evolve gradually through refactoring.
  Each version builds on the previous one.
  The Repository Pattern from Day 35 is still unchanged.
```

---

# SECTION 10 — THE COMPLETE EVOLUTION OF GUESSWISE (DAYS 35-42)

```
DAY 35: Planning + Architecture Design
  → Repository Pattern decided
  → Layered architecture sketched
  → JSON design created (database-aware)

DAY 36: Project Initialization
  → Folder structure created
  → Virtual environment
  → Data files designed

DAY 37: Data Layer
  → @dataclass models (Character, Question)
  → Abstract Repository interface
  → JsonRepository implementation
  → Data loading confirmed

DAY 38: Game Class + CLI
  → Game class with show_menu()
  → Input validation loops
  → Dictionary answer mapping
  → PostgreSQL 18 environment verified

DAY 39: Complete Game Loop
  → Generic play_game() (DRY principle)
  → select_category() with dual-list design
  → filter_characters() algorithm
  → 80 characters + 150 questions
  → update_attributes.py migration tool

DAY 40: Engine Refactor
  → CharacterEngine class extracted
  → QuestionEngine (index-based) extracted
  → Game now delegates to engines
  → SRP significantly improved

DAY 41: PostgreSQL Migration
  → database/ layer: database.py, models.py, seed.py, run_seed.py
  → 4 normalized tables: characters, attributes, character_attributes, questions
  → PostgresRepository implementing Repository interface
  → ONE line changed in game.py
  → Game behavior: identical

DAY 42: Knowledge Manager + v1.0
  → KnowledgeManager (decision engine)
  → QuestionEngine refactored (storage-only)
  → Dependency Injection between engines
  → Score-based question selection algorithm
  → process_answer() delegated from Game
  → Single Source of Truth enforced
  → GuessWise CLI v1.0 released
```

---

# SECTION 11 — LEETCODE #1480: RUNNING SUM OF 1D ARRAY

## Problem

Given array `nums`, return its running sum where `runningSum[i] = sum(nums[0]...nums[i])`.

```
Input:  [1, 2, 3, 4]
Output: [1, 3, 6, 10]
```

## Approach 1 — Brute Force O(n²)

```python
class Solution(object):
    def runningSum(self, nums):
        answer = []
        for i in range(len(nums)):
            answer.append(sum(nums[:i+1]))   # Recalculates from scratch each time
        return answer
```

**Why O(n²):** `sum(nums[:i+1])` is O(i) work. Called n times. Total: O(n²).

At i=3: calculates 1+2+3+4 (already computed 1+2+3 on the previous iteration).

## Approach 2 — Prefix Sum O(n) ✅ Submitted

```python
class Solution(object):
    def runningSum(self, nums):
        runningSum = []
        running_sum = 0
        for i in range(len(nums)):
            running_sum += nums[i]         # Add current, keep running total
            runningSum.append(running_sum)
        return runningSum
```

**The key insight:**

```
runningSum[i] = runningSum[i-1] + nums[i]

Each answer uses the PREVIOUS answer. No recalculation.

nums = [1, 2, 3, 4]

running_sum starts at 0.

Read 1: 0+1=1   → append 1    → [1]
Read 2: 1+2=3   → append 3    → [1,3]
Read 3: 3+3=6   → append 6    → [1,3,6]
Read 4: 6+4=10  → append 10   → [1,3,6,10]

1 addition per element. Single pass. O(n).
```

**Common mistakes made (documented):**

```python
# Mistake 1: wrong initialization
runningSum = [] * len(nums)   # [] * anything = [] (empty list!)

# Mistake 2: index assignment on empty list
runningSum[i] = value         # IndexError: list index out of range

# Mistake 3: sum is a function, not a list
sum[nums[i]]                  # TypeError: 'builtin_function_or_method' not subscriptable

# Mistake 4: summing the answer list instead of nums
running_sum = sum(runningSum) # Recalculating everything again (back to O(n²))
```

**Result:** ✅ Accepted | 54/54 test cases | Runtime: 0ms | Beats 100% | Memory: 12.46MB

## The Prefix Sum Pattern

```
This pattern appears in many problems:
  #724 Find Pivot Index      (already solved on Day 37)
  #303 Range Sum Query       (coming soon)
  #560 Subarray Sum Equals K (Medium)
  #238 Product of Array Except Self (Medium)

Core idea: "Don't recalculate. Accumulate."
  Store the running answer in a variable.
  Each new answer = previous answer + current element.
  O(n) instead of O(n²).
```

---

# SECTION 12 — MONTH 2 CHECKPOINT — DAY 42

The roadmap milestone for Day 42:

```
✅ Write Python classes, decorators, generators without help
   → All 8 GuessWise classes written from scratch: Game, CharacterEngine,
     QuestionEngine, KnowledgeManager, Repository, Character, Question, Seeder

✅ Write complex SQL JOIN queries
   → 14 LeetCode SQL problems solved (Days 29-35)
   → Real JOIN queries in PostgresRepository

✅ Understand async/await in Python
   → Covered in Day 25

✅ Know all HTTP methods and status codes by heart
   → Covered in Days 22-23

✅ Explain OOP (4 pillars) in an interview right now
   → GuessWise demonstrates all 4:
     Encapsulation: KnowledgeManager hides filtering logic
     Abstraction: Repository ABC hides storage details
     Inheritance: PostgresRepository extends Repository
     Polymorphism: JsonRepository or PostgresRepository — same interface

✅ Design a basic database schema on paper
   → 4-table normalized schema designed on Day 32, implemented on Day 41

✅ Have 2+ projects on GitHub with README
   → Backend-Developer-Journey repository (ongoing)
   → GuessWise v1.0 (ready to push)
   → README_GuessWise_v1.0.md written

✅ Can use SQLAlchemy to connect Python to PostgreSQL
   → database.py, models.py, seed.py, postgres_repository.py all working
```

**All 8 Month 2 goals: ACHIEVED.** ✅

---

# SECTION 13 — FUTURE ROADMAP (GuessWise v2)

GuessWise CLI v1.0 is complete. The architecture built here is the foundation for v2:

```
v2 Feature                  → What v1 already prepared
─────────────────────────────────────────────────────
FastAPI backend             → PostgresRepository is the data layer
REST API endpoints          → get_characters(), get_questions() already exist
Admin panel                 → Database schema is in place
User authentication         → users table can be added easily
Better decision algorithm   → Override KnowledgeManager.best_question()
AI/ML question selection    → Same interface, different implementation
Docker deployment           → Clean architecture, no platform coupling
Better algorithm (entropy)  → Replace score=abs() with information gain formula
```

**The Repository Pattern ensures none of the v2 changes require rewriting game logic.**

---

# REVISION SHEET

```
═══════════════════════════════════════════════════════════
GUESSWISE v1.0 — FINAL ARCHITECTURE
═══════════════════════════════════════════════════════════

LAYER MAP:
  Presentation  → main.py (3 lines)
  Business      → game.py (flow) + knowledge_manager.py (brain)
  Engine        → character_engine.py + question_engine.py
  Data          → repository/ (abstract + postgres impl)
  Database      → database/ (ORM models, seed)

CLASS RESPONSIBILITIES:
  Game              → application flow only
  CharacterEngine   → filter, count, guess
  QuestionEngine    → store, remove, remaining
  KnowledgeManager  → select best_question, process_answer
  PostgresRepo      → load data from PostgreSQL

KNOWLEDGE MANAGER ALGORITHM:
  For each remaining question:
    Count true_count, false_count across remaining characters
    Skip if either is 0 (useless question)
    score = abs(true_count - false_count)
    Keep question with minimum score
  Remove selected question from pool
  Return it

DEPENDENCY INJECTION:
  KnowledgeManager receives CharacterEngine + QuestionEngine
  Never creates its own copy of data
  Always reads from engines (single source of truth)

QUESTION ENGINE (Day 42):
  remaining() → list of unasked questions
  remove(q)   → mark question as asked
  finished()  → True when pool is empty
  count()     → how many remain

CORE PRINCIPLES DEMONSTRATED:
  SRP   → Each class has ONE reason to change
  DIP   → Depend on abstractions, not concretions
  OCP   → Extend (new KnowledgeManager subclass), don't modify
  DI    → Inject dependencies, don't create them
  SoT   → One source of truth per data item
```

---

## ✅ Day 42 Task Summary

| Task | Status |
|------|--------|
| Refactor QuestionEngine (remove index-based logic) | ✅ Done |
| Create KnowledgeManager | ✅ Done |
| Implement best_question() algorithm | ✅ Done |
| Implement process_answer() | ✅ Done |
| Refactor game.py to use KnowledgeManager | ✅ Done |
| Fix repeated-question bug | ✅ Done |
| Verify game plays end-to-end | ✅ Done |
| LeetCode #1480 Running Sum | ✅ Accepted (0ms, 100%) |
| Month 2 Checkpoint review | ✅ All 8 goals achieved |
| GuessWise CLI v1.0 released | ✅ Done |

---

## LeetCode Solved This Day

| Problem | Difficulty | Topic | Status | Runtime |
|---------|-----------|-------|--------|---------|
| #1480 Running Sum of 1d Array | Easy | Prefix Sum, Accumulation | ✅ Accepted 54/54 | 0ms, Beats 100% |

---

## GuessWise v1.0 — Final Stats

```
Duration:    Day 35 → Day 42 (8 days)
Files:       14 Python files
Classes:     8 (Game, CharacterEngine, QuestionEngine, KnowledgeManager,
               Repository, JsonRepository, PostgresRepository, Seeder)
DB Tables:   4 (characters, attributes, character_attributes, questions)
Characters:  80 (3 categories)
Questions:   150 (50 per category)
Version:     1.0
Status:      ✅ Complete
```

---

*Day 42 Complete. GuessWise CLI v1.0 released. Month 2 Checkpoint achieved.* ✅

*"Every great software project starts with simple code, but becomes valuable through thoughtful architecture and continuous refactoring."*
