# 🚀 Day 17 — Encapsulation, Polymorphism & Python Data Model

> **Week 3 • Day 17**
>
> **Goal:** Understand how Python protects data, how polymorphism makes code flexible, and how special dunder methods connect custom classes to Python’s built-in functions.

---

# 🎯 Why Day 17 Matters

This is the week where OOP starts feeling like real software design instead of just class syntax.

By the end of this day you will understand:

* How to hide and protect data
* How to control access to variables
* How Python handles getters and setters
* How `@property` works internally
* How polymorphism makes frameworks flexible
* How special dunder methods integrate your classes with Python
* Why these concepts are heavily used in FastAPI, Django and backend systems

This is one of the most important OOP topics for Python backend development.

---

# 🧠 What Is Encapsulation?

**Definition:**

Encapsulation is the process of:

* Wrapping data and methods together
* Restricting direct access to internal details
* Exposing only safe operations

Think of it as:

```text
Protecting Object Data
+
Controlling How It Is Used
```

---

# 🏧 Real-Life Example: ATM Machine

You can:

✅ Withdraw Money

✅ Deposit Money

✅ Check Balance

But you cannot:

❌ Directly modify bank database

❌ Directly change account records

❌ Directly edit transaction history

The ATM exposes only safe operations.

This is Encapsulation.

---

# Why Encapsulation Is Important

Without Encapsulation:

```python
account.balance = -1000000
```

Anyone can break your application.

With Encapsulation:

```python
account.deposit()
account.withdraw()
```

All updates go through validation.

This makes software:

* Secure
* Maintainable
* Predictable
* Professional

---

# 📌 Public Variables

Public variables are accessible from anywhere.

Example:

```python
class Student:

    def __init__(self):
        self.name = "Adyaprana"

s = Student()

print(s.name)
```

Output:

```text
Adyaprana
```

Public variables should be used only when unrestricted access is acceptable.

---

# 📌 Protected Variables

Python uses a convention:

```python
_age
```

Single underscore means:

```text
"Internal Use Recommended"
```

Example:

```python
class Student:

    def __init__(self):
        self._age = 22
```

Still accessible:

```python
print(student._age)
```

Output:

```text
22
```

Python does not block access.

It simply warns developers:

> "This variable is intended for internal use."

---

# 📌 Private Variables

Private variables use:

```python
__balance
```

Double underscore.

Example:

```python
class BankAccount:

    def __init__(self):
        self.__balance = 1000
```

Accessing directly:

```python
account.__balance
```

Results in:

```text
AttributeError
```

---

# 🧠 What Is Name Mangling?

Many beginners think:

```text
Private Variables Are Completely Hidden
```

This is not true.

Python performs:

```python
__balance
```

↓

```python
_BankAccount__balance
```

Internally.

Example:

```python
print(account._BankAccount__balance)
```

Output:

```text
1000
```

This process is called:

## Name Mangling

Purpose:

* Avoid accidental access
* Prevent naming conflicts
* Improve class safety

---

# 📌 Getters

Getter methods return private data.

Example:

```python
class Student:

    def __init__(self):
        self.__age = 23

    def get_age(self):
        return self.__age
```

Usage:

```python
student.get_age()
```

Output:

```text
23
```

---

# 📌 Setters

Setter methods update private data.

Example:

```python
def set_age(self, age):

    if age > 0:
        self.__age = age
```

Why?

Because validation is important.

Without validation:

```python
student.age = -50
```

Invalid data enters the system.

With setters:

```python
student.set_age(-50)
```

Rejected.

---

# Why Validation Matters In Backend

Real applications validate:

* Age
* Salary
* Email
* Password
* Balance
* Product Price

Every backend API performs validation.

Setters are the basic idea behind that.

---

# 📌 Modern Python Approach — @property

Traditional approach:

```python
student.get_age()
student.set_age(25)
```

Modern Python:

```python
student.age
student.age = 25
```

Looks cleaner.

More readable.

More Pythonic.

---

# Example

```python
class Student:

    def __init__(self):
        self._age = 23

    @property
    def age(self):
        return self._age
```

Usage:

```python
print(student.age)
```

Looks like an attribute.

Actually executes a method.

Magic? No.

Python Descriptor System.

---

# 📌 Property Setter

```python
@age.setter
def age(self, value):

    if value > 0:
        self._age = value
```

Now:

```python
student.age = 30
```

Valid.

---

```python
student.age = -10
```

Rejected.

This is how professional Python code is written.

---

# 🧠 Advanced Concept — Descriptors

Most beginners never learn this.

But interviewers sometimes ask.

`@property` is actually built using:

```text
Descriptor Protocol
```

Descriptors control:

* Reading attributes
* Writing attributes
* Deleting attributes

Python internally uses descriptors for:

* @property
* @staticmethod
* @classmethod
* Methods
* super()

Understanding descriptors later will make Python internals much easier.

---

# 📌 What Is Polymorphism?

Definition:

```text
Same Interface
Different Behavior
```

or

```text
Same Method Name
Different Implementation
```

---

# Animal Example

```python
class Dog:

    def sound(self):
        print("Bark")


class Cat:

    def sound(self):
        print("Meow")
```

Both contain:

```python
sound()
```

But behavior differs.

This is Polymorphism.

---

# Why Polymorphism Is Powerful

Imagine:

```python
animals = [Dog(), Cat()]
```

Loop:

```python
for animal in animals:
    animal.sound()
```

Output:

```text
Bark
Meow
```

The loop never checks:

```python
if Dog
if Cat
```

The object decides behavior.

This creates flexible software.

---

# 📌 Real Backend Example

Payment System:

```python
CreditCardPayment
UPIPayment
PayPalPayment
```

Each contains:

```python
process_payment()
```

Different implementation.

Same method name.

That is polymorphism.

---

# 📌 Shape Example

Parent:

```python
class Shape:
    def area(self):
        pass
```

Children:

```python
Circle
Rectangle
Triangle
```

Each calculates area differently.

But all expose:

```python
area()
```

This is a classic interview example.

---

# 📌 Dunder Methods

Dunder means:

```text
Double Underscore
```

Examples:

```python
__init__
__str__
__repr__
__len__
__eq__
```

Python automatically calls them.

These methods connect your objects to Python's built-in functions.

---

# 📌 **str**()

Controls:

```python
print(object)
```

Without:

```text
<student object at 0x123>
```

With:

```python
def __str__(self):
    return f"Student({self.name})"
```

Output:

```text
Student(Adyaprana)
```

Much cleaner.

---

# 📌 **repr**()

Purpose:

```text
Developer-Friendly Representation
```

Used in:

```python
repr(object)
```

and debugging tools.

---

# Difference Between **str** and **repr**

| **str**          | **repr**           |
| ---------------- | ------------------ |
| Human readable   | Developer readable |
| Used by print()  | Used by repr()     |
| Friendly display | Debugging display  |

---

# 📌 **len**()

Allows:

```python
len(object)
```

Example:

```python
class Playlist:

    def __len__(self):
        return len(self.songs)
```

Now:

```python
len(playlist)
```

works naturally.

---

# 📌 **eq**()

Controls:

```python
==
```

Example:

```python
def __eq__(self, other):
    return self.id == other.id
```

Without:

```python
s1 == s2
```

compares memory addresses.

With `__eq__`:

```python
s1 == s2
```

compares actual data.

Very important interview topic.

---

# 💼 Backend Development Connection

These concepts appear everywhere:

### FastAPI

```python
UserService
ProductService
OrderService
```

Use encapsulation.

---

### SQLAlchemy

Models use:

```python
@property
```

and custom methods.

---

### Django

Uses:

```python
__str__()
```

heavily.

---

### Pydantic

Uses encapsulation and validation extensively.

---

# 🎤 Interview Questions & Answers

## Q1. What is Encapsulation?

Encapsulation is the process of wrapping data and methods together while restricting direct access to internal implementation details. It improves security, maintainability, and code organization.

---

## Q2. Difference Between Public, Protected and Private Variables?

Public variables are directly accessible. Protected variables use a single underscore and are intended for internal use. Private variables use double underscores and trigger name mangling.

---

## Q3. What Is Name Mangling?

Name mangling is Python's process of internally renaming private variables.

Example:

```python
__balance
```

becomes:

```python
_BankAccount__balance
```

---

## Q4. Why Use Getters And Setters?

They provide validation and controlled access to internal data.

---

## Q5. What Is @property?

A decorator that allows methods to behave like attributes while still supporting validation and control.

---

## Q6. What Is Polymorphism?

Polymorphism allows the same method name to produce different behavior depending on the object.

---

## Q7. Real World Example Of Polymorphism?

Payment Gateway:

```text
Credit Card
UPI
PayPal
```

All implement:

```python
process_payment()
```

---

## Q8. Difference Between **str** And **repr**?

`__str__` is for users.

`__repr__` is for developers and debugging.

---

## Q9. Why Is **eq** Useful?

It allows object comparison based on actual data instead of memory location.

---

## Q10. Why Are Dunder Methods Important?

Because they integrate custom classes with Python's built-in functions and operators.

---

# ✅ Day 17 Success Checklist

✅ Learned Encapsulation

✅ Learned Public Variables

✅ Learned Protected Variables

✅ Learned Private Variables

✅ Learned Name Mangling

✅ Learned Getters

✅ Learned Setters

✅ Learned @property

✅ Learned Property Setters

✅ Learned Descriptor Basics

✅ Learned Polymorphism

✅ Learned Shape Polymorphism

✅ Learned Dunder Methods

✅ Learned **str**

✅ Learned **repr**

✅ Learned **len**

✅ Learned **eq**

✅ Practiced OOP Design Thinking

---

# 🎯 Day 17 Result

Before Day 17:

```text
You Could Create Classes
```

After Day 17:

```text
You Can Protect Data
Control Access
Customize Object Behavior
Write Flexible OOP Designs
```

You now understand the foundations used in:

```text
FastAPI
Django
SQLAlchemy
Pydantic
Enterprise Backend Systems
```

This is one of the most important OOP days in your backend roadmap and forms the bridge between basic classes and professional software architecture.
