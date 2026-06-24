# DAY 21 – WEEK 3 REVISION HANDBOOK

# PART 1 – TOP 50 PYTHON INTERVIEW QUESTIONS

---

## Q1. What is Python?

Python is a high-level, interpreted, object-oriented programming language known for its simple syntax and readability.

Features:
- Easy to learn
- Cross-platform
- Large community
- Huge library ecosystem
- Used in AI, Backend, Automation, Data Science

Example:

```python
print("Hello World")
```

---

## Q2. Why is Python called an interpreted language?

Python code is executed line by line by the Python Interpreter instead of being compiled directly into machine code.

Flow:

```text
Python Code
↓
Interpreter
↓
Bytecode
↓
Python Virtual Machine
↓
Output
```

---

## Q3. What are Variables in Python?

Variables are containers used to store data.

Example:

```python
name = "Adyaprana"
age = 23
```

---

## Q4. What are Python Data Types?

Built-in data types:

```python
int
float
str
bool
list
tuple
set
dict
NoneType
```

Example:

```python
age = 23
price = 99.99
name = "Adya"
```

---

## Q5. Difference Between List and Tuple?

| List | Tuple |
|--------|--------|
| Mutable | Immutable |
| [] | () |
| Slower | Faster |
| More Memory | Less Memory |

Example:

```python
my_list = [1,2,3]

my_tuple = (1,2,3)
```

---

## Q6. What is Mutability?

Mutable objects can be changed after creation.

Examples:

```python
list
dict
set
```

Immutable:

```python
int
str
tuple
```

---

## Q7. What is Type Casting?

Converting one datatype into another.

Example:

```python
age = "23"

age = int(age)
```

---

## Q8. Difference Between == and is ?

==

Checks values.

```python
a == b
```

is

Checks memory location.

```python
a is b
```

---

## Q9. What is None?

Represents absence of value.

Example:

```python
user = None
```

---

## Q10. What is Input Function?

Used to take user input.

```python
name = input("Enter name:")
```

---

## Q11. What are Operators?

Types:

- Arithmetic
- Comparison
- Logical
- Assignment
- Membership
- Identity

---

## Q12. Difference Between / and // ?

```python
10 / 3
```

Output:

```python
3.333
```

```python
10 // 3
```

Output:

```python
3
```

---

## Q13. What is Modulus Operator?

Returns remainder.

```python
10 % 3
```

Output:

```python
1
```

---

## Q14. What is String?

Collection of characters.

```python
name = "Python"
```

---

## Q15. What are String Methods?

Common methods:

```python
upper()

lower()

strip()

replace()

split()
```

---

## Q16. What is String Slicing?

Extract part of string.

```python
name = "Python"

print(name[0:3])
```

Output:

```python
Pyt
```

---

## Q17. What is f-string?

Modern string formatting.

```python
name = "Adya"

print(f"Hello {name}")
```

---

## Q18. What is if-elif-else?

Decision-making structure.

```python
if age > 18:
    print("Adult")
else:
    print("Minor")
```

---

## Q19. What are Nested Conditions?

Condition inside another condition.

```python
if age > 18:
    if salary > 50000:
        print("Eligible")
```

---

## Q20. What is a Loop?

Repeats code.

Types:

```python
for

while
```

---

## Q21. Difference Between for and while?

for:

Known iterations.

while:

Unknown iterations.

---

## Q22. What is range()?

Generates sequence.

```python
range(1,11)
```

---

## Q23. What is break?

Stops loop immediately.

```python
break
```

---

## Q24. What is continue?

Skips current iteration.

```python
continue
```

---

## Q25. What is enumerate()?

Returns index and value.

```python
for index,value in enumerate(names):
```

---

## Q26. What is List Comprehension?

Short way to create lists.

```python
nums = [x*x for x in range(5)]
```

---

## Q27. Advantages of List Comprehension?

- Faster
- Cleaner
- More Pythonic

---

## Q28. What is Dictionary?

Key-value pair collection.

```python
student = {
    "name":"Adya",
    "age":23
}
```

---

## Q29. What are Dictionary Methods?

```python
keys()

values()

items()

get()

update()
```

---

## Q30. What is Nested Dictionary?

Dictionary inside dictionary.

---

## Q31. What is Set?

Unordered collection of unique values.

```python
numbers = {1,2,3}
```

---

## Q32. Why Use Sets?

- Remove duplicates
- Fast lookup

---

## Q33. What is Union?

```python
a | b
```

Combines sets.

---

## Q34. What is Intersection?

```python
a & b
```

Common elements.

---

## Q35. What is Difference?

```python
a - b
```

---

## Q36. What is a Function?

Reusable block of code.

```python
def greet():
    print("Hello")
```

---

## Q37. Benefits of Functions?

- Reusability
- Maintainability
- Cleaner code

---

## Q38. What are Parameters?

Inputs of function.

```python
def add(a,b):
```

---

## Q39. What is Return Statement?

Returns result.

```python
return total
```

---

## Q40. Difference Between print() and return?

print:

Displays value.

return:

Sends value back.

---

## Q41. What are Default Arguments?

```python
def greet(name="Guest"):
```

---

## Q42. What is *args?

Accepts multiple positional arguments.

```python
def add(*args):
```

---

## Q43. What is **kwargs?

Accepts multiple keyword arguments.

```python
def show(**kwargs):
```

---

## Q44. What is Scope?

Accessibility of variables.

Types:

- Local
- Global

---

## Q45. What is Lambda Function?

Anonymous function.

```python
square = lambda x:x*x
```

---

## Q46. What is map()?

Applies function to every item.

```python
map(square,numbers)
```

---

## Q47. What is filter()?

Filters data.

```python
filter(is_even,numbers)
```

---

## Q48. What is zip()?

Combines multiple iterables.

```python
zip(names,ages)
```

---

## Q49. What is Exception Handling?

Handling runtime errors.

```python
try:
except:
```

---

## Q50. What are Common Exceptions?

```python
ValueError

TypeError

KeyError

IndexError

FileNotFoundError

ZeroDivisionError
```

---

# PART 2 – TOP 50 OOP INTERVIEW QUESTIONS

---

## Q51. What is OOP?

Object-Oriented Programming organizes software using classes and objects.

Benefits:

- Reusability
- Scalability
- Maintainability

---

## Q52. What is a Class?

Blueprint for creating objects.

```python
class Student:
    pass
```

---

## Q53. What is an Object?

Instance of a class.

```python
s1 = Student()
```

---

## Q54. Difference Between Class and Object?

Class:

Blueprint

Object:

Actual instance

---

## Q55. What is __init__()?

Constructor method.

Runs automatically when object is created.

---

## Q56. What is self?

Reference to current object.

---

## Q57. Why is self Required?

Allows access to object attributes and methods.

---

## Q58. What are Instance Variables?

Unique per object.

---

## Q59. What are Class Variables?

Shared by all objects.

---

## Q60. Difference Between Instance and Class Variables?

Instance:

Unique

Class:

Shared

---

## Q61. What are Methods?

Functions inside classes.

---

## Q62. What are Instance Methods?

Methods using self.

---

## Q63. What are Class Methods?

Methods using cls.

```python
@classmethod
```

---

## Q64. What are Static Methods?

Methods without self or cls.

```python
@staticmethod
```

---

## Q65. What is Encapsulation?

Protecting data by restricting access.

---

## Q66. Why Use Encapsulation?

Data security and validation.

---

## Q67. What are Public Variables?

Accessible everywhere.

---

## Q68. What are Protected Variables?

```python
_var
```

Convention only.

---

## Q69. What are Private Variables?

```python
__var
```

Uses name mangling.

---

## Q70. What is Name Mangling?

Python changes:

```python
__var
```

to:

```python
_ClassName__var
```

---

## Q71. What are Getters?

Methods used to access private data.

---

## Q72. What are Setters?

Methods used to update private data safely.

---

## Q73. What is @property?

Modern getter/setter approach.

---

## Q74. What is Inheritance?

Child class acquiring parent properties.

---

## Q75. Benefits of Inheritance?

- Reusability
- Less code duplication

---

## Q76. What is Single Inheritance?

One parent → one child.

---

## Q77. What is Multiple Inheritance?

Multiple parents → one child.

---

## Q78. What is Multilevel Inheritance?

Grandparent → Parent → Child.

---

## Q79. What is Hierarchical Inheritance?

One parent → multiple children.

---

## Q80. What is super()?

Calls parent class methods.

---

## Q81. What is Method Overriding?

Child modifies parent behavior.

---

## Q82. What is Polymorphism?

Same interface, different behavior.

---

## Q83. Benefits of Polymorphism?

Flexible and extensible code.

---

## Q84. What is Duck Typing?

Behavior matters, not type.

---

## Q85. What is Abstraction?

Hiding implementation details.

---

## Q86. Why Use Abstraction?

Reduce complexity.

---

## Q87. What is Abstract Class?

Class that cannot be instantiated directly.

---

## Q88. What is ABC Module?

Abstract Base Class module.

---

## Q89. What are Dunder Methods?

Special Python methods.

Examples:

```python
__init__

__str__

__repr__

__len__
```

---

## Q90. What is __str__()?

Human-readable object representation.

---

## Q91. What is __repr__()?

Developer-friendly representation.

---

## Q92. What is __len__()?

Custom behavior for len().

---

## Q93. What is __eq__()?

Custom equality comparison.

---

## Q94. What is Operator Overloading?

Changing behavior of operators.

---

## Q95. What are Decorators?

Functions that modify behavior of other functions.

---

## Q96. Why Are Decorators Important?

Used extensively in FastAPI and Django.

---

## Q97. What is MRO?

Method Resolution Order.

---

## Q98. What is Diamond Problem?

Ambiguity in multiple inheritance.

---

## Q99. What is Composition?

HAS-A relationship.

Example:

```python
Car HAS-A Engine
```

---

## Q100. Composition vs Inheritance?

Inheritance:

IS-A

Composition:

HAS-A

Modern software prefers Composition.


# PART 3 – TOP 25 DSA / LEETCODE INTERVIEW QUESTIONS

---

## Q101. What is Data Structure?

A Data Structure is a way of organizing, storing, and managing data efficiently.

Examples:

```python
List
Tuple
Set
Dictionary
Stack
Queue
Linked List
Tree
Graph
Heap
```

Why important?

Efficient data structures improve performance and reduce execution time.

---

## Q102. What is an Algorithm?

An Algorithm is a step-by-step procedure to solve a problem.

Example:

```python
Finding largest number

Searching an element

Sorting data
```

Good algorithms are:

- Correct
- Efficient
- Scalable

---

## Q103. What is Time Complexity?

Time Complexity measures how execution time grows as input size increases.

Example:

```python
n = 10
n = 1000
n = 100000
```

We analyze growth rate instead of actual seconds.

---

## Q104. What is Space Complexity?

Measures memory consumed by an algorithm.

Example:

```python
arr = [1,2,3]
```

Consumes additional memory.

---

## Q105. Explain Big-O Notation.

Big-O describes worst-case performance.

Common complexities:

```text
O(1)

O(log n)

O(n)

O(n log n)

O(n²)

O(2ⁿ)
```

Interview favorite question.

---

## Q106. What is O(1)?

Constant time.

Example:

```python
arr[0]
```

Execution time remains same regardless of input size.

---

## Q107. What is O(n)?

Linear time.

Example:

```python
for num in nums:
    print(num)
```

Runs proportional to input size.

---

## Q108. What is O(n²)?

Nested loop complexity.

Example:

```python
for i in nums:
    for j in nums:
        pass
```

Common beginner mistake.

---

## Q109. Difference Between Array and Linked List?

Array:

```text
Fast Indexing

Fixed Structure
```

Linked List:

```text
Dynamic

Sequential Access
```

---

## Q110. What is a Stack?

Follows:

```text
LIFO

Last In First Out
```

Example:

```python
stack = []

stack.append(10)

stack.pop()
```

Applications:

- Undo operations
- Browser history

---

## Q111. What is a Queue?

Follows:

```text
FIFO

First In First Out
```

Applications:

- Task scheduling
- Request handling

---

## Q112. What is Hashing?

Mapping data to keys for fast lookup.

Python Dictionary uses hashing internally.

Example:

```python
student = {
    "name":"Adya"
}
```

---

## Q113. Why Are Dictionaries Fast?

Average lookup complexity:

```text
O(1)
```

Because they use Hash Tables.

---

## Q114. What is Two Sum Problem?

Given:

```python
nums = [2,7,11,15]

target = 9
```

Return indices whose values add to target.

---

## Q115. Brute Force Solution for Two Sum?

```python
for i in range(len(nums)):
    for j in range(i+1,len(nums)):
        if nums[i]+nums[j]==target:
            return [i,j]
```

Complexity:

```text
O(n²)
```

---

## Q116. Optimal Solution for Two Sum?

Hash Map.

```python
seen = {}

for i,num in enumerate(nums):

    diff = target-num

    if diff in seen:
        return [seen[diff],i]

    seen[num]=i
```

Complexity:

```text
O(n)
```

---

## Q117. What is Sliding Window?

Technique for subarray problems.

Instead of recalculating every window:

Move window efficiently.

Used in:

```text
Maximum Sum Subarray

Longest Substring

LeetCode Problems
```

---

## Q118. What is Binary Search?

Search in sorted array.

Complexity:

```text
O(log n)
```

Example:

```python
mid = (left+right)//2
```

---

## Q119. When Can Binary Search Be Used?

Condition:

```text
Data Must Be Sorted
```

Most common interview follow-up.

---

## Q120. What is Recursion?

Function calling itself.

Example:

```python
def factorial(n):

    if n==1:
        return 1

    return n*factorial(n-1)
```

---

## Q121. What is Base Case in Recursion?

Stopping condition.

Without it:

```text
Infinite Recursion
```

---

## Q122. Difference Between Recursion and Iteration?

Recursion:

```text
Uses Call Stack
```

Iteration:

```text
Uses Loops
```

---

## Q123. What is Dynamic Programming?

Optimization technique.

Used when:

```text
Overlapping Subproblems

Optimal Substructure
```

Examples:

```text
Fibonacci

Knapsack

Climbing Stairs
```

---

## Q124. What is Greedy Algorithm?

Makes locally optimal choice.

Examples:

```text
Activity Selection

Coin Change

Huffman Coding
```

---

## Q125. How Many LeetCode Problems Should A Fresher Solve?

Target:

```text
50 Easy

50 Medium
```

Focus Areas:

✅ Arrays

✅ Strings

✅ Hash Maps

✅ Sliding Window

✅ Binary Search

✅ Recursion

✅ Basic Trees

More important than quantity:

```text
Understand Pattern

Explain Solution

Know Complexity
```

---

# PART 4 – TOP 25 BACKEND-ORIENTED PYTHON INTERVIEW QUESTIONS

---

## Q126. What is Backend Development?

Backend development handles:

```text
Business Logic

Database

Authentication

APIs

Server Processing
```

Users interact with frontend.

Backend does the actual work.

---

## Q127. What is an API?

API means:

```text
Application Programming Interface
```

Allows communication between applications.

Example:

```text
Frontend
↓
API
↓
Database
```

---

## Q128. What is REST API?

REST is an architectural style.

Uses:

```text
GET

POST

PUT

PATCH

DELETE
```

---

## Q129. Difference Between GET and POST?

GET:

```text
Fetch Data
```

POST:

```text
Create Data
```

---

## Q130. Difference Between PUT and PATCH?

PUT:

```text
Update Entire Resource
```

PATCH:

```text
Partial Update
```

---

## Q131. What is JSON?

JavaScript Object Notation.

Most common API data format.

Example:

```json
{
  "name":"Adya",
  "age":23
}
```

---

## Q132. Why Is JSON Popular?

Advantages:

```text
Readable

Lightweight

Language Independent

Easy Parsing
```

---

## Q133. What is HTTP?

Protocol used for communication on the web.

Browser and server communicate using HTTP.

---

## Q134. Common HTTP Status Codes?

```text
200 OK

201 Created

400 Bad Request

401 Unauthorized

403 Forbidden

404 Not Found

500 Internal Server Error
```

Interview favorite.

---

## Q135. What is Client-Server Architecture?

Client:

```text
Browser

Mobile App
```

Server:

```text
Backend Application
```

---

## Q136. What is Flask?

Lightweight Python backend framework.

Good for:

```text
APIs

Small Projects

Learning Backend
```

---

## Q137. What is FastAPI?

Modern Python backend framework.

Benefits:

```text
Fast

Async Support

Automatic Docs

Type Hints
```

---

## Q138. Why Is FastAPI Popular?

Because:

```text
High Performance

Easy Validation

Async Support

Developer Friendly
```

---

## Q139. What is Database?

System for storing data.

Examples:

```text
PostgreSQL

MySQL

MongoDB
```

---

## Q140. Difference Between SQL and NoSQL?

SQL:

```text
Tables

Rows

Columns
```

Examples:

```text
PostgreSQL

MySQL
```

NoSQL:

```text
Documents

Flexible Schema
```

Example:

```text
MongoDB
```

---

## Q141. What is PostgreSQL?

Open-source relational database.

Widely used in backend engineering.

---

## Q142. What is ORM?

Object Relational Mapping.

Converts:

```text
Database Rows
↓
Python Objects
```

Examples:

```text
SQLAlchemy

Django ORM
```

---

## Q143. Benefits of ORM?

```text
Cleaner Code

Less SQL

Database Abstraction
```

---

## Q144. What is Authentication?

Verifying user identity.

Example:

```text
Username + Password
```

---

## Q145. What is Authorization?

Determines what user can access.

Example:

```text
Admin

Moderator

User
```

---

## Q146. Difference Between Authentication and Authorization?

Authentication:

```text
Who Are You?
```

Authorization:

```text
What Can You Do?
```

---

## Q147. What is JWT?

JSON Web Token.

Used for:

```text
Authentication

Session Management
```

---

## Q148. What is Password Hashing?

Never store passwords directly.

Use:

```text
bcrypt

argon2
```

---

## Q149. What is Environment Variable?

Stores sensitive information.

Examples:

```text
API Keys

Database Passwords

Secret Keys
```

---

## Q150. What Skills Are Required For A Python Backend Developer?

Core Skills:
✅ Python
✅ OOP
✅ DSA
✅ Git & GitHub
✅ FastAPI / Flask
✅ PostgreSQL
✅ SQL
✅ REST APIs
✅ Authentication
✅ Linux Basics
✅ Deployment
✅ Cloud Basics (AWS)

# PART 5 – WEEK 1–3 RAPID REVISION SHEET

> Read this section every Sunday.
>
> Goal: Revise 20 days of learning in under 30 minutes.

---

# 🚀 WEEK 1 – PYTHON FUNDAMENTALS REVISION

---

## Variables

Used to store data.

Example:

```python
name = "Adyaprana"
age = 23
salary = 50000
```

Remember:

```text
Python is Dynamically Typed
```

---

## Data Types

```python
int
float
str
bool
list
tuple
dict
set
None
```

Interview:

Difference between Mutable and Immutable?

Mutable:

```python
list
dict
set
```

Immutable:

```python
int
float
str
tuple
bool
```

---

## Operators

Arithmetic:

```python
+
-
*
/
//
%
**
```

Comparison:

```python
==
!=
>
<
>=
<=
```

Logical:

```python
and
or
not
```

---

## Strings

Important Methods:

```python
upper()
lower()
strip()
replace()
split()
join()
find()
```

Important Interview Question:

```python
String is Immutable
```

---

## Conditions

```python
if
elif
else
```

Remember:

```text
Indentation Creates Blocks
```

No curly braces in Python.

---

## Loops

For Loop:

```python
for i in range(5):
```

While Loop:

```python
while True:
```

Keywords:

```python
break
continue
pass
```

---

## Lists

Methods:

```python
append()
insert()
remove()
pop()
sort()
reverse()
extend()
```

Interview:

List Comprehension

```python
squares = [x*x for x in range(10)]
```

---

## Tuples

Immutable.

Faster than Lists.

Used when data should not change.

---

## Dictionaries

Key Value Pair.

Methods:

```python
keys()
values()
items()
get()
update()
```

Backend APIs use dictionaries heavily.

---

## Sets

Properties:

```text
Unique Values

No Duplicates

Fast Lookup
```

Operations:

```python
union()

intersection()

difference()
```

---

# 🚀 WEEK 2 – INTERMEDIATE PYTHON REVISION

---

## Functions

Structure:

```python
def greet():
    pass
```

---

## Parameters vs Arguments

Parameter:

```python
def add(a,b)
```

Argument:

```python
add(5,10)
```

---

## Return

```python
return value
```

Remember:

```text
return sends data back

print only displays
```

---

## *args

Multiple positional arguments.

```python
def add(*args):
```

---

## **kwargs

Multiple keyword arguments.

```python
def show(**kwargs):
```

---

## Scope

Local:

```python
inside function
```

Global:

```python
outside function
```

Interview favorite.

---

## Lambda

Anonymous Function.

```python
lambda x:x*x
```

---

## map()

Apply function to every element.

---

## filter()

Filter elements.

---

## zip()

Combine iterables.

---

## sorted()

Powerful sorting function.

```python
sorted(data,key=lambda x:x["age"])
```

---

## Exception Handling

Structure:

```python
try:
except:
else:
finally:
```

---

## Common Exceptions

```python
ValueError

TypeError

KeyError

IndexError

FileNotFoundError

ZeroDivisionError
```

---

## File Handling

```python
open()
read()
write()
```

---

## Context Manager

Always prefer:

```python
with open() as file:
```

instead of:

```python
file.close()
```

---

## JSON

Backend's most important data format.

```python
json.load()

json.dump()
```

---

## Modules

Importing:

```python
import module

from module import function
```

---

## Virtual Environment

Create:

```bash
python -m venv env
```

Activate:

```bash
env\Scripts\activate
```

Must know for interviews.

---

# 🚀 WEEK 3 – OOP MASTER REVISION

---

## Class

Blueprint.

```python
class Student:
```

---

## Object

Instance of class.

```python
student = Student()
```

---

## Constructor

```python
__init__()
```

Runs automatically.

---

## self

Represents current object.

---

## Instance Variables

Unique per object.

---

## Class Variables

Shared across objects.

---

# Four Pillars

---

## Encapsulation

Protect data.

```python
__private
```

---

## Inheritance

Reuse code.

```python
class Dog(Animal)
```

---

## Polymorphism

Same interface.

Different behavior.

---

## Abstraction

Hide complexity.

Expose essentials.

---

# Advanced OOP

---

## Dunder Methods

```python
__init__

__str__

__repr__

__len__

__eq__
```

---

## Decorators

```python
@staticmethod

@classmethod

@property
```

---

## MRO

Method Resolution Order.

Used in Multiple Inheritance.

---

## Composition

HAS-A relationship.

Example:

```text
Car HAS-A Engine
```

---

## SOLID Principles

S

Single Responsibility

O

Open Closed

L

Liskov Substitution

I

Interface Segregation

D

Dependency Inversion

---

# 🎯 MOST IMPORTANT INTERVIEW TOPICS

Ranked by importance:

### Tier 1

✅ Functions

✅ OOP

✅ Dictionaries

✅ Lists

✅ Exception Handling

✅ API Basics

---

### Tier 2

✅ Decorators

✅ Generators

✅ Context Managers

✅ Modules

---

### Tier 3

✅ MRO

✅ SOLID

✅ Advanced Dunder Methods

---

# 🚀 WEEK 1–3 FINAL CHECKLIST

Python Fundamentals

✅ Variables

✅ Data Types

✅ Operators

✅ Strings

✅ Conditions

✅ Loops

✅ Lists

✅ Tuples

✅ Dictionaries

✅ Sets

Intermediate Python

✅ Functions

✅ Lambda

✅ Map

✅ Filter

✅ Zip

✅ Error Handling

✅ File Handling

✅ JSON

✅ Modules

✅ Virtual Environments

OOP

✅ Classes

✅ Objects

✅ Encapsulation

✅ Inheritance

✅ Polymorphism

✅ Abstraction

✅ Decorators

✅ MRO

✅ SOLID

If every box is checked:

```text
You are ready for Week 4
(Web Fundamentals + Backend Foundations)
```
# Day 21 Achievement

Completed:

✅ Python Fundamentals

✅ Intermediate Python

✅ OOP Foundations

✅ Advanced OOP

✅ GitHub Daily Progress

✅ 3 Weeks Consistency

---

# Week 4 Starts Next

Upcoming Topics:

✅ Internet Basics

✅ HTTP

✅ HTML

✅ CSS

✅ APIs

✅ Client Server Architecture

✅ Flask/FastAPI Introduction

You are now transitioning from:

```text
Python Programmer
```

to:

```text
Backend Developer
```