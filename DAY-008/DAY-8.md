# 🚀 Day 8 — Functions, Parameters, Return Values & Modular Programming

> Week 2 • Day 8
>
> Goal: Learn how professional software is built using functions, understand parameter passing, return values, scope, *args, **kwargs, lambda functions, docstrings, type hints, and refactor previous projects into reusable modules.

---

# 🎯 Why Functions Matter

Everything in backend development is built using functions:

```text
FastAPI Endpoints
Database Operations
Authentication Systems
Payment Processing
Email Services
File Uploads
API Integrations
```

A function is simply:

```text
A reusable block of code
that performs a specific task.
```

Python's official documentation emphasizes that functions are the core of extensible programming and support mandatory arguments, optional arguments, keyword arguments, and arbitrary argument lists.

---

# 🧠 Big Idea of Functions

Imagine a restaurant.

Without functions:

```python
take_order code
take_order code
take_order code

cook_food code
cook_food code

serve_food code
serve_food code
```

Huge repetition ❌

With functions:

```python
def take_order():
    pass

def cook_food():
    pass

def serve_food():
    pass
```

Write once.

Use forever.

This is exactly why software engineering scales.

---

# 📌 What is a Function?

A function is a named block of reusable code.

Syntax:

```python
def function_name():
    code
```

Example:

```python
def greet():
    print("Hello Adyaprana")
```

Function created.

But not executed.

---

# 📌 Calling a Function

```python
def greet():
    print("Hello Adyaprana")

greet()
```

Output:

```text
Hello Adyaprana
```

Function runs only when called.

---

# 📌 Why Use Functions?

Without Function:

```python
print("Welcome")
print("Welcome")
print("Welcome")
```

With Function:

```python
def welcome():
    print("Welcome")

welcome()
welcome()
welcome()
```

Cleaner.

Reusable.

Professional.

---

# 📌 Anatomy of a Function

```python
def add(a, b):
    return a + b
```

Breakdown:

```text
def        → keyword
add        → function name
a, b       → parameters
return     → returns result
```

---

# 📌 Parameters

Parameters allow data to enter a function.

Example:

```python
def greet(name):
    print("Hello", name)

greet("Adyaprana")
```

Output:

```text
Hello Adyaprana
```

---

# Multiple Parameters

```python
def student(name, age):
    print(name)
    print(age)

student("Adyaprana", 23)
```

Output:

```text
Adyaprana
23
```

---

# 🧠 Real Backend Example

```python
def create_user(username, email):
    print(username)
    print(email)
```

Imagine:

```python
create_user(
    "adyaprana",
    "adyaprana@gmail.com"
)
```

This is exactly how APIs receive data.

---

# 📌 Arguments vs Parameters

Students often confuse these.

Parameters:

```python
def add(a, b):
```

Arguments:

```python
add(10, 20)
```

Memory Trick:

```text
Parameter = Variable

Argument = Actual Value
```

---

# 📌 Return Values

One of the MOST IMPORTANT concepts.

---

## Print Version

```python
def add(a, b):
    print(a+b)

add(10,20)
```

Output:

```text
30
```

Problem:

Cannot reuse result.

---

## Return Version

```python
def add(a,b):
    return a+b

result = add(10,20)

print(result)
```

Output:

```text
30
```

Now result can be reused.

---

# 🎯 Interview Question

### Difference Between print() and return()

print():

```text
Displays result
```

return():

```text
Sends result back
```

Professional software uses return.

---

# Example

```python
def square(n):
    return n*n

print(square(5))
```

Output:

```text
25
```

---

# Why Return Matters in Backend

FastAPI Example:

```python
def get_user():
    return {
        "name":"Adyaprana"
    }
```

APIs return data.

Databases return data.

Functions return data.

---

# 📌 Types of Functions

---

## No Parameter No Return

```python
def hello():
    print("Hello")
```

---

## Parameter No Return

```python
def hello(name):
    print(name)
```

---

## No Parameter Return

```python
def get_number():
    return 100
```

---

## Parameter Return

```python
def add(a,b):
    return a+b
```

Most common type.

---

# 📌 Default Arguments

Provide default value.

Example:

```python
def greet(name="Guest"):
    print("Hello", name)

greet()
greet("Adyaprana")
```

Output:

```text
Hello Guest
Hello Adyaprana
```

---

# Why Default Arguments Matter

Backend APIs often have optional values.

Example:

```python
def get_users(limit=10):
    pass
```

If user doesn't provide limit:

```python
10
```

is used.

---

# 📌 Keyword Arguments

Normal:

```python
student("Adyaprana",23)
```

Keyword:

```python
student(
    age=23,
    name="Adyaprana"
)
```

Order doesn't matter.

---

# 📌 *args

Allows multiple positional arguments.

Normal:

```python
def add(a,b):
    return a+b
```

Only 2 values.

---

Using *args

```python
def add(*args):

    total = 0

    for num in args:
        total += num

    return total
```

Now:

```python
add(10,20,30,40)
```

Output:

```text
100
```

---

# What Does *args Store?

```python
(10,20,30,40)
```

Tuple.

---

# 📌 **kwargs

Allows multiple keyword arguments.

Example:

```python
def profile(**kwargs):
    print(kwargs)
```

Call:

```python
profile(
    name="Adyaprana",
    city="Bangalore"
)
```

Output:

```python
{
  'name':'Adyaprana',
  'city':'Bangalore'
}
```

---

# What Does **kwargs Store?

Dictionary.

Example:

```python
kwargs["name"]
```

Output:

```text
Adyaprana
```

---

# 🚀 Why FastAPI Uses Similar Concepts

When APIs receive:

```json
{
  "name":"Adyaprana",
  "city":"Bangalore"
}
```

Backend internally works with structures similar to dictionaries and keyword arguments.

That's why understanding **kwargs is valuable.

---

# 📌 Variable Scope

Scope determines where variables can be accessed.

---

# Local Scope

```python
def demo():

    x = 10

    print(x)
```

Works.

Outside?

```python
print(x)
```

Error.

Because x is local.

---

# Global Scope

```python
x = 100

def demo():
    print(x)

demo()
print(x)
```

Works everywhere.

---

# 🎯 Interview Question

Local vs Global

| Local           | Global           |
| --------------- | ---------------- |
| Inside Function | Outside Function |
| Safer           | Riskier          |
| Preferred       | Limited Use      |

Professional projects prefer local variables.

---

# 📌 Docstrings

Function documentation.

Example:

```python
def add(a,b):
    """
    Adds two numbers
    """
    return a+b
```

View documentation:

```python
help(add)
```

or

```python
print(add.__doc__)
```

---

# Why Docstrings Matter

Large companies require documentation.

Benefits:

✅ Easier maintenance

✅ Easier teamwork

✅ Better APIs

Research on Python code documentation highlights the importance of docstrings for understanding and maintaining software.

---

# 📌 Type Hints

Very important for modern Python.

Example:

```python
def add(a:int,b:int)->int:
    return a+b
```

Meaning:

```text
a should be int
b should be int
returns int
```

---

# Why Type Hints Matter

Used heavily in:

* FastAPI
* Large Projects
* IDE Autocomplete
* Code Reviews

Python supports optional typing, which became an important part of modern Python development.

---

# 📌 Lambda Functions

Small one-line anonymous functions.

Example:

```python
square = lambda x: x*x

print(square(5))
```

Output:

```text
25
```

---

# Normal vs Lambda

Normal:

```python
def square(x):
    return x*x
```

Lambda:

```python
lambda x:x*x
```

Shorter.

Useful for:

* Sorting
* Filtering
* Data Processing

---

# 🏗️ Project 1 — Grade Calculator Function

Convert Day 3 project into function.

```python
def calculate_grade(marks):

    if marks >= 90:
        return "A"

    elif marks >= 80:
        return "B"

    else:
        return "Fail"
```

Now reusable.

---

# 🏗️ Project 2 — Calculator Using Functions

Instead of one huge file:

```python
def add(a,b):
    return a+b

def sub(a,b):
    return a-b

def mul(a,b):
    return a*b

def div(a,b):
    return a/b
```

Cleaner.

Professional.

Modular.

---

# 🏗️ Project 3 — Prime Checker Function

```python
def is_prime(num):

    if num < 2:
        return False

    for i in range(2,num):

        if num%i==0:
            return False

    return True
```

Usage:

```python
print(is_prime(7))
```

Output:

```text
True
```

---

# 🔥 Refactor Week 1 Programs

Convert:

✅ Calculator

✅ Grade Checker

✅ Prime Checker

✅ Max Finde✅ Average Finder

Into functions.

This is exactly what software engineers do:

```text
Take working code
↓
Break into functions
↓
Make reusable modules
```

---

# 💼 Backend Connection

FastAPI Endpoint:

```python
def get_user():
    return {"id":1}
```

Authentication:

```python
def verify_token():
```

Database:

```python
def create_user():
```

Email:

```python
def send_email():
```

Backend development is essentially thousands of functions working together.

Python's ecosystem, including FastAPI and Flask, relies heavily on functions and modular code organization.

---

# 🎤 Most Important Interview Questions

## Q1. What is a function?

Reusable block of code.

---

## Q2. Why use functions?

Avoid repetition and improve reusability.

---

## Q3. Difference between parameter and argument?

Parameter → variable

Argument → actual value

---

## Q4. Difference between print() and return()?

print → display

return → send result back

---

## Q5. What is a default argument?

Predefined value used if argument not provided.

---

## Q6. What are keyword arguments?

Arguments passed using parameter names.

---

## Q7. What is *args?

Accepts unlimited positional arguments.

---

## Q8. What is **kwargs?

Accepts unlimited keyword arguments.

---

## Q9. What does **kwargs store?

Dictionary.

---

## Q10. What does *args store?

Tuple.

---

## Q11. What is scope?

Region where variable is accessible.

---

## Q12. Difference between local and global variable?

Local inside function.

Global outside function.

---

## Q13. What is a docstring?

Function documentation.

---

## Q14. What are type hints?

Optional type information.

---

## Q15. What is a lambda function?

Small one-line anonymous function.

---

# 🏆 Day 8 Success Checklist

* ✅ Learned Functions
* ✅ Learned Parameters
* ✅ Learned Arguments
* ✅ Learned Return Values
* ✅ Learned Default Arguments
* ✅ Learned Keyword Arguments
* ✅ Learned *args
* ✅ Learned **kwargs
* ✅ Learned Local Scope
* ✅ Learned Global Scope
* ✅ Learned Docstrings
* ✅ Learned Type Hints
* ✅ Learned Lambda Functions
* ✅ Refactored Week 1 Programs

---

# 🎯 Day 8 Result

You can now write modular programs, build reusable code, understand how real backend systems are organized, and work with advanced function concepts used in FastAPI, APIs, and professional Python projects.

You are no longer just writing scripts.

You are starting to think like a software engineer. 🚀
