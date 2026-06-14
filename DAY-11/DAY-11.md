# 🚀 Day 11 — File I/O, CSV, JSON & Data Persistence

> Week 2 • Day 11
>
> Goal: Learn how programs store data permanently, work with text files, CSV files, JSON files, understand file systems, context managers, serialization, and how real backend applications save and retrieve information.

---

# 🎯 Why Day 11 Is A Major Milestone

Until Day 10:

```text
Variables
Lists
Dictionaries
Functions
```

All data lived in:

```text
RAM (Memory)
```

Problem:

```python
name = "Adyaprana"
```

Program closes.

Data disappears.

❌ Lost forever.

---

# Day 11 Changes Everything

Now data can be stored in:

```text
Text Files
CSV Files
JSON Files
```

and survive after program closes.

Example:

```text
student.json
```

Program closes.

File remains.

Program restart✅
Data still exists.

✅ Permanent Storage

This is called:

```text
Persistence
```

One of the most important concepts in software engineering.

---

# 🧠 Variables vs Files vs Database

Many beginners don't understand this relationship.

---

# Variable

```python
name = "Adyaprana"
```

Stored in RAM.

Temporary.

Fast.

Lost after program exits.

---

# File

```text
student.txt
```

Stored on disk.

Permanent.

Slower.

Simple.

---

# Database

```text
PostgreSQL
MySQL
MongoDB
```

Permanent.

Organized.

Searchable.

Scalable.

---

# Backend Architecture

```text
Variables
↓
Files
↓
Databases
```

Day 11 is your bridge between variables and databases.

---

# 📌 What Is File I/O?

I/O means:

```text
Input / Output
```

Input:

```text
Read Data
```

Output:

```text
Write Data
```

File I/O means:

```text
Reading Files
Writing Files
```

Python provides built-in support through:

```python
open()
```

:contentReference[oaicite:0]{index=0}

---

# 📌 Understanding The File Lifecycle

Every file operation follows:

```text
Open
↓
Read/Write
↓
Close
```

Example:

```python
file = open("data.txt")

content = file.read()

file.close()
```

---

# Why Closing Matters

Imagine:

```text
1000 files opened
0 files closed
```

Eventually:

```text
Resource Leak
```

Application becomes unstable.

---

# Real Interview Question

## What Happens If You Forget close()?

Resources remain allocated.

In large applications this can cause:

- Memory issues
- File descriptor exhaustion
- Performance problems

---

# 📌 File Paths

Most beginners struggle here.

---

# Relative Path

```python
open("data.txt")
```

Python searches in current folder.

---

# Absolute Path

```python
open(
 "C:/Users/Adyaprana/data.txt"
)
```

Full location.

---

# Which Is Better?

Professional projects prefer:

```text
Relative Paths
```

because they work on multiple machines.

---

# 📌 File Modes (Deep Understanding)

---

## Read Mode

```python
open("data.txt","r")
```

Purpose:

```text
Read Existing File
```

File must exist.

---

## Write Mode

```python
open("data.txt","w")
```

Purpose:

```text
Overwrite File
```

Danger:

```text
Deletes Existing Content
```

---

## Append Mode

```python
open("data.txt","a")
```

Purpose:

```text
Add New Data
```

Safe.

Does not remove old data.

---

## Create Mode

```python
open("data.txt","x")
```

Creates file only if it doesn't exist.

Otherwise:

```text
FileExistsError
```

---

## Read + Write

```python
open("data.txt","r+")
```

Allows both.

Interview favorite.

---

# 🎤 Interview Question

## Difference Between w and a?

### w

```text
Overwrite Everything
```

---

### a

```text
Add New Data
Keep Old Data
```

This is one of the most common Python interview questions.

:contentReference[oaicite:1]{index=1}

---

# 📌 The File Pointer

Very important concept.

Every file has a cursor.

Example:

```text
HELLO WORLD
^
```

Position 0.

---

Read 5 characters:

```python
file.read(5)
```

Now:

```text
HELLO WORLD
     ^
```

Cursor moved.

---

# tell()

Returns current position.

```python
file.tell()
```

Example:

```python
file.read(5)

print(file.tell())
```

Output:

```text
5
```

---

# seek()

Moves cursor.

```python
file.seek(0)
```

Back to beginning.

Example:

```python
file.read(5)

file.seek(0)

file.read(5)
```

Reads same data again.

Very common in advanced interviews.

---

# 📌 Reading Large Files Efficiently

Most tutorials ignore this.

Bad:

```python
content = file.read()
```

Loads entire file.

Problem:

```text
5 GB File
```

Consumes huge memory.

---

Professional Approach

```python
for line in file:
    print(line)
```

Reads line-by-line.

Memory efficient.

---

# Chunk Reading

```python
chunk = file.read(1024)
```

Read:

```text
1024 bytes at a time
```

Used in:

- Video Processing
- Image Processing
- File Upload Systems

Corey Schafer's file handling tutorial highlights chunk-based reading for large files. :contentReference[oaicite:2]{index=2}

---

# 📌 Context Managers (with Statement)

One of the most important Python concepts.

Old Way:

```python
file = open("data.txt")

content = file.read()

file.close()
```

---

Modern Way:

```python
with open("data.txt") as file:

    content = file.read()
```

No close needed.

Python closes automatically.

---

# Why Use with?

Benefits:

✅ Cleaner

✅ Safer

✅ Automatic Cleanup

✅ Handles Exceptions

---

# Interview Question

## What Is A Context Manager?

A context manager automatically manages resources and guarantees cleanup when execution leaves the block.

Example:

```python
with open(...) as file:
```

is a context manager.

:contentReference[oaicite:3]{index=3}

---

# 📌 Encoding (Very Important)

Most beginners discover this only after errors.

Example:

```python
with open(
    "data.txt",
    encoding="utf-8"
)
```

Why?

Because:

```text
English
Hindi
Odia
Japanese
Emoji
```

all require proper encoding.

---

# Common Error

```text
UnicodeDecodeError
```

Often fixed using:

```python
encoding="utf-8"
```

---

# 📌 CSV Files

CSV:

```text
Comma Separated Values
```

Example:

```csv
Name,Age,City
Adyaprana,23,Bangalore
Rahul,22,Delhi
```

---

# Why CSV Exists

Excel uses CSV.

Business reports use CSV.

Analytics uses CSV.

Data Science uses CSV.

---

# Real World Examples

```text
Employee Records
Sales Reports
Student Data
Customer Lists
```

---

# csv.DictWriter()

Most beginners only learn csv.writer().

Professional code often uses:

```python
import csv

with open(
    "employees.csv",
    "w",
    newline=""
) as file:

    writer = csv.DictWriter(
        file,
        fieldnames=[
            "id",
            "name"
        ]
    )

    writer.writeheader()

    writer.writerow({
        "id":1,
        "name":"Adyaprana"
    })
```

Cleaner.

More readable.

---

# csv.DictReader()

```python
import csv

with open("employees.csv") as file:

    reader = csv.DictReader(file)

    for row in reader:
        print(row["name"])
```

Very common in industry.

---

# 📌 JSON (Most Important Topic Today)

JSON means:

```text
JavaScript Object Notation
```

JSON is the language of APIs.

Every backend developer works with JSON daily.

:contentReference[oaicite:4]{index=4}

---

# JSON Example

```json
{
  "id": 1,
  "name": "Adyaprana",
  "skills": [
      "Python",
      "SQL"
  ]
}
```

---

# Why JSON Won?

Because:

```text
Human Readable
Machine Readable
Language Independent
Lightweight
```

---

# Python Dictionary vs JSON

Python:

```python
{
 "name":"Adyaprana"
}
```

JSON:

```json
{
 "name":"Adyaprana"
}
```

Looks similar.

Not identical.

---

# Important Difference

Python:

```python
True
False
None
```

JSON:

```json
true
false
null
```

Interview favorite.

---

# 📌 Serialization

Advanced Concept.

Serialization means:

```text
Python Object
↓
JSON Text
```

Example:

```python
json.dumps(data)
```

---

# Deserialization

```text
JSON Text
↓
Python Object
```

Example:

```python
json.loads(text)
```

---

# dumps() vs dump()

Very Common Interview Question

---

# dump()

Writes JSON to file.

```python
json.dump(
    data,
    file
)
```

---

# dumps()

Returns JSON string.

```python
json.dumps(data)
```

Returns:

```python
'{"name":"Adyaprana"}'
```

---

# load() vs loads()

---

# load()

Reads JSON file.

```python
json.load(file)
```

---

# loads()

Reads JSON string.

```python
json.loads(text)
```

Extremely common interview question.

---

# 🧠 API Connection

Backend:

```python
return {
   "name":"Adyaprana"
}
```

---

FastAPI converts:

```python
Dictionary
```

into:

```json
{
 "name":"Adyaprana"
}
```

JSON Response.

This is exactly how modern APIs work.

---

# 📌 Binary Files

Most beginners only learn text files.

Important topic:

```text
Images
Videos
PDFs
Audio
```

are binary files.

---

Read Image:

```python
with open(
    "image.jpg",
    "rb"
) as file:

    data = file.read()
```

---

Write Image:

```python
with open(
    "copy.jpg",
    "wb"
) as file:

    file.write(data)
```

---

Modes:

```text
rb → Read Binary
wb → Write Binary
```

Very important interview topic.

Corey Schafer demonstrates binary file copying using rb/wb modes. :contentReference[oaicite:5]{index=5}

---

# 📌 Pickle (Bonus Concept)

Not in roadmap.

Good to know.

Python object:

```python
user = {
  "name":"Adya"
}
```

Save directly:

```python
import pickle

pickle.dump(user,file)
```

Load:

```python
pickle.load(file)
```

---

When To Use?

Python-only applications.

Not APIs.

JSON is usually preferred.

---

# 📌 Temporary Files

Used in:

```text
File Upload Systems
Image Processing
Report Generation
```

Python:

```python
import tempfile
```

Creates files that automatically disappear later.

Useful in backend systems.

---

# 🏗️ Project Idea 1

Inventory System

Store:

```json
[
  {
    "id":1,
    "name":"Laptop"
  }
]
```

Operations:

```text
Add Product
Delete Product
Search Product
Update Product
```

---

# 🏗️ Project Idea 2

Expense Tracker

Store expenses in:

```json
expenses.json
```

Generate:

```text
Monthly Reports
Category Totals
Statistics
```

---

# 🏗️ Project Idea 3

Log Management System

Store:

```text
User Actions
Login Events
Errors
```

in:

```text
app.log
```

Very backend oriented.

---

# 💼 Backend Connection

Every backend application uses:

```text
JSON
Files
Logs
CSV Exports
```

Examples:

```text
User Uploads
Profile Pictures
API Responses
Reports
Invoices
Backups
```

Day 11 is your first introduction to real-world data persistence.

---

# 🎤 Advanced Interview Questions

## Q1. Why is JSON preferred over XML?

JSON is smaller, easier to read, faster to parse, and maps naturally to programming language data structures.

---

## Q2. Difference Between dump() and dumps()?

dump()

Writes JSON to file.

dumps()

Returns JSON string.

---

## Q3. Difference Between load() and loads()?

load()

Reads JSON file.

loads()

Reads JSON string.

---

## Q4. Why use with instead of open() + close()?

with guarantees cleanup even if exceptions occur.

---

## Q5. What is serialization?

Converting an object into a storable/transmittable format.

Example:

```python
dict → JSON
```

---

## Q6. What is deserialization?

Converting stored/transmitted data back into objects.

Example:

```python
JSON → dict
```

---

## Q7. What is a file pointer?

Internal cursor that tracks current read/write position.

---

## Q8. Difference Between Text Files and Binary Files?

Text:

```text
Human Readable
```

Binary:

```text
Images
Videos
Audio
PDFs
```

Not human readable.

---

## Q9. Why are CSV files still used?

Because they are simple, lightweight, and supported by almost every analytics and spreadsheet tool.

---

## Q10. Which Day 11 topic is most important for backend developers?

Without question:

```text
JSON
Serialization
Context Managers
File Handling Basics
```

because APIs communicate using JSON.

---

# 🏆 Day 11 Success Checklist

- ✅ Learned File I/O
- ✅ Learned File Modes
- ✅ Learned File Paths
- ✅ Learned File Pointers
- ✅ Learned tell()
- ✅ Learned seek()
- ✅ Learned Context Managers
- ✅ Learned UTF-8 Encoding
- ✅ Learned CSV Files
- ✅ Learned DictReader
- ✅ Learned DictWriter
- ✅ Learned JSON
- ✅ Learned Serialization
- ✅ Learned Deserialization
- ✅ Learned Binary Files
- ✅ Learned Backend JSON Concepts

---

# 🎯 Day 11 Result

You can now store data permanently, read and write structured information, work with CSV reports, understand JSON APIs, manage files safely using context managers, and think beyond variables toward real-world data persistence.

This is a major backend milestone because:

```text
Backend Development
=
Receive Data
↓
Process Data
↓
Store Data
↓
Return Data
```

Day 11 teaches the "Store Data" part of software engineering.