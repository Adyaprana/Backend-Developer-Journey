# THEORY 1 — WHAT IS GIT?

# Imagine: You write code today.
# Tomorrow:
print("Hello")
# becomes
print("Bug")
# and project breaks.

# Without Git: Game Over
# With Git: Go back to yesterday
# Git tracks every change.



# THEORY 2 — GIT VS GITHUB

# Git --> Software installed on your computer, Local Version Control.
# GitHub --> Website, Stores Git repositories online.
# Think:
# Git = MS Word
# GitHub = Google Drive


# THEORY 3 — GIT WORKFLOW

# Working Directory
#       ↓
# git add
#       ↓
# Staging Area
#       ↓
# git commit
#       ↓
# Local Repository
#       ↓
# git push
#       ↓
# GitHub



# GIT INSTALLATION: 

# Check Git: git --version
# Output: git version 2.xx.x

# Configure Git
# Run once:
# git config --global user.name "Adyaprana Pradhan"
# git config --global user.email "your@email.com"
# Check: git config --list



# CREATE REPOSITORY: 

# Navigate: cd project-folder
# Initialize: git init
# Output: Initialized empty Git repository

# Check Status: git status
# Example:
# Untracked files:
# main.py

# Meaning:
# Git sees file.
# Not tracking yet.



# STAGING FILES:

# Add single file: git add main.py
# Add all files: git add .
# Check: git status
# Output: Changes to be committed

# COMMIT:
# Commit means: Take snapshot.
# git commit -m "Initial commit"
# Example (Good commit): git commit -m "Add contact book project"
# Bad commit: git commit -m "update"

# MEANINGFUL COMMITS:
# Good:
# git commit -m "Add login functionality"
# git commit -m "Fix password validation bug"
# git commit -m "Improve contact search feature"



# GITHUB PUSH: 

# Create repo on GitHub.
# Example: contact-book
# Connect: git remote add origin https://github.com/username/contact-book.git
# Check: git remote -v

# Push: git push -u origin main (First push only)
# After that: git push (enough)

# PULL:
# Download latest changes.
# git pull origin main

# CLONE 
# Download repository.
# git clone https://github.com/user/repo.git
# Example: git clone https://github.com/Adyaprana/Backend-Developer-Journey.git



# THEORY 4 — BRANCHES

# Why branches exist?
# Imagine: You want to add feature, Current code works so Don't touch main branch Create separate branch. 

# CREATE BRANCH
# See branches: git branch
# Create: git branch feature-login

# Switch: git checkout feature-login
# Modern way: git switch feature-login

# CREATE + SWITCH
# git checkout -b feature-login

# MERGE: 
# Go back: git checkout main
# Merge: git merge feature-login

# WORKING EXAMPLE: 
# git checkout -b add-search
# modify code
# git add .
# git commit -m "Add search feature"
# git checkout main
# git merge add-search



# GIT LOG: 

# View history: git log
# Compact: git log --oneline

# Example:
# e4c21 Add login feature
# c8f72 Fix bug
# a9d12 Initial commit
# SHOW CHANGES
# git diff

# Shows:
# Old line
# New line
# GIT SHOW
# git show commit_id
# Example: git show a9d12



# STASH: 

# Temporary save.
# Example: Boss says Switch task now, But your code unfinished.

# Use: git stash
# Later:git stash pop
# Get work back.




# EXTRA IMPORTANT TOPICS:

# .gitignore --> Ignore files.
# Example:
# __pycache__/
# .env
# venv/
# Create: .gitignore
# Every Python developer uses this.



# README.md --> (Every project should have)
# Project Name
# Features
# Installation
# Usage
# Screenshots
# Author

