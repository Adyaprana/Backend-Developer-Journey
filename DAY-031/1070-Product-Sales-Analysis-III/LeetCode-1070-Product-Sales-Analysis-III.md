# LeetCode 1070 — Product Sales Analysis III

![Difficulty](https://img.shields.io/badge/Difficulty-Easy-success)
![Database](https://img.shields.io/badge/Database-PostgreSQL-blue)
![Topic](https://img.shields.io/badge/Topic-Subquery_+_JOIN-orange)

---

# Problem Link

https://leetcode.com/problems/product-sales-analysis-iii/

---

# Problem Statement

Write a SQL query to report:

- product_id
- first_year
- quantity
- price

for the **first year** each product was sold.

Return the result table in any order.

---

# Table Schema

## Sales

| Column | Type |
|---------|------|
| sale_id | int |
| product_id | int |
| year | int |
| quantity | int |
| price | int |

- sale_id is the primary key.

---

# Create Table

```sql
CREATE TABLE Sales (
    sale_id INT PRIMARY KEY,
    product_id INT,
    year INT,
    quantity INT,
    price INT
);
```

---

# Insert Sample Data

```sql
INSERT INTO Sales VALUES
(1,100,2008,10,5000),
(2,100,2009,12,5000),
(7,200,2011,15,9000);
```

---

# View Table

```sql
SELECT * FROM Sales;
```

---

# Expected Output

| product_id | first_year | quantity | price |
|------------|------------|----------|-------|
|100|2008|10|5000|
|200|2011|15|9000|

---

# My Solution

```sql
SELECT
    s.product_id,
    f.first_year,
    s.quantity,
    s.price
FROM Sales s
JOIN
(
    SELECT
        product_id,
        MIN(year) AS first_year
    FROM Sales
    GROUP BY product_id
) AS f
ON s.product_id = f.product_id
AND s.year = f.first_year;
```

---

# Explanation

The problem asks for information about the **first sale** of every product.

First, we find the earliest (`MIN`) year for every product.

Then we join that result back to the original Sales table to retrieve the corresponding quantity and price.

---

# Query Breakdown

### Inner Query

```sql
SELECT
    product_id,
    MIN(year) AS first_year
FROM Sales
GROUP BY product_id;
```

Creates a temporary table containing:

| product_id | first_year |
|------------|------------|
|100|2008|
|200|2011|

---

### JOIN

```sql
JOIN (...) AS f
```

Joins the temporary table with the original Sales table.

---

### Matching Condition

```sql
ON s.product_id = f.product_id
AND s.year = f.first_year
```

Matches only the first sale of each product.

---

# Approach

1. Find the minimum year for each product.
2. Store the result as a derived table.
3. Join it with the Sales table.
4. Match product_id and first year.
5. Return the required columns.

---

# Why This Approach?

The first query identifies **which year** was the first sale.

However, it doesn't contain the quantity or price.

Joining back to the original table retrieves those missing columns.

---

# Visualization

Sales

| Product | Year | Qty | Price |
|---------|------|-----|------|
|100|2008|10|5000|
|100|2009|12|5000|
|200|2011|15|9000|

Subquery

| Product | First Year |
|---------|------------|
|100|2008|
|200|2011|

JOIN

| Product | Year | Qty | Price |
|---------|------|-----|------|
|100|2008|10|5000|
|200|2011|15|9000|

---

# Time Complexity

Let **n** be the number of sales records.

**Time Complexity**

```
O(n)
```

The table is scanned once for the subquery and joined efficiently.

---

# Space Complexity

```
O(k)
```

Where **k** is the number of distinct products.

---

# Interview Questions

### Q1. Why use MIN(year)?

To find the earliest sale year for each product.

---

### Q2. Why GROUP BY product_id?

Because we need one earliest year per product.

---

### Q3. Why join back to the Sales table?

The subquery only returns the first year.

The original table contains quantity and price.

---

### Q4. What is a Derived Table?

A temporary result created by a subquery inside the FROM clause.

---

### Q5. Could this be solved using Window Functions?

Yes.

Using `ROW_NUMBER()` or `RANK()`.

---

# Common Mistakes

❌ Forgetting GROUP BY

```sql
SELECT product_id, MIN(year)
```

Invalid.

---

❌ Joining only on product_id

```sql
ON s.product_id = f.product_id
```

This returns every sale for that product.

You must also match

```sql
AND s.year = f.first_year
```

---

# Key Concepts Learned

- GROUP BY
- MIN()
- Subquery
- Derived Table
- INNER JOIN
- Table Aliases

---

# What I Learned

- How to create a derived table using a subquery.
- How to combine aggregate results with the original table.
- Why joins are needed after aggregation.
- How to retrieve additional columns after finding an aggregate value.

---

# LeetCode Submission

**Status**

✅ Accepted

**Runtime**

944 ms

**Memory**

0.00 MB

**Language**

PostgreSQL

**Test Cases Passed**

10 / 10

---

# Revision Notes

Remember:

- MIN() finds the earliest value.
- GROUP BY creates one group per product.
- Subquery creates a temporary table.
- JOIN retrieves additional columns from the original table.

---

# SQL Keywords Used

- SELECT
- FROM
- JOIN
- GROUP BY
- MIN()
- Subquery
- AS

---

# Tags

SQL • PostgreSQL • Subquery • GROUP BY • MIN() • JOIN • Database • LeetCode Easy