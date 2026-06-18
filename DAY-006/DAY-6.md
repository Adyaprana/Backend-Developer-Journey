# 🚀 Day 6 — Dictionaries, Sets & Real-World Data Modeling

> Week 1 • Day 6
>
> Goal: Learn how Python stores real-world data using Dictionaries and Sets. Understand API responses, JSON data, nested dictionaries, and unique-value handling.

---

# 🎯 Why Day 6 Is Important

Days 1–5 taught you:

```text
Variables
Input
Conditions
Loops
Lists
Tuples
```

Day 6 teaches how real applications store data.

When you become a Backend Developer, almost every API response will look like:

```json
{
  "name": "Adyaprana",
  "age": 23,
  "city": "Bangalore"
}
```

This is a Dictionary.

Most backend development is:

```text
Receive JSON
↓
Convert to Dictionary
↓
Process Data
↓
Return Dictionary
↓
Convert back to JSON
```

That is why Dictionaries are one of the most important Python concepts.

---

# 📌 What Is A Dictionary?

A Dictionary stores data as:

```text
KEY : VALUE
```

Example:

```python
student = {
    "name": "Adyaprana",
    "age": 23,
    "city": "Bangalore"
}
```

Think of an ID card:

```text
Name  → Adyaprana
Age   → 23
City  → Bangalore
```

Each label is a KEY.

Each stored value is a VALUE.

---

# 🤔 Why Not Use A List?

List:

```python
data = ["Adyaprana", 23, "Bangalore"]
```

To get age:

```python
data[1]
```

Question:

```text
What is index 1?
```

Hard to understand.

Dictionary:

```python
student["age"]
```

Much clearer.

This is why databases, APIs, and backend applications heavily use dictionaries.

---

# 📌 Characteristics of Dictionaries

### Mutable

Can be modified.

```python
student["age"] = 24
```

---

### Unordered (Conceptually)

Access is by key, not position.

---

### Key Must Be Unique

Wrong:

```python
student = {
    "name": "Adyaprana",
    "name": "Hari"
}
```

Output:

```python
{
    "name": "Hari"
}
```

Second key overwrites first.

---

# 📌 Creating Dictionaries

```python
student = {
    "name": "Adyaprana",
    "roll": "25mcac57",
    "age": 23,
    "course": "MCA"
}
```

---

# 📌 Accessing Values

```python
print(student["name"])
```

Output:

```text
Adyaprana
```

---

```python
print(student["age"])
```

Output:

```text
23
```

---

# 📌 get() Method

Professional developers usually use:

```python
student.get("name")
```

instead of

```python
student["name"]
```

Why?

Because missing keys cause errors.

---

Example:

```python
student.get("salary")
```

Output:

```python
None
```

No error.

This is extremely important in APIs because API data may not always contain every field.

---

# 🎤 Interview Question

### Why Use get() Instead of []?

Because:

```python
student["salary"]
```

causes:

```python
KeyError
```

while:

```python
student.get("salary")
```

returns:

```python
None
```

Safer.

---

# 📌 Updating Values

```python
student["age"] = 24
```

Output:

```python
{
    "age": 24
}
```

---

# 📌 Adding New Key

```python
student["city"] = "Bangalore"
```

Output:

```python
{
    "city": "Bangalore"
}
```

---

# 📌 Deleting Data

### del

```python
del student["city"]
```

---

### pop()

```python
student.pop("age")
```

---

# 📌 keys()

Returns all keys.

```python
student.keys()
```

Output:

```python
dict_keys(
['name','roll','age']
)
```

---

# 📌 values()

Returns all values.

```python
student.values()
```

---

# 📌 items()

Returns both.

```python
student.items()
```

Output:

```python
('name', 'Adyaprana')
```

---

# 📌 Loop Through Dictionary

One of the most important concepts.

```python
for key, value in student.items():
    print(key, value)
```

Output:

```text
name Adyaprana
roll 25mcac57
age 23
```

---

# 📌 Nested Dictionaries

Dictionary inside Dictionary.

Example:

```python
student = {
    "name":"Adyaprana",
    "address":{
        "city":"Bangalore"
    }
}
```

Access:

```python
student["address"]["city"]
```

Output:

```text
Bangalore
```

---

# 🚀 Why Nested Dictionaries Matter

Because API responses look like this:

```python
response = {
    "user":{
        "id":1,
        "name":"Adyaprana",
        "profile":{
            "city":"Bangalore"
        }
    }
}
```

Access:

```python
response["user"]["profile"]["city"]
```

Output:

```text
Bangalore
```

This is exactly how FastAPI and REST APIs return data.

---

# 📌 Real Backend Example

Imagine:

```json
{
  "user": {
    "id": 1,
    "name": "Adyaprana",
    "email": "test@gmail.com"
  }
}
```

Backend receives:

```python
data["user"]["email"]
```

Every day.

---

# 📌 Sets

A Set stores unique values.

Example:

```python
numbers = {1,2,3,3,3,4}
```

Output:

```python
{1,2,3,4}
```

Duplicates automatically removed.

---

# Why Use Sets?

### Remove Duplicates

```python
emails = [
  "a@gmail.com",
  "a@gmail.com",
  "b@gmail.com"
]

unique = set(emails)
```

---

### Fast Searching

Faster than lists.

---

### Validation

Check whether item already exists.

---

# 📌 Set Operations

Assume:

```python
A = {1,2,3,4}
B = {3,4,5,6}
```

---

# Union

Combine everything.

```python
A | B
```

Output:

```python
{1,2,3,4,5,6}
```

---

# Intersection

Common elements.

```python
A & B
```

Output:

```python
{3,4}
```

---

# Difference

Unique values.

```python
A - B
```

Output:

```python
{1,2}
```

---

# 🎤 Interview Question

### List vs Set

| List               | Set           |
| ------------------ | ------------- |
| Duplicates Allowed | No Duplicates |
| Ordered            | Unordered     |
| Slower Search      | Faster Search |

---

# 📌 Dictionary Comprehension

Just like List Comprehension.

Traditional:

```python
squares = {}

for i in range(5):
    squares[i] = i*i
```

---

Pythonic:

```python
squares = {
    i:i*i
    for i in range(5)
}
```

Output:

```python
{
 0:0,
 1:1,
 2:4,
 3:9,
 4:16
}
```

---

# 🏗️ Project 1 — Student Grade Book

Structure:

```python
student_grade_book = {
   "stu-1": {
      ...
   }
}
```

Each student contains:

```python
name
roll
course
grades
```

This is a real-world data model.

---

# Concepts Used

### Nested Dictionary

### Looping Through Dictionary

### Calculating Percentage

### Pass/Fail Logic

### Aggregation

These are backend concepts.

---

# 🏗️ Project 2 — Word Frequency Counter

Input:

```text
python is good python is easy
```

Output:

```python
{
 'python':2,
 'is':2,
 'good':1,
 'easy':1
}
```

---

# How It Works

Step 1:

```python
words = text.split()
```

Result:

```python
['python','is','good']
```

---

Step 2:

Create empty dictionary.

```python
frequency = {}
```

---

Step 3:

Count words.

```python
if word in frequency:
```

Update count.

Otherwise:

```python
frequency[word] = 1
```

This is a very common interview problem.

---

# 🔥 Additional Practice Completed

You solved:

✅ Create Dictionaries

✅ Access Values

✅ Update Values

✅ Delete Values

✅ keys()

✅ values()

✅ items()

✅ Nested Dictionaries

✅ Student Database

✅ Employee Database

✅ Dictionary Comprehension

✅ Student Grade Book✅ Word Frequency Counter

---

# 💼 Backend Connection

FastAPI Response:

```python
return {
    "id":1,
    "name":"Adyaprana"
}
```

Dictionary.

---

Database Record:

```python
user = {
   "id":1,
   "email":"test@gmail.com"
}
```

Dictionary.

---

JWT Token Payload:

```python
payload = {
   "user_id":1
}
```

Dictionary.

---

JSON Response:

```json
{
  "success": true
}
```

Dictionary.

Backend development = Dictionaries everywhere.

---

# 🎤 Most Important Interview Questions

## Q1. What is a Dictionary?

Key-value data structure.

---

## Q2. Why use Dictionary over List?

More readable and faster lookup by key.

---

## Q3. What does get() do?

Safely retrieves value.

---

## Q4. Difference between [] and get()?

[] → KeyError

get() → None

---

## Q5. What does keys() return?

All keys.

---

## Q6. What does values() return?

All values.

---

## Q7. What does items() return?

Key-value pairs.

---

## Q8. What is Nested Dictionary?

Dictionary inside dictionary.

---

## Q9. What is a Set?

Collection of unique values.

---

## Q10. Why use Sets?

Remove duplicates and fast searching.

---

## Q11. What is Union?

Combines all values.

---

## Q12. What is Intersection?

Returns common values.

---

## Q13. What is Dictionary Comprehension?

Compact way to create dictionaries.

---

## Q14. What is Word Frequency Counter?

Counts occurrence of each word.

Very common interview question.

---

# 🏆 Day 6 Success Checklist

* ✅ Learned Dictionaries
* ✅ Learned get()
* ✅ Learned update/delete
* ✅ Learned keys()
* ✅ Learned values()
* ✅ Learned items()
* ✅ Learned Dictionary Looping
* ✅ Learned Nested Dictionaries
* ✅ Learned Sets
* ✅ Learned Set Operations
* ✅ Learned Dictionary Comprehension
* ✅ Built Student Grade Book
* ✅ Built Word Frequency Counter

---

# 🎯 Day 6 Result

You can now model real-world data structures, process API-like responses, build nested data models, count information efficiently, and work with unique datasets.

You are ready for Day 7:

Functions, Parameters, Return Values, Scope, Lambda Functions, and Modular Programming.
