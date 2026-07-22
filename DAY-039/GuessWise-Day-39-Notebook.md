# GuessWise — Day 39 Notebook

# Backend Developer Journey
**Project:** GuessWise (CLI Akinator Clone)
**Day:** 39

## Goal
Transform GuessWise into a playable CLI game with:
- Category selection
- Multiple questions
- Candidate filtering
- Guessing
- Play Again

---

## Architecture

```text
main.py
    |
    v
Game
 ├── start()
 ├── show_menu()
 ├── select_category()
 ├── play_game()
 ├── filter_characters()
 ├── show_remaining_candidates()
 └── play_again()

Repository
    |
    v
JSON Files
```

---

## Why play_game() instead of character_mode()

Old:

character_mode()
animal_mode()
object_mode()

Problem:
- Duplicate logic
- Hard to maintain
- Hard to extend

New:

show_menu()
    |
select_category()
    |
play_game()

Only the dataset changes; the game logic stays the same.

---

## Why current_category?

Stores the active dataset so Play Again reloads the correct category.

---

## Why current_questions?

Instead of using all questions, each category has its own filtered question list.

Example future JSON:

```json
{
  "id": 1,
  "category": "character",
  "text": "Is your character real?",
  "attribute": "real"
}
```

---

## Filtering Algorithm

```python
self.characters = [
    character
    for character in self.characters
    if character.attributes.get(attribute) == expected_value
]
```

Using `.get()` prevents KeyError when an attribute is missing.

---

## Game Flow

```text
Menu
 |
Select Category
 |
Ask Question
 |
Filter Candidates
 |
One Candidate?
 |-- Yes -> Guess
 |-- No -> Next Question
 |-- None -> No Match
```

---

## Methods Added

- start()
- show_menu()
- select_category()
- play_game()
- filter_characters()
- show_remaining_candidates()
- play_again()

---

## Challenges Solved

1. Removed duplicated game modes.
2. Added reusable game loop.
3. Introduced category filtering.
4. Implemented candidate filtering.
5. Added replay support.
6. Prepared architecture for PostgreSQL migration.

---

## Files Worked On

```text
GuessWise/
├── game.py
├── main.py
├── repository/
│   ├── repository.py
│   └── json_repository.py
├── models/
│   ├── character.py
│   └── question.py
└── data/
    ├── characters.json
    └── questions.json
```

---

## Expected Output

```text
Question 1

Is your character real?

1. Yes
2. No
3. Probably
4. Probably Not
5. Don't Know

Remaining Candidates:
- Virat Kohli
- Sachin Tendulkar

🎉 I guessed your answer!
```

---

## Day 39 Completed

- Generic game loop
- Category selection
- Category-specific questions
- Filtering algorithm
- Guessing logic
- Replay system
- Clean architecture ready for Day 40
