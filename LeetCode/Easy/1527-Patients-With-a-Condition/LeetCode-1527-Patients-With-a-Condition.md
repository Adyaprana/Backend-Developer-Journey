# LeetCode 1527 — Patients With a Condition

![Difficulty](https://img.shields.io/badge/Difficulty-Easy-success)
![Database](https://img.shields.io/badge/Database-PostgreSQL-blue)
![Topic](https://img.shields.io/badge/Topic-LIKE_+_Wildcards-orange)

---

# Problem Link

https://leetcode.com/problems/patients-with-a-condition/

---

# Problem Statement

Write a SQL query to find all patients who have **Type I Diabetes**.

A patient has Type I Diabetes if the string **DIAB1** appears:

- At the beginning of the `conditions` string.
- Or after a space.

Return:

- patient_id
- patient_name
- conditions

---

# Table Schema

## Patients

| Column | Type |
|---------|------|
| patient_id | int |
| patient_name | varchar |
| conditions | varchar |

Each row contains one patient's medical conditions separated by spaces.

---

# Create Table

```sql
CREATE TABLE Patients (
    patient_id INT PRIMARY KEY,
    patient_name VARCHAR(100),
    conditions VARCHAR(255)
);
```

---

# Insert Sample Data

```sql
INSERT INTO Patients VALUES
(1,'Daniel','YFEV COUGH'),
(2,'Alice','DIAB100 MYOP'),
(3,'Bob','ACNE DIAB100'),
(4,'George','DIAB201'),
(5,'Tom','FEVER');
```

---

# View Table

```sql
SELECT * FROM Patients;
```

---

# Expected Output

| patient_id | patient_name | conditions |
|------------|--------------|------------|
|2|Alice|DIAB100 MYOP|
|3|Bob|ACNE DIAB100|

---

# My Solution

```sql
SELECT
    patient_id,
    patient_name,
    conditions
FROM Patients
WHERE conditions LIKE 'DIAB1%'
   OR conditions LIKE '% DIAB1%';
```

---

# Explanation

The problem asks us to find patients whose conditions contain **DIAB1** as a complete condition code.

There are two possible cases:

1. `DIAB1` is the **first** condition.
2. `DIAB1` appears **after a space**.

The `LIKE` operator with `%` wildcard allows us to match both cases.

---

# Query Breakdown

### SELECT

Returns the required columns.

---

### FROM

Reads data from the Patients table.

---

### WHERE

Filters only patients having Type I Diabetes.

---

### LIKE

```sql
LIKE 'DIAB1%'
```

Matches strings that begin with **DIAB1**.

Example:

```
DIAB100 MYOP
```

---

```sql
LIKE '% DIAB1%'
```

Matches **DIAB1** appearing after a space.

Example:

```
ACNE DIAB100
```

---

# Approach

1. Read all patients.
2. Check if `conditions` starts with `DIAB1`.
3. Otherwise check whether `DIAB1` appears after a space.
4. Return matching patients.

---

# Why This Approach?

Using only

```sql
LIKE '%DIAB1%'
```

would incorrectly match values like

```
XXDIAB100
```

The problem requires `DIAB1` to be a separate condition, either at the beginning or after a space.

---

# Visualization

Patients

| Conditions |
|------------|
|DIAB100 MYOP|
|ACNE DIAB100|
|DIAB201|
|YFEV COUGH|

Check

```
DIAB100 MYOP
```

Matches

```
LIKE 'DIAB1%'
```

✔

---

Check

```
ACNE DIAB100
```

Matches

```
LIKE '% DIAB1%'
```

✔

---

Check

```
DIAB201
```

Does not start with

```
DIAB1
```

✘

---

# Time Complexity

```
O(n × m)
```

Where:

- **n** = number of patients
- **m** = average length of the condition string

---

# Space Complexity

```
O(1)
```

---

# Interview Questions

### Q1. What does `%` mean?

It matches **zero or more characters**.

---

### Q2. What does LIKE do?

It performs pattern matching on strings.

---

### Q3. Why two LIKE conditions?

Because `DIAB1` can appear:

- At the beginning.
- After a space.

---

### Q4. Why not use

```sql
LIKE '%DIAB1%'
```

It would match invalid substrings.

---

### Q5. What does

```sql
'% DIAB1%'
```

mean?

Any characters

↓

Space

↓

DIAB1

↓

Any characters

---

# Common Mistakes

❌

```sql
LIKE '%DIAB1%'
```

Matches unwanted values.

---

❌ Forgetting the space

```sql
'%DIAB1%'
```

Wrong.

Correct

```sql
'% DIAB1%'
```

---

# Key Concepts Learned

- LIKE
- Wildcards (%)
- String Pattern Matching
- WHERE
- OR

---

# What I Learned

- How SQL searches text using LIKE.
- How `%` wildcard works.
- How to match words at the beginning or middle of a string.
- Why pattern matching is important in databases.

---

# LeetCode Submission

**Status**

✅ Accepted

**Runtime**

216 ms

**Memory**

0.00 MB

**Language**

PostgreSQL

**Test Cases Passed**

17 / 17

---

# Revision Notes

Remember:

- `LIKE` searches text patterns.
- `%` means any number of characters.
- `'DIAB1%'` matches at the beginning.
- `'% DIAB1%'` matches after a space.

---

# SQL Keywords Used

- SELECT
- FROM
- WHERE
- LIKE
- OR

---

# Tags

SQL • PostgreSQL • LIKE • Wildcards • Pattern Matching • Database • LeetCode Easy