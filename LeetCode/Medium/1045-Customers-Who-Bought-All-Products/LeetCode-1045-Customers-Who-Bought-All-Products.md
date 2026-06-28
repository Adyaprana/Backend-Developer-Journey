# LeetCode 1045 — Customers Who Bought All Products

![Difficulty](https://img.shields.io/badge/Difficulty-Medium-orange)
![Database](https://img.shields.io/badge/Database-PostgreSQL-blue)
![Topic](https://img.shields.io/badge/Topic-COUNT(DISTINCT)_+_Subquery-orange)

---

# Problem Link

https://leetcode.com/problems/customers-who-bought-all-products/

---

# Problem Statement

Write a SQL query to find the customers who bought **every product** listed in the `Product` table.

Return only the `customer_id`.

The result can be returned in any order.

---

# Table Schema

## Customer

| Column | Type |
|---------|------|
| customer_id | int |
| product_key | int |

Each row indicates that a customer purchased a product.

---

## Product

| Column | Type |
|---------|------|
| product_key | int |

Contains every available product.

---

# Create Tables

```sql
CREATE TABLE Product (
    product_key INT PRIMARY KEY
);

CREATE TABLE Customer (
    customer_id INT,
    product_key INT
);
```

---

# Insert Sample Data

```sql
INSERT INTO Product VALUES
(5),
(6);

INSERT INTO Customer VALUES
(1,5),
(1,6),
(2,5),
(3,5),
(3,6);
```

---

# View Tables

```sql
SELECT * FROM Product;

SELECT * FROM Customer;
```

---

# Expected Output

| customer_id |
|-------------|
|1|
|3|

Customer **1** and **3** purchased every product.

---

# My Solution

```sql
SELECT
    customer_id
FROM Customer
GROUP BY customer_id
HAVING COUNT(DISTINCT product_key) =
(
    SELECT COUNT(*)
    FROM Product
);
```

---

# Explanation

The problem asks us to find customers who purchased **all available products**.

First, we group purchases by customer.

Then we count the number of **different** products purchased by each customer.

Finally, we compare that count with the total number of products in the Product table.

If both counts are equal, the customer bought every product.

---

# Query Breakdown

### SELECT

```sql
SELECT customer_id
```

Returns the customer ID.

---

### GROUP BY

```sql
GROUP BY customer_id
```

Creates one group for each customer.

---

### COUNT(DISTINCT)

```sql
COUNT(DISTINCT product_key)
```

Counts unique products purchased by each customer.

---

### Subquery

```sql
SELECT COUNT(*)
FROM Product
```

Returns the total number of available products.

---

### HAVING

```sql
HAVING COUNT(DISTINCT product_key) =
(
    SELECT COUNT(*)
    FROM Product
)
```

Keeps only customers whose unique product count equals the total number of products.

---

# Approach

1. Group purchases by customer.
2. Count distinct products purchased by each customer.
3. Count total products using a subquery.
4. Compare both counts.
5. Return customers whose counts match.

---

# Why This Approach?

A customer who bought all products must have purchased exactly the same number of **unique products** as exist in the Product table.

Using `COUNT(DISTINCT)` prevents duplicate purchases from being counted multiple times.

---

# Visualization

Customer Table

| Customer | Product |
|----------|---------|
|1|5|
|1|6|
|2|5|
|3|5|
|3|6|

GROUP BY

| Customer | Distinct Products |
|----------|-------------------|
|1|2|
|2|1|
|3|2|

Product Table

| Product |
|---------|
|5|
|6|

Total Products

```
COUNT(*) = 2
```

Comparison

```
Customer 1 → 2 = 2 ✅
Customer 2 → 1 = 2 ❌
Customer 3 → 2 = 2 ✅
```

Return

```
1
3
```

---

# Time Complexity

Let:

- **n** = number of purchase records
- **m** = number of products

**Time Complexity**

```
O(n + m)
```

---

# Space Complexity

```
O(k)
```

Where **k** is the number of customers.

---

# Interview Questions

### Q1. Why use COUNT(DISTINCT)?

To avoid counting duplicate product purchases.

---

### Q2. Why not COUNT(product_key)?

A customer may buy the same product multiple times.

---

### Q3. Why use GROUP BY?

To calculate the product count for each customer.

---

### Q4. Why use a subquery?

To determine the total number of available products.

---

### Q5. Why compare the two counts?

If both counts are equal, the customer has bought every product.

---

# Common Mistakes

❌ Incorrect

```sql
COUNT(product_key)
```

Duplicate purchases would be counted.

---

❌ Incorrect

```sql
SELECT COUNT(DISTINCT product_key)
FROM Customer;
```

This counts products across all customers, not the Product table.

---

Correct

```sql
SELECT COUNT(*)
FROM Product;
```

---

# Key Concepts Learned

- GROUP BY
- HAVING
- COUNT(DISTINCT)
- Scalar Subquery
- Aggregate Functions

---

# What I Learned

- How to count unique values.
- Why DISTINCT is important with COUNT().
- How to compare grouped aggregates with a subquery.
- How scalar subqueries return a single value.

---

# LeetCode Submission

**Status**

✅ Accepted

**Runtime**

473 ms

**Memory**

0.00 MB

**Language**

PostgreSQL

**Test Cases Passed**

9 / 9

---

# Revision Notes

Remember:

- COUNT(DISTINCT) ignores duplicates.
- GROUP BY creates one group per customer.
- HAVING filters grouped data.
- Scalar subqueries return a single value.
- Compare aggregate values using HAVING.

---

# SQL Keywords Used

- SELECT
- FROM
- GROUP BY
- HAVING
- COUNT()
- DISTINCT
- Subquery

---

# Tags

SQL • PostgreSQL • GROUP BY • HAVING • COUNT(DISTINCT) • Subquery • Database • LeetCode Medium