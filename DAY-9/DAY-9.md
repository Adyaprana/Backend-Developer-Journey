# 🚀 Day 9 — Functional Python: Lambda, Map, Filter, Zip & Sorted

> Week 2 • Day 9
>
> Goal: Learn Functional Programming concepts used in modern Python, understand how data transformations work, and write cleaner, more professional code.

---

# 🎯 Why Day 9 Matters

Up until now you have learned:

```text
Variables
Conditions
Loops
Lists
Tuples
Dictionaries
Functions
```

Most beginners solve problems using:

```python
for item in data:
    ...
```

Professional Python developers often use:

```python
map()
filter()
zip()
sorted()
lambda
```

These tools allow you to process data faster, write less code, and think in terms of transformations rather than instructions. Functional programming tools are part of Python's built-in toolkit and are widely used for data processing and transformations. :contentReference[oaicite:0]{index=0}

---

# 🧠 What Is Functional Programming?

Traditional Programming:

```python
result = []

for n in numbers:
    result.append(n * 2)
```

Functional Programming:

```python
result = list(
    map(lambda x: x * 2, numbers)
)
```

Same output.

Less code.

More expressive.

---

# Traditional Thinking

```text
Take item
↓
Process item
↓
Store item
↓
Repeat
```

---

# Functional Thinking

```text
Transform Collection
```

Instead of focusing on each step, you focus on the result.

This becomes extremely useful when processing:

- API Responses
- Database Records
- CSV Files
- JSON Data
- Analytics Data

---

# 📌 Lambda Functions

Lambda means:

```text
Anonymous Function
```

Anonymous means:

```text
Function without a name
```

---

# Normal Function

```python
def square(x):
    return x * x
```

---

# Lambda Version

```python
square = lambda x: x * x
```

Output:

```python
print(square(5))
```

Result:

```text
25
```

---

# Lambda Syntax

```python
lambda parameters: expression
```

Structure:

```text
Input → Processing → Output
```

---

# Example 1

```python
add_ten = lambda x: x + 10

print(add_ten(5))
```

Output:

```text
15
```

---

# Example 2

```python
multiply = lambda x, y: x * y

print(multiply(4, 5))
```

Output:

```text
20
```

---

# Example 3

```python
is_even = lambda x: x % 2 == 0

print(is_even(8))
```

Output:

```text
True
```

---

# Example 4

```python
full_name = lambda first, last: f"{first} {last}"

print(
    full_name(
        "Adyaprana",
        "Pradhan"
    )
)
```

Output:

```text
Adyaprana Pradhan
```

---

# When Should You Use Lambda?

✅ Short Functions

✅ One-Time Use

✅ Sorting

✅ Mapping

✅ Filtering

---

# When NOT To Use Lambda?

❌ Complex Logic

❌ Multiple Conditions

❌ Large Functions

❌ Production Business Logic

---

# 🎤 Interview Question

## Why Was Lambda Introduced?

Lambda allows developers to create small throwaway functions without writing a full function definition.

It makes code shorter and is commonly used with:

```python
map()
filter()
sorted()
```

---

# 📌 map()

map() applies a function to every element.

Think:

```text
Input List
↓
Transform Each Item
↓
Output List
```

Python's map() applies a function to each item of an iterable and returns a map object. :contentReference[oaicite:1]{index=1}

---

# Without map()

```python
numbers = [1,2,3,4]

result = []

for n in numbers:
    result.append(n * 2)
```

---

# Using map()

```python
numbers = [1,2,3,4]

result = list(
    map(
        lambda x: x * 2,
        numbers
    )
)
```

Output:

```python
[2,4,6,8]
```

---

# Example: Square Numbers

```python
numbers = [1,2,3,4]

result = list(
    map(
        lambda x: x**2,
        numbers
    )
)
```

Output:

```python
[1,4,9,16]
```

---

# Example: Currency Conversion

```python
usd = [10,20,30]

inr = list(
    map(
        lambda x: x * 83,
        usd
    )
)
```

Output:

```python
[830,1660,2490]
```

---

# Example: Extract Emails

```python
users = [
    {"email":"a@gmail.com"},
    {"email":"b@gmail.com"}
]

emails = list(
    map(
        lambda u: u["email"],
        users
    )
)
```

Output:

```python
[
 'a@gmail.com',
 'b@gmail.com'
]
```

Very common backend operation.

---

# 📌 filter()

filter() removes unwanted data.

Think:

```text
Input Data
↓
Apply Condition
↓
Keep Matching Records
```

filter() returns only elements that satisfy a condition. :contentReference[oaicite:2]{index=2}

---

# Without filter()

```python
evens = []

for n in numbers:

    if n % 2 == 0:
        evens.append(n)
```

---

# Using filter()

```python
numbers = [1,2,3,4,5,6]

evens = list(
    filter(
        lambda x: x % 2 == 0,
        numbers
    )
)
```

Output:

```python
[2,4,6]
```

---

# Example: Filter Adults

```python
ages = [12,18,25,15,30]

adults = list(
    filter(
        lambda age: age >= 18,
        ages
    )
)
```

Output:

```python
[18,25,30]
```

---

# Example: Active Users

```python
users = [
    {"name":"A","active":True},
    {"name":"B","active":False},
    {"name":"C","active":True}
]

active_users = list(
    filter(
        lambda u: u["active"],
        users
    )
)
```

Very common API filtering logic.

---

# Difference Between map() and filter()

map():

```text
Transforms Data
```

Example:

```python
1 → 10
2 → 20
3 → 30
```

---

filter():

```text
Selects Data
```

Example:

```python
1 ❌
2 ✅
3 ❌
4 ✅
```

---

# 📌 zip()

zip() combines multiple iterables element-by-element into tuples. :contentReference[oaicite:3]{index=3}

Think:

```text
List A
List B
↓
Pair Together
```

---

# Example

```python
names = ["A","B","C"]

marks = [90,80,70]

print(
    list(zip(names, marks))
)
```

Output:

```python
[
 ('A',90),
 ('B',80),
 ('C',70)
]
```

---

# Real Life Example

```python
countries = [
    "India",
    "USA",
    "Japan"
]

capitals = [
    "Delhi",
    "Washington",
    "Tokyo"
]

result = dict(
    zip(
        countries,
        capitals
    )
)
```

Output:

```python
{
 "India":"Delhi",
 "USA":"Washington",
 "Japan":"Tokyo"
}
```

---

# Important Interview Question

## What Happens If Lengths Differ?

```python
a = [1,2,3]
b = [10]
```

```python
list(zip(a,b))
```

Output:

```python
[(1,10)]
```

zip stops at the shortest iterable. :contentReference[oaicite:4]{index=4}

---

# Advanced Zip Trick (Unzipping)

```python
pairs = [
    ("A",90),
    ("B",80)
]

names, marks = zip(*pairs)

print(names)
print(marks)
```

Output:

```python
('A','B')
(90,80)
```

Very common interview question.

---

# 📌 sorted()

sorted() returns a new sorted list.

Unlike:

```python
list.sort()
```

which modifies the original list.

---

# Example

```python
numbers = [5,2,8,1]

print(
    sorted(numbers)
)
```

Output:

```python
[1,2,5,8]
```

---

# Descending Sort

```python
sorted(
    numbers,
    reverse=True
)
```

Output:

```python
[8,5,2,1]
```

---

# Key Argument

Most important sorted() feature.

---

# Sort By Length

```python
words = [
    "python",
    "go",
    "javascript"
]

print(
    sorted(
        words,
        key=len
    )
)
```

Output:

```python
[
 'go',
 'python',
 'javascript'
]
```

---

# Sort By Last Character

```python
words = [
    "apple",
    "cat",
    "dog"
]

sorted(
    words,
    key=lambda x: x[-1]
)
```

Output:

```python
[
 'apple',
 'dog',
 'cat'
]
```

---

# Real Backend Example

Sort Users By Age

```python
users = [
  {"name":"A","age":30},
  {"name":"B","age":20},
  {"name":"C","age":25}
]

sorted_users = sorted(
    users,
    key=lambda u: u["age"]
)
```

Very common in APIs.

---

# 📌 map() vs List Comprehension

Map:

```python
list(
    map(
        lambda x:x*x,
        numbers
    )
)
```

---

List Comprehension:

```python
[
 x*x
 for x in numbers
]
```

Many Python developers prefer comprehensions because they are often more readable. :contentReference[oaicite:5]{index=5}

---

# Filter vs List Comprehension

Filter:

```python
list(
 filter(
   lambda x:x>10,
   numbers
 )
)
```

---

Comprehension:

```python
[
 x
 for x in numbers
 if x > 10
]
```

---

# 🚀 New Concept: reduce()

Not in roadmap but important.

Python:

```python
from functools import reduce
```

---

# Example

```python
from functools import reduce

numbers = [1,2,3,4]

result = reduce(
    lambda a,b:a+b,
    numbers
)
```

Output:

```text
10
```

Think:

```text
1+2+3+4
```

reduce() is frequently asked in interviews. :contentReference[oaicite:6]{index=6}

---

# 🚀 New Concept: any()

Returns True if ANY value is True.

```python
numbers = [False, False, True]

print(any(numbers))
```

Output:

```text
True
```

---

# 🚀 New Concept: all()

Returns True if ALL values are True.

```python
numbers = [True, True, True]

print(all(numbers))
```

Output:

```text
True
```

Very useful in validation systems.

---

# 🏗️ Project 1 — Student Ranking System

Tasks:

- Add grace marks using map()
- Remove failed students using filter()
- Sort by marks using sorted()
- Combine names and marks using zip()

This combines everything learned today.

---

# 🏗️ Project 2 — Product Catalog Processor

```python
products = [
 {"name":"Laptop","price":50000},
 {"name":"Mouse","price":500}
]
```

Tasks:

- Filter expensive products
- Sort by price
- Extract names
- Create report

Very backend-oriented practice.

---

# 💼 Backend Connection

API Response:

```python
users = response.json()
```

Extract names:

```python
map(...)
```

Filter active users:

```python
filter(...)
```

Sort leaderboard:

```python
sorted(...)
```

Combine IDs and Names:

```python
zip(...)
```

These concepts appear frequently in data pipelines, APIs, analytics workflows, and backend services. :contentReference[oaicite:7]{index=7}

---

# 🎤 Advanced Interview Questions

## Q1. Why does map() return a map object instead of a list?

In Python 3, map() returns an iterator for memory efficiency.

The data is generated only when needed.

This saves memory when processing huge datasets. :contentReference[oaicite:8]{index=8}

---

## Q2. Why do many developers prefer List Comprehension over map()?

List comprehensions are often easier to read and more Pythonic.

Example:

```python
[x*x for x in numbers]
```

is usually easier to understand than:

```python
map(lambda x:x*x,numbers)
```

:contentReference[oaicite:9]{index=9}

---

## Q3. What is the biggest limitation of lambda?

Lambda can only contain ONE expression.

You cannot write:

```python
if
for
while
multiple statements
```

inside a lambda.

---

## Q4. Difference between sorted() and sort()?

sorted():

- Returns new list
- Works on any iterable

sort():

- Modifies original list
- Works only on lists

---

## Q5. What does the key parameter do?

key determines HOW sorting is performed.

Example:

```python
sorted(
 users,
 key=lambda u:u["age"]
)
```

Sorts using age.

---

## Q6. Explain a real-world use case of zip().

Combining:

```python
User IDs
User Names
Emails
```

into structured records.

Used heavily when processing CSV files and API data.

---

## Q7. Explain map() in one sentence.

map() transforms every item in a collection.

---

## Q8. Explain filter() in one sentence.

filter() selects only items matching a condition.

---

## Q9. Explain Functional Programming in simple words.

Instead of telling Python HOW to do something step-by-step, you describe WHAT transformation should happen.

---

## Q10. Which concept from Day 9 is used most in backend development?

Most common:

```text
sorted()
zip()
list comprehensions
filtering API data
```

Lambda appears frequently but usually in small helper operations.

---

# 🏆 Day 9 Success Checklist

- ✅ Learned Functional Programming
- ✅ Learned Lambda Functions
- ✅ Learned map()
- ✅ Learned filter()
- ✅ Learned zip()
- ✅ Learned sorted()
- ✅ Learned key parameter
- ✅ Learned map vs comprehension
- ✅ Learned filter vs comprehension
- ✅ Learned reduce()
- ✅ Learned any()
- ✅ Learned all()
- ✅ Built ranking system logic
- ✅ Built product processor logic

---

# 🎯 Day 9 Result

You can now transform, filter, combine, sort, and process collections of data using modern Python techniques.

This is a major step toward writing professional Python code because most real-world backend systems spend their time processing collections of data rather than individual values.