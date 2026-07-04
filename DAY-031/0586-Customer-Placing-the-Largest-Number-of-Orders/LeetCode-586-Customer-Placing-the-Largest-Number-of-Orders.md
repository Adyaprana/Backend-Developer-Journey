# LeetCode 586 — Customer Placing the Largest Number of Orders

![Difficulty](https://img.shields.io/badge/Difficulty-Easy-success)
![Database](https://img.shields.io/badge/Database-PostgreSQL-blue)
![Topic](https://img.shields.io/badge/Topic-GROUP_BY_+_ORDER_BY_+_LIMIT-orange)

---

# Problem Link

https://leetcode.com/problems/customer-placing-the-largest-number-of-orders/

---

# Problem Statement

Write a SQL query to find the customer who has placed the largest number of orders.

The test cases are generated so that exactly one customer has placed more orders than any other customer.

Return the customer number.

---

# Table Schema

## Orders

| Column | Type |
|---------|------|
| order_number | int |
| customer_number | int |

- `order_number` is the primary key.
- Each row represents one order placed by a customer.

---

# Create Table

```sql
CREATE TABLE Orders (
    order_number INT PRIMARY KEY,
    customer_number INT
);
```

---

# Insert Sample Data

```sql
INSERT INTO Orders (order_number, customer_number) VALUES
(1,1),
(2,1),
(3,3),
(4,2),
(5,2),
(6,2),
(7,3);
```

---

# View Table

```sql
SELECT * FROM Orders;
```

---

# Expected Output

| customer_number |
|-----------------|
| 2 |

Customer **2** placed the highest number of orders.

---

# My Solution

```sql
SELECT
    customer_number
FROM Orders
GROUP BY customer_number
ORDER BY COUNT(order_number) DESC
LIMIT 1;
```

---

# Explanation

The problem asks us to find the customer with the highest number of orders.

First, we group all orders by `customer_number`.

Next, we count how many orders each customer has placed.

Then we sort the counts in descending order.

Finally, we return only the first row using `LIMIT 1`.

---

# Query Breakdown

### SELECT

```sql
SELECT customer_number
```

Returns the customer number.

---

### FROM

```sql
FROM Orders
```

Reads data from the Orders table.

---

### GROUP BY

```sql
GROUP BY customer_number
```

Groups all orders belonging to the same customer.

---

### ORDER BY

```sql
ORDER BY COUNT(order_number) DESC
```

Sorts customers from highest order count to lowest.

---

### LIMIT

```sql
LIMIT 1
```

Returns only the customer with the highest number of orders.

---

# Approach

1. Read data from the Orders table.
2. Group records by customer.
3. Count each customer's orders.
4. Sort by order count in descending order.
5. Return the first customer.

---

# Why This Approach?

We need to compare the number of orders placed by each customer.

- `GROUP BY` creates one group per customer.
- `COUNT()` counts each customer's orders.
- `ORDER BY DESC` places the highest count first.
- `LIMIT 1` returns only the top customer.

---

# Visualization

Orders

| Customer |
|----------|
|1|
|1|
|2|
|2|
|2|
|3|
|3|

After GROUP BY

| Customer | Orders |
|----------|--------|
|1|2|
|2|3|
|3|2|

After ORDER BY DESC

| Customer | Orders |
|----------|--------|
|2|3|
|1|2|
|3|2|

LIMIT 1

```
Customer 2
```

---

# Time Complexity

Let **n** be the number of orders.

**Time Complexity**

```
O(n log n)
```

Grouping requires scanning all rows, and sorting the grouped results takes additional time.

---

# Space Complexity

```
O(k)
```

Where **k** is the number of distinct customers.

---

# Interview Questions

### Q1. Why use GROUP BY?

To group orders for each customer.

---

### Q2. Why COUNT(order_number)?

To count how many orders each customer placed.

---

### Q3. Why ORDER BY DESC?

To place the customer with the most orders first.

---

### Q4. Why LIMIT 1?

To return only the customer with the highest order count.

---

### Q5. Can COUNT(*) be used?

Yes.

```sql
COUNT(*)
```

works the same here because every row represents one order.

---

# Common Mistakes

❌ Forgetting GROUP BY

```sql
SELECT customer_number
ORDER BY COUNT(order_number);
```

Invalid query.

---

❌ Sorting in ascending order

```sql
ORDER BY COUNT(order_number) ASC
```

Returns the customer with the fewest orders.

---

❌ Forgetting LIMIT

Returns every customer instead of the top one.

---

# Key Concepts Learned

- SELECT
- FROM
- GROUP BY
- COUNT()
- ORDER BY
- DESC
- LIMIT

---

# What I Learned

- How to count grouped records.
- How to sort aggregate values.
- How ORDER BY works with COUNT().
- How LIMIT returns the top result.

---

# LeetCode Submission

**Status**

✅ Accepted

**Runtime**

254 ms

**Memory**

0.00 MB

**Language**

PostgreSQL

**Test Cases Passed**

19 / 19

---

# Revision Notes

Remember:

- GROUP BY groups records.
- COUNT() counts rows.
- ORDER BY DESC sorts highest first.
- LIMIT returns only the required number of rows.

---

# SQL Keywords Used

- SELECT
- FROM
- GROUP BY
- COUNT()
- ORDER BY
- DESC
- LIMIT

---

# Tags

SQL • PostgreSQL • GROUP BY • ORDER BY • LIMIT • COUNT() • Database • LeetCode Easy