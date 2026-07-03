# LeetCode 577 — Employee Bonus

![Difficulty](https://img.shields.io/badge/Difficulty-Easy-success)
![Database](https://img.shields.io/badge/Database-PostgreSQL-blue)
![Topic](https://img.shields.io/badge/Topic-LEFT+JOIN-orange)

---

# Problem Link

https://leetcode.com/problems/employee-bonus/

---

# Problem Statement

Write a SQL query to report the **name** and **bonus** of each employee whose bonus is **less than 1000**.

Employees who have **not received a bonus** should also be included.

Return the result table in any order.

---

# Table Schema

## Employee

| Column | Type |
|---------|------|
| empId | int |
| name | varchar |
| supervisor | int |
| salary | int |

- `empId` is the primary key.

---

## Bonus

| Column | Type |
|---------|------|
| empId | int |
| bonus | int |

- `empId` is a foreign key referencing `Employee`.

---

# Create Tables

```sql
CREATE TABLE Employee (
    empId INT PRIMARY KEY,
    name VARCHAR(255),
    supervisor INT,
    salary INT
);

CREATE TABLE Bonus (
    empId INT,
    bonus INT,
    FOREIGN KEY (empId) REFERENCES Employee(empId)
);
```

---

# Insert Sample Data

```sql
INSERT INTO Employee (empId, name, supervisor, salary)
VALUES
(3,'Brad',NULL,4000),
(1,'John',3,1000),
(2,'Dan',3,2000),
(4,'Thomas',3,4000);

INSERT INTO Bonus (empId, bonus)
VALUES
(2,500),
(4,2000);
```

---

# View Data

```sql
SELECT * FROM Employee;

SELECT * FROM Bonus;
```

---

# Expected Output

| name | bonus |
|------|-------|
| Brad | NULL |
| John | NULL |
| Dan | 500 |

Thomas is excluded because his bonus is **2000**, which is greater than or equal to **1000**.

---

# My Solution

```sql
SELECT
    Employee.name,
    Bonus.bonus
FROM Employee
LEFT JOIN Bonus
ON Employee.empId = Bonus.empId
WHERE Bonus.bonus < 1000
   OR Bonus.bonus IS NULL;
```

---

# Explanation

The problem asks us to return every employee whose:

- bonus is less than **1000**, or
- does not have a bonus.

Since employees without a bonus do not have matching rows in the `Bonus` table, we use a **LEFT JOIN**.

After joining, employees without bonuses have `NULL` in the `bonus` column, so we include them using `IS NULL`.

---

# Query Breakdown

### SELECT

```sql
SELECT
    Employee.name,
    Bonus.bonus
```

Returns the required columns.

---

### FROM

```sql
FROM Employee
```

Uses Employee as the primary table.

---

### LEFT JOIN

```sql
LEFT JOIN Bonus
```

Keeps every employee even if they have no bonus record.

---

### ON

```sql
ON Employee.empId = Bonus.empId
```

Matches employees with their bonuses.

---

### WHERE

```sql
WHERE Bonus.bonus < 1000
   OR Bonus.bonus IS NULL;
```

Filters employees whose bonus is less than 1000 or who have no bonus.

---

# Approach

1. Start with the `Employee` table.
2. Use a `LEFT JOIN` to include every employee.
3. Match records using `empId`.
4. Filter employees whose bonus is less than `1000` or `NULL`.
5. Return the employee name and bonus.

---

# Why This Approach?

The problem requires employees without bonuses to appear in the result.

An `INNER JOIN` would remove those employees.

Using a `LEFT JOIN` ensures every employee is included.

---

# Time Complexity

Let:

- **n** = number of employees
- **m** = number of bonus records

**Time Complexity**

```
O(n + m)
```

---

# Space Complexity

```
O(1)
```

(Excluding the output.)

---

# Interview Questions

### Q1. Why use LEFT JOIN?

Because employees without bonus records must also appear.

---

### Q2. Why not INNER JOIN?

INNER JOIN removes employees who don't have matching bonus records.

---

### Q3. Why use `IS NULL`?

Employees without bonus records have `NULL` after the LEFT JOIN.

---

### Q4. Which column is used to join both tables?

`empId`

---

### Q5. Why use OR?

Because either condition qualifies an employee.

---

# Common Mistakes

❌ Using INNER JOIN

```sql
INNER JOIN Bonus
```

Employees without bonuses disappear.

---

❌ Forgetting `IS NULL`

```sql
WHERE bonus < 1000;
```

Employees with no bonus are excluded.

---

❌ Joining on the wrong column

```sql
Employee.salary = Bonus.bonus
```

Always join using the related key (`empId`).

---

# Key Concepts Learned

- SELECT
- FROM
- LEFT JOIN
- ON
- WHERE
- OR
- IS NULL
- Foreign Key

---

# What I Learned

- How LEFT JOIN preserves unmatched rows.
- How NULL values appear after a LEFT JOIN.
- How to filter joined data correctly.
- Why `IS NULL` is necessary after a LEFT JOIN.

---

# LeetCode Submission

**Status**

✅ Accepted

**Language**

PostgreSQL

**Test Cases Passed**

26 / 26

---

# Revision Notes

Remember:

- LEFT JOIN keeps all rows from the left table.
- Missing matches become NULL.
- Use `IS NULL` to include unmatched rows.
- Filter using `WHERE`.

---

# SQL Keywords Used

- SELECT
- FROM
- LEFT JOIN
- ON
- WHERE
- OR
- IS NULL

---

# Tags

SQL • PostgreSQL • LEFT JOIN • NULL Handling • Database • LeetCode Easy