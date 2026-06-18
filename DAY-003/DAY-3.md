# 🚀 Day 3 — Conditions, Comparison Operators & Decision Making

> Week 1 • Day 3
>
> Goal: Learn how programs make decisions using if, elif, else, comparison operators, logical operators, and nested conditions.

---

# 📌 Topics Covered

## 1. if✅

## 2. if-else Statement

## 3. elif Statement

## 4. Comparison Operators

## 5. Logical Operators

## 6. Nested if

## 7. Membership Operator (in)

## 8. Grade Calculator Project

## 9. FizzBuzz Problem

---

# 🧠 Why Conditions Matter

Until Day 2, your programs executed every line.

Now your programs can make decisions.

Example:

```python
age = 20

if age >= 18:
    print("Adult")
```

Output:

```text
Adult
```

This is the foundation of:

* Login Systems
* Authentication
* Banking Apps
* E-Commerce
* APIs
* Backend Development

---

# 📌 if Statement

Used when there is only one condition.

Syntax:

```python
if condition:
    code
```

Example:

```python
age = 23

if age >= 18:
    print("You are an adult")
```

---

# 📌 if-else Statement

Used when there are two possibilities.

Syntax:

```python
if condition:
    code
else:
    code
```

Example:

```python
age = 16

if age >= 18:
    print("Adult")
else:
    print("Minor")
```

---

# 📌 elif Statement

Used when there are multiple conditions.

Syntax:

```python
if condition:
    code

elif condition:
    code

else:
    code
```

Example:

```python
marks = 85

if marks >= 90:
    print("A")
elif marks >= 80:
    print("B")
else:
    print("Fail")
```

---

# 📌 Comparison Operators

Used to compare values.

Output is always:

```python
True
```

or

```python
False
```

---

## Equal To

```python
5 == 5
```

Output:

```python
True
```

---

## Not Equal To

```python
5 != 5
```

Output:

```python
False
```

---

## Greater Than

```python
5 > 3
```

Output:

```python
True
```

---

## Less Than

```python
5 < 3
```

Output:

```python
False
```

---

## Greater Than Equal To

```python
5 >= 5
```

Output:

```python
True
```

---

## Less Than Equal To

```python
5 <= 5
```

Output:

```python
True
```

---

# 🎯 Interview Question

### Q. What do comparison operators return?

Answer:

They return Boolean values:

```python
True
False
```

Comparison operators are heavily used inside conditions.

---

# 📌 Logical Operators

Used to combine conditions.

---

## AND

Both conditions must be true.

```python
age = 25
citizen = True

if age >= 18 and citizen:
    print("Eligible")
```

Output:

```text
Eligible
```

---

### Truth Table

```text
True AND True     = True
True AND False    = False
False AND True    = False
False AND False   = False
```

---

## OR

At least one condition must be true.

```python
marks = 80

if marks >= 90 or marks >= 75:
    print("Scholarship Eligible")
```

---

### Truth Table

```text
True OR True      = True
True OR False     = True
False OR True     = True
False OR False    = False
```

---

## NOT

Reverses result.

```python
is_raining = False

if not is_raining:
    print("Go Outside")
```

---

### Truth Table

```text
not True  = False
not False = True
```

---

# 🎯 Interview Question

### Q. Difference between AND and OR?

AND:

All conditions must be true.

OR:

At least one condition must be true.

---

# 📌 Nested if

Nested if means:

IF inside IF.

Example:

```python
age = 20

if age >= 18:

    if age >= 21:
        print("Can Drink")

    else:
        print("Adult")
```

---

## Login System Example

```python
username = "admin"
password = "1234"

if username == "admin":

    if password == "1234":
        print("Login Successful")

    else:
        print("Wrong Password")

else:
    print("Wrong Username")
```

This is your first taste of authentication logic.

---

# 📌 Membership Operator

Checks whether a value exists.

Operator:

```python
in
```

Example:

```python
skills = ["Python", "SQL"]

if "Python" in skills:
    print("Good")
```

Output:

```text
Good
```

---

# 🏗️ Project 1 — Grade Calculator

Problem:

Take marks input.

Output grade.

Example:

```text
90+ = A
80+ = B
70+ = C
60+ = D
50+ = PASS
Below 50 = FAIL
```

---

### Professional Version

```python
if marks > 100 or marks < 0:
    print("Invalid Marks")
```

Input validation is a professional programming skill.

---

# 🏗️ Project 2 — FizzBuzz

Rules:

```text
Divisible by 3      → Fizz
Divisible by 5      → Buzz
Divisible by Both   → FizzBuzz
```

Example:

```python
if num % 3 == 0 and num % 5 == 0:
    print("FizzBuzz")
elif num % 3 == 0:
    print("Fizz")
elif num % 5 == 0:
    print("Buzz")
```

---

# 🚨 Why FizzBuzz Is Famous

Many companies use FizzBuzz to check:

* Logic
* Conditions
* Modulus Operator
* Problem Solving

Surprisingly many candidates fail it.

---

# 🔥 Important Practice Problems

## Even Odd Checker

```python
number % 2 == 0
```

---

## Positive Negative Checker

```python
if num > 0:
```

---

## Largest of 2 Numbers

```python
if num1 > num2:
```

---

## Largest of 3 Numbers

Uses:

```python
and
```

---

## Voting Eligibility

Uses:

```python
age >= 18 and citizen
```

---

## Login System

Uses:

```python
Nested if
```

These are common beginner interview questions.

---

# 💼 Backend Connection

Everything in backend development depends on conditions.

Authentication:

```python
if password_correct:
```

Authorization:

```python
if user.role == "admin":
```

Payments:

```python
if balance >= amount:
```

API Security:

```python
if token_valid:
```

Database Validation:

```python
if email_exists:
```

You will use if statements every single day as a backend developer.

---

# 🎤 Most Important Interview Questions

## Q1. Difference between if and if-else?

if:

One condition.

if-else:

Two possible outcomes.

---

## Q2. Difference between if and elif?

if starts condition chain.

elif adds additional conditions.

---

## Q3. What does == mean?

Checks equality.

---

## Q4. Difference between = and == ?

```python
=
```

Assignment.

```python
==
```

Comparison.

---

## Q5. What does != mean?

Not Equal To.

---

## Q6. What is a Boolean?

A datatype with only:

```python
True
False
```

---

## Q7. What does AND do?

Returns True only if all conditions are True.

---

## Q8. What does OR do?

Returns True if at least one condition is True.

---

## Q9. What does NOT do?

Reverses result.

---

## Q10. What is Nested if?

An if statement inside another if statement.

---

## Q11. What is Membership Operator?

Checks existence.

Example:

```python
"Python" in skills
```

---

## Q12. What is FizzBuzz?

A classic interview problem using:

* Conditions
* Modulus
* Logical Operators

---

# 🏆 Day 3 Success Checklist

* ✅ Learned if
* ✅ Learned if-else
* ✅ Learned elif
* ✅ Learned comparison operators
* ✅ Learned logical operators
* ✅ Learned nested if
* ✅ Learned membership operator
* ✅ Built grade calculator
* ✅ Solved FizzBuzz
* ✅ Practiced decision-making problems

---

# 🎯 Day 3 Result

You can now build programs that make decisions, validate input, authenticate users, calculate grades, and solve basic interview problems.

You are ready for Day 4:

Loops (for, while), range(), break, continue, nested loops, and pattern programs.
