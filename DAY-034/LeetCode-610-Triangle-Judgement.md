# LeetCode 610 — Triangle Judgement

![Difficulty](https://img.shields.io/badge/Difficulty-Easy-success)
![Database](https://img.shields.io/badge/Database-PostgreSQL-blue)
![Topic](https://img.shields.io/badge/Topic-CASE_WHEN-orange)

---

# Problem Link

https://leetcode.com/problems/triangle-judgement/

---

# Problem Statement

Write a SQL query to determine whether three given side lengths can form a triangle.

Return:

- x
- y
- z
- triangle ("Yes" or "No")

A triangle is valid if:

```
x + y > z
y + z > x
x + z > y
```

---

# Table Schema

## Triangle

| Column | Type |
|---------|------|
| x | int |
| y | int |
| z | int |

Each row represents the lengths of three sides.

---

# Create Table

```sql
CREATE TABLE Triangle (
    x INT,
    y INT,
    z INT
);
```

---

# Insert Sample Data

```sql
INSERT INTO Triangle VALUES
(13,15,30),
(10,20,15);
```

---

# View Table

```sql
SELECT * FROM Triangle;
```

---

# Expected Output

| x | y | z | triangle |
|---|---|---|----------|
|13|15|30|No|
|10|20|15|Yes|

---

# My Solution

```sql
SELECT
    x,
    y,
    z,
    CASE
        WHEN x + y > z
         AND y + z > x
         AND x + z > y
        THEN 'Yes'
        ELSE 'No'
    END AS triangle
FROM Triangle;
```

---

# Explanation

The problem requires checking whether three sides satisfy the Triangle Inequality Theorem.

Instead of filtering rows, we return every row and classify it as either:

- Yes
- No

using the `CASE` expression.

---

# Query Breakdown

### SELECT

Returns all three sides.

---

### CASE

Checks whether all three triangle conditions are true.

---

### WHEN

```sql
x+y>z
AND
y+z>x
AND
x+z>y
```

If all conditions are true:

```
Yes
```

Otherwise:

```
No
```

---

### END

Returns the final value in the column named

```
triangle
```

---

# Approach

1. Read each row.
2. Check the triangle inequality.
3. Use CASE to return "Yes" or "No".
4. Display the result.

---

# Why CASE?

The problem doesn't ask us to remove rows.

Instead, every row must be labeled.

CASE is SQL's equivalent of an **if-else** statement.

---

# Visualization

Triangle

| x | y | z |
|---|---|---|
|10|20|15|

Check

```
10+20 >15 ✔
20+15 >10 ✔
10+15 >20 ✔
```

Return

```
Yes
```

---

Triangle

|13|15|30|

Check

```
13+15 >30 ✘
```

Return

```
No
```

---

# Time Complexity

```
O(n)
```

Each row is checked once.

---

# Space Complexity

```
O(1)
```

---

# Interview Questions

### Q1. What is CASE?

CASE is SQL's conditional statement (similar to if-else).

---

### Q2. Why not WHERE?

WHERE removes rows.

The problem requires every row to be returned.

---

### Q3. Can CASE have multiple WHEN clauses?

Yes.

```sql
CASE
WHEN ...
WHEN ...
ELSE ...
END
```

---

### Q4. Why use AND?

A valid triangle must satisfy all three conditions.

---

### Q5. What happens if one condition fails?

The result becomes

```
No
```

---

# Common Mistakes

❌ Using OR

```sql
x+y>z
OR
y+z>x
```

Wrong.

All three conditions must be true.

---

❌ Forgetting ELSE

Always provide an ELSE case.

---

# Key Concepts Learned

- CASE
- WHEN
- THEN
- ELSE
- END
- Boolean Expressions
- AND Operator

---

# What I Learned

- CASE works like if-else in SQL.
- How to create computed columns.
- How to implement business rules inside SQL.
- How to validate triangle conditions.

---

# Revision Notes

Remember:

- CASE is SQL's if-else.
- WHEN checks a condition.
- THEN returns a value.
- ELSE handles all remaining cases.
- END finishes the CASE expression.

---

# SQL Keywords Used

- SELECT
- CASE
- WHEN
- THEN
- ELSE
- END
- AS

---

# Tags

SQL • PostgreSQL • CASE WHEN • Conditional Logic • Database • LeetCode Easy