
# Step 1 — Create the Project Folder
# Create a new folder: guesswise/
# my path is -> "C:\A_MY THINGS\001\Backend-Developer-Journey\Project\GuessWise"
# Open it in VS Code.



# Step 2 — Create a Virtual Environment
# Inside the project:  python -m venv .venv
# Activate it-> Windows: .venv\Scripts\activate
# Then check: python --version

# like this:

# Microsoft Windows [Version 10.0.26200.8737]
# (c) Microsoft Corporation. All rights reserved.
# C:\A_MY THINGS\001\Backend-Developer-Journey\Project\GuessWise> python -m venv .venv
# C:\A_MY THINGS\001\Backend-Developer-Journey\Project\GuessWise>"c:\A_MY THINGS\001\Backend-Developer-Journey\Project\GuessWise\.venv\Scripts\activate"
# (.venv) C:\A_MY THINGS\001\Backend-Developer-Journey\Project\GuessWise>.venv\Scripts\activate
# (.venv) C:\A_MY THINGS\001\Backend-Developer-Journey\Project\GuessWise>python --version
# Python 3.12.3
# (.venv) C:\A_MY THINGS\001\Backend-Developer-Journey\Project\GuessWise>




# Step 3 — Initialize Git
# git init --> i already have



# Step 4 — Create .gitignore
# Include at least:
# .venv/
# __pycache__/
# *.pyc
# .vscode/ --> already have




# Step 5 — Create requirements.txt
# For Version 1 it can even be empty, or later you'll add packages as needed.




# Step 6 — Create the Folder Structure
# guesswise/
# ├── main.py
# ├── game.py
# ├── README.md
# ├── requirements.txt
# ├── .gitignore
# ├── models/
# │   ├── __init__.py
# │   ├── character.py
# │   └── question.py
# ├── repository/
# │   ├── __init__.py
# │   ├── repository.py
# │   └── json_repository.py
# ├── engines/
# │   ├── __init__.py
# │   ├── character_engine.py
# │   └── question_engine.py
# ├── utils/
# │   ├── __init__.py
# │   ├── display.py
# │   └── validation.py
# ├── data/
# │   ├── characters.json
# │   └── questions.json
# └── tests/
# Notice every Python package contains an __init__.py.






# Step 7 — Write the README
# Don't write everything today.
# Just include:
# Project name
# Description
# Version
# Folder structure
# Technologies
# Roadmap
# We'll improve it later.





# Step 8 — Think About the Data
# Before writing classes, ask:

# What is a Character?
# For example:
# id
# name
# category
# traits (or answers to questions)

# Similarly, what is a Question?
# id
# text
# Design the data first. Code comes after.




# Step 9 — Create the Model Classes

# Create:
# Character
# Question
# These are plain data models.
# No game logic yet.





# Step 10 — Design the Repository
# Ask yourself:
# If tomorrow I replace JSON with PostgreSQL, should the Game class change?
# The answer should be No.

# That's why we create a repository interface first.
# It might define methods like:

# load_characters()
# load_questions()
# save_characters()
# save_questions()
# The JSON repository will implement those methods.




# Step 11 — Create Sample JSON Data
# Don't add 50 characters yet.
# Start with 3–5.
# For example:
# Lion
# Tiger
# Elephant

# Or:
# Harry Potter
# Spider-Man
# Batman

# Keep it small so you can test quickly.





# Step 12 — Test the Repository

# Write a tiny script that:
# Reads the JSON files.
# Creates Character objects.
# Prints them.
# If this works, you've successfully connected your data layer.




