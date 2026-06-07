# 🚀 Day 4 — Loops, Iteration & Pattern Programming

> Week 1 • Day 4
>
> Goal: Learn how to repeat tasks using loops, iterate through strings and lists, use break & continue, solve counting problems, and build logic-heavy programs.

---

# 📌 Topics Covered

## 1. What is a Loop?

## 2. for Loop

## 3. range()

## 4. Looping Through Strings

## 5. Looping Through Lists

## 6. enumerate()

## 7. while Loop

## 8. break Statement

## 9. continue Statement

## 10. Nested Loops

## 11. Pattern Programming

## 12. Multiplication Table Project

## 13. Reverse String Project

## 14. Prime Number Checker

## 15. Prime Numbers 1–100

---

# 🧠 What Is A Loop?

A loop repeatedly executes a block of code.

Without loop:

```python
print("Hello")
print("Hello")
print("Hello")
print("Hello")
print("Hello")
```

With loop:

```python
for i in range(5):
    print("Hello")
```

A loop helps reduce repetition and write efficient code.

---

# 📌 for Loop

Used when the number of iterations is known.

Syntax:

```python
for variable in sequence:
    code
```

Example:

```python
for i in range(5):
    print(i)
```

Output:

```text
0
1
2
3
4
```

---

# 📌 range()

Generates a sequence of numbers.

Syntax:

```python
range(start, stop, step)
```

---

## Example 1

```python
for i in range(5):
    print(i)
```

Output:

```text
0 1 2 3 4
```

---

## Example 2

```python
for i in range(1, 6):
    print(i)
```

Output:

```text
1 2 3 4 5
```

---

## Example 3

```python
for i in range(2, 11, 2):
    print(i)
```

Output:

```text
2 4 6 8 10
```

---

# 🎯 Interview Question

### Q. Does range(5) include 5?

No.

```python
range(5)
```

Produces:

```text
0 1 2 3 4
```

Stop value is excluded.

---

# 📌 Looping Through Strings

Strings are iterable.

Example:

```python
name = "Adyaprana"

for ch in name:
    print(ch)
```

Output:

```text
A
d
y
a
p
r
a
n
a
```

Every character is accessed one by one.

---

# 📌 Looping Through Lists

Example:

```python
skills = ["Python", "SQL", "Git"]

for skill in skills:
    print(skill)
```

Output:

```text
Python
SQL
Git
```

---

# 📌 enumerate()

Provides index and value together.

Example:

```python
skills = ["Python", "SQL", "Git"]

for index, skill in enumerate(skills):
    print(index, skill)
```

Output:

```text
0 Python
1 SQL
2 Git
```

---

# 🎯 Interview Question

### Q. Why use enumerate()?

Because it gives both:

* Index
* Value

at the same time.

Useful in real-world applications.

---

# 📌 while Loop

Used when number of iterations is unknown.

Syntax:

```python
while condition:
    code
```

Example:

```python
num = 1

while num <= 5:
    print(num)
    num += 1
```

Output:

```text
1
2
3
4
5
```

---

# 🎯 Interview Question

### Difference Between for and while?

for:

Used when iterations are known.

while:

Used when iterations are unknown.

---

# 📌 Infinite Loop

Example:

```python
while True:
    print("Hello")
```

This never stops.

Use carefully.

---

# 📌 break Statement

Stops loop immediately.

Example:

```python
for i in range(10):

    if i == 5:
        break

    print(i)
```

Output:

```text
0
1
2
3
4
```

Loop terminates at 5.

---

# 📌 continue Statement

Skips current iteration.

Example:

```python
for i in range(10):

    if i == 5:
        continue

    print(i)
```

Output:

```text
0
1
2
3
4
6
7
8
9
```

5 is skipped.

---

# 📌 Password Checker

Real-world example using while + break.

```python
password = "python"

while True:

    user = input("Enter Password: ")

    if user == password:
        print("Access Granted")
        break
```

This is a beginner version of authentication systems.

---

# 📌 Nested Loops

Loop inside another loop.

Syntax:

```python
for i in range():
    for j in range():
        code
```

Example:

```python
for i in range(3):
    for j in range(3):
        print("*", end=" ")
    print()
```

Output:

```text
* * *
* * *
* * *
```

---

# 📌 Pattern Programming

## Square Pattern

```python
for i in range(5):
    for j in range(5):
        print("*", end=" ")
    print()
```

Output:

```text
* * * * *
* * * * *
* * * * *
* * * * *
* * * * *
```

---

## Triangle Pattern

```python
for i in range(1, 6):
    for j in range(i):
        print("*", end=" ")
    print()
```

Output:

```text
*
* *
* * *
* * * *
* * * * *
```

Pattern programming builds logic and nested-loop skills.

---

# 🏗️ Project 1 — Multiplication Table

Example:

```python
number = 5

for i in range(1, 11):
    print(f"{number} x {i} = {number*i}")
```

Output:

```text
5 x 1 = 5
5 x 2 = 10
...
5 x 10 = 50
```

Uses:

* Input
* Loops
* Arithmetic Operators
* f-Strings

---

# 🏗️ Project 2 — Reverse String

Method 1:

```python
reverse = ""

for ch in text:
    reverse = ch + reverse
```

Method 2:

```python
print(text[::-1])
```

Example:

```text
Python
```

Output:

```text
nohtyP
```

---

# 🏗️ Project 3 — Prime Number Checker

Prime Number:

Only divisible by:

* 1
* Itself

Examples:

```text
2
3
5
7
11
13
17
```

---

Example:

```python
is_prime = True

for i in range(2, num):

    if num % i == 0:
        is_prime = False
        break
```

If divisible by any number:

```text
Not Prime
```

Otherwise:

```text
Prime
```

---

# 🏗️ Project 4 — Print Prime Numbers 1–100

Logic:

```python
for num in range(2,101):
```

Check every number.

Print only primes.

This is your first moderately difficult algorithm.

---

# 📌 Loop Else

Python supports:

```python
for i in range(5):
    print(i)

else:
    print("Loop Finished")
```

Output:

```text
Loop Finished
```

Runs when loop ends normally.

---

# 📌 Counting With Loops

Example:

Count vowels.

```python
word = "python"
count = 0

for ch in word:

    if ch in "aeiou":
        count += 1
```

This concept is extremely important.

---

# 🔥 Important Practice Problems

You solved:

✅ Print 1–100

✅ Even Numbers

✅ Odd Numbers

✅ Sum 1–100

✅ Factorial

✅ Multiplication Table

✅ Reverse String

✅ Count Vowels

✅ Prime Checker

✅ Print Primes 1–100

✅ Password Checker

✅ Star Square Pattern

✅ Star Triangle Pattern

✅ Number Triangle Pattern

These are common beginner coding interview questions.

---

# 💼 Backend Connection

Loops are used everywhere.

Reading Database Records:

```python
for user in users:
```

Processing API Data:

```python
for item in response:
```

Log Analysis:

```python
for line in file:
```

Email Sending:

```python
for user in subscribers:
```

Loops are one of the most used programming concepts in backend development.

---

# 🎤 Most Important Interview Questions

## Q1. What is a loop?

A loop repeatedly executes code.

---

## Q2. Difference between for and while?

for:

Known iterations.

while:

Unknown iterations.

---

## Q3. What is range()?

Generates a sequence of numbers.

---

## Q4. Does range(10) include 10?

No.

It stops at 9.

---

## Q5. What does break do?

Stops loop immediately.

---

## Q6. What does continue do?

Skips current iteration.

---

## Q7. What is an infinite loop?

A loop that never stops.

Example:

```python
while True:
```

---

## Q8. What is enumerate()?

Returns index and value together.

---

## Q9. What is a nested loop?

Loop inside another loop.

---

## Q10. What is a prime number?

Only divisible by 1 and itself.

---

## Q11. What is factorial of 5?

```text
5 × 4 × 3 × 2 × 1 = 120
```

---

## Q12. Why are loops important?

They automate repetitive tasks and process large amounts of data efficiently.

---

# 🏆 Day 4 Success Checklist

* ✅ Learned for loop
* ✅ Learned range()
* ✅ Learned enumerate()
* ✅ Learned string iteration
* ✅ Learned list iteration
* ✅ Learned while loop
* ✅ Learned break
* ✅ Learned continue
* ✅ Learned nested loops
* ✅ Built multiplication table
* ✅ Built reverse string program
* ✅ Built prime checker
* ✅ Printed primes 1–100
* ✅ Solved pattern programs

---

# 🎯 Day 4 Result

You can now automate repetitive tasks, process collections of data, build pattern programs, solve prime-number problems, and write logic that repeats efficiently.

You are ready for Day 5:

Lists, Tuples, Indexing, Slicing, List Methods, and Collection Handling.
