import json
from pathlib import Path

# -----------------------------
# File Paths
# -----------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

CHARACTER_FILE = BASE_DIR / "data" / "characters.json"
QUESTION_FILE = BASE_DIR / "data" / "questions.json"

# -----------------------------
# Load Questions
# -----------------------------

with open(QUESTION_FILE, "r", encoding="utf-8") as file:
    question_groups = json.load(file)

category_attributes = {}

for group in question_groups:
    category = group["category"]

    attributes = [
        question["attribute"]
        for question in group["questions"]
    ]

    category_attributes[category] = attributes

# -----------------------------
# Load Characters
# -----------------------------

with open(CHARACTER_FILE, "r", encoding="utf-8") as file:
    characters = json.load(file)

# -----------------------------
# Add Missing Attributes
# -----------------------------

updated = 0

for character in characters:

    category = character["category"]

    required_attributes = category_attributes.get(category, [])

    attributes = character.setdefault("attributes", {})

    for attribute in required_attributes:

        if attribute not in attributes:
            attributes[attribute] = False
            updated += 1

# -----------------------------
# Save
# -----------------------------

with open(CHARACTER_FILE, "w", encoding="utf-8") as file:
    json.dump(characters, file, indent=2)

print("=" * 40)
print("Migration Complete")
print("=" * 40)
print(f"Characters : {len(characters)}")
print(f"Attributes Added : {updated}")
print("characters.json updated successfully.")