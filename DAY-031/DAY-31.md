# DAY 31 — SQL AGGREGATIONS + SUBQUERIES: THE COMPLETE HANDBOOK

> **Goal:** Master GROUP BY, HAVING, aggregate functions, ORDER BY, LIMIT, OFFSET, and subqueries. Build real analytics queries used in every backend application.
>
> **Week:** W5 — SQL + PostgreSQL (Days 29–42)
>
> **Status:** ✅

---

# 🎯 Learning Roadmap

```
SQL Aggregations + Subqueries

  ✅ GROUP BY, HAVING, ORDER BY, LIMIT, OFFSET
  ✅ COUNT(), SUM(), AVG(), MAX(), MIN()
  ✅ Subqueries — queries inside queries
  ✅ Practice: Find Top 5 Customers by Total Orders
  ✅ Practice: Monthly Revenue Report

  ▶ sqlzoo.net Level 7+ + HackerRank SQL Easy section
```

## Day 31 Checklist

- [ ] Explain GROUP BY without notes
- [ ] Explain the difference between WHERE and HAVING
- [ ] Write the SQL execution order from memory (8 steps)
- [ ] Use COUNT(), SUM(), AVG(), MAX(), MIN() in one query
- [ ] Write ORDER BY + LIMIT for Top-N queries
- [ ] Write pagination using LIMIT + OFFSET
- [ ] Write a subquery in WHERE clause
- [ ] Write a subquery in FROM clause (derived table)
- [ ] Build the Top 5 Customers report
- [ ] Build the Monthly Revenue report
- [ ] Solve LeetCode 586 — Customer Placing Largest Orders ✅
- [ ] Solve LeetCode 596 — Classes With at Least 5 Students ✅
- [ ] Solve LeetCode 570 — Managers with 5+ Direct Reports ✅
- [ ] Solve LeetCode 1070 — Product Sales Analysis III ✅

---

# SECTION 1 — CONCEPTUAL SUMMARY

## GROUP BY — Grouping Rows Into Summary Rows

**Definition:** GROUP BY combines all rows that share the same value in a specified column into a single group, then lets you run calculations on each group.

**The mental model:**

```
Without GROUP BY:
orders table:
┌──────────┬─────────────┬────────┐
│ order_id │ customer_id │ amount │
├──────────┼─────────────┼────────┤
│      101 │           1 │    500 │
│      102 │           1 │    700 │
│      103 │           2 │    900 │
│      104 │           1 │   1800 │
│      105 │           2 │   1200 │
└──────────┴─────────────┴────────┘
5 individual rows. Hard to see the big picture.

With GROUP BY customer_id:
┌─────────────┬──────────────┬────────────┐
│ customer_id │ order_count  │ total_spent│
├─────────────┼──────────────┼────────────┤
│           1 │            3 │       3000 │
│           2 │            2 │       2100 │
└─────────────┴──────────────┴────────────┘
2 summary rows. Instantly useful.
```

**Why it exists:** Real business questions are about groups, not individual rows. "How much did each customer spend?" "How many employees in each department?" "What was revenue per month?" These all need GROUP BY.

**Backend example:** Every analytics dashboard, sales report, and admin panel uses GROUP BY.

```sql
-- Most common GROUP BY pattern
SELECT customer_id, COUNT(*) AS orders, SUM(amount) AS total
FROM orders
GROUP BY customer_id;
```

---

## HAVING — Filtering Groups After GROUP BY

**Definition:** HAVING filters groups created by GROUP BY. It is the WHERE clause for groups.

**WHERE vs HAVING — the most important distinction:**

```
WHERE  → filters individual ROWS    → runs BEFORE GROUP BY
HAVING → filters GROUPS             → runs AFTER  GROUP BY

You cannot use aggregate functions (COUNT, SUM, etc.) in WHERE.
You CAN use aggregate functions in HAVING.
```

**Visual:**

```
Raw table: 10 rows
       ↓
WHERE filters rows  →  8 rows remain
       ↓
GROUP BY groups rows  →  3 groups created
       ↓
HAVING filters groups  →  2 groups kept
       ↓
SELECT produces final result: 2 rows
```

```sql
-- ❌ WRONG — cannot use COUNT in WHERE
SELECT department, COUNT(*)
FROM employees
WHERE COUNT(*) > 5           -- ERROR!
GROUP BY department;

-- ✅ CORRECT — use HAVING for group conditions
SELECT department, COUNT(*)
FROM employees
GROUP BY department
HAVING COUNT(*) > 5;
```

---

## ORDER BY — Sorting Results

**Definition:** ORDER BY sorts the final result set by one or more columns, either ascending (ASC) or descending (DESC).

```sql
-- Ascending (A→Z, 1→100) — default if not specified
SELECT * FROM products ORDER BY price ASC;

-- Descending (Z→A, 100→1)
SELECT * FROM products ORDER BY price DESC;

-- Sort by multiple columns
SELECT * FROM employees
ORDER BY department ASC, salary DESC;
-- Sort by department first, then by salary within each department
```

**Always use ORDER BY with LIMIT.** Without it, the "top N" results are arbitrary and unreliable.

---

## LIMIT — Restricting Number of Results

**Definition:** LIMIT tells SQL to return only the first N rows of the result.

```sql
-- Get only 5 rows
SELECT * FROM orders LIMIT 5;

-- Top 3 most expensive products
SELECT name, price
FROM products
ORDER BY price DESC
LIMIT 3;
```

**Backend use:** Top-N reports, "most popular", "highest revenue", preview data without loading millions of rows.

---

## OFFSET — Skipping Rows (Pagination)

**Definition:** OFFSET tells SQL to skip the first N rows before returning results. Combined with LIMIT, it powers pagination.

```sql
-- Page 1: rows 1-10
SELECT * FROM products ORDER BY id LIMIT 10 OFFSET 0;

-- Page 2: rows 11-20
SELECT * FROM products ORDER BY id LIMIT 10 OFFSET 10;

-- Page 3: rows 21-30
SELECT * FROM products ORDER BY id LIMIT 10 OFFSET 20;

-- Formula: OFFSET = (page_number - 1) × items_per_page
```

**Backend example (FastAPI):**

```
GET /products?page=3&limit=20
→ LIMIT 20 OFFSET 40
```

---

## COUNT() — How Many Rows?

**Definition:** COUNT() returns the number of rows that match a condition.

```sql
COUNT(*)          -- Count ALL rows, including NULLs
COUNT(column)     -- Count rows where column is NOT NULL
COUNT(DISTINCT column)  -- Count unique values only
```

```sql
-- Count all orders
SELECT COUNT(*) AS total_orders FROM orders;   -- 10

-- Count orders with an amount (excludes NULLs)
SELECT COUNT(amount) FROM orders;

-- Count unique customers who placed orders
SELECT COUNT(DISTINCT customer_id) FROM orders;
```

---

## SUM() — Total of Numeric Values

**Definition:** SUM() adds up all values in a numeric column.

```sql
SELECT SUM(amount) AS total_revenue FROM orders;       -- Total of all orders
SELECT SUM(salary) AS payroll FROM employees;          -- Total salary bill
SELECT SUM(stock * price) AS inventory_value FROM products;  -- Calculated column
```

**SUM ignores NULL values.** If a row has NULL in the amount column, it is skipped.

---

## AVG() — Average Value

**Definition:** AVG() calculates the mean (average) of a numeric column.

```sql
SELECT AVG(amount) AS avg_order FROM orders;
SELECT AVG(salary) AS avg_salary FROM employees;
SELECT ROUND(AVG(rating), 2) AS avg_rating FROM reviews;  -- Round to 2 decimals
```

**AVG also ignores NULL values.**

---

## MAX() and MIN() — Extreme Values

**Definition:** MAX() returns the largest value; MIN() returns the smallest.

```sql
SELECT MAX(amount) FROM orders;    -- Highest single order
SELECT MIN(amount) FROM orders;    -- Lowest single order
SELECT MAX(salary) FROM employees; -- Highest paid employee
SELECT MIN(hire_date) FROM employees;  -- Earliest hire date
```

**MAX and MIN work on numbers, dates, and strings (alphabetical for strings).**

---

## Subqueries — Queries Inside Queries

**Definition:** A subquery is a complete SQL query written inside another query. The inner query runs first, and its result is used by the outer query.

**Three types of subqueries:**

```
1. Subquery in WHERE clause  → Filter using a calculated value
2. Subquery in FROM clause   → Use as a temporary table (derived table)
3. Subquery in SELECT clause → Calculate a value for each row (scalar subquery)
```

```sql
-- Type 1: Subquery in WHERE
-- "Find all orders above the average order amount"
SELECT * FROM orders
WHERE amount > (SELECT AVG(amount) FROM orders);
-- Inner query runs first: calculates the average (e.g., 785)
-- Outer query then filters: WHERE amount > 785

-- Type 2: Subquery in FROM (Derived Table)
-- "Show total revenue per customer for customers who spent more than 1000"
SELECT sub.customer_id, sub.total
FROM (
    SELECT customer_id, SUM(amount) AS total
    FROM orders
    GROUP BY customer_id
) AS sub
WHERE sub.total > 1000;

-- Type 3: Scalar Subquery in SELECT
-- "Show each order's amount and the overall average"
SELECT
    order_id,
    amount,
    (SELECT AVG(amount) FROM orders) AS avg_amount,
    amount - (SELECT AVG(amount) FROM orders) AS diff_from_avg
FROM orders;
```

---

# SECTION 2 — COMPLETE SQL SCRIPT (COPY AND RUN IN pgAdmin)

```sql
-- ═══════════════════════════════════════════════════════════════
-- DAY 31 — SQL AGGREGATIONS + SUBQUERIES: COMPLETE SCRIPT
-- Copy everything below and run in pgAdmin Query Editor.
-- ═══════════════════════════════════════════════════════════════


-- ─────────────────────────────────────────────────────────────────
-- STEP 1: CLEANUP
-- ─────────────────────────────────────────────────────────────────

DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS customers;


-- ─────────────────────────────────────────────────────────────────
-- STEP 2: CREATE TABLES
-- ─────────────────────────────────────────────────────────────────

CREATE TABLE customers (
    customer_id   SERIAL        PRIMARY KEY,
    customer_name VARCHAR(100)  NOT NULL,
    city          VARCHAR(50)
);

CREATE TABLE orders (
    order_id    SERIAL          PRIMARY KEY,
    customer_id INT             REFERENCES customers(customer_id),
    order_date  DATE            NOT NULL,
    amount      NUMERIC(10, 2)  NOT NULL
);


-- ─────────────────────────────────────────────────────────────────
-- STEP 3: INSERT DATA
-- ─────────────────────────────────────────────────────────────────

INSERT INTO customers (customer_name, city) VALUES
('Adyaprana', 'Bangalore'),
('Rahul',     'Delhi'),
('Priya',     'Mumbai'),
('Amit',      'Kolkata'),
('Sneha',     'Chennai');

INSERT INTO orders (customer_id, order_date, amount) VALUES
(1, '2026-01-02',  500.00),
(1, '2026-01-08',  700.00),
(1, '2026-02-01', 1800.00),
(2, '2026-01-05',  900.00),
(2, '2026-03-01', 1200.00),
(3, '2026-02-11',  300.00),
(3, '2026-02-25',  450.00),
(4, '2026-03-04',  600.00),
(4, '2026-03-10',  400.00),
(5, '2026-01-12', 1000.00);


-- ─────────────────────────────────────────────────────────────────
-- STEP 4: VIEW RAW DATA
-- ─────────────────────────────────────────────────────────────────

SELECT * FROM customers;
SELECT * FROM orders;


-- ─────────────────────────────────────────────────────────────────
-- STEP 5: AGGREGATE FUNCTIONS
-- ─────────────────────────────────────────────────────────────────

-- COUNT: How many orders exist?
SELECT COUNT(*) AS total_orders FROM orders;
-- Result: 10

-- COUNT with condition
SELECT COUNT(*) AS large_orders FROM orders WHERE amount > 500;
-- Result: 7

-- COUNT DISTINCT: How many unique customers placed orders?
SELECT COUNT(DISTINCT customer_id) AS unique_customers FROM orders;
-- Result: 5

-- SUM: Total revenue
SELECT SUM(amount) AS total_revenue FROM orders;
-- Result: 7850.00

-- AVG: Average order value
SELECT ROUND(AVG(amount), 2) AS avg_order FROM orders;
-- Result: 785.00

-- MAX: Highest single order
SELECT MAX(amount) AS highest_order FROM orders;
-- Result: 1800.00

-- MIN: Lowest single order
SELECT MIN(amount) AS lowest_order FROM orders;
-- Result: 300.00

-- All aggregates in one query
SELECT
    COUNT(*)                    AS total_orders,
    SUM(amount)                 AS total_revenue,
    ROUND(AVG(amount), 2)       AS avg_order,
    MAX(amount)                 AS max_order,
    MIN(amount)                 AS min_order
FROM orders;


-- ─────────────────────────────────────────────────────────────────
-- STEP 6: GROUP BY
-- ─────────────────────────────────────────────────────────────────

-- Total orders and revenue per customer
SELECT
    customer_id,
    COUNT(*)            AS order_count,
    SUM(amount)         AS total_spent,
    ROUND(AVG(amount), 2) AS avg_order
FROM orders
GROUP BY customer_id
ORDER BY total_spent DESC;

-- Orders per city (JOIN required)
SELECT
    c.city,
    COUNT(o.order_id)   AS order_count,
    SUM(o.amount)       AS city_revenue
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.city
ORDER BY city_revenue DESC;


-- ─────────────────────────────────────────────────────────────────
-- STEP 7: HAVING — Filter Groups
-- ─────────────────────────────────────────────────────────────────

-- Customers who placed more than 1 order
SELECT
    customer_id,
    COUNT(*) AS order_count
FROM orders
GROUP BY customer_id
HAVING COUNT(*) > 1
ORDER BY order_count DESC;

-- Customers whose total spending exceeds 1000
SELECT
    customer_id,
    SUM(amount) AS total_spent
FROM orders
GROUP BY customer_id
HAVING SUM(amount) > 1000
ORDER BY total_spent DESC;

-- Customers with total spending between ₹500 and ₹2000
SELECT
    customer_id,
    SUM(amount) AS total_spent
FROM orders
GROUP BY customer_id
HAVING SUM(amount) BETWEEN 500 AND 2000
ORDER BY total_spent DESC;

-- WHERE + GROUP BY + HAVING together
-- Orders in January, grouped by customer, keeping only customers spending over 500
SELECT
    customer_id,
    COUNT(*)    AS jan_orders,
    SUM(amount) AS jan_revenue
FROM orders
WHERE EXTRACT(MONTH FROM order_date) = 1       -- WHERE filters rows first
GROUP BY customer_id
HAVING SUM(amount) > 500                        -- HAVING filters groups after
ORDER BY jan_revenue DESC;


-- ─────────────────────────────────────────────────────────────────
-- STEP 8: ORDER BY
-- ─────────────────────────────────────────────────────────────────

-- Sort by amount ascending (lowest first)
SELECT * FROM orders ORDER BY amount ASC;

-- Sort by amount descending (highest first)
SELECT * FROM orders ORDER BY amount DESC;

-- Sort by date
SELECT * FROM orders ORDER BY order_date ASC;

-- Sort by customer name alphabetically
SELECT * FROM customers ORDER BY customer_name ASC;

-- Sort by multiple columns
SELECT customer_id, amount, order_date
FROM orders
ORDER BY customer_id ASC, amount DESC;


-- ─────────────────────────────────────────────────────────────────
-- STEP 9: LIMIT
-- ─────────────────────────────────────────────────────────────────

-- Top 3 highest orders
SELECT * FROM orders
ORDER BY amount DESC
LIMIT 3;

-- Top 1 — single highest order
SELECT * FROM orders
ORDER BY amount DESC
LIMIT 1;

-- Cheapest 5 orders
SELECT * FROM orders
ORDER BY amount ASC
LIMIT 5;


-- ─────────────────────────────────────────────────────────────────
-- STEP 10: OFFSET (Pagination)
-- ─────────────────────────────────────────────────────────────────

-- Page 1 (rows 1-3)
SELECT * FROM orders ORDER BY amount DESC LIMIT 3 OFFSET 0;

-- Page 2 (rows 4-6)
SELECT * FROM orders ORDER BY amount DESC LIMIT 3 OFFSET 3;

-- Page 3 (rows 7-9)
SELECT * FROM orders ORDER BY amount DESC LIMIT 3 OFFSET 6;

-- Last 2 orders by date
SELECT * FROM orders ORDER BY order_date DESC LIMIT 2 OFFSET 8;


-- ─────────────────────────────────────────────────────────────────
-- STEP 11: SUBQUERIES
-- ─────────────────────────────────────────────────────────────────

-- Subquery in WHERE: Orders above average
SELECT *
FROM orders
WHERE amount > (SELECT AVG(amount) FROM orders)
ORDER BY amount DESC;

-- Subquery in WHERE: Customer with most orders
SELECT customer_name
FROM customers
WHERE customer_id = (
    SELECT customer_id
    FROM orders
    GROUP BY customer_id
    ORDER BY COUNT(*) DESC
    LIMIT 1
);

-- Subquery in WHERE: Orders placed by customers from Bangalore
SELECT *
FROM orders
WHERE customer_id IN (
    SELECT customer_id
    FROM customers
    WHERE city = 'Bangalore'
);

-- Subquery in FROM (Derived Table): Revenue per customer > 1000
SELECT sub.customer_id, sub.total_revenue
FROM (
    SELECT customer_id, SUM(amount) AS total_revenue
    FROM orders
    GROUP BY customer_id
) AS sub
WHERE sub.total_revenue > 1000
ORDER BY sub.total_revenue DESC;

-- Scalar Subquery in SELECT: Each order with the overall average
SELECT
    order_id,
    customer_id,
    amount,
    ROUND((SELECT AVG(amount) FROM orders), 2) AS overall_avg,
    amount - ROUND((SELECT AVG(amount) FROM orders), 2) AS diff
FROM orders
ORDER BY diff DESC;

-- EXISTS subquery: Customers who have placed at least one order
SELECT customer_name
FROM customers c
WHERE EXISTS (
    SELECT 1
    FROM orders o
    WHERE o.customer_id = c.customer_id
);

-- NOT EXISTS: Customers who have NEVER placed an order
SELECT customer_name
FROM customers c
WHERE NOT EXISTS (
    SELECT 1
    FROM orders o
    WHERE o.customer_id = c.customer_id
);


-- ─────────────────────────────────────────────────────────────────
-- STEP 12: PROJECT 1 — TOP 5 CUSTOMERS BY TOTAL REVENUE
-- ─────────────────────────────────────────────────────────────────

SELECT
    c.customer_name,
    c.city,
    COUNT(o.order_id)           AS total_orders,
    SUM(o.amount)               AS total_revenue,
    ROUND(AVG(o.amount), 2)     AS avg_order_value,
    MAX(o.amount)               AS largest_order,
    MIN(o.amount)               AS smallest_order
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.customer_name, c.city
ORDER BY total_revenue DESC
LIMIT 5;

-- Expected result:
-- customer_name | city      | orders | revenue | avg   | max  | min
-- Adyaprana     | Bangalore | 3      | 3000.00 | 1000  | 1800 | 500
-- Rahul         | Delhi     | 2      | 2100.00 | 1050  | 1200 | 900
-- Sneha         | Chennai   | 1      | 1000.00 | 1000  | 1000 | 1000
-- ...


-- ─────────────────────────────────────────────────────────────────
-- STEP 13: PROJECT 2 — MONTHLY REVENUE REPORT
-- ─────────────────────────────────────────────────────────────────

SELECT
    DATE_TRUNC('month', order_date)     AS month,
    TO_CHAR(order_date, 'Month YYYY')   AS month_label,
    COUNT(*)                            AS total_orders,
    SUM(amount)                         AS monthly_revenue,
    ROUND(AVG(amount), 2)               AS avg_order,
    MAX(amount)                         AS highest_order,
    MIN(amount)                         AS lowest_order
FROM orders
GROUP BY DATE_TRUNC('month', order_date), TO_CHAR(order_date, 'Month YYYY')
ORDER BY month ASC;

-- Expected result:
-- month      | label          | orders | revenue | avg
-- 2026-01-01 | January 2026   | 4      | 3100.00 | 775
-- 2026-02-01 | February 2026  | 3      | 2550.00 | 850
-- 2026-03-01 | March 2026     | 3      | 2200.00 | 733

-- Find the best month (highest revenue)
SELECT
    DATE_TRUNC('month', order_date) AS month,
    SUM(amount) AS revenue
FROM orders
GROUP BY DATE_TRUNC('month', order_date)
ORDER BY revenue DESC
LIMIT 1;
```

---

## LeetCode 586 — Customer Placing Largest Number of Orders

```sql
-- ═══════════════════════════════════════════════════════════════
-- LeetCode #586 — Customer Placing the Largest Number of Orders
-- Difficulty: Easy | Status: ✅ Accepted (19/19 test cases)
-- Runtime: 254ms | Memory: 0.00 MB | Beats memory: 100%
-- ═══════════════════════════════════════════════════════════════

DROP TABLE IF EXISTS Orders;

CREATE TABLE Orders (
    order_number    INT PRIMARY KEY,
    customer_number INT
);

INSERT INTO Orders VALUES
(1,1),(2,1),(3,3),(4,2),(5,2),(6,2),(7,3);

-- SOLUTION
SELECT customer_number
FROM Orders
GROUP BY customer_number
ORDER BY COUNT(order_number) DESC
LIMIT 1;

-- Steps:
-- GROUP BY creates one row per customer
-- COUNT(order_number) counts their orders
-- ORDER BY DESC puts the highest count first
-- LIMIT 1 returns only the winner

-- Expected: customer_number = 2 (placed 3 orders)

-- FOLLOW-UP: What if there is a TIE?
-- Return ALL customers with the maximum order count
SELECT customer_number
FROM Orders
GROUP BY customer_number
HAVING COUNT(*) = (
    SELECT MAX(cnt)
    FROM (
        SELECT COUNT(*) AS cnt
        FROM Orders
        GROUP BY customer_number
    ) AS sub
);
```

---

## LeetCode 596 — Classes With at Least 5 Students

```sql
-- ═══════════════════════════════════════════════════════════════
-- LeetCode #596 — Classes With at Least 5 Students
-- Difficulty: Easy | Status: ✅ Accepted (11/11 test cases)
-- Runtime: 295ms | Memory: 0.00 MB | Beats memory: 100%
-- ═══════════════════════════════════════════════════════════════

DROP TABLE IF EXISTS Courses;

CREATE TABLE Courses (
    student VARCHAR(50),
    class   VARCHAR(50)
);

INSERT INTO Courses VALUES
('A','Math'),('B','English'),('C','Math'),('D','Biology'),
('E','Math'),('F','Computer'),('G','Math'),('H','Math'),('I','Math');

-- SOLUTION
SELECT class
FROM Courses
GROUP BY class
HAVING COUNT(student) >= 5;

-- GROUP BY creates one group per class
-- COUNT(student) counts enrolled students
-- HAVING filters: keep only classes with 5+ students

-- Expected: Math (has 6 students: A,C,E,G,H,I)

-- WHY NOT WHERE?
-- WHERE COUNT(student) >= 5  → ❌ ERROR
-- COUNT() is an aggregate function, cannot be in WHERE.
-- HAVING runs AFTER GROUP BY → ✅ correct placement
```

---

## LeetCode 570 — Managers with at Least 5 Direct Reports

```sql
-- ═══════════════════════════════════════════════════════════════
-- LeetCode #570 — Managers with at Least 5 Direct Reports
-- Difficulty: Medium | Status: ✅ Accepted (11/11 test cases)
-- Runtime: 341ms | Memory: 0.00 MB | Beats memory: 100%
-- ═══════════════════════════════════════════════════════════════

DROP TABLE IF EXISTS Employee;

CREATE TABLE Employee (
    id         INT PRIMARY KEY,
    name       VARCHAR(50),
    department VARCHAR(50),
    managerId  INT
);

INSERT INTO Employee VALUES
(101,'John','A',NULL),(102,'Dan','A',101),(103,'James','A',101),
(104,'Amy','A',101),(105,'Anne','A',101),(106,'Ron','B',101),(107,'Sam','B',102);

-- SOLUTION
-- Self JOIN: e = employees, m = managers (same table, two roles)
-- GROUP BY manager, COUNT direct reports
-- HAVING filters managers with 5+ reports
SELECT m.name
FROM Employee e
JOIN Employee m ON m.id = e.managerId
GROUP BY m.id, m.name
HAVING COUNT(*) >= 5;

-- Alternative with subquery:
SELECT name
FROM Employee
WHERE id IN (
    SELECT managerId
    FROM Employee
    GROUP BY managerId
    HAVING COUNT(*) >= 5
);

-- Expected: John (manages 5 employees: Dan, James, Amy, Anne, Ron)
```

---

## LeetCode 1070 — Product Sales Analysis III

```sql
-- ═══════════════════════════════════════════════════════════════
-- LeetCode #1070 — Product Sales Analysis III
-- Difficulty: Medium | Status: ✅ Accepted (10/10 test cases)
-- Runtime: 944ms | Memory: 0.00 MB | Beats memory: 100%
-- ═══════════════════════════════════════════════════════════════

DROP TABLE IF EXISTS Sales;

CREATE TABLE Sales (
    sale_id    INT PRIMARY KEY,
    product_id INT,
    year       INT,
    quantity   INT,
    price      INT
);

INSERT INTO Sales VALUES
(1,100,2008,10,5000),(2,100,2009,12,5000),(7,200,2011,15,9000);

-- SOLUTION: Subquery (derived table) + JOIN
-- Step 1 (subquery): Find MIN(year) for each product
-- Step 2 (JOIN): Get quantity and price for that first year

SELECT
    s.product_id,
    f.first_year,
    s.quantity,
    s.price
FROM Sales s
JOIN (
    SELECT product_id, MIN(year) AS first_year
    FROM Sales
    GROUP BY product_id
) AS f
ON s.product_id = f.product_id
AND s.year = f.first_year;

-- The subquery returns:
-- product_id | first_year
-- 100        | 2008
-- 200        | 2011

-- The JOIN matches it back with the original table
-- to get quantity and price

-- Expected:
-- 100 | 2008 | 10 | 5000
-- 200 | 2011 | 15 | 9000
```

---

# SECTION 3 — DEEP THEORY

## SQL Execution Order (Most Important Concept)

You WRITE SQL in this order:

```sql
SELECT   customer_id, SUM(amount) AS total
FROM     orders
WHERE    order_date >= '2026-01-01'
GROUP BY customer_id
HAVING   SUM(amount) > 1000
ORDER BY total DESC
LIMIT    5
OFFSET   0;
```

But SQL PROCESSES it in this order:

```
Step 1: FROM     → Load the orders table into memory
Step 2: WHERE    → Filter rows: only orders from 2026 onward
Step 3: GROUP BY → Group filtered rows by customer_id
Step 4: HAVING   → Filter groups: only customers spending > 1000
Step 5: SELECT   → Pick which columns to show, run SUM()
Step 6: ORDER BY → Sort the result by total DESC
Step 7: LIMIT    → Keep only the first 5 rows
Step 8: OFFSET   → Skip 0 rows from the start
```

**Why this matters:**

```
1. You cannot use a SELECT alias in WHERE:
   SELECT age * 2 AS double_age
   FROM students
   WHERE double_age > 40;   -- ❌ ERROR: double_age doesn't exist at WHERE stage

   Fix: WHERE age * 2 > 40   -- ✅

2. You cannot use aggregate functions in WHERE:
   WHERE SUM(amount) > 1000  -- ❌ ERROR: SUM runs at SELECT stage, not WHERE

   Fix: HAVING SUM(amount) > 1000  -- ✅

3. HAVING can reference SELECT aliases in PostgreSQL (exception):
   SELECT customer_id, SUM(amount) AS total
   GROUP BY customer_id
   HAVING total > 1000;  -- ✅ Works in PostgreSQL (not all databases)
```

---

## Why GROUP BY Works

GROUP BY physically reorganizes the result set into groups.

```
Raw data:
customer_id | amount
1           | 500
1           | 700
2           | 900
1           | 1800
2           | 1200

GROUP BY customer_id:
Group 1 (customer_id = 1):  [500, 700, 1800]
Group 2 (customer_id = 2):  [900, 1200]

Now aggregate functions operate on each group:
COUNT(*):   [3,    2   ]
SUM():      [3000, 2100]
AVG():      [1000, 1050]
```

**GROUP BY Rule:** Every column in SELECT must either:

```
1. Appear in the GROUP BY clause
2. Be wrapped in an aggregate function (COUNT, SUM, AVG, MAX, MIN)
```

```sql
-- ❌ ERROR: customer_name is in SELECT but not in GROUP BY
SELECT customer_id, customer_name, SUM(amount)
FROM orders
GROUP BY customer_id;

-- ✅ CORRECT: add customer_name to GROUP BY
SELECT customer_id, customer_name, SUM(amount)
FROM orders
GROUP BY customer_id, customer_name;
```

---

## Common Beginner Mistakes

```
Mistake 1: Using WHERE instead of HAVING for aggregates
  Wrong:  WHERE COUNT(*) > 5
  Right:  HAVING COUNT(*) > 5

Mistake 2: Not including all non-aggregate columns in GROUP BY
  Wrong:  SELECT name, dept, COUNT(*) GROUP BY dept
  Right:  SELECT name, dept, COUNT(*) GROUP BY name, dept

Mistake 3: Using LIMIT without ORDER BY
  Wrong:  SELECT * FROM orders LIMIT 5
  Returns random 5 rows. Not reliable. No guarantee of which 5.
  Right:  SELECT * FROM orders ORDER BY amount DESC LIMIT 5

Mistake 4: Confusing COUNT(*) and COUNT(column)
  COUNT(*)        → Counts all rows including NULL
  COUNT(amount)   → Counts only rows where amount is NOT NULL

Mistake 5: Forgetting OFFSET starts at 0
  Page 1: OFFSET 0  (not OFFSET 1!)
  Page 2: OFFSET 10
  Page 3: OFFSET 20

Mistake 6: Subquery returning multiple rows in WHERE = clause
  Wrong:  WHERE id = (SELECT id FROM orders)       -- if multiple rows returned
  Right:  WHERE id IN (SELECT id FROM orders)      -- use IN for multiple rows

Mistake 7: Using ORDER BY in a subquery unnecessarily
  SELECT * FROM (SELECT * FROM orders ORDER BY amount) sub  -- ORDER BY here is pointless
  The outer query determines the final order.
```

---

# SECTION 4 — IMPORTANT THINGS TO KNOW (20 POINTS)

```
 1. GROUP BY collapses multiple rows into one row per group.

 2. HAVING is WHERE for groups. Use HAVING with aggregate functions.

 3. WHERE runs BEFORE GROUP BY. HAVING runs AFTER GROUP BY.

 4. You cannot use aggregate functions (COUNT, SUM, AVG) in WHERE.

 5. Every column in SELECT must either be in GROUP BY or be aggregated.

 6. ORDER BY should almost always come with LIMIT.
    Without ORDER BY, LIMIT returns unpredictable rows.

 7. OFFSET starts at 0. Page 1 = OFFSET 0, Page 2 = OFFSET 10.

 8. COUNT(*) counts all rows including NULLs.
    COUNT(column) skips NULLs in that column.

 9. SUM() and AVG() both ignore NULL values automatically.

10. MAX() and MIN() work on numbers, dates, AND text (alphabetically for text).

11. ROUND(AVG(column), 2) prevents very long decimal numbers in output.

12. DISTINCT inside aggregate: COUNT(DISTINCT city) counts unique cities only.

13. Subqueries in WHERE must return the right number of rows:
    =  expects exactly 1 row  (use with LIMIT 1 or MIN/MAX)
    IN expects 0 or more rows (safe for multiple)

14. Derived tables (subquery in FROM) must always have an alias:
    FROM (SELECT ...) AS sub   ← 'AS sub' is required in PostgreSQL.

15. GROUP BY does NOT sort results. Always add ORDER BY if order matters.

16. DATE_TRUNC('month', date) truncates a date to the first day of the month.
    Useful for grouping orders by month.

17. EXTRACT(MONTH FROM date) extracts just the month number (1-12).
    EXTRACT(YEAR FROM date) extracts the year.

18. COALESCE(SUM(amount), 0) replaces NULL with 0.
    Useful when LEFT JOIN produces NULL in aggregates.

19. HAVING can reference aggregate expressions but is recomputed.
    In PostgreSQL, you can also use SELECT aliases in HAVING.

20. SQL execution order:
    FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT → OFFSET
```

---

# SECTION 5 — INTERVIEW QUESTIONS (25 QUESTIONS)

## Q1. Write a query to find total orders per customer.

```sql
SELECT customer_id, COUNT(*) AS total_orders
FROM orders
GROUP BY customer_id
ORDER BY total_orders DESC;
```

**Concept:** Basic GROUP BY + COUNT.
**Difficulty:** Easy | **Frequency:** Very High

---

## Q2. Find customers who placed at least 2 orders.

```sql
SELECT customer_id, COUNT(*) AS order_count
FROM orders
GROUP BY customer_id
HAVING COUNT(*) >= 2
ORDER BY order_count DESC;
```

**Concept:** GROUP BY + HAVING for filtering groups.
**Difficulty:** Easy | **Frequency:** Very High

---

## Q3. What is the difference between WHERE and HAVING?

```
WHERE:
  → Filters individual ROWS before grouping
  → Cannot use aggregate functions
  → Runs at Step 2 in SQL execution order

HAVING:
  → Filters GROUPS after GROUP BY
  → CAN use aggregate functions (COUNT, SUM, AVG, etc.)
  → Runs at Step 4 in SQL execution order

Example:
  -- WHERE filters rows
  SELECT dept, COUNT(*)
  FROM employees
  WHERE salary > 30000          -- filter rows first
  GROUP BY dept
  HAVING COUNT(*) > 3;          -- then filter groups
```

**Difficulty:** Easy | **Frequency:** Very High

---

## Q4. Find the customer with the highest total spending.

```sql
SELECT customer_id, SUM(amount) AS total_spent
FROM orders
GROUP BY customer_id
ORDER BY total_spent DESC
LIMIT 1;
```

**Concept:** GROUP BY + SUM + ORDER BY + LIMIT 1 pattern.
**Difficulty:** Easy | **Frequency:** High

---

## Q5. Find all orders that are above the average order amount.

```sql
SELECT *
FROM orders
WHERE amount > (SELECT AVG(amount) FROM orders)
ORDER BY amount DESC;
```

**Concept:** Subquery in WHERE clause. Inner query calculates average; outer query filters.
**Difficulty:** Medium | **Frequency:** Very High

---

## Q6. Write a query to implement pagination (page 3, 10 items per page).

```sql
SELECT *
FROM orders
ORDER BY order_id ASC
LIMIT 10
OFFSET 20;       -- (page 3 - 1) × 10 = 20
```

**Formula:** `OFFSET = (page_number - 1) × items_per_page`
**Difficulty:** Easy | **Frequency:** High (every backend developer needs this)

---

## Q7. Find monthly revenue for the entire year.

```sql
SELECT
    DATE_TRUNC('month', order_date) AS month,
    COUNT(*)                        AS orders,
    SUM(amount)                     AS revenue
FROM orders
GROUP BY DATE_TRUNC('month', order_date)
ORDER BY month;
```

**Concept:** DATE_TRUNC for grouping by time period.
**Difficulty:** Medium | **Frequency:** High

---

## Q8. Find customers whose total spending is between ₹1000 and ₹3000.

```sql
SELECT customer_id, SUM(amount) AS total
FROM orders
GROUP BY customer_id
HAVING SUM(amount) BETWEEN 1000 AND 3000
ORDER BY total;
```

**Concept:** HAVING with BETWEEN.
**Difficulty:** Easy | **Frequency:** Medium

---

## Q9. Find departments where the average salary is greater than the company-wide average.

```sql
SELECT department, ROUND(AVG(salary), 2) AS dept_avg
FROM employees
GROUP BY department
HAVING AVG(salary) > (SELECT AVG(salary) FROM employees)
ORDER BY dept_avg DESC;
```

**Concept:** Subquery inside HAVING clause.
**Difficulty:** Medium | **Frequency:** High

---

## Q10. What does COUNT(*) vs COUNT(column) do differently?

```
COUNT(*)           → Counts EVERY row, including rows with NULL values
COUNT(column_name) → Counts only rows where column_name is NOT NULL

Example:
  amount values: [500, 700, NULL, 900, NULL]
  COUNT(*)       → 5
  COUNT(amount)  → 3
```

**Difficulty:** Easy | **Frequency:** Very High

---

## Q11. Find the top 3 products by revenue.

```sql
SELECT
    product_id,
    SUM(revenue) AS total_revenue
FROM sales
GROUP BY product_id
ORDER BY total_revenue DESC
LIMIT 3;
```

**Concept:** Top-N query pattern with GROUP BY + ORDER BY + LIMIT.
**Difficulty:** Easy | **Frequency:** High

---

## Q12. Find customers who have NEVER placed an order.

```sql
-- Method 1: LEFT JOIN + IS NULL
SELECT c.customer_name
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_id IS NULL;

-- Method 2: NOT IN subquery
SELECT customer_name
FROM customers
WHERE customer_id NOT IN (
    SELECT DISTINCT customer_id FROM orders
);

-- Method 3: NOT EXISTS
SELECT customer_name
FROM customers c
WHERE NOT EXISTS (
    SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id
);
```

**Concept:** Anti-join — three methods.
**Difficulty:** Medium | **Frequency:** Very High

---

## Q13. Find the second highest salary in the company.

```sql
-- Method 1: OFFSET
SELECT DISTINCT salary
FROM employees
ORDER BY salary DESC
LIMIT 1 OFFSET 1;

-- Method 2: Subquery
SELECT MAX(salary)
FROM employees
WHERE salary < (SELECT MAX(salary) FROM employees);

-- Method 3: DENSE_RANK (advanced)
SELECT salary
FROM (
    SELECT salary, DENSE_RANK() OVER (ORDER BY salary DESC) AS rnk
    FROM employees
) sub
WHERE rnk = 2;
```

**Difficulty:** Medium | **Frequency:** Very High

---

## Q14. What is a subquery? What are the three places you can use it?

```
A subquery is a complete SQL query nested inside another query.
The inner query executes first, and its result is used by the outer query.

Three locations:

1. In WHERE clause (most common)
   WHERE amount > (SELECT AVG(amount) FROM orders)

2. In FROM clause (derived table)
   FROM (SELECT customer_id, SUM(amount) FROM orders GROUP BY customer_id) AS sub

3. In SELECT clause (scalar subquery)
   SELECT name, (SELECT COUNT(*) FROM orders WHERE customer_id = c.id) AS order_count
   FROM customers c
```

**Difficulty:** Medium | **Frequency:** Very High

---

## Q15. Find classes with more than 5 students enrolled.

```sql
SELECT class, COUNT(*) AS enrolled
FROM courses
GROUP BY class
HAVING COUNT(*) > 5
ORDER BY enrolled DESC;
```

**Concept:** Basic GROUP BY + HAVING + COUNT.
**Difficulty:** Easy | **Frequency:** Medium

---

## Q16. How do you find duplicate records in a table?

```sql
-- Find email addresses that appear more than once
SELECT email, COUNT(*) AS occurrences
FROM users
GROUP BY email
HAVING COUNT(*) > 1
ORDER BY occurrences DESC;
```

**Concept:** GROUP BY + HAVING COUNT > 1 is the standard duplicate detection pattern.
**Difficulty:** Medium | **Frequency:** Very High

---

## Q17. Find the average order value per city.

```sql
SELECT
    c.city,
    ROUND(AVG(o.amount), 2) AS avg_order_value,
    COUNT(o.order_id)        AS order_count
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.city
ORDER BY avg_order_value DESC;
```

**Concept:** JOIN + GROUP BY on joined column.
**Difficulty:** Medium | **Frequency:** High

---

## Q18. Write a query to get the running total of revenue by date.

```sql
SELECT
    order_date,
    amount,
    SUM(amount) OVER (ORDER BY order_date) AS running_total
FROM orders
ORDER BY order_date;
```

**Concept:** Window function (SUM OVER). More advanced than today's topics.
**Difficulty:** Hard | **Frequency:** Medium

---

## Q19. What happens if you use ORDER BY without LIMIT?

```
The entire result set is sorted. Every row is returned, but in sorted order.
ORDER BY without LIMIT is valid and often useful for reporting.

ORDER BY becomes essential when used with LIMIT:
  Without ORDER BY + LIMIT: you get arbitrary rows (unpredictable)
  With ORDER BY + LIMIT: you get a reliable, deterministic result

Example:
  LIMIT 5                        → 5 random rows (unreliable!)
  ORDER BY amount DESC LIMIT 5   → Top 5 highest amounts (reliable)
```

**Difficulty:** Easy | **Frequency:** High

---

## Q20. Find customers who placed orders in ALL months of 2026.

```sql
SELECT customer_id
FROM orders
WHERE EXTRACT(YEAR FROM order_date) = 2026
GROUP BY customer_id
HAVING COUNT(DISTINCT EXTRACT(MONTH FROM order_date)) = 12;
```

**Concept:** COUNT DISTINCT inside HAVING.
**Difficulty:** Hard | **Frequency:** Medium

---

## Q21. Find the month with the highest total revenue.

```sql
SELECT
    DATE_TRUNC('month', order_date) AS month,
    SUM(amount) AS revenue
FROM orders
GROUP BY DATE_TRUNC('month', order_date)
ORDER BY revenue DESC
LIMIT 1;
```

**Difficulty:** Easy | **Frequency:** High

---

## Q22. How would you implement "show top 5 products, excluding the best seller"?

```sql
SELECT product_id, SUM(revenue) AS total
FROM sales
GROUP BY product_id
ORDER BY total DESC
LIMIT 5 OFFSET 1;      -- Skip the #1 bestseller, show #2 through #6
```

**Concept:** LIMIT + OFFSET for excluding top result.
**Difficulty:** Medium | **Frequency:** Medium

---

## Q23. Find customers whose average order is above the overall average.

```sql
SELECT
    customer_id,
    ROUND(AVG(amount), 2) AS customer_avg
FROM orders
GROUP BY customer_id
HAVING AVG(amount) > (SELECT AVG(amount) FROM orders)
ORDER BY customer_avg DESC;
```

**Concept:** Subquery inside HAVING.
**Difficulty:** Medium | **Frequency:** High

---

## Q24. What is a derived table? Give an example.

```
A derived table is a subquery in the FROM clause.
It creates a temporary, unnamed table that only exists during the query.
It MUST have an alias.

Example:
SELECT sub.customer_id, sub.total
FROM (
    SELECT customer_id, SUM(amount) AS total
    FROM orders
    GROUP BY customer_id
) AS sub          -- 'AS sub' is REQUIRED
WHERE sub.total > 1000;

The inner query creates a table:
  customer_id | total
  1           | 3000
  2           | 2100
  ...

The outer query then filters this temporary table.
```

**Difficulty:** Medium | **Frequency:** High

---

## Q25. How do you count orders per customer per month?

```sql
SELECT
    customer_id,
    DATE_TRUNC('month', order_date) AS month,
    COUNT(*) AS monthly_orders,
    SUM(amount) AS monthly_revenue
FROM orders
GROUP BY customer_id, DATE_TRUNC('month', order_date)
ORDER BY customer_id, month;
```

**Concept:** Multi-column GROUP BY combining customer and time period.
**Difficulty:** Medium | **Frequency:** High

---

# SECTION 6 — BACKEND CONNECTION

## How Every Topic Maps to Real Backend Development

**GROUP BY + aggregates → Dashboard APIs:**

```python
# FastAPI endpoint: GET /analytics/revenue
@app.get("/analytics/revenue")
async def get_revenue_by_customer():
    query = """
        SELECT
            c.customer_name,
            COUNT(o.order_id)   AS total_orders,
            SUM(o.amount)       AS total_revenue
        FROM customers c
        LEFT JOIN orders o ON c.customer_id = o.customer_id
        GROUP BY c.customer_id, c.customer_name
        ORDER BY total_revenue DESC;
    """
    rows = await db.fetch_all(query)
    return rows
```

**LIMIT + OFFSET → Pagination:**

```python
# FastAPI endpoint: GET /orders?page=2&limit=20
@app.get("/orders")
async def get_orders(page: int = 1, limit: int = 20):
    offset = (page - 1) * limit
    query = f"""
        SELECT *
        FROM orders
        ORDER BY order_date DESC
        LIMIT {limit}
        OFFSET {offset};
    """
    # In production: use parameterized queries
    # LIMIT $1 OFFSET $2  with values (limit, offset)
    rows = await db.fetch_all(query)
    return {
        "page": page,
        "limit": limit,
        "data": rows
    }
```

**Subqueries → Business logic queries:**

```python
# Find customers above average — used in targeted marketing
query = """
    SELECT c.customer_name, c.email, sub.total
    FROM customers c
    JOIN (
        SELECT customer_id, SUM(amount) AS total
        FROM orders
        GROUP BY customer_id
    ) sub ON c.customer_id = sub.customer_id
    WHERE sub.total > (SELECT AVG(total_amount) FROM customer_stats)
    ORDER BY sub.total DESC;
"""
```

**Monthly Revenue Report → Executive Dashboards:**

```python
# Used in admin panels, Metabase, Grafana, internal tools
query = """
    SELECT
        DATE_TRUNC('month', order_date) AS month,
        SUM(amount)                     AS revenue,
        COUNT(*)                        AS orders
    FROM orders
    WHERE EXTRACT(YEAR FROM order_date) = 2026
    GROUP BY DATE_TRUNC('month', order_date)
    ORDER BY month;
"""
```

---

# SECTION 7 — PRACTICE QUESTIONS

## Easy (15 Questions)

1. Count the total number of rows in the orders table.
2. Find the total revenue across all orders.
3. Find the average order amount.
4. Find the most expensive single order.
5. Find the cheapest single order.
6. Sort all orders from highest to lowest amount.
7. Show the first 3 orders by date.
8. Show orders placed in February 2026 only.
9. Count how many orders each customer placed.
10. Show all customers ordered alphabetically by name.
11. Show the 5 most recent orders.
12. Show page 2 (items 4-6) of orders sorted by amount descending.
13. Find the total amount spent by customer_id = 1.
14. Count orders where amount is greater than 500.
15. Find the highest and lowest amounts for each customer.

## Medium (10 Questions)

1. Find customers who placed more than 2 orders.
2. Find customers whose total spending exceeds the average per-customer spending.
3. Show monthly revenue for the entire dataset.
4. Find the customer with the single largest order.
5. Find all orders that are above the overall average order amount.
6. Show customers and their order count, only for those who have placed at least 1 order from Bangalore.
7. Find the top 3 cities by total revenue generated.
8. Find orders placed in January, grouped by customer, keeping only customers who spent more than ₹800 in January.
9. Show the first order date for each customer.
10. Find customers who placed orders in at least 2 different months.

## Hard (5 Questions)

1. For each month, show revenue AND the difference from the previous month's revenue.
2. Find customers who placed orders in every month that appears in the orders table.
3. Show the top 2 customers per city by total spending.
4. Find products that were sold in their first year AND also sold in at least one subsequent year.
5. Implement a leaderboard: rank customers by total spending, showing their rank, name, and total.

---

# SECTION 8 — LEETCODE PROBLEMS

| # | Problem | Topic | Difficulty | Status |
|---|---------|-------|-----------|--------|
| 586 | Customer Placing the Largest Number of Orders | GROUP BY + ORDER BY + LIMIT | Easy | ✅ |
| 596 | Classes With at Least 5 Students | GROUP BY + HAVING | Easy | ✅ |
| 570 | Managers with at Least 5 Direct Reports | Self JOIN + GROUP BY + HAVING | Medium | ✅ |
| 1070 | Product Sales Analysis III | Subquery + JOIN + MIN() | Medium | ✅ |

---

# SECTION 9 — MINI PROJECTS

## Project 1: Student Performance Report

```sql
-- Create and populate a students + grades table
-- Generate: average grade per student, top performers, failing students
-- Use GROUP BY, HAVING, ORDER BY, subquery for above-average filter
```

---

# SECTION 10 — REVISION SHEET

```
═══════════════════════════════════════════════════════
SQL AGGREGATIONS + SUBQUERIES — ONE-PAGE REVISION
═══════════════════════════════════════════════════════

AGGREGATE FUNCTIONS:
  COUNT(*)         → Count all rows including NULLs
  COUNT(col)       → Count non-NULL values
  COUNT(DISTINCT)  → Count unique values
  SUM(col)         → Total (ignores NULLs)
  AVG(col)         → Mean average (ignores NULLs)
  MAX(col)         → Largest value
  MIN(col)         → Smallest value

GROUP BY:
  SELECT col, AGG_FN() FROM table GROUP BY col;
  Rule: Non-aggregate SELECT columns MUST be in GROUP BY.

HAVING:
  HAVING AGG_FN() > value;
  Use instead of WHERE when filtering aggregated results.

ORDER BY:
  ORDER BY col ASC;    → Lowest to highest (default)
  ORDER BY col DESC;   → Highest to lowest

LIMIT + OFFSET:
  LIMIT 10 OFFSET 20;  → Skip 20, return next 10
  Page N formula: OFFSET = (N-1) × page_size

SUBQUERIES:
  WHERE amount > (SELECT AVG(amount) FROM orders)
  FROM (SELECT ...) AS alias        ← alias required
  WHERE id IN (SELECT id FROM ...)  ← use IN for multiple rows

SQL EXECUTION ORDER:
  FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT

KEY RULES:
  ❌ WHERE cannot use aggregate functions → use HAVING
  ❌ LIMIT without ORDER BY is unreliable
  ❌ Subquery returning multiple rows with = → use IN
  ❌ Derived table without alias → error in PostgreSQL
  ✅ COUNT(*) includes NULLs, COUNT(col) excludes them
  ✅ ROUND(AVG(col), 2) for clean decimal output

MEMORY TRICKS:
  WHERE = filter rows (before grouping)
  HAVING = filter groups (after grouping)
  LIMIT = how many rows
  OFFSET = how many to skip
  Subquery = query inside query, runs first
```

---

## LeetCode Solved This Day

| Problem | Difficulty | Status | Runtime |
|---------|-----------|--------|---------|
| #586 Customer Placing Largest Orders | Easy | ✅ Accepted 19/19 | 254ms |
| #596 Classes With at Least 5 Students | Easy | ✅ Accepted 11/11 | 295ms |
| #570 Managers with ≥5 Direct Reports | Medium | ✅ Accepted 11/11 | 341ms |
| #1070 Product Sales Analysis III | Medium | ✅ Accepted 10/10 | 944ms |

---

## 🎥 Recommended Resources

> **▶ sqlzoo.net Level 7+** — Interactive aggregate exercises directly in the browser
>
> **▶ HackerRank SQL Easy section** — Practice COUNT, SUM, AVG, GROUP BY in a competitive environment

---

*Day 31 Complete.* ✅
