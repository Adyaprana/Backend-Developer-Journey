
# LeetCode 619 — Biggest Single Number

![Difficulty](https://img.shields.io/badge/Difficulty-Easy-success)
![Database](https://img.shields.io/badge/Database-PostgreSQL-blue)
![Topic](https://img.shields.io/badge/Topic-GROUP_BY_+_HAVING_+_Subquery-orange)

---

# Problem Link

https://leetcode.com/problems/biggest-single-number/

---

# Problem Statement

Write a SQL query to find the **largest number that appears exactly once**.

If there is **no single number**, return **NULL**.

Return:

- num

---

# Table Schema

## MyNumbers

| Column | Type |
|---------|------|
| num | int |

The table may contain duplicate numbers.

---

# Create Table

```sql
CREATE TABLE MyNumbers (
    num INT
);
```

---

# Insert Sample Data

```sql
INSERT INTO MyNumbers VALUES
(8),
(8),
(3),
(3),
(1),
(4),
(5),
(6),
(6);
```

---

# View Table

```sql
SELECT * FROM MyNumbers;
```

---

# Expected Output

| num |
|-----|
|5|

Unique numbers are:

```
1
4
5
```

Largest = **5**

---

# My Solution

```sql
SELECT
    MAX(num) AS num
FROM
(
    SELECT
        num
    FROM MyNumbers
    GROUP BY num
    HAVING COUNT(*) = 1
) AS unique_numbers;
```

---

# Explanation

The problem asks for the **largest number that appears exactly once**.

First, we group numbers and keep only those appearing once using `HAVING COUNT(*) = 1`.

Then we apply `MAX()` to those remaining numbers.

If no unique numbers exist, `MAX()` automatically returns `NULL`.

---

# Query Breakdown

### Inner Query

```sql
SELECT
    num
FROM MyNumbers
GROUP BY num
HAVING COUNT(*) = 1;
```

Returns only unique numbers.

Example

| num |
|-----|
|1|
|4|
|5|

---

### Outer Query

```sql
SELECT MAX(num)
```

Returns the largest unique number.

If the inner query returns no rows:

```
MAX()
```

returns

```
NULL
```

which is exactly what the problem requires.

---

# Approach

1. Group numbers.
2. Keep only numbers appearing once.
3. Use MAX() to find the largest one.
4. Return NULL automatically if none exist.

---

# Why This Approach?

Using only

```sql
ORDER BY num DESC
LIMIT 1
```

returns **no rows** when no unique number exists.

Using

```sql
MAX()
```

returns

```
NULL
```

which satisfies the problem requirements.

---

# Visualization

Original Table

| num |
|-----|
|8|
|8|
|3|
|3|
|1|
|4|
|5|
|6|
|6|

After GROUP BY

| num | count |
|-----|-------|
|1|1|
|3|2|
|4|1|
|5|1|
|6|2|
|8|2|

After HAVING

| num |
|-----|
|1|
|4|
|5|

MAX()

```
5
```

---

# Special Case

Input

| num |
|-----|
|1|
|1|
|2|
|2|

After HAVING

```
Empty Table
```

MAX()

```
NULL
```

---

# Time Complexity

Let **n** be the number of rows.

**Time Complexity**

```
O(n)
```

---

# Space Complexity

```
O(k)
```

Where **k** is the number of distinct numbers.

---

# Interview Questions

### Q1. Why GROUP BY?

To count occurrences of each number.

---

### Q2. Why HAVING?

To keep only numbers appearing exactly once.

---

### Q3. Why MAX()?

To return the largest unique number.

---

### Q4. Why not ORDER BY DESC LIMIT 1?

Because if no unique numbers exist, it returns **no rows**, not **NULL**.

---

### Q5. What does MAX() return on an empty table?

```
NULL
```

---

# Common Mistakes

❌

```sql
ORDER BY num DESC
LIMIT 1
```

Returns zero rows when no unique number exists.

---

❌

```sql
HAVING COUNT(num)=1
AND num=MAX(num)
```

`MAX(num)` is calculated inside each group, so it always equals `num`.

---

# Key Concepts Learned

- GROUP BY
- HAVING
- COUNT()
- MAX()
- Aggregate on Subquery
- NULL

---

# What I Learned

- How to filter grouped data.
- How aggregate functions can be applied to subqueries.
- Why MAX() is useful for returning NULL.
- The difference between LIMIT and aggregate functions.

---

# LeetCode Submission

**Status**

✅ Accepted

**Runtime**

201 ms

**Memory**

0.00 MB

**Language**

PostgreSQL

**Test Cases Passed**

18 / 18

---

# Revision Notes

Remember:

- GROUP BY groups numbers.
- HAVING filters grouped rows.
- MAX() returns the largest value.
- MAX() returns NULL on an empty result.
- Aggregate functions can operate on subqueries.

---

# SQL Keywords Used

- SELECT
- FROM
- GROUP BY
- HAVING
- COUNT()
- MAX()
- Subquery
- AS

---

# Tags

SQL • PostgreSQL • GROUP BY • HAVING • COUNT() • MAX() • Subquery • Aggregate Functions • Database • LeetCode Easy