# 🚀 Day 2 — Input, Operators, Strings & Calculator Project

> Week 1 • Day 2
>
> Goal: Learn how to take user input, perform calculations, manipulate strings, and build your first interactive Python project.

---

# 📌 Topics Covered

## 1. User Input

## 2. Type Conversion

## 3. Arithmetic Operators

## 4. String Methods

## 5. f-Strings

## 6. Calculator Project

## 7. Area Calculator Project

---

# 📌 input() Function

The input() function is used to take input from the user.

Example:

```python
name = input("Enter your name: ")
print(name)
```

Output:

```text
Enter your name: Adyaprana
Adyaprana
```

---

# Important Rule

Everything coming from input() is a STRING by default.

Example:

```python
age = input("Enter age: ")
print(type(age))
```

Output:

```python
<class 'str'>
```

---

# Why Type Conversion is Needed

Suppose:

```python
age = input("Enter age: ")
```

If user enters:

```text
23
```

Python still stores it as:

```python
"23"
```

Not:

```python
23
```

Therefore:

```python
age = int(input("Enter age: "))
```

---

# 📌 Type Conversion with Input

## Integer Input

```python
age = int(input("Enter age: "))
```

---

## Float Input

```python
cgpa = float(input("Enter CGPA: "))
```

---

## String Input

```python
name = str(input("Enter name: "))
```

---

# 📌 Interview Question

### Q. Why does Python convert input() into string?

Because Python cannot predict what datatype the user will enter.

Therefore input() always returns a string.

---

# 📌 Arithmetic Operators

Operators are symbols used to perform mathematical operations.

---

## Addition (+)

```python
5 + 3
```

Output:

```text
8
```

---

## Subtraction (-)

```python
10 - 4
```

Output:

```text
6
```

---

## Multiplication (*)

```python
5 * 5
```

Output:

```text
25
```

---

## Division (/)

```python
10 / 2
```

Output:

```text
5.0
```

Always returns float.

---

## Floor Division (//)

```python
10 // 3
```

Output:

```text
3
```

Removes decimal part.

---

## Modulus (%)

```python
10 % 3
```

Output:

```text
1
```

Returns remainder.

---

## Power (**)

```python
2 ** 3
```

Output:

```text
8
```

Means:

```text
2 × 2 × 2
```

---

# 📌 Interview Questions

### Q. Difference between / and // ?

Division (/)

```python
10 / 3
```

Output:

```text
3.3333
```

Floor Division (//)

```python
10 // 3
```

Output:

```text
3
```

---

### Q. What does modulus operator do?

Returns remainder after division.

Example:

```python
10 % 3
```

Output:

```text
1
```

Used heavily for:

* Even/Odd checking
* DSA problems
* Loops

---

# 📌 Strings

A string is a sequence of characters.

Example:

```python
name = "Adyaprana"
```

Datatype:

```python
str
```

---

# 📌 String Methods

---

## upper()

Converts to uppercase.

```python
name.upper()
```

Output:

```text
ADYAPRANA
```

---

## lower()

Converts to lowercase.

```python
name.lower()
```

Output:

```text
adyaprana
```

---

## capitalize()

Capitalizes first character.

```python
name.capitalize()
```

Output:

```text
Adyaprana
```

---

## title()

Capitalizes every word.

```python
title()
```

---

## strip()

Removes spaces from both ends.

```python
" Hello ".strip()
```

Output:

```text
Hello
```

---

## replace()

Replace part of string.

```python
sentence.replace("Python","Java")
```

Output:

```text
I love Java
```

---

## split()

Converts string into list.

```python
text.split()
```

Output:

```python
['Hello', 'How', 'Are', 'You']
```

---

## len()

Returns length.

```python
len("Python")
```

Output:

```text
6
```

---

## index()

Returns position.

```python
name.index("p")
```

Output:

```text
4
```

---

# 📌 String Slicing

```python
name = "Adyaprana"

print(name[0])
print(name[1:5])
```

Output:

```text
A
dyap
```

---

# 📌 Interview Questions

### Q. Are strings mutable?

No.

Strings are immutable.

They cannot be changed after creation.

---

### Q. What is len()?

Returns total number of characters.

---

### Q. What is split() used for?

Splits string into list.

Example:

```python
"Python Java C".split()
```

Output:

```python
['Python', 'Java', 'C']
```

---

# 📌 f-Strings

Modern way of formatting strings.

Old Method:

```python
print("My name is", name)
```

New Method:

```python
print(f"My name is {name}")
```

---

# Advantages of f-Strings

✅ Cleaner

✅ Faster

✅ Easy to read

✅ Used in professional backend development

---

Example:

```python
name = "Adyaprana"
age = 23

print(f"My name is {name}")
print(f"I am {age} years old")
```

---

Expressions inside f-Strings:

```python
print(f"In 5 years I will be {age + 5}")
```

Output:

```text
In 5 years I will be 28
```

---

# 📌 Backend Connection

FastAPI Example:

```python
username = "admin"

return {
    "message": f"Welcome {username}"
}
```

You will use f-strings every day in backend development.

---

# 🏗️ Project 1 — Calculator

Concepts Used:

* input()
* float()
* operators
* variables
* f-strings

Operations:

* Addition
* Subtraction
* Multiplication
* Division
* Floor Division
* Modulus
* Power

This is your first mini real-world project.

---

# 🏗️ Project 2 — Area Calculator

Formulas Learned

Rectangle:

```text
Area = Length × Breadth
```

Triangle:

```text
Area = 0.5 × Base × Height
```

Square:

```text
Area = Side²
```

Circle:

```text
Area = π × r²
```

This project combines:

* Input
* Math
* Variables
* Output formatting

---

# 🔥 Most Important Interview Questions

### Q1. What does input() return?

String

---

### Q2. Why use int() with input()?

To convert string into integer.

---

### Q3. Difference between input() and print()?

input()

Takes data.

print()

Displays data.

---

### Q4. Difference between / and // ?

/ gives decimal

// removes decimal

---

### Q5. What is modulus operator?

Returns remainder.

---

### Q6. What is string slicing?

Extracting part of a string.

Example:

```python
name[1:5]
```

---

### Q7. What are f-strings?

Modern way of formatting strings.

---

### Q8. Why are f-strings important?

Used heavily in:

* FastAPI
* Flask
* Logging
* APIs
* Backend development

---

### Q9. What does len() do?

Returns length of string.

---

### Q10. What does split() do?

Converts string into list.

---

# 🏆 Day 2 Success Checklist

* [x] Learned input()
* [x] Learned type conversion
* [x] Learned arithmetic operators
* [x] Learned string methods
* [x] Learned string slicing
* [x] Learned f-strings
* [x] Built calculator project
* [x] Built area calculator project
* [x] Practiced user input programs
* [x] Understood backend use cases

---

# 🎯 Day 2 Result

You can now create interactive programs that take user input, process data, manipulate strings, and perform calculations.

You are ready for Day 3:

Conditions (if, elif, else), comparison operators, logical operators, and decision-making programs.
