# DAY 24 — GIT & GITHUB: THE COMPLETE GUIDE

> **Goal:** Master version control from zero — understand Git's internal architecture, daily workflows, branching strategies, and advanced concepts that separate beginners from professional developers.
>
> **Week:** W4 — How the Web Works + Git + Advanced Python
>
> **Status:** ✅

---

## 🎯 Learning Roadmap & Core Concepts

### What Today Covers (Your Program)

```
Git + GitHub — Full Setup

  ✅ git init, git add, git commit -m, git status, git log
  ✅ git push, git pull, git clone
  ✅ Branching: git branch, git checkout, git merge
  ✅ Create a new repo on GitHub, push your Contact Book project
  ✅ Practice: make 5 commits with meaningful messages

  ▶ Kunal Kushwaha: Git & GitHub in 1 video (Hindi/English) ⭐
```

### Core Concepts Checklist

- [ ] Essential Plumbing vs. Porcelain Commands
- [ ] The `.git` folder — what every file inside it means
- [ ] The Three States: Working Directory → Staging Area → Repository
- [ ] Local vs. Remote Workflows
- [ ] Branching, Merging, and Conflict Resolution Strategies
- [ ] What you studied today vs. What new advanced patterns you need to master
- [ ] Git as a Directed Acyclic Graph (DAG)
- [ ] Git Hooks, Tags, Rebase, Cherry-pick, Bisect

### What You Studied Today vs. What You Need Next

| What You Studied Today | What This File Adds |
|---|---|
| git init, add, commit | How these create objects inside `.git/objects/` |
| git push, pull, clone | Remote tracking branches, fetch vs. merge internals |
| Branching + merge | Fast-forward vs. three-way merge, conflict resolution |
| git stash, .gitignore | All stash commands, gitignore pattern syntax |
| README.md structure | OpenAPI + Postman collection versioning via Git |
| 15 basic interview Q&A | 10 multi-paragraph production-level answers |

---

## 📚 Deep Dive Theory, Core Documentation & Resources

### Why Version Control Powers Everything

Every professional tool you will use as a backend developer is version-controlled:

```
Your FastAPI code           → Git + GitHub
Your Postman collections    → Can be exported as JSON and committed
Your Hoppscotch workspaces  → Can be exported and version-controlled
Your ReqRes mock configs    → Environment variables tracked in .env.example
Your Docker configs         → Dockerfile committed to repo
Your database migrations    → Tracked as numbered migration files
Your API documentation      → OpenAPI spec (openapi.json) committed and diffed
Your CI/CD pipelines        → .github/workflows/ci.yml committed
```

When you commit a Postman collection JSON to your repository, every team member gets the exact same set of API requests. When the API changes, the collection is updated in the same PR as the code. Code review covers both the implementation and the tests together.

ReqRes gives you a public mock API so you can build and test frontend or HTTP client code without having a backend running. When you store your ReqRes-based test scripts in a Git repo, your entire team runs the same tests against the same mock responses.

web.dev's deployment guides recommend treating your build configuration, Lighthouse CI thresholds, and performance budgets as files committed to Git — not settings in a dashboard. This way, changes to deployment criteria are reviewed, audited, and reversible.

---

### The Mental Model — Git as a Time Machine

```
Without Git:
  project_v1.py
  project_v2_FINAL.py
  project_v2_FINAL_actually_final.py
  project_v2_FINAL_actually_final_2.py

With Git:
  One folder.
  Every version accessible.
  Every change attributed to a person.
  Every change explained with a message.
  Any version restorable instantly.
```

Every `git commit` is a **snapshot** of your entire project at that moment. Not a diff. Not a change log. A complete photograph.

Git is efficient because if a file didn't change between two commits, Git stores a reference to the same blob instead of copying the file again.

---

### Git vs. GitHub — The Exact Difference

```
Git    = Software installed on your computer
         Tracks changes locally
         Works 100% offline
         Created by Linus Torvalds in April 2005
         (He built it in 10 days to manage the Linux kernel)

GitHub = A website: github.com
         Stores Git repositories online
         Enables collaboration
         Adds PRs, Issues, Actions on top of Git
         Owned by Microsoft since 2018
```

**The best analogy:**

```
Git    → Microsoft Word   (software on your machine)
GitHub → Google Drive     (where you store and share)

You can use Word without Google Drive.
You can use Git without GitHub.
But together they are extremely powerful.
```

Other hosting platforms that work with the same Git commands:

```
GitLab     → gitlab.com     (CI/CD built in, open-source friendly)
Bitbucket  → bitbucket.org  (popular in enterprise with Jira)
Azure Repos → Microsoft ecosystem (used at large companies)
Gitea      → Self-hosted, lightweight
```

---

### Centralized vs. Distributed Version Control

**Old way — SVN (Centralized):**

```
Developer A ──┐
Developer B ──┼──► Central Server  (single source of truth)
Developer C ──┘

Problems:
  Server goes down → nobody can commit or see history
  Every operation needs network
  No offline work possible
  Branching is slow (copies entire folder)
```

**Git's way — Distributed:**

```
Developer A has FULL COMPLETE copy of repo (all history)
Developer B has FULL COMPLETE copy of repo (all history)
Developer C has FULL COMPLETE copy of repo (all history)

Benefits:
  Work offline completely
  Every developer has full backup
  Branching is instant (just a text file with a hash)
  GitHub is just one of many possible remotes
```

---

## 📁 Git Internals — The .git Folder

When you run `git init`, Git creates a `.git/` folder. This folder **IS** the repository. Delete it and all version history is gone (project files remain but Git tracking is erased).

```
.git/
├── HEAD                 ← "You are here" — points to current branch
├── config               ← Repo-specific settings (remote URL, user, etc.)
├── description          ← Used by GitWeb (ignore for normal use)
├── index                ← The staging area (binary file)
│
├── objects/             ← The object database (all your data lives here)
│   ├── 2e/
│   │   └── abc123...    ← Blob / tree / commit / tag objects
│   ├── pack/            ← Packed objects (compressed for efficiency)
│   └── info/
│
├── refs/                ← Named pointers to commits
│   ├── heads/           ← Local branches
│   │   ├── main         ← Contains commit hash of tip of main
│   │   └── feature-x   ← Contains commit hash of tip of feature-x
│   ├── remotes/         ← Remote tracking branches
│   │   └── origin/
│   │       └── main     ← Where GitHub's main was last time you fetched
│   └── tags/            ← Version markers
│
└── logs/                ← History of where HEAD has pointed (used by reflog)
```

Read the HEAD file yourself:

```bash
cat .git/HEAD
# ref: refs/heads/main
```

Read a branch file:

```bash
cat .git/refs/heads/main
# e4c21f8a3b2d4c5e6f7a8b9c0d1e2f3a4b5c6d7e
```

A branch is literally a 41-byte text file containing one commit hash. That is why creating a branch in Git is instant.

---

### Git's Four Object Types

Git stores everything in `.git/objects/` as one of four types. Every object is identified by the SHA-1 hash of its content.

**1. Blob — stores file content**

```
A blob contains only the RAW CONTENT of a file.
It does NOT know the filename.
It does NOT know where it lives in the directory.

Two files with identical content = one blob shared between them.
```

```bash
# See the hash Git would use for any content
echo "Hello World" | git hash-object --stdin
# 557db03de997c86a4a028e1ebd3a1ceb225be238
```

---

**2. Tree — stores directory structure**

```
A tree is like a directory listing.
It maps: filename → blob hash + file permissions

Example tree object:
  100644 blob a9d12...  main.py
  100644 blob c8f72...  utils.py
  040000 tree b2e45...  src/
```

Trees contain other trees (subdirectories). The root tree for any commit represents the complete project structure.

---

**3. Commit — stores snapshot metadata**

```
A commit object contains:
  tree    e4c21...    ← Points to the root tree (snapshot)
  parent  a9d12...    ← Points to previous commit (can have 2 for merges)
  author  Adyaprana <adya@email.com> 1719567890 +0530
  committer Adyaprana <adya@email.com> 1719567890 +0530

  feat: add login functionality
```

A commit does NOT store the files directly. It points to a tree, which points to blobs.

---

**4. Tag — stores a named pointer to a commit**

```
tag object:
  object  e4c21...   ← The commit it marks
  type    commit
  tag     v1.0.0
  tagger  Adyaprana <adya@email.com>

  Release version 1.0.0 — First stable release
```

---

### Git as a Directed Acyclic Graph (DAG)

This is the most important mental model. Once you see this, Git makes complete sense.

```
Every commit is a node.
Every commit points backward to its parent(s).
Branch names are just labels (pointers) on nodes.
HEAD is a pointer to whichever label you're currently on.

         HEAD
          ↓
         main
          ↓
A ← B ← C ← D ← E
              ↑
           feature

After feature merges into main:

A ← B ← C ← D ← E ← M
              ↑       ↑
              └── F ──┘
              feature
```

"Directed" — edges go one way (child → parent).
"Acyclic" — no loops possible (a commit cannot be its own ancestor).
"Graph" — nodes connected by edges.

This structure is why branching is free, merging is logical, and history is immutable.

---

### The Three States of Every File

```
┌─────────────────────────────────────────────────────┐
│                  Working Directory                   │
│   Files you see and edit in your project folder.    │
│   Changes here are NOT tracked yet.                  │
│                                                     │
│   git add filename                                  │
└────────────────────┬────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────┐
│                   Staging Area                       │
│   Files ready to be included in the next commit.   │
│   Snapshot is prepared but not permanently saved.   │
│   Stored in .git/index                              │
│                                                     │
│   git commit -m "message"                          │
└────────────────────┬────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────┐
│              Local Repository (.git/)               │
│   Permanent snapshot stored in .git/objects/        │
│   Full history. All commits.                        │
│                                                     │
│   git push                                         │
└────────────────────┬────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────┐
│           Remote Repository (GitHub)                │
│   Stored on GitHub's servers.                       │
│   Accessible to all collaborators.                  │
└─────────────────────────────────────────────────────┘
```

---

### Plumbing vs. Porcelain Commands

Git has two layers of commands:

**Porcelain — the commands you use every day:**

```bash
git init      git clone     git add       git commit
git push      git pull      git fetch     git status
git log       git diff      git branch    git checkout
git merge     git rebase    git stash     git tag
```

These are user-friendly, high-level commands.

**Plumbing — the internal engine commands:**

```bash
git hash-object    # Compute and store an object
git cat-file       # Read an object from the database
git ls-files       # Show what's in the staging index
git write-tree     # Create a tree from the index
git commit-tree    # Create a commit from a tree
git update-ref     # Update a reference (branch pointer)
git rev-parse      # Parse and resolve commit identifiers
```

You almost never use plumbing commands directly. But knowing they exist explains exactly what each porcelain command is doing internally.

---

## 🔧 Core Commands — Deep Mechanics

### 1. `git init` — Creating a Repository

**What you type:**

```bash
mkdir my-project
cd my-project
git init -b main
# Initialized empty Git repository in /home/adya/my-project/.git/
```

**What happens inside `.git/`:**

```
Creates:
  .git/HEAD              ← Contains: ref: refs/heads/main
  .git/config            ← Repo config (branch name, remote URL later)
  .git/objects/          ← Empty object database
  .git/refs/heads/       ← Empty (no commits, no branches yet)
```

At this point, `main` branch does not technically exist yet — it will be created on the first commit.

```bash
# Always initialize with explicit branch name (modern practice)
git init -b main

# Or set default globally (run once)
git config --global init.defaultBranch main
```

---

### 2. `git add` — Staging Changes

**What you type:**

```bash
git add main.py       # Stage one file
git add .             # Stage everything in current directory
git add src/          # Stage entire directory
git add *.py          # Stage all Python files
```

**What happens internally:**

```
1. Git reads the file content
2. Computes SHA-1 hash of the content
3. Stores content as a blob in .git/objects/
4. Updates .git/index with:
   filename → blob_hash + file_mode + timestamp
```

The index (staging area) is now a snapshot ready to become a commit.

**Power variations:**

```bash
git add -p main.py        # Interactive — stage only parts of a file
git add -A                # Stage new + modified + deleted files
git add -u                # Stage only modified + deleted (not new files)
git diff --cached         # Review exactly what is staged
git restore --staged auth.py  # Unstage a file (keep changes in working dir)
```

The `-p` (patch) flag is extremely useful. Git shows you each changed chunk and asks whether to stage it:

```
Stage this hunk? [y,n,q,a,d,/,e,?]
y = yes, n = no, s = split smaller, e = edit manually
```

This lets you create clean, focused commits from messy work sessions.

---

### 3. `git commit -m` — Creating a Snapshot

**What you type:**

```bash
git commit -m "feat: add contact search by name and phone"
```

**What happens internally:**

```
1. Git reads the current state of .git/index (staging area)
2. Creates tree objects for all directories
3. Creates a root tree object pointing to all file blobs
4. Creates a commit object containing:
   - Pointer to root tree
   - Pointer to parent commit
   - Author info + timestamp
   - Your commit message
5. Updates .git/refs/heads/main to the new commit's hash
6. The staging area now matches the repository state
```

**Conventional Commits standard (used at professional companies):**

```
Format: <type>(<scope>): <short description>

Types:
  feat      → New feature added
  fix       → Bug fixed
  docs      → Documentation only
  style     → Formatting, no logic change
  refactor  → Code restructured (no new feature, no bug fix)
  test      → Adding or fixing tests
  chore     → Build tools, dependencies, config

Examples:
  feat(auth): add JWT refresh token endpoint
  fix(users): resolve null pointer in profile update
  docs(readme): add installation instructions
  refactor(db): move SQL queries to repository layer
  test(orders): add unit tests for payment validation
  chore(deps): upgrade FastAPI to 0.110.0
```

**Other commit commands:**

```bash
# Commit without message (opens editor)
git commit

# Amend last commit message (before pushing)
git commit --amend -m "Better message"

# Add forgotten file to last commit (before pushing)
git add forgotten.py
git commit --amend --no-edit

# Commit all tracked modified files (skip git add)
git commit -am "fix: quick typo fix"
```

---

### 4. `git status` & `git log` — Reading Repository State

**`git status` output explained:**

```bash
git status

# On branch main
# Your branch is up to date with 'origin/main'.
#
# Changes to be committed:        ← In staging area
#   new file:   auth.py
#   modified:   main.py
#
# Changes not staged for commit:  ← Modified, not yet added
#   modified:   utils.py
#
# Untracked files:                ← Git sees but is not tracking
#   config.py
#   __pycache__/
```

```bash
# Short status (great for quick check)
git status -s

# A  auth.py      (A = Added to staging)
# M  main.py      (first column = staging, second = working dir)
#  M utils.py     (space = not staged, M = modified in working dir)
# ?? config.py    (?? = Untracked)
```

**`git log` formatting flags:**

```bash
# Default (verbose)
git log

# One line per commit
git log --oneline
# e4c21f8 feat: add login functionality
# c8f720a Initial project setup

# With branch and tag decorations
git log --oneline --decorate
# e4c21f8 (HEAD -> main, origin/main) feat: add login

# Visual branch graph (very useful)
git log --oneline --graph --all
# * e4c21f8 (HEAD -> main) feat: add login
# | * d9e0f1a (feature-search) WIP: search in progress
# |/
# * c8f720a chore: initial project setup

# Full beautiful graph
git log --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit

# Filter by author
git log --author="Adyaprana"

# Filter by date
git log --since="1 week ago"
git log --after="2026-06-01"

# Search commit messages
git log --grep="login"

# Show last 5 commits
git log -5

# Show what files changed in each commit
git log --stat

# Show full diffs for each commit
git log -p
```

---

### 5. `git push`, `git pull`, `git clone` — Remote Workflows

**`git clone` — Download a complete repository:**

```bash
git clone https://github.com/Adyaprana/Backend-Developer-Journey.git

# What actually happens:
# 1. Creates Backend-Developer-Journey/ directory
# 2. Initializes .git/ inside it
# 3. Downloads ALL objects (every commit, branch, tag, ever)
# 4. Creates remote tracking refs (origin/main, origin/develop, etc.)
# 5. Sets remote "origin" = the URL you cloned from
# 6. Checks out the default branch (usually main)
```

```bash
# Clone into specific folder name
git clone URL my-folder

# Clone specific branch only (fast for large repos)
git clone -b develop URL

# Shallow clone — only the latest commit (fastest)
git clone --depth 1 URL
```

---

**`git push` — Upload commits to GitHub:**

```bash
# First push: -u sets upstream tracking
git push -u origin main

# After that, just:
git push

# What happens internally:
# 1. Git finds commits in local main not yet in remote main
# 2. Packages them as a pack file
# 3. Sends to GitHub
# 4. GitHub updates refs/heads/main to your latest commit
```

```bash
# Push all tags
git push origin --tags

# Push specific tag
git push origin v1.0.0

# Delete a remote branch
git push origin --delete feature-old

# Force push (DANGEROUS — overwrites remote history)
git push --force

# Safer force push — fails if remote has changed since you last fetched
git push --force-with-lease
```

**The golden rule of force push:**

```
NEVER force push to main or any shared branch.
Only force push to your own feature branch that nobody else is working on.
Force push rewrites history. If teammates based work on your old commits,
their repositories become incompatible with yours.
```

---

**`git fetch` vs `git pull` — This is Critical:**

```bash
# git fetch:
# Downloads all new objects and updates remote tracking refs
# Does NOT touch your local branch or working directory
# You can examine what changed before integrating

git fetch origin
git log HEAD..origin/main --oneline   # See what's new on remote
git diff HEAD origin/main             # See the actual diff
git merge origin/main                 # Decide to merge when ready

# git pull = git fetch + git merge (combined)
git pull origin main

# Pull with rebase instead of merge (keeps history linear)
git pull --rebase origin main
```

**Why professionals prefer `git fetch` over `git pull`:**

```
git pull is automatic and can create unwanted merge commits.
git fetch gives you visibility and control.
You see what changed, decide how to integrate, then merge on your terms.
```

---

### 6. Branching — `git branch`, `git checkout`, `git merge`

**Why branches exist:**

```
Without branches:
  All developers push to main simultaneously
  Constant conflicts
  Half-finished features go to production
  You can't experiment without breaking things

With branches:
  Developer A: feature/auth (separate line of development)
  Developer B: feature/payment (separate line)
  main: always working, always deployable
  Merge only when feature is complete and tested
```

**Branch commands:**

```bash
# List local branches
git branch

# List all branches (local + remote)
git branch -a

# Create a branch
git branch feature-search

# Switch to a branch (two ways)
git checkout feature-search     # Old way (still works)
git switch feature-search       # Modern way (Git 2.23+)

# Create AND switch in one command
git checkout -b feature-search  # Old way
git switch -c feature-search    # Modern way

# Rename current branch
git branch -m new-name

# Delete merged branch
git branch -d feature-search

# Force delete (unmerged)
git branch -D feature-search

# Push branch to GitHub
git push origin feature-search

# Delete remote branch
git push origin --delete feature-search
```

---

**Fast-Forward Merge (Linear History):**

Happens when the current branch has NOT moved since the feature branch was created.

```
Before merge:

main:           A ── B
                         \
feature-search:           C ── D ── E

Fast-forward possible:
main just moves its pointer forward to E.
No merge commit created.
History stays perfectly linear.
```

```bash
git checkout main
git merge feature-search
# Updating c8f720a..e4c21f8
# Fast-forward
#  search.py | 30 ++++++++++++++++++++++++++++++
```

---

**Three-Way Merge (Diverged Branches):**

Happens when both branches have new commits since they diverged.

```
Before merge:

main:     A ── B ── C ── D
                \
feature:         E ── F

main has commits C and D after the diverge point (B).
Feature has commits E and F.
Fast-forward impossible — both sides moved.
```

Git uses the **common ancestor (B)** as the base, compares B→D and B→F, and combines into a new merge commit M:

```
After merge:

main:  A ── B ── C ── D ── M
                \          ↑
feature:         E ── F ───┘
```

M has two parents: D and F.

```bash
git checkout main
git merge feature-search
# Merge made by the 'recursive' strategy.
#  search.py | 30 +++++++++++++
```

---

**Resolving Merge Conflicts:**

Conflicts occur when both branches changed the **same line** of the same file.

```python
# What you see in search.py after conflict:
def search_contacts(query):
<<<<<<< HEAD
    # main branch's version
    return [c for c in contacts if query in c["name"]]
=======
    # feature branch's version
    return [c for c in contacts if query.lower() in c["name"].lower()]
>>>>>>> feature-search
```

Reading the markers:

```
<<<<<<< HEAD        → Your current branch (main) starts here
=======             → Separator
>>>>>>> feature     → Incoming branch ends here
```

Fix it by deleting all markers and keeping what's correct:

```python
def search_contacts(query):
    # Use case-insensitive search (better UX)
    return [c for c in contacts if query.lower() in c["name"].lower()]
```

```bash
# After resolving all conflicts:
git add search.py
git commit -m "merge: combine search with case-insensitive matching"

# To abort and go back before the merge:
git merge --abort
```

---

## 💻 Code Examples & Practical Implementations

### Full Setup — Contact Book Project from Zero to GitHub

#### Step 1 — One-Time Git Configuration

```bash
# Run these once on any new machine
git config --global user.name "Adyaprana Pradhan"
git config --global user.email "your@email.com"
git config --global init.defaultBranch main
git config --global core.editor "nano"    # or: code --wait

# Verify
git config --list
```

---

#### Step 2 — Create Project Files

```bash
mkdir contact-book
cd contact-book
touch main.py contact.py storage.py README.md .gitignore
```

Add this to `.gitignore`:

```gitignore
# Virtual environments
venv/
.venv/
env/

# Environment variables — NEVER commit secrets
.env
*.env

# Python cache
__pycache__/
*.pyc
*.pyo

# Database files
*.db
*.sqlite3

# IDE files
.vscode/
.idea/
.DS_Store

# Distribution
dist/
build/
*.egg-info/

# Test coverage
.coverage
htmlcov/
.pytest_cache/
```

---

#### Step 3 — Initialize Git

```bash
git init -b main
git status
# Shows: Untracked files: main.py, contact.py, storage.py, etc.
```

---

#### Step 4 — Five Meaningful Commits

**Commit 1 — Project Foundation**

```python
# main.py
def main():
    print("=== Contact Book ===")
    print("Version 1.0.0")

if __name__ == "__main__":
    main()
```

```bash
git add .gitignore README.md main.py
git commit -m "chore: initialize contact book project with gitignore"
```

---

**Commit 2 — Contact Model**

```python
# contact.py
class Contact:
    def __init__(self, name: str, phone: str, email: str):
        self.name = name
        self.phone = phone
        self.email = email

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "phone": self.phone,
            "email": self.email
        }

    def __str__(self) -> str:
        return f"{self.name} | {self.phone} | {self.email}"

    def __repr__(self) -> str:
        return f"Contact(name={self.name!r}, phone={self.phone!r})"
```

```bash
git add contact.py
git commit -m "feat(model): add Contact class with name, phone, email and to_dict method"
```

---

**Commit 3 — JSON Storage Layer**

```python
# storage.py
import json
import os
from typing import List, Optional

FILENAME = "contacts.json"

def _load_contacts() -> List[dict]:
    if not os.path.exists(FILENAME):
        return []
    with open(FILENAME, "r") as f:
        return json.load(f)

def _save_contacts(contacts: List[dict]) -> None:
    with open(FILENAME, "w") as f:
        json.dump(contacts, f, indent=2)

def add_contact(contact_dict: dict) -> None:
    contacts = _load_contacts()
    contacts.append(contact_dict)
    _save_contacts(contacts)

def get_all_contacts() -> List[dict]:
    return _load_contacts()
```

```bash
git add storage.py
git commit -m "feat(storage): add JSON file persistence with load and save helpers"
```

---

**Commit 4 — Search and Delete**

```python
# Add to storage.py

def search_contacts(query: str) -> List[dict]:
    """Search by name, phone, or email (case-insensitive)."""
    query = query.lower()
    contacts = _load_contacts()
    return [
        c for c in contacts
        if query in c["name"].lower()
        or query in c["phone"]
        or query in c["email"].lower()
    ]

def delete_contact(name: str) -> bool:
    """Delete first contact matching name. Returns True if deleted."""
    contacts = _load_contacts()
    filtered = [c for c in contacts if c["name"].lower() != name.lower()]
    if len(filtered) < len(contacts):
        _save_contacts(filtered)
        return True
    return False
```

```bash
git add storage.py
git commit -m "feat(storage): add case-insensitive search and delete by name"
```

---

**Commit 5 — Complete CLI Interface**

```python
# main.py
from contact import Contact
from storage import add_contact, get_all_contacts, search_contacts, delete_contact

def main():
    print("=== Contact Book ===\n")
    while True:
        print("1. Add Contact")
        print("2. View All")
        print("3. Search")
        print("4. Delete")
        print("5. Exit")
        choice = input("\nChoice: ").strip()

        if choice == "1":
            name  = input("Name: ").strip()
            phone = input("Phone: ").strip()
            email = input("Email: ").strip()
            if not name or not phone:
                print("❌ Name and phone are required.")
                continue
            add_contact(Contact(name, phone, email).to_dict())
            print(f"✅ '{name}' saved.\n")

        elif choice == "2":
            contacts = get_all_contacts()
            if not contacts:
                print("No contacts yet.\n")
            else:
                for i, c in enumerate(contacts, 1):
                    print(f"  {i}. {c['name']} | {c['phone']} | {c['email']}")
                print()

        elif choice == "3":
            q = input("Search: ").strip()
            results = search_contacts(q)
            if results:
                for c in results:
                    print(f"  → {c['name']} | {c['phone']} | {c['email']}")
            else:
                print("No matches found.")
            print()

        elif choice == "4":
            name = input("Delete name: ").strip()
            if delete_contact(name):
                print(f"✅ '{name}' deleted.\n")
            else:
                print(f"❌ '{name}' not found.\n")

        elif choice == "5":
            print("Goodbye! 👋")
            break

if __name__ == "__main__":
    main()
```

```bash
git add main.py
git commit -m "feat(cli): add interactive menu with add/view/search/delete and input validation"
```

---

#### Step 5 — Create GitHub Repo and Push

```bash
# On GitHub:
# 1. Click "+" → "New repository"
# 2. Name: contact-book
# 3. Description: CLI contact manager in Python
# 4. Public
# 5. DO NOT check "Add a README" (you already have local files)
# 6. Click "Create repository"

# Back in terminal:
git remote add origin https://github.com/Adyaprana/contact-book.git
git remote -v
# origin  https://github.com/Adyaprana/contact-book.git (fetch)
# origin  https://github.com/Adyaprana/contact-book.git (push)

git push -u origin main

# Verify your 5 commits on GitHub
git log --oneline
# abc1234 (HEAD -> main, origin/main) feat(cli): add interactive menu
# def5678 feat(storage): add case-insensitive search and delete by name
# ghi9012 feat(storage): add JSON file persistence with load and save helpers
# jkl3456 feat(model): add Contact class with name, phone, email and to_dict
# mno7890 chore: initialize contact book project with gitignore
```

---

#### Step 6 — Feature Branch Workflow

```bash
# Create feature branch for a new "edit contact" feature
git switch -c feature/edit-contact

# Make changes to storage.py
# Add update_contact function
# Commit
git add storage.py
git commit -m "feat(storage): add update_contact function to edit existing entries"

# Push branch to GitHub
git push origin feature/edit-contact

# On GitHub: open a Pull Request from feature/edit-contact into main
# Review the diff, merge
# Or merge locally:
git switch main
git merge feature/edit-contact
git push

# Clean up
git branch -d feature/edit-contact
git push origin --delete feature/edit-contact
```

---

### README.md Template for Contact Book

````markdown
# Contact Book 📒

A command-line contact management application built with Python.

## Features

- ✅ Add contacts (name, phone, email)
- ✅ View all saved contacts
- ✅ Case-insensitive search by name, phone, or email
- ✅ Delete contacts by name
- ✅ Persistent JSON storage

## Tech Stack

- Python 3.10+
- JSON file storage
- No external dependencies

## Installation

```bash
git clone https://github.com/Adyaprana/contact-book.git
cd contact-book
python main.py
```

## Project Structure

```
contact-book/
├── main.py        → Entry point and CLI interface
├── contact.py     → Contact model class
├── storage.py     → JSON storage operations
├── .gitignore     → Files excluded from tracking
└── README.md      → This file
```

## Author

**Adyaprana Pradhan**
GitHub: [@Adyaprana](https://github.com/Adyaprana)
LinkedIn: [adyaprana21](https://linkedin.com/in/adyaprana21)
````

---

## 🚀 Beyond the Basics: What You Must Also Know

### Git Reset — Undoing Commits

```bash
# Undo last commit, keep changes staged
git reset --soft HEAD~1

# Undo last commit, keep changes unstaged (files intact)
git reset --mixed HEAD~1

# Undo last commit AND DELETE the changes (DANGEROUS)
git reset --hard HEAD~1

# Reset to a specific commit
git reset --hard abc1234
```

**Visual of the three modes:**

```
Starting state:  [commits: A B C]  staging: empty  files: clean

After --soft HEAD~1:
  commits: A B    staging: C's changes staged    files: unchanged

After --mixed HEAD~1:
  commits: A B    staging: empty                 files: C's changes kept

After --hard HEAD~1:
  commits: A B    staging: empty                 files: C's changes GONE
```

**Rule:** Only use `--hard` on commits you have NOT pushed. If you reset pushed commits, use `git revert` instead.

---

### Git Revert — Safe Undo for Pushed Commits

```bash
# Creates a new commit that undoes a previous commit
# History is preserved — nothing is deleted
git revert abc1234

# Revert last 3 commits
git revert HEAD~3..HEAD

# Revert without auto-commit (review first)
git revert --no-commit abc1234
```

**When to use reset vs. revert:**

```
git reset  → Unpushed local commits. Cleaning up before push.
git revert → Already pushed commits. Safe for shared branches.
             Creates an audit trail: "we intentionally undid X."
```

---

### Git Stash — Save Work Without Committing

```bash
# Scenario: Boss says "fix this bug NOW" but you're mid-feature
git stash                                      # Save all changes
git stash push -m "Half-done search feature"   # With name
git stash push --include-untracked             # Include new files too

# See all stashes (it's a stack)
git stash list
# stash@{0}: WIP on feature-search: Half-done search
# stash@{1}: WIP on main: quick experiment

# Restore and remove top stash
git stash pop

# Restore specific stash
git stash pop stash@{1}

# Restore without removing (keep in list)
git stash apply

# Show stash contents
git stash show -p

# Delete specific stash
git stash drop stash@{0}

# Delete ALL stashes
git stash clear

# Create a branch from a stash
git stash branch fix-branch stash@{0}
```

---

### Rebase vs. Merge — The Golden Rules

**What rebase does:**

Rebase moves your branch's commits to start from a new base commit. It replays each commit one by one on top of the new base.

```
Before rebase:

main:     A ── B ── C ── D
                \
feature:         E ── F

After: git checkout feature && git rebase main

main:     A ── B ── C ── D
                              \
feature:                       E' ── F'

E' and F' are NEW commits (new hashes) with same changes.
```

**Merge vs. Rebase comparison:**

```
git merge feature:
  → Creates a merge commit M
  → Preserves exact history ("this is when the merge happened")
  → Good for: public branches, auditing, pull requests

git rebase main (then merge):
  → Rewrites history as if you always branched from latest main
  → Creates linear, clean history
  → Good for: local feature branches, keeping history readable
```

**The Golden Rule of Rebase:**

```
NEVER rebase commits that have been pushed to a shared branch.

Rebase rewrites commit hashes.
If teammates have built work on your original commit hashes,
their history becomes incompatible with your rewritten history.
This causes confusion and data loss risk.

Safe to rebase:
  ✅ Your local feature branch (not yet pushed)
  ✅ A feature branch only YOU are working on

Never rebase:
  ❌ main
  ❌ develop
  ❌ Any branch shared with teammates
```

---

### Interactive Rebase — Cleaning Up Before Pushing

```bash
# Clean up last 4 commits before pushing
git rebase -i HEAD~4

# Editor opens showing:
# pick abc1234 WIP
# pick def5678 fix typo
# pick ghi9012 more work
# pick jkl3456 WIP again

# Edit to:
# pick abc1234 WIP             ← Keep first commit
# squash def5678 fix typo      ← Combine into previous
# squash ghi9012 more work     ← Combine into previous
# reword jkl3456 WIP again     ← Keep but edit message
```

**Interactive rebase commands:**

```
pick    → Keep commit as-is
reword  → Keep commit, change message
edit    → Pause here to amend files
squash  → Combine into previous commit (keep both messages)
fixup   → Combine into previous commit (discard this message)
drop    → Delete this commit entirely
```

---

### Git Tags — Semantic Versioning

Tags mark specific commits as releases. They never move (unlike branches).

```bash
# Lightweight tag (just a pointer, no metadata)
git tag v1.0.0

# Annotated tag (recommended — has message, author, date)
git tag -a v1.0.0 -m "First stable release — all CRUD operations working"

# Tag a specific past commit
git tag -a v0.9.0 abc1234 -m "Beta release"

# List all tags
git tag
git tag -l "v1.*"

# Show tag details
git show v1.0.0

# Push to GitHub
git push origin v1.0.0
git push origin --tags     # Push all at once

# Delete tag
git tag -d v1.0.0
git push origin --delete v1.0.0
```

**Semantic Versioning format: `MAJOR.MINOR.PATCH`**

```
MAJOR → Breaking change (v1.0.0 → v2.0.0)
        Old clients must update
        e.g., Changed response format, removed endpoint

MINOR → New feature, backward-compatible (v1.0.0 → v1.1.0)
        Old clients still work
        e.g., Added search endpoint

PATCH → Bug fix (v1.0.0 → v1.0.1)
        No new features, just fixes
        e.g., Fixed null pointer in search

Examples:
  v1.0.0  → First stable release
  v1.0.1  → Fixed crash when contacts.json is empty
  v1.1.0  → Added email validation on contact creation
  v2.0.0  → Changed storage format (breaking change)
```

---

### Visualizing Git as a DAG

```bash
# Best command for visualizing Git history
git log --oneline --graph --all --decorate

# Example output for a real project:
# * e4c21f8 (HEAD -> main, origin/main) feat(cli): add interactive menu
# * d9e0f1a feat(storage): add search and delete
# | * f1a2b3c (feature/export) WIP: CSV export
# |/
# * c8f720a feat(storage): add JSON persistence
# * b4d5e6f feat(model): add Contact class
# * a1b2c3d chore: initialize project
```

Each `*` is a commit node. Lines show parent relationships. Branch labels are just pointers on nodes.

---

### Git Hooks — Automated Quality Gates

Hooks are scripts in `.git/hooks/` that run at specific Git events.

```bash
ls .git/hooks/
# pre-commit.sample
# commit-msg.sample
# pre-push.sample
# post-commit.sample
# post-merge.sample
```

**Create a pre-commit hook that blocks bad code:**

```bash
# Create hook file (remove .sample)
touch .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

```bash
#!/bin/bash
# .git/hooks/pre-commit

echo "🔍 Running pre-commit checks..."

# 1. Check Python syntax on all staged .py files
STAGED_PY=$(git diff --cached --name-only --diff-filter=ACM | grep '\.py$')
for file in $STAGED_PY; do
    python -m py_compile "$file"
    if [ $? -ne 0 ]; then
        echo "❌ Syntax error in $file. Commit blocked."
        exit 1
    fi
done

# 2. Block committing .env files
if git diff --cached --name-only | grep -q "\.env$"; then
    echo "❌ Attempting to commit .env file! Commit blocked."
    exit 1
fi

echo "✅ All checks passed."
exit 0
```

Now every `git commit` runs these checks automatically.

---

**Commit message hook (enforce conventional commits):**

```bash
#!/bin/bash
# .git/hooks/commit-msg

MSG=$(cat "$1")
PATTERN="^(feat|fix|docs|style|refactor|test|chore)(\(.+\))?: .{1,72}$"

if ! echo "$MSG" | grep -qE "$PATTERN"; then
    echo "❌ Commit message format invalid."
    echo "   Required: type(scope): description"
    echo "   Example:  feat(auth): add JWT login endpoint"
    exit 1
fi
exit 0
```

**Sharing hooks with your team:**

```bash
mkdir .githooks
# Move your hook scripts here
git config core.hooksPath .githooks
# Now commit .githooks/ to the repo
# Every team member gets the same hooks automatically
```

---

### Cherry-pick — Apply Specific Commits

```bash
# Scenario: feature branch has a bug fix you need in main NOW
# but the feature itself is not ready to merge

git log --oneline feature-payment
# abc1234 Fix: null pointer in payment validation  ← just this fix
# def5678 WIP: half-finished payment form
# ghi9012 WIP: payment gateway integration

# Apply only the bug fix to main
git checkout main
git cherry-pick abc1234
# Creates a NEW commit on main with the same changes
```

```bash
# Cherry-pick a range
git cherry-pick abc1234..ghi9012

# Cherry-pick without committing (just stage the changes)
git cherry-pick --no-commit abc1234
```

---

### Git Bisect — Find the Commit That Broke Everything

```bash
# Scenario: A bug exists somewhere in the last 50 commits

git bisect start

# Mark current state as broken
git bisect bad

# Mark a known good commit
git bisect good v1.0.0

# Git checks out the middle commit
# You test it:
python main.py   # Does the bug exist?

git bisect good   # Bug not here → Git moves later
# or
git bisect bad    # Bug is here → Git moves earlier

# After ~6 iterations Git says:
# "abc1234 is the first bad commit"

git bisect reset   # Return to original state
```

Binary search on 50 commits: only 6 tests needed instead of 50.

---

## 💼 Elite Technical Interview Questions & Comprehensive Answers

### Q1. What is the fundamental difference between Git and SVN? How does Git's snapshot-based architecture work under the hood?

Git and SVN represent two fundamentally different philosophies in version control.

SVN (Subversion) is a **centralized** system. All history lives on one central server. Developers check out working copies, not complete repositories. Every meaningful operation — creating a branch, viewing history, committing — requires a network round-trip to the central server. If the server is unavailable, the team is blocked.

SVN stores history as **changesets** (deltas): a series of diffs applied on top of a base version. To reconstruct file version 50, SVN applies 49 diffs sequentially. This makes historical reconstruction slower as history grows.

Git is a **distributed** system. Every clone is a complete repository with full history. Every developer has a perfect local backup. You can commit, branch, view history, and merge entirely offline. The "remote" on GitHub is just another peer, not a privileged central authority.

Git stores history as **snapshots**, not diffs. Each commit points to a tree object representing the complete state of the project at that moment. If a file is unchanged between commits, Git stores a pointer to the same blob rather than duplicating it, making storage efficient despite the snapshot model.

Under the hood, Git's object database stores four types of immutable content-addressed objects identified by SHA-1 hashes: blobs (file contents), trees (directory structures), commits (snapshot metadata + parent pointers), and tags (named commit pointers). This structure forms a Directed Acyclic Graph where each commit node points to its parent(s), making branching free (just a 41-byte pointer file) and merging logical (find common ancestor, compare both sides).

---

### Q2. What is the exact difference between `git fetch` and `git pull`? When would a fast-forward merge fail?

`git fetch origin` downloads all new objects (commits, trees, blobs, tags) from the remote and updates the **remote tracking references** (`origin/main`, `origin/develop`, etc.) to reflect the remote's current state. It does NOT touch your local branches or working directory. Your local `main` is completely unchanged.

`git pull` is syntactic sugar for `git fetch` followed immediately by `git merge` (or `git rebase` with `--rebase`). It downloads remote changes and automatically integrates them into your current branch.

**Why professionals prefer `git fetch` over `git pull`:**

`git fetch` gives you visibility before integration. You can run `git log HEAD..origin/main --oneline` to see exactly what changed remotely, and `git diff HEAD origin/main` to review the actual code differences. Then you decide consciously how to integrate. `git pull` integrates blindly and can create unexpected merge commits.

**When fast-forward merge fails:**

A fast-forward merge moves the current branch pointer forward to the tip of the incoming branch. It is only possible when the current branch is a direct ancestor of the incoming branch — meaning no new commits have been made on the current branch since it diverged.

Fast-forward fails when both branches have new commits since their diverge point. If main has commits C and D, and the feature branch has commits E and F, both added after their common ancestor B, Git cannot simply move main's pointer forward. It must perform a three-way merge using ancestor B as the base, comparing B→D (main's changes) with B→F (feature's changes), and creating a new merge commit M with two parents.

Conflict resolution: when both branches modify the same line, Git writes conflict markers into the file. You resolve by editing the file to keep the correct version, removing all markers, then running `git add` on the resolved file and `git commit` to complete the merge.

---

### Q3. How does Git track file renames and deletions if it doesn't store explicit rename metadata?

Git does NOT store explicit rename metadata anywhere in its object database. This surprises many developers.

Git stores only blobs (file content), trees (filename-to-blob mappings), and commits (tree pointers). When you rename `contact.py` to `models/contact.py`:

- The blob object is identical — same SHA-1 hash, same content
- The old tree has `contact.py → blob_hash`
- The new tree has `models/contact.py → blob_hash`

Git detects the rename **at diff time** through a similarity detection algorithm. When comparing two trees, if a blob disappears from one filename and appears at another filename, Git heuristically concludes it was renamed. The similarity threshold defaults to 50% (configurable via `-M` flag).

Practical consequence:

```bash
git log contact.py
# History stops before the rename

git log --follow models/contact.py
# --follow tells git log to trace through renames
# Shows complete history including commits before the rename
```

Deletions work similarly — a blob present in one tree but absent in the next tree is a deletion. Git never needs to explicitly record "this file was deleted" because the absence of the filename in the next tree snapshot is itself the record.

This architecture makes the object database simpler and storage more efficient. Renamed files with unchanged content cost zero additional storage.

---

### Q4. What is the detached HEAD state? How does it happen, how do you fix it, and how can you use it safely?

Normally, HEAD is a **symbolic reference** pointing to a branch name, which in turn points to a commit:

```bash
cat .git/HEAD
# ref: refs/heads/main
```

When you commit, HEAD stays on the branch, and the branch pointer moves forward with the new commit.

Detached HEAD means HEAD points **directly to a commit hash** instead of to a branch name:

```bash
cat .git/HEAD
# e4c21f8a3b2d4c5e6f7a8b9c0d1e2f3a4b5c6d7e
```

**How it happens:**

```bash
git checkout abc1234         # Checkout a specific commit
git checkout v1.0.0          # Checkout a tag
git checkout origin/main     # Checkout a remote tracking branch
```

**The danger:**

If you make new commits in detached HEAD state, those commits are not reachable from any branch. When you switch away, they become orphaned. Git's garbage collector will eventually delete them (after 90 days by default).

**How to fix it:**

```bash
# If you just looked around (no new commits):
git switch main     # Simply return to a branch

# If you made commits you want to keep:
git switch -c save-my-work    # Create a branch at current position
# Now your commits are safely on a branch

# Or cherry-pick the commits onto main:
git log --oneline             # Note the hashes
git switch main
git cherry-pick abc1234 def5678
```

**Safe use of detached HEAD:**

```bash
# Inspect old code without any risk
git checkout v1.0.0

# Browse code, run it, compare behavior
# Do NOT make commits here

# Return cleanly
git switch main
```

---

### Q5. What is `git reflog` and how does it save you from disaster?

`git reflog` records every position HEAD has pointed to, including commits that no longer exist in the main graph because of resets, rebases, or dropped commits.

```bash
git reflog

# abc1234 HEAD@{0}: commit: feat: add search
# def5678 HEAD@{1}: reset: moving to HEAD~1  ← you reset here
# ghi9012 HEAD@{2}: commit: feat: add delete  ← this commit is "gone"
# jkl3456 HEAD@{3}: commit: feat: add storage
```

If you accidentally ran `git reset --hard HEAD~3` and lost three commits:

```bash
# Reflog still shows those commit hashes
git reset --hard ghi9012   # Restore to that commit
```

Reflog entries expire after 90 days by default. Before that window, nothing is truly lost unless the objects are garbage collected.

---

### Q6. What is the difference between `git merge`, `git rebase`, and `git squash merge`? When should you use each?

**git merge:**

Creates a merge commit (a commit with two parents). Preserves the exact history of when branches diverged and were integrated. The history graph is non-linear but accurately reflects what happened. Best for: integrating long-running branches, PR merges, any situation where audit trail matters.

**git rebase:**

Replays commits from your branch on top of another branch's tip, creating new commit objects (same changes, new hashes, new parent). Results in linear history as if you had always branched from the latest point. Best for: updating a local feature branch with main's latest changes before pushing. Forbidden on shared branches.

**git squash merge:**

Takes all commits from a feature branch and combines them into a single new commit on the target branch. The feature branch's individual commits are not preserved in the target branch's history.

```bash
git merge --squash feature-search
git commit -m "feat: add contact search (squashed)"
```

Best for: small features or bug fixes where the individual work-in-progress commits add noise rather than value. The PR diff is preserved but the commit-by-commit WIP history is not.

**Summary:**

```
Merge       → Non-linear. Full history preserved. Use for PRs.
Rebase      → Linear. Rewrites local history. Use on local branches only.
Squash      → Linear. Collapses feature to one commit. Use for small features.
```

---

### Q7. How does Git handle large repositories efficiently?

When a repository grows, Git employs several efficiency mechanisms:

**Pack files:**

Instead of storing each object as a separate loose file in `.git/objects/`, Git periodically packs objects together using delta compression. Similar objects (e.g., two versions of the same large file) are stored as a base + delta, dramatically reducing disk space.

```bash
git gc                 # Manually trigger garbage collection and packing
git count-objects -v   # See how many loose objects exist
```

**Shallow clones:**

```bash
git clone --depth 1 URL
# Downloads only the latest commit's tree and blobs
# No history beyond that
# Much faster for CI/CD pipelines
```

**Git LFS (Large File Storage):**

For large binary files (images, videos, ML model weights), regular Git is inefficient. Git LFS replaces large files in the repository with pointer files, storing the actual content on a separate LFS server.

```bash
git lfs install
git lfs track "*.psd"      # Track Photoshop files
git lfs track "*.mp4"      # Track videos
git add .gitattributes
```

**Sparse checkout:**

Clone a large monorepo but only checkout the subdirectory you need:

```bash
git clone --no-checkout URL
git sparse-checkout init --cone
git sparse-checkout set backend/     # Only checkout the backend folder
git checkout main
```

---

### Q8. Explain Pull Requests — what are they technically and what best practices make them effective?

A Pull Request (PR) is a GitHub/GitLab/Bitbucket feature built on top of Git. It is a formal request to merge commits from one branch into another, with a code review interface.

Technically, a PR is metadata stored on the hosting platform — not a Git concept. It references two branch pointers and provides a UI for comparing the diff, leaving comments, running automated checks, and approving or requesting changes.

**The professional PR workflow:**

```
1. Create feature branch from main
2. Implement feature in small, focused commits
3. Push branch to GitHub
4. Open PR: title, description explaining WHY (not what)
5. Automated CI runs: tests, linting, security scans
6. Teammates review the diff line by line
7. Review can: Approve / Request Changes / Comment
8. Author addresses feedback (new commits are added to the PR)
9. Once approved and all checks pass: merge
10. Branch is deleted
11. Deployment triggered (if CD is configured)
```

**PR best practices:**

```
→ Keep PRs small (under 400 lines diff — easier to review)
→ One PR = one logical change (don't mix features)
→ Write description: what changed, why, how to test it
→ Reference issues: "Fixes #42" auto-closes the issue on merge
→ Make all CI checks pass before requesting review
→ Review your own diff before requesting others
→ Use Draft PRs for WIP (Work in Progress) — shows team you're working on it
→ Don't merge your own PR (get someone else to approve)
→ Delete the branch after merging
→ Respond to all review comments even if just "acknowledged, fixed in abc1234"
```

---

### Q9. What is git bisect and how does binary search help find bugs?

`git bisect` automates binary search across commit history to find the exact commit that introduced a bug.

Scenario: Your app has a bug. It worked 50 commits ago. Checking each of 50 commits manually would take hours.

Binary search: check the middle commit (25). If the bug exists there, search the first half (1-25). If not, search the second half (26-50). Each test halves the remaining range. 50 commits = 6 tests maximum.

```bash
git bisect start

# Current state is broken
git bisect bad

# This old commit is known to work
git bisect good v1.0.0

# Git checks out commit in the middle
# You test:
python -m pytest tests/
# or manually verify

git bisect good    # Bug not here → Git moves to later half
# OR
git bisect bad     # Bug here → Git moves to earlier half

# After ~6 rounds:
# "abc1234 is the first bad commit"
# Git shows you the commit: who, when, what changed

git bisect reset   # Return to original HEAD
```

**Automated bisect:**

```bash
# Provide a test script — Git runs it automatically on each commit
git bisect run python -m pytest tests/test_search.py -q

# Git automatically bisects without your input
# Exits when it finds the first bad commit
```

---

### Q10. What happens during `git push` if remote has changes you don't have?

```bash
git push origin main
# error: failed to push some refs to 'https://github.com/...'
# hint: Updates were rejected because the remote contains work
# hint: that you do not have locally. Integrate the remote changes
# hint: before pushing again.
```

This happens because your local `main` and `origin/main` have diverged. Your push would create a non-linear, ambiguous history on the remote.

Git refuses to accept a push that would require a force push to apply.

**Solution:**

```bash
# Option 1: Merge (creates merge commit)
git fetch origin
git merge origin/main
git push

# Option 2: Rebase (creates linear history)
git fetch origin
git rebase origin/main
git push

# Option 3: Pull with rebase (same as option 2 in one command)
git pull --rebase origin main
git push
```

**Why does this happen in a team?**

Two developers both branch from commit B. Developer A pushes commit C. Developer B also made commit D from B. When B tries to push D, the remote is at C (not B), so the push is rejected. Developer B must integrate C first, then push.

This is the correct behavior — it prevents silent history divergence and forces explicit integration decisions.

---

## 📋 Common Mistakes to Avoid

```
1. Committing .env files with secrets
   Fix: Add .env to .gitignore BEFORE your first commit
   If it slipped: git rm --cached .env, rotate the secret immediately

2. Vague commit messages: "update", "fix", "changes", "asdf"
   Fix: feat(scope): describe what changed and why

3. One giant commit at end of day
   Fix: Small, atomic commits as you complete each piece of work

4. Working directly on main
   Fix: One branch per feature. main is always deployable.

5. Force pushing to shared branches
   Fix: Never force push to main. Only use --force-with-lease on your own feature branches.

6. Not pulling before pushing
   Fix: Always git fetch + check before pushing

7. Committing large binaries (images, videos, models)
   Fix: Use Git LFS for files over a few MB

8. Deleting a branch before merging
   Fix: git branch -d (lowercase) is safe — fails if unmerged

9. Never using git diff before committing
   Fix: git diff --cached shows you exactly what's staged before committing

10. Not using .gitignore from day one
    Fix: Add gitignore before the first commit or it becomes messy to fix later
```

---

## 📋 Day 24 Assignments

✅ Configure Git globally with your name and email

✅ Create the Contact Book project with the exact 5 commits shown above

✅ Push it to a new GitHub repository

✅ Create a `feature/edit-contact` branch, add a feature, merge it back to main

✅ Write a proper `.gitignore` for Python projects

✅ Write a `README.md` with installation instructions

✅ Run `git log --oneline --graph --all` and understand the output

✅ Intentionally create a merge conflict, resolve it, commit the resolution

✅ Practice `git stash` — stash, switch branch, pop back

✅ Create a `git tag -a v1.0.0` with a message for your first working version

✅ Set up a `pre-commit` hook that checks Python syntax

✅ Open `.git/HEAD` and a `.git/refs/heads/main` and read the raw content

---

## 📋 Day 24 Backend Developer Checkpoint

If you can explain without notes:

**Core Concepts:**
✅ Git vs GitHub — the actual difference
✅ Why distributed beats centralized VCS
✅ The three states of a file (working, staging, repository)
✅ The four Git object types (blob, tree, commit, tag)
✅ What the `.git` folder contains
✅ Git as a Directed Acyclic Graph (DAG)

**Core Commands:**
✅ git init — what it creates in `.git/`
✅ git add — blob creation and index update
✅ git commit — commit object structure
✅ git status — all three sections of the output
✅ git log — --oneline, --graph, --all, --decorate
✅ git fetch vs git pull — the critical difference
✅ git push — what happens when it's rejected

**Branching:**
✅ What a branch is internally (a text file with one hash)
✅ What HEAD is and what detached HEAD means
✅ Fast-forward merge vs Three-way merge
✅ How to create, switch, merge, delete branches
✅ How to resolve a merge conflict step by step

**Advanced:**
✅ git reset --soft vs --mixed vs --hard
✅ git revert vs git reset (when to use each)
✅ git stash — push, pop, list, drop, clear
✅ Rebase vs Merge (the golden rule)
✅ Git Tags and Semantic Versioning
✅ Git Hooks (pre-commit, commit-msg)
✅ git bisect — binary search for bugs
✅ git cherry-pick — apply specific commits
✅ git reflog — the disaster recovery tool

**Workflow:**
✅ The 5-commit Contact Book project
✅ Pull Request workflow
✅ Conventional Commits format
✅ GitFlow vs GitHub Flow

---

Tomorrow when you push code and open a Pull Request, you won't just be running commands.

You'll know:

```
Every commit is an immutable DAG node in .git/objects/
Every branch is a 41-byte pointer file in .git/refs/heads/
Every push packages new objects and sends them to GitHub
Fast-forward means your history is a clean straight line
Three-way merge means both sides diverged and Git found the common ancestor
A PR is a request to integrate your DAG node into the shared graph
The .git/ folder IS the repository — everything else is a working copy
```

**That's the difference between a developer who uses Git and one who understands Git.**

---

## 🎥 Recommended Learning Video

> **✅ Kunal Kushwaha: Git & GitHub in 1 video (Hindi/English) ⭐**
>
> The single best Git tutorial for absolute beginners.
> Kunal explains every concept visually with live demos.
> Available in Hindi and English.
>
> Watch the video first for the visual intuition.
> Then come back and re-read this file.
> The second reading will make 10x more sense because
> you'll map every concept here to what you saw on screen.

---

*Day 24 Complete.* ✅