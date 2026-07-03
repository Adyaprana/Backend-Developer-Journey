# LeetCode 181 — Employees Earning More Than Their Managers

![Difficulty](https://img.shields.io/badge/Difficulty-Easy-success)
![Database](https://img.shields.io/badge/Database-PostgreSQL-blue)
![Topic](https://img.shields.io/badge/Topic-Self+JOIN-orange)

---

# Problem Link

https://leetcode.com/problems/employees-earning-more-than-their-managers/

---

# Problem Statement

Write a SQL query to find the employees who earn **more than their managers**.

Return the employee names.

The result can be returned in any order.

---

# Table Schema

## Employee

| Column | Type |
|---------|------|
| id | int |
| name | varchar |
| salary | int |
| managerId | int |

- `id` is the primary key.
- `managerId` references another employee's `id`.

---

# Create Table

```sql
CREATE TABLE Employee (
    id INT PRIMARY KEY,
    name VARCHAR(255),
    salary INT,
    managerId INT
);
```

---

# Insert Sample Data

```sql
INSERT INTO Employee (id, name, salary, managerId)
VALUES
(1,'Joe',70000,3),
(2,'Henry',80000,4),
(3,'Sam',60000,NULL),
(4,'Max',90000,NULL);
```

---

# View Data

```sql
SELECT * FROM Employee;
```

---

# Expected Output

| Employee |
|----------|
| Joe |

Joe earns **70,000**, while his manager Sam earns **60,000**.

---

# My Solution

```sql
SELECT
    e2.name AS Employee
FROM Employee e1
JOIN Employee e2
ON e1.id = e2.managerId
WHERE e1.salary < e2.salary;
```

---

# Explanation

Both employees and managers are stored in the **same table**.

To compare an employee's salary with their manager's salary, we join the `Employee` table with itself.

- `e1` represents the **manager**
- `e2` represents the **employee**

We join them where:

```sql
e1.id = e2.managerId
```

Then compare salaries.

If the employee earns more than the manager:

```sql
e2.salary > e1.salary
```

the employee's name is returned.

---

# Query Breakdown

### SELECT

```sql
SELECT
    e2.name AS Employee
```

Returns the employee's name.

---

### FROM

```sql
FROM Employee e1
```

`e1` represents the manager.

---

### JOIN

```sql
JOIN Employee e2
```

Joins the same table again.

`e2` represents the employee.

---

### ON

```sql
ON e1.id = e2.managerId
```

Matches each employee with their manager.

---

### WHERE

```sql
WHERE e1.salary < e2.salary;
```

Returns employees whose salary is greater than their manager's salary.

---

# Approach

1. Treat the Employee table as two separate tables using aliases.
2. One alias represents managers.
3. Another alias represents employees.
4. Match employees with their managers.
5. Compare salaries.
6. Return employee names.

---

# Why This Approach?

Managers are also employees.

Since both exist in the same table, a **Self JOIN** is the correct solution.

Using aliases allows us to compare rows within the same table.

---

# Self JOIN Visualization

Employee Table

| id | name | salary | managerId |
|----|------|--------|-----------|
|1|Joe|70000|3|
|3|Sam|60000|NULL|

After Self Join

| Manager | Employee |
|----------|----------|
|Sam|Joe|

Salary Comparison

```
60000 < 70000
```

Return

```
Joe
```

---

# Time Complexity

Let **n** be the number of employees.

**Time Complexity**

```
O(n)
```

(With indexed joins.)

---

# Space Complexity

```
O(1)
```

Excluding the output.

---

# Interview Questions

### Q1. Why is this called a Self JOIN?

Because the table is joined with itself.

---

### Q2. Why use aliases?

Without aliases SQL cannot distinguish between the two copies of the same table.

---

### Q3. What does `e1` represent?

The manager.

---

### Q4. What does `e2` represent?

The employee.

---

### Q5. Which column connects employees and managers?

`managerId`

---

# Common Mistakes

❌ Joining on the wrong columns

```sql
e1.id = e2.id
```

Incorrect.

---

Correct

```sql
e1.id = e2.managerId
```

---

❌ Comparing salaries in the wrong direction

```sql
e1.salary > e2.salary
```

Would return managers instead of employees.

---

❌ Forgetting table aliases

Self joins always require aliases.

---

# Key Concepts Learned

- SELECT
- FROM
- JOIN
- Self JOIN
- Table Aliases
- WHERE
- Comparison Operators

---

# What I Learned

- How to join a table with itself.
- Why aliases are required in a Self JOIN.
- How manager-employee relationships are represented.
- How to compare values between related rows.

---

# LeetCode Submission

**Status**

✅ Accepted

**Runtime**

220 ms

**Memory**

0.00 MB

**Language**

PostgreSQL

**Test Cases Passed**

14 / 14

---

# Revision Notes

Remember:

- Self JOIN = join a table with itself.
- Always use aliases.
- Match `managerId` with `id`.
- Compare employee salary with manager salary.

---

# SQL Keywords Used

- SELECT
- FROM
- JOIN
- ON
- WHERE
- AS

---

# Tags

SQL • PostgreSQL • Self JOIN • Table Aliases • Database • LeetCode Easy