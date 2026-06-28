# LeetCode 584 — Find Customer Referee

![Difficulty](https://img.shields.io/badge/Difficulty-Easy-success)
![Database](https://img.shields.io/badge/Database-PostgreSQL-blue)
![Topic](https://img.shields.io/badge/Topic-WHERE+NULL-orange)

---

# Problem Link

https://leetcode.com/problems/find-customer-referee/

---

# Problem Statement

Find the names of customers who were **not referred by the customer with id = 2**.

Return the result table in any order.

---

# Table Schema

## Customer

| Column | Type |
|---------|------|
| id | int |
| name | varchar |
| referee_id | int |

- `id` is the primary key.
- `referee_id` stores the id of the customer who referred them.
- `referee_id` can be `NULL`.

---

# Create Table

```sql
CREATE TABLE Customer (
    id INT PRIMARY KEY,
    name VARCHAR(255),
    referee_id INT
);
```

---

# Insert Sample Data

```sql
INSERT INTO Customer (id, name, referee_id)
VALUES
(1,'Will',NULL),
(2,'Jane',NULL),
(3,'Alex',2),
(4,'Bill',NULL),
(5,'Zack',1),
(6,'Mark',2);
```

---

# View Data

```sql
SELECT * FROM Customer;
```

---

# Expected Output

| name |
|------|
| Will |
| Jane |
| Bill |
| Zack |

Alex and Mark are excluded because their `referee_id` is **2**.

---

# My Solution

```sql
SELECT
    name
FROM Customer
WHERE referee_id != 2
   OR referee_id IS NULL;
```

---

# Explanation

The problem asks us to return customers who **were not referred by customer 2**.

There are two valid cases:

- The customer's `referee_id` is **not equal to 2**.
- The customer has **no referee**, meaning `referee_id` is `NULL`.

Since either condition is acceptable, we use the `OR` operator.

---

# Query Breakdown

### SELECT

```sql
SELECT name
```

Returns only the customer's name.

---

### FROM

```sql
FROM Customer
```

Reads data from the Customer table.

---

### WHERE

```sql
WHERE referee_id != 2
   OR referee_id IS NULL;
```

Filters customers whose referee is not customer `2`, or who do not have a referee.

---

# Why `IS NULL`?

In SQL, `NULL` means **unknown or missing value**.

A comparison like:

```sql
referee_id != 2
```

does **not** include rows where `referee_id` is `NULL`.

Therefore, we must explicitly check:

```sql
referee_id IS NULL
```

to include customers with no referee.

---

# Approach

1. Read the `Customer` table.
2. Filter customers whose `referee_id` is not `2`.
3. Also include customers whose `referee_id` is `NULL`.
4. Return only the `name` column.

---

# Why This Approach?

The problem is purely a filtering problem.

No JOINs, GROUP BY, or sorting are required.

The `WHERE` clause with `OR` and `IS NULL` satisfies all conditions.

---

# Time Complexity

Let **n** be the number of rows.

**Time Complexity**

```
O(n)
```

Each row is checked once.

---

# Space Complexity

```
O(1)
```

No extra memory is used.

---

# Interview Questions

### Q1. Why use `IS NULL` instead of `= NULL`?

Because SQL uses `IS NULL` to check for missing values.

---

### Q2. Why isn't `referee_id != 2` enough?

Because comparisons with `NULL` return unknown, so rows with `NULL` would be excluded.

---

### Q3. What does `NULL` represent?

A missing or unknown value.

---

### Q4. Which clause filters rows?

The `WHERE` clause.

---

### Q5. Why use `OR`?

Because either condition should include the customer.

---

# Common Mistakes

❌ Incorrect

```sql
WHERE referee_id != 2;
```

Customers with `NULL` referee values are excluded.

---

❌ Incorrect

```sql
WHERE referee_id = NULL;
```

Always use:

```sql
WHERE referee_id IS NULL;
```

---

# Key Concepts Learned

- SELECT
- FROM
- WHERE
- OR
- NULL
- IS NULL
- Comparison Operators

---

# What I Learned

- How SQL handles `NULL` values.
- Why `IS NULL` is required instead of `= NULL`.
- How to combine multiple conditions using `OR`.
- How to filter data correctly when missing values are present.

---

# LeetCode Submission

**Status**

✅ Accepted

**Runtime**

266 ms

**Memory**

0.00 MB

**Language**

PostgreSQL

**Test Cases Passed**

19 / 19

---

# Revision Notes

Remember:

- `NULL` is not equal to anything.
- Use `IS NULL` to check missing values.
- Use `OR` when either condition should match.
- Always return only the requested columns.

---

# SQL Keywords Used

- SELECT
- FROM
- WHERE
- OR
- IS NULL

---

# Tags

SQL • PostgreSQL • WHERE Clause • NULL Values • Filtering • LeetCode Easy