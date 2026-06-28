# LeetCode 570 — Managers with at Least 5 Direct Reports

![Difficulty](https://img.shields.io/badge/Difficulty-Medium-orange)
![Database](https://img.shields.io/badge/Database-PostgreSQL-blue)
![Topic](https://img.shields.io/badge/Topic-Self_JOIN_+_GROUP_BY_+_HAVING-orange)

---

# Problem Link

https://leetcode.com/problems/managers-with-at-least-5-direct-reports/

---

# Problem Statement

Write a SQL query to find the names of managers who have **at least 5 direct reports**.

Return the manager names.

The result can be returned in any order.

---

# Table Schema

## Employee

| Column | Type |
|---------|------|
| id | int |
| name | varchar |
| department | varchar |
| managerId | int |

- `id` is the primary key.
- `managerId` references another employee's `id`.

---

# Create Table

```sql
CREATE TABLE Employee (
    id INT PRIMARY KEY,
    name VARCHAR(50),
    department VARCHAR(50),
    managerId INT
);
```

---

# Insert Sample Data

```sql
INSERT INTO Employee VALUES
(101,'John','A',NULL),
(102,'Dan','A',101),
(103,'James','A',101),
(104,'Amy','A',101),
(105,'Anne','A',101),
(106,'Ron','B',101),
(107,'Sam','B',102);
```

---

# View Table

```sql
SELECT * FROM Employee;
```

---

# Expected Output

| name |
|------|
| John |

John manages Dan, James, Amy, Anne, and Ron.

Total direct reports = **5**

---

# My Solution

```sql
SELECT
    m.name AS name
FROM Employee e
JOIN Employee m
ON m.id = e.managerId
GROUP BY m.id, m.name
HAVING COUNT(*) >= 5;
```

---

# Explanation

Managers and employees are stored in the same table.

We perform a **Self JOIN** to connect each employee with their manager.

Then we group employees by their manager and count the number of direct reports.

Finally, we keep only managers with at least **5** direct reports.

---

# Query Breakdown

### SELECT

```sql
SELECT
    m.name AS name
```

Returns the manager's name.

---

### FROM

```sql
FROM Employee e
```

`e` represents employees.

---

### JOIN

```sql
JOIN Employee m
```

`m` represents managers.

---

### ON

```sql
ON m.id = e.managerId
```

Matches every employee with their manager.

---

### GROUP BY

```sql
GROUP BY
    m.id,
    m.name
```

Creates one group for each manager.

---

### HAVING

```sql
HAVING COUNT(*) >= 5;
```

Keeps only managers with at least five direct reports.

---

# Approach

1. Treat Employee as two tables using aliases.
2. Join employees with their managers.
3. Group employees by manager.
4. Count employees in each group.
5. Return managers having at least five reports.

---

# Why This Approach?

Each employee stores their manager's id.

A Self JOIN connects employees to managers.

`GROUP BY` groups all employees under each manager.

`COUNT(*)` counts direct reports.

`HAVING` filters managers based on the count.

---

# Self JOIN Visualization

Employee

| id | name | managerId |
|----|------|-----------|
|102|Dan|101|
|103|James|101|
|104|Amy|101|
|105|Anne|101|
|106|Ron|101|

Manager

| id | name |
|----|------|
|101|John|

After JOIN

| Manager | Employee |
|----------|----------|
|John|Dan|
|John|James|
|John|Amy|
|John|Anne|
|John|Ron|

COUNT(*)

```
John = 5
```

HAVING

```
5 >= 5
```

Return

```
John
```

---

# Time Complexity

Let **n** be the number of employees.

**Time Complexity**

```
O(n)
```

---

# Space Complexity

```
O(k)
```

Where **k** is the number of managers.

---

# Interview Questions

### Q1. Why use a Self JOIN?

Because managers and employees are stored in the same table.

---

### Q2. Why GROUP BY manager?

To count the number of employees under each manager.

---

### Q3. Why HAVING instead of WHERE?

HAVING filters aggregated results.

---

### Q4. Why COUNT(*)?

To count the total number of direct reports.

---

### Q5. Why group by both `m.id` and `m.name`?

`m.id` uniquely identifies the manager, while `m.name` is selected in the output. Grouping by both satisfies SQL grouping rules.

---

# Common Mistakes

❌ Using WHERE COUNT(*)

```sql
WHERE COUNT(*) >= 5
```

Aggregate functions cannot be used inside WHERE.

---

❌ Joining on the wrong columns

```sql
e.id = m.id
```

Incorrect.

Correct:

```sql
m.id = e.managerId
```

---

❌ Forgetting GROUP BY

Without grouping, SQL cannot count reports per manager.

---

# Key Concepts Learned

- Self JOIN
- GROUP BY
- HAVING
- COUNT(*)
- Table Aliases

---

# What I Learned

- How to count related rows using a Self JOIN.
- How GROUP BY works with joined tables.
- Why HAVING filters aggregate results.
- How managers and employees can exist in the same table.

---

# LeetCode Submission

**Status**

✅ Accepted

**Language**

PostgreSQL

---

# Revision Notes

Remember:

- Self JOIN connects employees to managers.
- GROUP BY creates one row per manager.
- COUNT(*) counts direct reports.
- HAVING filters grouped data.

---

# SQL Keywords Used

- SELECT
- FROM
- JOIN
- ON
- GROUP BY
- HAVING
- COUNT(*)

---

# Tags

SQL • PostgreSQL • Self JOIN • GROUP BY • HAVING • COUNT() • Database • LeetCode Medium