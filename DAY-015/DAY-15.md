# 🚀 Day 15 — Object-Oriented Programming (OOP), Classes & Objects

> Week 3 • Day 15
>
> Goal: Understand how real-world software is modeled using objects, learn classes, objects, constructors, methods, memory management, and the foundations of OOP used in Python backend development.

---

# 🎯 Why OOP Is So Important

Look at modern software:

```text
Instagram
YouTube
Netflix
Amazon
Uber
```

All are built using:

```text
Objects
Classes
Relationships
```

Not thousands of random functions.

---

# Why OOP Exists

Imagine building:

```text
Banking System
```

Without OOP:

```python
account_name_1
account_balance_1

account_name_2
account_balance_2

account_name_3
account_balance_3
```

Very messy.

---

With OOP:

```python
BankAccount
```

Create unlimited accounts.

Clean.

Scalable.

Professional.

This is why OOP became one of the most important programming paradigms.

---

# 🧠 What Is OOP?

OOP stands for:

```text
Object-Oriented Programming
```

Definition:

```text
A programming paradigm
that organizes code using
objects and classes.
```

Think:

```text
Data
+
Behavior
=
Object
```

Your notes already introduced this idea using a BankAccount example. :contentReference[oaicite:0]{index=0}

---

# Real Life Understanding

A Car has:

```text
Data:
Color
Brand
Speed
Fuel
```

And:

```text
Actions:
Start
Stop
Accelerate
Brake
```

---

In OOP:

```text
Data + Actions
=
Object
```

---

# 📌 What Is A Class?

A class is:

```text
Blueprint
Template
Design
```

for creating objects.

---

# House Example

Blueprint:

```text
Class
```

Actual House:

```text
Object
```

---

# Student Example

Class:

```python
class Student:
    pass
```

This creates:

```text
Blueprint Only
```

No student exists yet. :contentReference[oaicite:1]{index=1}

---

# 📌 What Is An Object?

Object means:

```text
Real Instance
Created From Class
```

Example:

```python
s1 = Student()
```

Now:

```text
Real Object Exists
```

---

# Important Interview Point

One Class:

```text
Student
```

Can Create:

```text
100
1000
10000
```

Objects.

---

# Example

```python
class Student:
    pass

s1 = Student()
s2 = Student()
s3 = Student()
```

Three separate objects.

Exactly what you practiced. 

---

# 📌 Memory Concept (Very Important)

Most beginners skip this.

Huge mistake.

---

Example:

```python
s1 = Student()
s2 = Student()
```

Memory:

```text
Object 1
Memory A

Object 2
Memory B
```

Different locations.

---

Therefore:

```python
s1.name = "Adya"
```

does NOT affect:

```python
s2.name
```

Each object owns its own data. :contentReference[oaicite:3]{index=3}

---

# 📌 Constructor (__init__)

One of the most important interview topics.

Constructor:

```python
__init__()
```

Runs automatically when object is created.

Example:

```python
class Student:

    def __init__(self):
        print("Created")
```

Output:

```text
Created
```

automatically. :contentReference[oaicite:4]{index=4}

---

# Why Constructors Exist

Without Constructor:

```text
Empty Object
```

---

With Constructor:

```text
Initialize Data
Immediately
```

---

# Example

```python
class Student:

    def __init__(self,name):

        self.name = name
```

Now every student gets a name automatically.

---

# 📌 Understanding self

Most confusing topic for beginners.

---

# Wrong Thinking

```text
Special Keyword
Magic
```

---

# Correct Thinking

```text
self
=
Current Object
```

---

Example

```python
class Student:

    def __init__(self,name):

        self.name = name
```

Create:

```python
s1 = Student("Adya")
```

Python internally does:

```python
s1.name = "Adya"
```

Exactly what your notes explain. :contentReference[oaicite:5]{index=5}

---

# Mental Model

Imagine:

```python
s1 = Student("Adya")
```

self becomes:

```python
s1
```

---

Create:

```python
s2 = Student("Rahul")
```

self becomes:

```python
s2
```

Different object.

Different data.

---

# 📌 Instance Variables

Definition:

```text
Variables Unique
To Each Object
```

Example:

```python
self.name
self.age
self.email
```

---

Example

```python
class Student:

    def __init__(self,name):

        self.name = name
```

Objects:

```python
s1 = Student("Adya")
s2 = Student("Rahul")
```

Output:

```text
Adya
Rahul
```

Different values.

Exactly as you practiced. :contentReference[oaicite:6]{index=6}

---

# 📌 Class Variables

Definition:

```text
Variables Shared
By All Objects
```

Example:

```python
class Student:

    school = "KJC"
```

Every student shares:

```text
KJC
```

---

# Memory Visualization

```text
Student Class
|
|-- school = KJC

Student 1
|
|-- name = Adya

Student 2
|
|-- name = Rahul
```

---

# When To Use Class Variables?

Examples:

```text
Company Name
Tax Rate
App Version
Country
```

Shared information.

---

# Interview Question

## Difference Between Instance And Class Variable?

Instance Variable:

```text
Unique Per Object
```

Class Variable:

```text
Shared By All Objects
```

Your notes introduced this distinction clearly. :contentReference[oaicite:7]{index=7}

---

# 📌 Methods

Method = Function Inside Class.

---

# Instance Method

Uses:

```python
self
```

Can access object data.

Example:

```python
def greet(self):
```

Instance methods work on a specific object. :contentReference[oaicite:8]{index=8}

---

# Example

```python
class Student:

    def __init__(self,name):
        self.name = name

    def greet(self):
        print(
            f"Hello {self.name}"
        )
```

---

# Why Instance Methods Exist

Because every object behaves differently.

---

Example

```python
s1.greet()
```

Output:

```text
Hello Adya
```

---

```python
s2.greet()
```

Output:

```text
Hello Rahul
```

Same method.

Different object.

Different result.

---

# 📌 Class Methods

Decorator:

```python
@classmethod
```

Uses:

```python
cls
```

instead of:

```python
self
```

Your notes introduced this concept. :contentReference[oaicite:9]{index=9}

---

# Why Class Methods Exist

Work with:

```text
Class Data
```

instead of:

```text
Object Data
```

---

Example

```python
class Student:

    school = "KJC"

    @classmethod
    def get_school(cls):
        return cls.school
```

---

# Real Use Cases

Factory Methods

Configuration

Counters

Global Settings

Database Connections

---

# 📌 Static Methods

Decorator:

```python
@staticmethod
```

Uses:

```text
No self
No cls
```

Exactly as shown in your practice notes. :contentReference[oaicite:10]{index=10}

---

# Why Static Methods Exist

Utility functions logically related to class.

Example:

```python
class Math:

    @staticmethod
    def add(a,b):
        return a+b
```

---

# Real Examples

Validation

Calculations

Formatting

Helpers

---

# Method Comparison

| Type     | Uses self | Uses cls |
|----------|-----------|----------|
| Instance |   ✅     |   ❌   |
| Class    |   ❌     |   ✅   |
| Static   |   ❌     |   ❌   |

-✅
# 📌 Magic Methods (Dunder Methods)

Advanced Topic.

Dunder:

```text
Double Underscore
```

Examples:

```python
__init__
__str__
__len__
__repr__
```

---

# __str__()

Controls printing.

Example:

```python
class Student:

    def __str__(self):
        return self.name
```

Without:

```text
<student object at ...>
```

With:

```text
Adyaprana
```

Exactly what you experimented with. :contentReference[oaicite:11]{index=11}

---

# 📌 Object Identity

Advanced Interview Topic.

Example:

```python
s1 = Student("A")
s2 = Student("A")
```

Question:

```text
Same Data
Same Object?
```

Answer:

```text
NO
```

Different objects.

Different memory.

---

# Check Using id()

```python
print(id(s1))
print(id(s2))
```

Different IDs.

---

# 📌 Encapsulation (Preview)

Very Important OOP Pillar.

Definition:

```text
Bundle Data
+
Methods
Together
```

Example:

```python
class BankAccount
```

contains:

```text
Balance
Deposit
Withdraw
```

inside one unit.

Your notes briefly previewed this concept. :contentReference[oaicite:12]{index=12}

---

# Four Pillars Of OOP

You only study first pillar today.

---

# Encapsulation

Protect Data

---

# Inheritance

Reuse Code

---

# Polymorphism

Same Interface

Different Behavior

---

# Abstraction

Hide Complexity

---

These dominate backend interviews.

---

# 📌 Composition vs Inheritance (Preview)

Many senior developers prefer:

```text
Composition
```

over:

```text
Inheritance
```

---

Example

Car HAS Engine

```text
Composition
```

instead of:

```text
Car IS Engine
```

---

Important for future OOP learning.

---

# 🏦 Better BankAccount Design

Your practice version already supports:

```text
Deposit
Withdraw
Balance
```



Professional improvements could include:

```python
if amount <= 0:
    raise ValueError()
```

---

Prevent:

```text
Negative Deposits
```

---

Check:

```text
Insufficient Funds
```

---

Add:

```text
Transaction History
```

---

Generate:

```text
Account IDs
```

This is how software evolves.

---

# 📌 OOP In Backend Development

FastAPI:

```python
class UserService:
```

---

Database:

```python
class User:
```

---

Authentication:

```python
class TokenManager:
```

---

Payment:

```python
class PaymentGateway:
```

Backend projects are filled with classes.

---

# 💼 Real Companies Use OOP For

```text
Users
Products
Orders
Invoices
Notifications
Payments
Databases
```

Everything becomes an object.

---

# 🎤 Advanced Interview Questions

## Q1. What Is OOP?

OOP is a programming paradigm that organizes software around objects containing both data and behavior.

---

## Q2. What Is A Class?

A blueprint used to create objects.

---

## Q3. What Is An Object?

An instance created from a class.

---

## Q4. What Is self?

A reference to the current object.

---

## Q5. Why Is __init__ Called A Constructor?

Because it initializes the object immediately after creation.

---

## Q6. Difference Between Class And Object?

Class:

```text
Blueprint
```

Object:

```text
Real Instance
```

---

## Q7. Difference Between Instance And Class Variables?

Instance:

```text
Unique Per Object
```

Class:

```text
Shared Across Objects
```

---

## Q8. Difference Between Instance, Class And Static Methods?

Instance:

```text
Works With Object
```

Class:

```text
Works With Class
```

Static:

```text
Independent Utility
```

---

## Q9. Why Is OOP Useful?

It improves:

```text
Organization
Reusability
Scalability
Maintainability
```

---

## Q10. Why Is OOP Important For Backend Engineers?

Because frameworks like:

```text
FastAPI
Django
SQLAlchemy
Pydantic
```

heavily use classes and objects.

---

# 🏆 Day 15 Success Checklist

- ✅ Learned OOP
- ✅ Learned Classes
- ✅ Learned Objects
- ✅ Learned Constructors
- ✅ Learned self
- ✅ Learned Instance Variables
- ✅ Learned Class Variables
- ✅ Learned Instance Methods
- ✅ Learned Class Methods
- ✅ Learned Static Methods
- ✅ Learned __str__()
- ✅ Learned Object Identity
- ✅ Learned Encapsulation Basics
- ✅ Built BankAccount Class
- ✅ Created Multiple Objects

---

# 🎯 Day 15 Result

You have entered the most important phase of Python backend development.

Before Day 15:

```text
You wrote programs.
```

After Day 15:

```text
You can model real-world entities
using classes and objects.
```

This is the foundation for:

```text
OOP Design
FastAPI
Django
SQLAlchemy
ORMs
Microservices
System Design
```

Mastering OOP will make the next stages of your backend roadmap significantly easier.