# 🚀 Day 1 — Python Setup, Variables & Type Conversion

> Week 1 • Day 1
>
> Goal: Understand what Python is, write your first programs, learn variables, data types, type checking, and type conversion.

---

# 📌 Topics Covered

## 1. What is Python?

Python is a high-level, interpreted, general-purpose programming language.

It is used for:

* Backend Development
* Web Development
* AI & Machine Learning
* Automation
* Data Science
* Cybersecurity
* Scripting

---

## Why is Python Popular?

### Advantages

✅ Easy to learn

✅ Easy syntax

✅ Huge community

✅ Large number of libraries

✅ Used by top companies

Examples:

* Google
* Netflix
* Spotify
* Instagram
* Dropbox
* OpenAI

---

# 📌 First Python Program

```python
print("Hello Adyaprana")
```

Output:

```text
Hello Adyaprana
```

---

# 📌 print() Function

Used to display output on screen.

Example:

```python
print("Python")
print(100)
print(True)
```

Output:

```text
Python
100
True
```

---

# 📌 Comments

Comments are ignored by Python.

Used to explain code.

### Single Line Comment

```python
# This is a comment
```

---

### Multi-line Comment

```python
"""
This is
a multi-line
comment
"""
```

---

# 📌 Escape Sequences

Escape sequences allow special formatting.

### New Line

```python
print("Hello\nWorld")
```

Output:

```text
Hello
World
```

---

### Tab

```python
print("Hello\tWorld")
```

Output:

```text
Hello    World
```

---

### Backslash

```python
print("\\")
```

Output:

```text
\
```

---

### Double Quote

```python
print("\"Python\"")
```

Output:

```text
"Python"
```

---

### Single Quote

```python
print("\'Python\'")
```

Output:

```text
'Python'
```

---

# 📌 Variables

Variables store data.

Example:

```python
name = "Adyaprana"
age = 22
cgpa = 9.5
```

---

## Variable Naming Rules

### Valid

```python
name
student_name
age2
my_variable
```

### Invalid

```python
2age
student-name
class
```

---

# 📌 Data Types

Python supports many data types.

---

## String (str)

Stores text.

```python
name = "Adyaprana"
```

---

## Integer (int)

Stores whole numbers.

```python
age = 22
```

---

## Float

Stores decimal numbers.

```python
cgpa = 9.5
```

---

## Boolean

Stores True or False.

```python
is_student = True
```

---

# 📌 Creating Multiple Variables

```python
name = "Adyaprana"
age = 22
cgpa = 9.5
is_student = True
```

---

# 📌 type() Function

Used to check datatype.

Example:

```python
name = "Adyaprana"

print(type(name))
```

Output:

```python
<class 'str'>
```

---

# 📌 Type Conversion

Converting one datatype into another.

---

## String to Integer

```python
age = "23"

age = int(age)
```

---

## String to Float

```python
salary = "50000.50"

salary = float(salary)
```

---

## Integer to String

```python
number = 100

number = str(number)
```

---

## Float to Integer

```python
cgpa = 9.5

cgpa = int(cgpa)
```

Output:

```text
9
```

Decimal part gets removed.

---

# 📌 Day 1 Mini Practice

### Program 1

Print your details.

```python
print("Adyaprana")
print("Bangalore")
```

---

### Program 2

Create 10 variables and print them.

---

### Program 3

Check datatype using type()

---

### Program 4

Convert age string into integer

---

### Program 5

Convert integer into string

---

# 🎯 Interview Questions

## Q1. What is Python?

Python is a high-level interpreted programming language used in backend development, AI, automation, data science, and web development.

---

## Q2. Why is Python called an interpreted language?

Because Python code executes line by line using an interpreter.

---

## Q3. What is a variable?

A variable is a container that stores data values.

Example:

```python
age = 22
```

---

## Q4. What are Python's main data types?

* str
* int
* float
* bool

---

## Q5. What is the difference between int and float?

int:

```python
10
```

float:

```python
10.5
```

---

## Q6. What does type() do?

Returns datatype of a variable.

Example:

```python
type(age)
```

---

## Q7. What is type conversion?

Changing one datatype into another.

Example:

```python
int("23")
```

---

## Q8. Difference between implicit and explicit conversion?

Implicit:

Python automatically converts.

Explicit:

Programmer converts.

Example:

```python
int("23")
```

---

## Q9. What is a comment?

Comments are ignored by Python and used for explanation.

---

## Q10. What are escape sequences?

Special characters beginning with backslash.

Examples:

```python
\n
\t
\\
\"
\'
```

---

# 🔥 Backend Interview Connection

These Day 1 concepts are used everywhere in backend development:

### Variables

```python
username = "admin"
```

---

### Data Types

```python
user_id = 1
price = 99.99
is_active = True
```

---

### Type Conversion

```python
user_id = int(request.query_params["id"])
```

Used constantly in FastAPI and Flask APIs.

---

# 🏆 Day 1 Success Checklist

* ✅ Installed Python
* ✅ Installed VS Code
* ✅ Ran first Python program
* ✅ Learned variables
* ✅ Learned data types
* ✅ Used type()
* ✅ Performed type conversion
* ✅ Learned comments
* ✅ Learned escape sequences
* ✅ Wrote multiple practice programs

---

## Day 1 Result

If you understand everything in this file without looking at notes, you have successfully completed Day 1 and are ready for Day 2: Input, Operators, Strings & Calculator Projec✅