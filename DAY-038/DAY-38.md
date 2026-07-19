# DAY 38 — GuessWise: Game Class, Menu System + LeetCode Linear Traversal

> **Project:** GuessWise — From Data Loading to Interactive CLI
>
> **Path:** `C:\A_MY THINGS\001\Backend-Developer-Journey\Project\GuessWise`
>
> **LeetCode:** #485 Max Consecutive Ones ✅ (Linear Traversal / Running Counter pattern)
>
> **Status:** ✅ Day 38 Complete — Game is now interactive, environment verified (PostgreSQL 18 detected)

---

# 🎯 What Was Built Today

```
✅ Game class — controls overall application flow
✅ Game flow: start() → load data → show_menu()
✅ Main menu with Character/Animal/Object/Exit options
✅ Character mode with question display
✅ User answer collection (Yes/No/Probably/Probably Not/Don't Know)
✅ Input validation with retry loop
✅ Dictionary-based answer mapping (no messy if/elif chains)
✅ PostgreSQL 18 confirmed installed (preparation for Day 40)
✅ LeetCode #485 solved (Brute Force + Linear Traversal)
```

GuessWise went from "a project that loads JSON and prints it" to **a project you can actually run and interact with in the terminal.**

---

# 📁 Project State After Day 38

```
GuessWise/
│
├── main.py                      ← Updated: now starts the Game
├── game.py                      ← ✅ NEW — Game class with menu system
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

# SECTION 1 — WHY THE Game CLASS EXISTS

## Single Responsibility, Layer by Layer

```
Repository layer (Day 37):
  Responsibility: WHERE does data come from?
  Knows about: JSON files, file paths, json.load()
  Knows nothing about: menus, user input, game rules

Game layer (Day 38):
  Responsibility: WHAT does the application DO?
  Knows about: menus, game flow, coordinating engines
  Knows nothing about: file paths, SQL, JSON internals
```

The `Game` class is the **conductor** — it doesn't play any instrument itself, it tells other classes when to act.

```python
class Game:
    def __init__(self):
        self.repository = JsonRepository()   # Game doesn't know it's JSON specifically
                                              # It just knows "a repository"

    def start(self):
        self.characters = self.repository.get_characters()  # Ask, don't read directly
        self.questions  = self.repository.get_questions()
```

**What Game does NOT do:**

```
❌ open("data/characters.json")     ← That's the repository's job
❌ cursor.execute("SELECT ...")     ← That's also the repository's job
❌ Format raw dictionaries          ← Models already did that on Day 37
```

---

## Why `self.characters` Instead of a Local Variable

```python
# WRONG — local variable disappears after the method ends
def start(self):
    characters = self.repository.get_characters()
    self.show_menu()
    # When show_menu() needs characters later, they're already gone!


# CORRECT — instance attribute persists for the object's lifetime
def start(self):
    self.characters = self.repository.get_characters()
    self.show_menu()
    # Now self.characters is accessible from ANY method on this Game object,
    # for as long as the Game object exists.
```

```
Local variable:    lives only inside the function that created it
self.attribute:    lives as long as the object (self) exists

Future methods that will need self.characters:
  ask_question()
  filter_characters()
  guess_character()

All of these are methods on the SAME Game object,
so they all share self.characters.
```

---

# SECTION 2 — THE GAME CODE

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

            choice = input("\nEnter your choice (1-4): ").strip()

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
            print("\n=========================")
            print("Character Mode")
            print("=========================")
            print("\nQuestion 1\n")

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

            choice = input("\nEnter your choice (1-5): ").strip()

            if choice in answers:
                print(f"You selected: {answers[choice]}")
                break

            print("Invalid choice! Please enter a number from 1 to 5.")
```

## main.py

```python
from game import Game

game = Game()
game.start()
```

**main.py is now extremely thin.** It does exactly one thing: create a Game and start it. All actual logic lives in `game.py`. This is intentional — `main.py` is the entry point, not the brain.

---

# SECTION 3 — PROJECT FLOW

```
main.py
    │
    ▼
Game.start()
    │
    ├──► Load Characters (via repository)
    │
    ├──► Load Questions (via repository)
    │
    └──► Show Menu
              │
              ├──► Character Mode
              │         │
              │         ├──► Display Question
              │         │
              │         ├──► Get Answer
              │         │
              │         └──► Print Selected Answer
              │
              ├──► Animal Mode (placeholder)
              ├──► Object Mode (placeholder)
              └──► Exit
```

---

# SECTION 4 — WHY show_menu() AND character_mode() ARE SEPARATE METHODS

## Method Decomposition

```python
def show_menu(self):
    # ONE responsibility: display main menu, route to correct mode
    ...

def character_mode(self):
    # ONE responsibility: handle the character-quiz flow
    ...
```

**Why not put everything in one giant method?**

```
A single 200-line method:
  ❌ Hard to read
  ❌ Hard to test
  ❌ Hard to debug
  ❌ Hard to extend (adding Animal mode means editing the same giant block)

Separate methods:
  ✅ Each method has ONE clear job (Single Responsibility Principle)
  ✅ Adding animal_mode() later is trivial — just another method
  ✅ Easy to test character_mode() in isolation
  ✅ Easy to read — show_menu() reads like a table of contents
```

This is the same principle from Day 36's architecture design, applied at the method level instead of the file level.

---

# SECTION 5 — WHY DICTIONARY MAPPING INSTEAD OF if/elif CHAINS

## The Problem With Long if/elif Chains

```python
# Verbose, repetitive, hard to scale
if choice == "1":
    print("You selected: Yes")
elif choice == "2":
    print("You selected: No")
elif choice == "3":
    print("You selected: Probably")
elif choice == "4":
    print("You selected: Probably Not")
elif choice == "5":
    print("You selected: Don't Know")
else:
    print("Invalid choice!")
```

## The Dictionary Solution

```python
answers = {
    "1": "Yes",
    "2": "No",
    "3": "Probably",
    "4": "Probably Not",
    "5": "Don't Know"
}

choice = input("\nEnter your choice (1-5): ").strip()

if choice in answers:
    print(f"You selected: {answers[choice]}")
```

**Why this is better:**

```
✅ Adding a new answer = add one dictionary entry, not a whole elif block
✅ choice in answers → O(1) lookup, instant validation
✅ Code reads like a data table, not a wall of logic
✅ Mapping data is separated from control flow — easier to maintain
✅ This pattern scales: 5 answers or 500 answers, code stays the same shape
```

This is a recurring backend pattern: **prefer data structures over conditional chains** whenever the logic is really "look this value up."

---

# SECTION 6 — EXPECTED CONSOLE OUTPUT

```
Game Started
Loaded 5 characters
Loaded 8 questions

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

Is your character a real person?

1. Yes
2. No
3. Probably
4. Probably Not
5. Don't Know

Enter your choice (1-5): 1

You selected: Yes
```

This confirms the full chain works:

```
Repository loads data → Game stores it → Menu displays →
Character mode runs → Question shows → Answer is captured and validated
```

---

# SECTION 7 — ENVIRONMENT CHECK: POSTGRESQL CONFIRMED

Before Day 40 (PostgreSQL migration), the database environment was verified in pgAdmin:

```
ID:          1
Name:        PostgreSQL 18
Server type: PostgreSQL
Version:     PostgreSQL 18.4 on x86_64-windows, compiled by msvc-19.4
Comments:    Auto-detected PostgreSQL 18 installation
             Data directory: C:\Program Files\PostgreSQL\18\data
```

**Why check this now, two days before the migration?**

```
Confirming the database is installed and running EARLY avoids
a surprise blocker on Day 40 when the actual migration work begins.

This is a habit of professional developers:
verify your environment before you need it, not when you're blocked by it.
```

---

# SECTION 8 — CONCEPTS LEARNED TODAY

```
✅ Layered Architecture — presentation (menu) vs business (game flow) vs data (repository)
✅ Repository Pattern in action — Game uses self.repository without knowing it's JSON
✅ Separation of Concerns — Game never touches files or SQL directly
✅ Single Responsibility Principle — show_menu() and character_mode() each do ONE thing
✅ Instance attributes (self.x) for state that must persist across method calls
✅ Method decomposition — breaking logic into small, focused methods
✅ Input validation with a retry loop (while True + break on valid input)
✅ Dictionary lookup mapping — replacing long if/elif chains with data structures
✅ CLI design — clear menus, numbered choices, friendly prompts
```

---

# SECTION 9 — LEETCODE #485: MAX CONSECUTIVE ONES

## Problem

Given a binary array, find the maximum number of consecutive 1's.

```
nums = [1, 1, 0, 1, 1, 1]
         └─2─┘   └──3──┘
Answer: 3
```

## Brute Force — O(n²)

```python
class Solution(object):
    def findMaxConsecutiveOnes(self, nums):
        maximum = 0

        for i in range(len(nums)):
            if nums[i] == 1:
                count = 0
                j = i
                while j < len(nums) and nums[j] == 1:
                    count += 1
                    j += 1
                maximum = max(maximum, count)

        return maximum
```

**Why it's slow:** For every `1` found, an inner loop re-walks the same consecutive sequence that may have already been partially counted from an earlier starting index. Nested loops → O(n²) in the worst case (all 1's).

## Linear Traversal (Optimal) — O(n) ✅ Submitted

```python
class Solution(object):
    def findMaxConsecutiveOnes(self, nums):
        count = 0
        max_count = 0

        for num in nums:
            if num == 1:
                count += 1
                if count > max_count:
                    max_count = count
            else:
                count = 0

        return max_count
```

**The running counter pattern:**

```
See a 1  → increment running count, update max if needed
See a 0  → reset running count to 0 (streak broken)

Single pass through the array. Only two variables used.
```

**Dry run:**

```
nums = [1, 1, 0, 1, 1, 1]

1 → count=1, max=1
1 → count=2, max=2
0 → count=0
1 → count=1, max=2
1 → count=2, max=2
1 → count=3, max=3

Return 3 ✅
```

## Complexity

```
Brute Force:        Time O(n²)   Space O(1)
Linear Traversal:    Time O(n)    Space O(1)
```

## Why This Pattern Matters

```
"Running counter that resets on a condition" is one of the most common
interview patterns for array problems:
  → Longest streak of any repeated value
  → Longest substring without repeating characters (similar idea, sliding window)
  → Max consecutive characters in a string

The core idea: avoid recomputation by carrying state forward
through a single pass, instead of restarting from scratch each time.

This is the same family of thinking as yesterday's Prefix Sum problem (#724) —
"don't recalculate, accumulate."
```

---

# ✅ Day 38 Task Summary

| Task | Status |
|------|--------|
| Create Game class | ✅ Done |
| Implement start() — load data, show menu | ✅ Done |
| Implement show_menu() — main CLI menu | ✅ Done |
| Implement character_mode() — question flow | ✅ Done |
| Input validation with retry loop | ✅ Done |
| Dictionary-based answer mapping | ✅ Done |
| Update main.py to use Game | ✅ Done |
| Verify PostgreSQL 18 installation | ✅ Done |
| LeetCode #485 Brute Force | ✅ Done |
| LeetCode #485 Linear Traversal | ✅ Accepted |

---

# 📅 What's Coming: Day 39

```
Day 39 goals — make the game actually PLAYABLE:

1. CharacterEngine (engines/character_engine.py)
   - Hold the list of "remaining" characters
   - filter(attribute, answer) → removes characters that don't match
   - count() → how many characters remain
   - guess() → returns the final character when only 1 remains

2. Wire character_mode() to actually loop through ALL questions
   (currently it only shows question[0] — that hardcoding gets fixed)

3. Connect answers to CharacterEngine.filter()
   - "Yes" → keep characters where attributes[question.attribute] == True
   - "No"  → keep characters where attributes[question.attribute] == False

4. Add the guess reveal:
   "Is your character [name]?" → win/lose response

5. Refactor + error handling + polish (stable Version 1 by end of week)

By end of Day 39: GuessWise is a complete, playable, end-to-end game.
```

---

*Day 38 Complete. Game is interactive. Menu system working. Character flow established. Filtering logic comes next.* ✅