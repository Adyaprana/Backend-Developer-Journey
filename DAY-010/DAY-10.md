# 🚀 Day 10 — Error Handling, Exceptions & Defensive Programming

> Week 2 • Day 10
>
> Goal: Learn how professional software handles failures gracefully, understand Python's exception system, build robust applications, validate data properly, and prevent crashes.

---

# 🎯 Why Day 10 Is One of the Most Important Days

Many beginners think:

```text
Programming = Making Things Work
```

Professional developers know:

```text
Programming = Making Things Work
             +
Making Things Fail Safely
```

The biggest difference between beginner code and production code is:

```text
Error Handling
```

A beginner writes:

```python
age = int(input("Age: "))
```

User enters:

```text
hello
```

Program crashes ❌

---

Professional version:

```python
try:
    age = int(input("Age: "))
except ValueError:
    print("Please enter a valid number")
```

Program continues running ✅

This is called:

```text
Defensive Programming
```

Writing software that expects users to make mistakes.

---

# 🧠 What Is An Exception?

An Exception is:

```text
A runtime error that interrupts
the normal flow of a program.
```

Example:

```python
10 / 0
```

Output:

```text
ZeroDivisionError
```

Python immediately stops execution.

---

# Compilation Error vs Runtime Error

## Syntax Error

Detected before execution.

```python
if True
    print("Hello")
```

Output:

```text
SyntaxError
```

---

## Runtime Error

Occurs while program runs.

```python
10 / 0
```

Output:

```text
ZeroDivisionError
```

---

# Why Python Uses Exceptions

Imagine:

```text
Instagram
YouTube
Amazon
Google
```

Millions of users.

Users enter:

```text
Wrong Passwords
Wrong Emails
Invalid Data
Unexpected Inputs
```

Applications cannot crash.

Instead:

```text
Detect Error
↓
Handle Error
↓
Continue Running
```

This is why exceptions exist. :contentReference[oaicite:0]{index=0}

---

# 📌 The Exception Hierarchy

Many students don't know this.

Every Python exception inherits from:

```python
BaseException
```

Most application exceptions inherit from:

```python
Exception
```

Example hierarchy:

```text
BaseException
│
├── Exception
│   │
│   ├── ValueError
│   ├── TypeError
│   ├── KeyError
│   ├── IndexError
│   ├── FileNotFoundError
│   ├── ZeroDivisionError
│   ├── NameError
│   └── AttributeError
```

Understanding this helps in interviews.

---

# 📌 try Block

The try block contains code that may fail.

Example:

```python
try:
    number = int(input("Number: "))
```

Python says:

```text
Try running this.
If something goes wrong,
jump to except.
```

---

# 📌 except Block

Handles the error.

Example:

```python
try:
    number = int(input())

except ValueError:
    print("Invalid Number")
```

Output:

```text
Invalid Number
```

Program survives.

---

# 🧠 Mental Model

Think of try-except like a safety net.

```text
Program
   ↓
Risky Operation
   ↓
Exception?
   ↓
YES → except
NO  → continue
```

---

# 📌 Why Generic except Is Dangerous

Bad:

```python
try:
    data = open("users.txt")

except:
    print("Error")
```

Problem:

```text
Hides Real Errors
Makes Debugging Difficult
```

---

Professional Version:

```python
try:
    data = open("users.txt")

except FileNotFoundError:
    print("File Missing")
```

More precise.

More professional.

Python documentation recommends handling specific exceptions whenever possible. ([python.org](https://docs.python.org/3/tutorial/errors.html))

---

# 📌 Multiple Exceptions

Example:

```python
try:

    num = int(input())

    print(100 / num)

except ValueError:

    print("Enter Number")

except ZeroDivisionError:

    print("Cannot Divide By Zero")
```

---

Why?

Because:

```text
Different Errors
Need Different Solutions
```

---

# 📌 Exception Objects

Most beginners ignore this.

Huge mistake.

Example:

```python
try:
    int("abc")

except ValueError as error:
    print(error)
```

Output:

```text
invalid literal for int()
```

The variable:

```python
error
```

contains details about the exception.

---

# Why Exception Objects Matter

Imagine API failure.

```python
except Exception as e:
    log_error(e)
```

Now you know exactly what failed.

---

# 📌 else Block

Very misunderstood topic.

Syntax:

```python
try:
    code

except:
    error

else:
    success
```

---

Example:

```python
try:
    age = int(input())

except ValueError:
    print("Invalid")

else:
    print("Valid Input")
```

---

Important Rule:

```text
else executes ONLY if
NO exception occurs.
```

---

# Why else Exists?

Keeps:

```text
Success Logic
```

separate from:

```text
Error Logic
```

This improves code readability. :contentReference[oaicite:1]{index=1}

---

# 📌 finally Block

One of the most important concepts in backend development.

Runs:

```text
ALWAYS
```

Even if:

```text
Error Happens
Program Returns
Exception Occurs
```

---

Example:

```python
try:
    print(10/0)

except:
    print("Error")

finally:
    print("Cleanup")
```

Output:

```text
Error
Cleanup
```

---

# Real World Example

Database Connection

```python
try:
    connect()

except:
    handle_error()

finally:
    disconnect()
```

Why?

Because resources must always be released.

---

# 📌 Context Managers (New Concept)

Most tutorials don't explain this early.

Modern Python uses:

```python
with
```

instead of manual cleanup.

Example:

```python
with open("data.txt") as file:
    data = file.read()
```

No need:

```python
file.close()
```

Python closes automatically.

This internally uses exception handling.

---

# 📌 Common Exceptions Every Python Developer Must Know

---

## ValueError

Correct datatype.

Wrong value.

Example:

```python
int("hello")
```

---

## TypeError

Wrong datatype operation.

Example:

```python
"5" + 5
```

---

## IndexError

Index doesn't exist.

```python
numbers[100]
```

---

## KeyError

Dictionary key missing.

```python
user["salary"]
```

---

## NameError

Variable doesn't exist.

```python
print(age)
```

---

## AttributeError

Method doesn't exist.

```python
10.upper()
```

---

## FileNotFoundError

File missing.

```python
open("abc.txt")
```

---

## ZeroDivisionError

```python
100 / 0
```

---

# 🎤 Interview Question

## Difference Between ValueError and TypeError?

### ValueError

Correct datatype.

Wrong value.

Example:

```python
int("abc")
```

String expected.

String provided.

But value invalid.

---

### TypeError

Wrong datatype itself.

Example:

```python
"5" + 5
```

String and Integer incompatible.

---

# 📌 Raising Exceptions

Python automatically raises exceptions.

You can create your own.

Example:

```python
age = -5

if age < 0:
    raise ValueError(
        "Age Cannot Be Negative"
    )
```

Output:

```text
ValueError:
Age Cannot Be Negative
```

---

# Why Raise Exceptions?

Business Rules.

Example:

Banking:

```python
if amount <= 0:
    raise ValueError(
        "Invalid Transaction"
    )
```

---

E-Commerce:

```python
if stock == 0:
    raise ValueError(
        "Out Of Stock"
    )
```

---

Authentication:

```python
if not token:
    raise ValueError(
        "Token Missing"
    )
```

Professional software constantly raises exceptions. :contentReference[oaicite:2]{index=2}

---

# 📌 Custom Exceptions

Advanced Topic.

Create your own exception class.

Example:

```python
class InvalidAgeError(Exception):
    pass
```

Usage:

```python
age = -10

if age < 0:
    raise InvalidAgeError(
        "Negative Age"
    )
```

---

# Why Custom Exceptions?

More readable.

Instead of:

```python
ValueError
```

you get:

```python
InvalidAgeError
```

Much clearer.

---

# Example: Banking System

```python
class InsufficientFundsError(Exception):
    pass
```

Usage:

```python
if withdraw > balance:
    raise InsufficientFundsError(
        "Not Enough Balance"
    )
```

Real-world backend systems use custom exceptions extensively.

---

# 📌 Exception Chaining

Advanced Interview Topic.

Example:

```python
try:
    int("abc")

except ValueError as e:
    raise RuntimeError(
        "User Input Failed"
    ) from e
```

Now Python remembers:

```text
Original Error
+
New Error
```

Useful for debugging large systems.

---

# 📌 Logging Exceptions

Never do:

```python
except:
    print("Error")
```

Professional apps use:

```python
import logging
```

Example:

```python
logging.error(error)
```

Why?

Because production servers don't have a terminal open.

Logs are essential.

---

# 📌 Assertions

Another overlooked feature.

Example:

```python
age = 20

assert age >= 18
```

If false:

```python
AssertionError
```

---

Used for:

```text
Testing
Validation
Debugging
```

---

# 🚀 EAFP vs LBYL

Very popular Python interview topic.

---

## LBYL

Look Before You Leap

```python
if key in data:
    print(data[key])
```

---

## EAFP

Easier to Ask Forgiveness than Permission

```python
try:
    print(data[key])

except KeyError:
    pass
```

Python culture generally prefers EAFP.

Very important interview topic.

---

# 🏗️ Project Idea 1 — ATM System

Features:

```text
Deposit
Withdraw
Check Balance
Custom Exceptions
Validation
```

Errors handled:

```text
Invalid Amount
Insufficient Funds
Wrong Input
```

---

# 🏗️ Project Idea 2 — Login System

Handle:

```text
Wrong Username
Wrong Password
Empty Fields
Invalid Input
```

Using:

```python
raise
try
except
```

---

# 🏗️ Project Idea 3 — Student Result Manager

Validate:

```text
Marks
Age
Name
```

Handle:

```text
Out Of Range Values
Wrong Datatypes
Missing Data
```

---

# 💼 Backend Connection

FastAPI:

```python
raise HTTPException(
    status_code=404,
    detail="User Not Found"
)
```

---

Django:

```python
try:
    user = User.objects.get(id=1)

except User.DoesNotExist:
    pass
```

---

Database:

```python
try:
    save()

except DatabaseError:
    rollback()
```

Every backend application depends heavily on exception handling.

---

# 🎤 Advanced Interview Questions

## Q1. Why should you avoid a bare except?

A bare except catches every exception, including unexpected programming mistakes. This can hide bugs and make debugging difficult. Specific exceptions are safer because they handle only expected failures.

---

## Q2. Difference Between except Exception and except ValueError?

except ValueError catches only ValueError.

except Exception catches almost all application exceptions.

Specific exceptions should generally come first.

---

## Q3. Why is finally important?

finally guarantees execution regardless of success or failure.

It is commonly used for:

- Closing files
- Closing database connections
- Releasing resources
- Cleanup operations

---

## Q4. What is exception propagation?

If an exception is not handled, Python moves upward through function calls searching for a handler.

If no handler exists:

```text
Program Crashes
```

---

## Q5. What is a custom exception?

A user-defined exception class created by inheriting from Exception.

Used to represent business-specific failures.

---

## Q6. What is the purpose of raise?

raise manually creates an exception.

Useful for:

- Validation
- Business Rules
- Security Checks
- API Error Responses

---

## Q7. Difference Between Error Handling and Validation?

Validation checks whether input is acceptable.

Error Handling deals with unexpected failures.

Both are essential.

---

## Q8. Why do production APIs return errors instead of crashing?

Because users should receive meaningful responses while the application continues serving other requests.

Example:

```json
{
  "error": "Invalid Email"
}
```

instead of:

```text
500 Internal Server Error
```

---

# 🏆 Day 10 Success Checklist

- ✅ Learned Exceptions
- ✅ Learned try
- ✅ Learned except
- ✅ Learned else
- ✅ Learned finally
- ✅ Learned specific exceptions
- ✅ Learned exception objects
- ✅ Learned raise
- ✅ Learned custom exceptions
- ✅ Learned assertions
- ✅ Learned logging basics
- ✅ Learned EAFP vs LBYL
- ✅ Learned backend error handling patterns

---

# 🎯 Day 10 Result

You can now write programs that survive invalid input, handle failures gracefully, enforce business rules, create custom exceptions, and build software that behaves like real-world production applications.

This is one of the biggest transitions in your Python journey:

```text
Beginner:
Makes Programs Work

Professional:
Makes Programs Work
AND
Makes Programs Fail Safely
✅