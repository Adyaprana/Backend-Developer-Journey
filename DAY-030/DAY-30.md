# DAY 30 — SQL JOINs: THE MOST IMPORTANT SQL TOPIC

> **Goal:** Master every type of SQL JOIN — combine data from multiple tables, find unmatched records, and understand self-joins. Every backend role needs this.
>
> **Week:** W5 — SQL + PostgreSQL (Days 29–42)
>
> **Status:** ✅

---

# 🎯 Learning Roadmap

```
SQL JOINs — Most Important SQL Topic

  ✅ INNER JOIN — records that match in both tables
  ✅ LEFT JOIN  — all left + matching right records
  ✅ RIGHT JOIN, FULL OUTER JOIN
  ✅ Practice: Create users + orders tables, write JOIN queries
  ✅ Self-join (employee-manager relationship)

  ▶ sqlzoo.net — Level 4 to 6 (JOINs section)
```

## Day 30 Checklist

- [ ] Explain what a JOIN is and why databases need it
- [ ] Draw the Venn diagram for each JOIN type from memory
- [ ] Write INNER JOIN and explain what disappears
- [ ] Write LEFT JOIN and explain what NULL means
- [ ] Find users who have NO orders using LEFT JOIN + IS NULL
- [ ] Write a SELF JOIN for the employee-manager relationship
- [ ] Solve LeetCode 175 — Combine Two Tables ✅
- [ ] Solve LeetCode 584 — Find Customer Referee ✅
- [ ] Solve LeetCode 595 — Big Countries ✅
- [ ] Solve LeetCode 577 — Employee Bonus ✅
- [ ] Solve LeetCode 181 — Employees Earning More Than Their Managers ✅


---

# SECTION 1 — CONCEPTUAL SUMMARY

## Why Do We Need JOINs?

Real databases never store everything in one giant table. That would create enormous duplication and inconsistency. Instead, data is split into multiple related tables.

```
ONE BIG TABLE (bad design):
┌────┬────────────┬─────────┬──────────┬───────┐
│ id │ user_name  │ city    │ product  │ price │
├────┼────────────┼─────────┼──────────┼───────┤
│  1 │ Adyaprana  │ Blore   │ Laptop   │ 80000 │
│  1 │ Adyaprana  │ Blore   │ Mouse    │  1200 │
│  2 │ Rahul      │ Delhi   │ Keyboard │  2500 │
└────┴────────────┴─────────┴──────────┴───────┘
Problem: Adyaprana's name and city are repeated.
         If city changes → must update every row.
         Inconsistency risk.

NORMALIZED (correct design):
users table:          orders table:
┌────┬────────────┐   ┌──────────┬─────────┬──────────┬───────┐
│ id │ name       │   │ order_id │ user_id │ product  │ price │
├────┼────────────┤   ├──────────┼─────────┼──────────┼───────┤
│  1 │ Adyaprana  │   │      101 │       1 │ Laptop   │ 80000 │
│  2 │ Rahul      │   │      102 │       1 │ Mouse    │  1200 │
│  3 │ Priya      │   │      103 │       2 │ Keyboard │  2500 │
└────┴────────────┘   └──────────┴─────────┴──────────┴───────┘

JOIN brings these back together when needed.
```

**JOIN = the glue that combines related tables in a single query.**

---

## The Four JOIN Types — Venn Diagram

```
TABLE A (users)          TABLE B (orders)
   ┌──────────┐             ┌──────────┐
   │  Priya   │             │ Monitor  │
   │  Ankit   │   ┌─────┐   │ (user 5) │
   │          │   │Match│   │          │
   │ Adyaprana│───│─────│───│ Laptop   │
   │  Rahul   │   │ ing │   │ Mouse    │
   │          │   └─────┘   │ Keyboard │
   └──────────┘             └──────────┘

INNER JOIN    → Only the overlapping middle section
LEFT JOIN     → All of A + overlapping middle
RIGHT JOIN    → All of B + overlapping middle
FULL OUTER    → Everything from both A and B
```

---

## INNER JOIN — Only Matching Records

INNER JOIN returns rows that have a **matching value in both tables**. If a user has no order, they disappear. If an order has no matching user, it disappears too.

Think of it as the intersection of two sets — only what both tables have in common.

```
users:               orders:
Adyaprana ──────────► Laptop     ✅ matched
Rahul     ──────────► Keyboard   ✅ matched
Priya     (no order)             ❌ excluded
Ankit     (no order)             ❌ excluded
          order user_id=5 (no user)  ❌ excluded

INNER JOIN result:
Adyaprana | Laptop
Rahul     | Keyboard
```

**Backend use:** "Show me all orders with the customer's name" — you only care about orders that have a real customer attached.

---

## LEFT JOIN — Everything from Left + Matching from Right

LEFT JOIN keeps **every row from the left table**, and fills in NULL for the right table columns when no match is found.

```
users (LEFT):         orders (RIGHT):
Adyaprana ──────────► Laptop     ✅ has data
Rahul     ──────────► Keyboard   ✅ has data
Priya     ─── NULL ──► (nothing)  NULL returned
Ankit     ─── NULL ──► (nothing)  NULL returned

LEFT JOIN result:
Adyaprana | Laptop
Rahul     | Keyboard
Priya     | NULL       ← still appears, just no order data
Ankit     | NULL       ← still appears, just no order data
```

**Backend use:** "Show me all users — even those who haven't placed any orders yet." Also: "Find users who have NEVER ordered" by filtering `WHERE orders.order_id IS NULL`.

---

## RIGHT JOIN — Everything from Right + Matching from Left

RIGHT JOIN keeps **every row from the right table**, and fills in NULL for the left table when no match is found. It is the mirror image of LEFT JOIN.

```
users (LEFT):         orders (RIGHT):
Adyaprana ──────────► Laptop     ✅ has data
Rahul     ──────────► Keyboard   ✅ has data
(no user) ─── NULL ──► Monitor   ← orphan order still appears

RIGHT JOIN result:
Adyaprana | Laptop
Rahul     | Keyboard
NULL      | Monitor    ← order without a user still appears
```

**Backend use:** "Show me all orders — even if the customer account was deleted" (orphan orders). In practice, RIGHT JOIN is rare; most developers rewrite it as a LEFT JOIN by swapping table order.

---

## FULL OUTER JOIN — Everything from Both Tables

FULL OUTER JOIN returns **all rows from both tables**. Where there is no match, NULL fills the gap.

```
FULL OUTER JOIN result:
Adyaprana | Laptop      ← matched
Rahul     | Keyboard    ← matched
Priya     | NULL        ← user with no order
Ankit     | NULL        ← user with no order
NULL      | Monitor     ← order with no user
```

**Backend use:** Data reconciliation — "Find all records that don't have a match on either side." Useful for data audits, migration checks, finding orphaned records in both directions.

---

## SELF JOIN — A Table Joins Itself

A SELF JOIN is when a table is joined with itself. It is used when a table has a column that references another row in the same table.

The classic example is an **employees table** where a manager is also an employee:

```
employees table:
┌────────┬────────────────┬────────────┐
│ emp_id │ employee_name  │ manager_id │
├────────┼────────────────┼────────────┤
│      1 │ CEO            │ NULL       │ ← has no manager
│      2 │ Manager        │ 1          │ ← reports to CEO (emp_id=1)
│      3 │ Developer A    │ 2          │ ← reports to Manager (emp_id=2)
│      4 │ Developer B    │ 2          │ ← reports to Manager (emp_id=2)
└────────┴────────────────┴────────────┘

Self join connects: employees.manager_id → employees.emp_id
Result: each employee listed next to their manager's name
```

---

## Primary Key vs Foreign Key

```
PRIMARY KEY:
  → Uniquely identifies each row in a table
  → Cannot be NULL
  → Cannot have duplicates
  → Example: users.id

FOREIGN KEY:
  → References the PRIMARY KEY of another table
  → Creates the relationship between tables
  → Can have duplicates (many orders can belong to one user)
  → Can be NULL (optional relationship)
  → Example: orders.user_id references users.id

THE JOIN CONDITION:
  ON users.id = orders.user_id
  ↑ Primary Key    ↑ Foreign Key
```

---

# SECTION 2 — FULL WORKING CODE TEMPLATE

## Complete JOIN Script — Copy and Run in pgAdmin

```sql
-- ═══════════════════════════════════════════════════════════════
-- DAY 30 — SQL JOINs: COMPLETE WORKING SCRIPT
-- Copy this entire script into pgAdmin Query Editor and run it.
-- ═══════════════════════════════════════════════════════════════


-- ─────────────────────────────────────────────────────────────────
-- STEP 1: CLEANUP — Drop existing tables in correct order
-- orders must be dropped before users (foreign key dependency)
-- ─────────────────────────────────────────────────────────────────

DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS employees;
DROP TABLE IF EXISTS users;


-- ─────────────────────────────────────────────────────────────────
-- STEP 2: CREATE TABLES
-- ─────────────────────────────────────────────────────────────────

-- Users table: one row per user
CREATE TABLE users (
    id   INTEGER      PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    city VARCHAR(100)
);

-- Orders table: one row per order
-- user_id is a FOREIGN KEY referencing users.id
CREATE TABLE orders (
    order_id INTEGER      PRIMARY KEY,
    user_id  INTEGER,              -- Links to users.id (foreign key)
    product  VARCHAR(100),
    amount   INTEGER
);

-- Employees table: manager_id references emp_id in the SAME table
CREATE TABLE employees (
    emp_id        INTEGER      PRIMARY KEY,
    employee_name VARCHAR(100) NOT NULL,
    manager_id    INTEGER      -- References emp_id in the same table (self-join)
);


-- ─────────────────────────────────────────────────────────────────
-- STEP 3: INSERT DATA
-- ─────────────────────────────────────────────────────────────────

-- Users: 4 users — Priya and Ankit will have no orders
INSERT INTO users VALUES
(1, 'Adyaprana', 'Bangalore'),
(2, 'Rahul',     'Delhi'),
(3, 'Priya',     'Mumbai'),
(4, 'Ankit',     'Pune');

-- Orders: user_id=5 doesn't exist in users → orphan order
INSERT INTO orders VALUES
(101, 1, 'Laptop',   80000),
(102, 1, 'Mouse',     1200),
(103, 2, 'Keyboard',  2500),
(104, 5, 'Monitor',  15000);    -- user_id=5 doesn't exist → orphan order

-- Employees: CEO has no manager (NULL), everyone else reports to someone
INSERT INTO employees VALUES
(1, 'CEO',         NULL),   -- Top of the hierarchy
(2, 'Manager',     1),      -- Reports to CEO (emp_id=1)
(3, 'Developer A', 2),      -- Reports to Manager (emp_id=2)
(4, 'Developer B', 2);      -- Reports to Manager (emp_id=2)


-- ─────────────────────────────────────────────────────────────────
-- STEP 4: VIEW RAW TABLES (always verify before joining)
-- ─────────────────────────────────────────────────────────────────

SELECT * FROM users;
SELECT * FROM orders;
SELECT * FROM employees;


-- ─────────────────────────────────────────────────────────────────
-- STEP 5: INNER JOIN
-- Returns ONLY rows where users.id = orders.user_id
-- Priya (id=3) and Ankit (id=4) have no orders → excluded
-- order_id=104 (user_id=5) has no user → excluded
-- ─────────────────────────────────────────────────────────────────

SELECT
    users.id,
    users.name,
    users.city,
    orders.product,
    orders.amount
FROM users
INNER JOIN orders
ON users.id = orders.user_id;

-- Expected result:
-- id | name      | city      | product  | amount
-- ---+-----------+-----------+----------+-------
--  1 | Adyaprana | Bangalore | Laptop   |  80000
--  1 | Adyaprana | Bangalore | Mouse    |   1200
--  2 | Rahul     | Delhi     | Keyboard |   2500


-- ─────────────────────────────────────────────────────────────────
-- STEP 6: LEFT JOIN
-- Returns ALL users + matching orders
-- Priya and Ankit appear with NULL in the orders columns
-- The orphan order (user_id=5) is still excluded (it's on the RIGHT)
-- ─────────────────────────────────────────────────────────────────

SELECT
    users.name,
    orders.product,
    orders.amount
FROM users
LEFT JOIN orders
ON users.id = orders.user_id;

-- Expected result:
-- name      | product  | amount
-- ----------+----------+-------
-- Adyaprana | Laptop   |  80000
-- Adyaprana | Mouse    |   1200
-- Rahul     | Keyboard |   2500
-- Priya     | NULL     |   NULL   ← no order, but still appears
-- Ankit     | NULL     |   NULL   ← no order, but still appears


-- ─────────────────────────────────────────────────────────────────
-- STEP 7: RIGHT JOIN
-- Returns ALL orders + matching users
-- The orphan order (user_id=5) appears with NULL for user columns
-- Priya and Ankit (no orders) are excluded (they're on the LEFT)
-- ─────────────────────────────────────────────────────────────────

SELECT
    users.name,
    orders.order_id,
    orders.product,
    orders.amount
FROM users
RIGHT JOIN orders
ON users.id = orders.user_id;

-- Expected result:
-- name      | order_id | product  | amount
-- ----------+----------+----------+-------
-- Adyaprana |      101 | Laptop   |  80000
-- Adyaprana |      102 | Mouse    |   1200
-- Rahul     |      103 | Keyboard |   2500
-- NULL      |      104 | Monitor  |  15000   ← orphan order, no user


-- ─────────────────────────────────────────────────────────────────
-- STEP 8: FULL OUTER JOIN
-- Returns EVERYTHING — matched, unmatched users, unmatched orders
-- ─────────────────────────────────────────────────────────────────

SELECT
    users.name,
    orders.order_id,
    orders.product,
    orders.amount
FROM users
FULL OUTER JOIN orders
ON users.id = orders.user_id;

-- Expected result:
-- name      | order_id | product  | amount
-- ----------+----------+----------+-------
-- Adyaprana |      101 | Laptop   |  80000
-- Adyaprana |      102 | Mouse    |   1200
-- Rahul     |      103 | Keyboard |   2500
-- Priya     |     NULL | NULL     |   NULL   ← user with no order
-- Ankit     |     NULL | NULL     |   NULL   ← user with no order
-- NULL      |      104 | Monitor  |  15000   ← order with no user


-- ─────────────────────────────────────────────────────────────────
-- STEP 9: SELF JOIN — Employee + Manager
-- The employees table joins with ITSELF
-- e = employee alias, m = manager alias (same table, two roles)
-- LEFT JOIN used so CEO (NULL manager) still appears
-- ─────────────────────────────────────────────────────────────────

SELECT
    e.employee_name AS employee,
    m.employee_name AS manager
FROM employees e
LEFT JOIN employees m
ON e.manager_id = m.emp_id;

-- Expected result:
-- employee    | manager
-- ------------+---------
-- CEO         | NULL       ← CEO has no manager
-- Manager     | CEO
-- Developer A | Manager
-- Developer B | Manager


-- ─────────────────────────────────────────────────────────────────
-- STEP 10: PRACTICAL PATTERNS (most asked in interviews)
-- ─────────────────────────────────────────────────────────────────

-- Pattern 1: Users who HAVE placed at least one order
SELECT DISTINCT
    users.name
FROM users
INNER JOIN orders
ON users.id = orders.user_id;

-- Result: Adyaprana, Rahul


-- Pattern 2: Users who have NEVER placed an order
-- Trick: LEFT JOIN + filter WHERE right side IS NULL
SELECT
    users.name
FROM users
LEFT JOIN orders
ON users.id = orders.user_id
WHERE orders.order_id IS NULL;

-- Result: Priya, Ankit


-- Pattern 3: Orders that belong to NO user (orphan orders)
-- Trick: RIGHT JOIN + filter WHERE left side IS NULL
SELECT
    orders.order_id,
    orders.product,
    orders.amount
FROM users
RIGHT JOIN orders
ON users.id = orders.user_id
WHERE users.id IS NULL;

-- Result: order_id=104, Monitor, 15000


-- Pattern 4: Total spending per user (with names)
SELECT
    users.name,
    SUM(orders.amount)  AS total_spent,
    COUNT(orders.order_id) AS order_count
FROM users
INNER JOIN orders
ON users.id = orders.user_id
GROUP BY users.name
ORDER BY total_spent DESC;

-- Result:
-- name      | total_spent | order_count
-- ----------+-------------+------------
-- Adyaprana |       81200 |           2
-- Rahul     |        2500 |           1


-- Pattern 5: Show ALL users even if no order, with total (NULL if no orders)
SELECT
    users.name,
    COALESCE(SUM(orders.amount), 0) AS total_spent
FROM users
LEFT JOIN orders
ON users.id = orders.user_id
GROUP BY users.name
ORDER BY total_spent DESC;

-- Result:
-- name      | total_spent
-- ----------+------------
-- Adyaprana |       81200
-- Rahul     |        2500
-- Priya     |           0   ← COALESCE converts NULL to 0
-- Ankit     |           0


-- Pattern 6: Using table aliases for cleaner queries
-- Instead of writing full table names, use aliases
SELECT
    u.name,
    o.product,
    o.amount
FROM users u              -- 'u' is alias for users
INNER JOIN orders o       -- 'o' is alias for orders
ON u.id = o.user_id
WHERE o.amount > 5000;

-- Result: only high-value orders with user names
```

---

## Practice Challenges Script

```sql
-- ═══════════════════════════════════════════════════════════════
-- PRACTICE CHALLENGES — Run after the main script above
-- ═══════════════════════════════════════════════════════════════


-- Challenge 1: Show all products purchased by Adyaprana
SELECT
    u.name,
    o.product,
    o.amount
FROM users u
INNER JOIN orders o
ON u.id = o.user_id
WHERE u.name = 'Adyaprana';

-- Expected: Laptop 80000, Mouse 1200


-- Challenge 2: Find orders that don't belong to any user
SELECT
    o.order_id,
    o.product,
    o.amount
FROM users u
RIGHT JOIN orders o
ON u.id = o.user_id
WHERE u.id IS NULL;

-- Expected: order_id=104, Monitor, 15000


-- Challenge 3: List every employee with their manager's name
SELECT
    e.employee_name AS employee,
    COALESCE(m.employee_name, 'No Manager') AS manager
FROM employees e
LEFT JOIN employees m
ON e.manager_id = m.emp_id;

-- Expected: CEO - No Manager, Manager - CEO, Developer A - Manager, etc.


-- Challenge 4: Add a new user with no orders, verify in LEFT JOIN
INSERT INTO users VALUES (5, 'Sneha', 'Chennai');

SELECT
    u.name,
    o.product
FROM users u
LEFT JOIN orders o
ON u.id = o.user_id
WHERE u.name = 'Sneha';
-- Expected: Sneha | NULL


-- Challenge 5: Add an order with non-existent user_id, verify in RIGHT JOIN
INSERT INTO orders VALUES (109, 9, 'TV', 40000);

SELECT
    u.name,
    o.order_id,
    o.product
FROM users u
RIGHT JOIN orders o
ON u.id = o.user_id
WHERE u.id IS NULL;
-- Expected: NULL | 109 | TV, NULL | 104 | Monitor


-- Challenge 6: Show users from Bangalore who have placed orders
SELECT
    u.name,
    u.city,
    o.product
FROM users u
INNER JOIN orders o
ON u.id = o.user_id
WHERE u.city = 'Bangalore';

-- Expected: Adyaprana | Bangalore | Laptop, Mouse


-- Challenge 7: Show total amount spent, only for users who spent more than ₹5000
SELECT
    u.name,
    SUM(o.amount) AS total_spent
FROM users u
INNER JOIN orders o
ON u.id = o.user_id
GROUP BY u.name
HAVING SUM(o.amount) > 5000
ORDER BY total_spent DESC;

-- Expected: Adyaprana 81200


-- Challenge 8: Full audit — show every user and every order, matched or not
SELECT
    COALESCE(u.name, 'Unknown User')    AS user_name,
    COALESCE(o.product, 'No Order')     AS product,
    COALESCE(o.amount::TEXT, 'N/A')     AS amount
FROM users u
FULL OUTER JOIN orders o
ON u.id = o.user_id
ORDER BY u.name NULLS LAST;
```

---

## LeetCode 175 — Combine Two Tables

```sql
-- ═══════════════════════════════════════════════════════════════
-- LeetCode #175 — Combine Two Tables
-- Difficulty: Easy | Status: ✅ Accepted (8/8 test cases)
-- Runtime: 268ms | Memory: 0.00 MB | Beats memory: 100%
-- ═══════════════════════════════════════════════════════════════

-- Problem: Show firstName, lastName, city, state for EVERY person.
-- If a person has no address, return NULL for city and state.

-- Setup
DROP TABLE IF EXISTS Address;
DROP TABLE IF EXISTS Person;

CREATE TABLE Person (
    personId  INT PRIMARY KEY,
    firstName VARCHAR(50),
    lastName  VARCHAR(50)
);

CREATE TABLE Address (
    addressId INT PRIMARY KEY,
    personId  INT,
    city      VARCHAR(100),
    state     VARCHAR(100),
    FOREIGN KEY (personId) REFERENCES Person(personId)
);

INSERT INTO Person (personId, firstName, lastName) VALUES
(1, 'Wang',  'Allen'),
(2, 'Alice', 'Bob');

INSERT INTO Address (addressId, personId, city, state) VALUES
(1, 2, 'New York City', 'New York');
-- Note: personId=1 (Wang/Allen) has NO address → will show NULL

-- View tables
SELECT * FROM Person;
SELECT * FROM Address;

-- SOLUTION: LEFT JOIN because we need EVERY person
-- Person is the left table (every row must appear)
-- Address is the right table (NULL if no match)
SELECT
    Person.firstName,
    Person.lastName,
    Address.city,
    Address.state
FROM Person
LEFT JOIN Address
ON Person.personId = Address.personId;

-- Why LEFT JOIN and not INNER JOIN?
-- INNER JOIN would EXCLUDE Wang/Allen (no address) → wrong answer
-- LEFT JOIN KEEPS Wang/Allen and shows NULL for city/state → correct

-- Expected Output:
-- firstName | lastName | city          | state
-- ----------+----------+---------------+----------
-- Wang      | Allen    | NULL          | NULL
-- Alice     | Bob      | New York City | New York
```

---

## LeetCode 584 — Find Customer Referee

```sql
-- ═══════════════════════════════════════════════════════════════
-- LeetCode #584 — Find Customer Referee
-- Difficulty: Easy | Status: ✅ Accepted (19/19 test cases)
-- Runtime: 266ms | Memory: 0.00 MB | Beats memory: 100%
-- ═══════════════════════════════════════════════════════════════

-- Problem: Find customers NOT referred by customer with id=2.
-- Also include customers with no referee at all (referee_id IS NULL).

-- Setup
DROP TABLE IF EXISTS Customer;

CREATE TABLE Customer (
    id          INT PRIMARY KEY,
    name        VARCHAR(255),
    referee_id  INT    -- Can be NULL (no referee)
);

INSERT INTO Customer (id, name, referee_id) VALUES
(1, 'Will', NULL),   -- No referee → should appear
(2, 'Jane', NULL),   -- No referee → should appear
(3, 'Alex', 2),      -- Referred by customer 2 → EXCLUDE
(4, 'Bill', NULL),   -- No referee → should appear
(5, 'Zack', 1),      -- Referred by customer 1 → should appear
(6, 'Mark', 2);      -- Referred by customer 2 → EXCLUDE

SELECT * FROM Customer;

-- SOLUTION
-- Two valid cases:
-- Case 1: referee_id is NOT 2 (referred by someone else)
-- Case 2: referee_id IS NULL (not referred by anyone)
-- Use OR to combine both conditions
SELECT
    name
FROM Customer
WHERE referee_id != 2
   OR referee_id IS NULL;

-- WHY IS NULL is required:
-- In SQL, NULL means "unknown/missing"
-- NULL != 2 evaluates to UNKNOWN (not TRUE and not FALSE)
-- So 'referee_id != 2' alone would EXCLUDE NULL rows (wrong!)
-- We must explicitly add 'OR referee_id IS NULL'

-- Expected Output:
-- name
-- ----
-- Will
-- Jane
-- Bill
-- Zack
```

---

## LeetCode 595 — Big Countries

```sql
-- ═══════════════════════════════════════════════════════════════
-- LeetCode #595 — Big Countries
-- Difficulty: Easy | Status: ✅ Accepted (7/7 test cases)
-- Runtime: 303ms | Memory: Optimized | Beats memory: 100%
-- ═══════════════════════════════════════════════════════════════

-- Problem: A country is "big" if area >= 3,000,000 OR population >= 25,000,000
-- Return name, population, area for all big countries.

-- Setup
DROP TABLE IF EXISTS World;

CREATE TABLE World (
    name        VARCHAR(255) PRIMARY KEY,
    continent   VARCHAR(255),
    area        INT,
    population  INT,
    gdp         BIGINT
);

INSERT INTO World (name, continent, area, population, gdp) VALUES
('Afghanistan', 'Asia',   652230,  25500100,  20343000000),  -- Big: population >= 25M
('Albania',     'Europe',  28748,   2831741,  12960000000),  -- Not big
('Algeria',     'Africa', 2381741, 37100000, 188681000000),  -- Big: population >= 25M
('Andorra',     'Europe',    468,     78115,   3712000000),  -- Not big
('Angola',      'Africa', 1246700, 20609294, 100990000000);  -- Not big (area < 3M, pop < 25M)

SELECT * FROM World;

-- SOLUTION
-- A country qualifies if EITHER condition is true → use OR
SELECT
    name,
    population,
    area
FROM World
WHERE area >= 3000000
   OR population >= 25000000;

-- WHY OR and not AND?
-- AND would require BOTH conditions to be true (too restrictive)
-- OR returns countries satisfying at least one condition (correct)

-- Expected Output:
-- name        | population | area
-- ------------+------------+---------
-- Afghanistan |   25500100 |  652230
-- Algeria     |   37100000 | 2381741
```

---
```sql
-- ═══════════════════════════════════════════════════════════════
-- LeetCode #577 — Employee Bonus
-- Difficulty: Easy | Status: ✅ Accepted (26/26 test cases)
-- Runtime: 266ms | Memory: 0.00 MB | Beats Memory: 100%
-- ═══════════════════════════════════════════════════════════════

-- Problem:
-- Show the name and bonus of every employee whose bonus is
-- less than 1000.
-- Employees without a bonus should also be included.

-- Setup
DROP TABLE IF EXISTS Bonus;
DROP TABLE IF EXISTS Employee;

CREATE TABLE Employee (
    empId INT PRIMARY KEY,
    name VARCHAR(50),
    supervisor INT,
    salary INT
);

CREATE TABLE Bonus (
    empId INT,
    bonus INT,
    FOREIGN KEY (empId) REFERENCES Employee(empId)
);

INSERT INTO Employee (empId, name, supervisor, salary) VALUES
(3, 'Brad', NULL, 4000),
(1, 'John', 3, 1000),
(2, 'Dan', 3, 2000),
(4, 'Thomas', 3, 4000);

INSERT INTO Bonus (empId, bonus) VALUES
(2, 500),
(4, 2000);
-- Brad and John have NO bonus record

-- View Tables
SELECT * FROM Employee;
SELECT * FROM Bonus;

-- SOLUTION:
-- LEFT JOIN keeps every employee.
-- Employees without a bonus will have NULL.
-- We keep employees whose bonus is less than 1000
-- OR whose bonus is NULL.

SELECT
    Employee.name,
    Bonus.bonus
FROM Employee
LEFT JOIN Bonus
ON Employee.empId = Bonus.empId
WHERE Bonus.bonus < 1000
   OR Bonus.bonus IS NULL;

-- Why LEFT JOIN?
-- INNER JOIN would remove employees without bonus records.
-- The problem requires employees with no bonus to appear.
-- LEFT JOIN keeps all employees and returns NULL
-- for missing bonus values.

-- Why IS NULL?
-- NULL cannot be compared using = or !=.
-- We must explicitly use IS NULL.

-- Expected Output:
--
-- name  | bonus
-- ------+-------
-- Brad  | NULL
-- John  | NULL
-- Dan   | 500
--
-- Thomas is NOT included because
-- his bonus is 2000 (>=1000).
```
---

```sql

-- ═══════════════════════════════════════════════════════════════
-- LeetCode #181 — Employees Earning More Than Their Managers
-- Difficulty: Easy | Status: ✅ Accepted (14/14 test cases)
-- Runtime: 220ms | Memory: 0.00 MB | Beats runtime: 98%
-- ═══════════════════════════════════════════════════════════════

-- Problem:
-- Find the names of employees whose salary is greater
-- than their manager's salary.

-- Setup
DROP TABLE IF EXISTS Employee;

CREATE TABLE Employee (
    id INT PRIMARY KEY,
    name VARCHAR(50),
    salary INT,
    managerId INT
);

INSERT INTO Employee (id, name, salary, managerId) VALUES
(1, 'Joe',   70000, 3),
(2, 'Henry', 80000, 4),
(3, 'Sam',   60000, NULL),
(4, 'Max',   90000, NULL);

-- View table
SELECT * FROM Employee;

-- SOLUTION: SELF JOIN
-- We join the Employee table with itself.
--
-- e1 → Manager
-- e2 → Employee
--
-- Match:
-- Manager's id = Employee's managerId
--
-- Then compare salaries.

SELECT
    e2.name AS Employee
FROM Employee e1
JOIN Employee e2
ON e1.id = e2.managerId
WHERE e1.salary < e2.salary;

-- Why SELF JOIN?
-- Managers are also employees and stored in the SAME table.
-- We need to compare two rows from the same table,
-- so we use a SELF JOIN with aliases.

-- Join Visualization
--
-- e1 (Manager)
--
-- id | name | salary
-- -------------------
-- 3  | Sam  | 60000
--
-- e2 (Employee)
--
-- id | name | salary | managerId
-- -------------------------------
-- 1  | Joe  | 70000  | 3
--
-- Matching Condition
--
-- e1.id = e2.managerId
-- 3     =      3
--
-- Salary Comparison
--
-- e1.salary < e2.salary
-- 60000     < 70000
--
-- Therefore:
-- Joe earns more than Sam.

-- Why not compare e1.salary > e2.salary?
-- That would return managers earning more than employees,
-- which is the opposite of the problem.

-- Expected Output:
--
-- Employee
-- --------
-- Joe

```
---
# SECTION 3 — IMPORTANT THINGS TO KNOW

## 1. JOIN Always Needs an ON Condition

```sql
-- ❌ WRONG — no ON condition → Cartesian product
SELECT * FROM users
INNER JOIN orders;
-- If users has 4 rows and orders has 4 rows → 4×4 = 16 rows (meaningless)

-- ✅ CORRECT — always specify the matching condition
SELECT * FROM users
INNER JOIN orders
ON users.id = orders.user_id;
```

A **Cartesian product** (also called a Cross Join) pairs every row from the left table with every row from the right table. For large tables, this produces billions of rows and crashes the database.

---

## 2. INNER JOIN Removes Unmatched Rows — Silently

```sql
-- You might think this shows all users:
SELECT users.name, orders.product
FROM users
INNER JOIN orders
ON users.id = orders.user_id;

-- But users with NO orders simply disappear.
-- There is no error. No warning. They just aren't in the result.
-- Use LEFT JOIN if you want to see all users regardless.
```

This silently missing data is a common bug in production backend applications.

---

## 3. NULL Is Not Equal to Anything

```sql
-- ❌ This will NOT find NULL rows
WHERE referee_id != 2;
-- NULL != 2 evaluates to UNKNOWN, not TRUE
-- So NULL rows are EXCLUDED from the result

-- ✅ Always add IS NULL explicitly
WHERE referee_id != 2
   OR referee_id IS NULL;

-- ❌ Never compare with = NULL
WHERE referee_id = NULL;   -- Always returns nothing!

-- ✅ Always use IS NULL / IS NOT NULL
WHERE referee_id IS NULL;
WHERE referee_id IS NOT NULL;
```

---

## 4. Self Join Requires Table Aliases

```sql
-- ❌ WRONG — SQL doesn't know which "employees" you mean
SELECT employee_name, employee_name
FROM employees
JOIN employees
ON manager_id = emp_id;

-- ✅ CORRECT — use aliases to distinguish the two roles
SELECT
    e.employee_name AS employee,
    m.employee_name AS manager
FROM employees e           -- 'e' = employee role
LEFT JOIN employees m      -- 'm' = manager role
ON e.manager_id = m.emp_id;
```

---

## 5. Drop Order Matters with Foreign Keys

```sql
-- ❌ WRONG — cannot drop users while orders references it
DROP TABLE IF EXISTS users;    -- Error if orders exists with foreign key

-- ✅ CORRECT — drop child table (orders) before parent (users)
DROP TABLE IF EXISTS orders;   -- Remove foreign key table first
DROP TABLE IF EXISTS users;    -- Then remove primary key table
```

---

## 6. LEFT JOIN to Find Missing Records (The Anti-Join Pattern)

```sql
-- One of the most useful patterns in backend development:
-- "Find all X that have no corresponding Y"

-- Users without any orders:
SELECT users.name
FROM users
LEFT JOIN orders ON users.id = orders.user_id
WHERE orders.order_id IS NULL;   -- NULL means no match was found

-- Products never ordered:
SELECT products.name
FROM products
LEFT JOIN order_items ON products.id = order_items.product_id
WHERE order_items.id IS NULL;

-- Students not enrolled in any course:
SELECT students.name
FROM students
LEFT JOIN enrollments ON students.id = enrollments.student_id
WHERE enrollments.id IS NULL;
```

---

## 7. Use Table Aliases for Readability

```sql
-- Without aliases (verbose, hard to read):
SELECT
    users.name,
    orders.product,
    orders.amount
FROM users
INNER JOIN orders
ON users.id = orders.user_id;

-- With aliases (clean, professional):
SELECT
    u.name,
    o.product,
    o.amount
FROM users u
INNER JOIN orders o
ON u.id = o.user_id;

-- Aliases are MANDATORY for self-joins (can't use same name twice)
SELECT e.employee_name, m.employee_name AS manager
FROM employees e
LEFT JOIN employees m
ON e.manager_id = m.emp_id;
```

---

# SECTION 4 — TOP INTERVIEW QUESTIONS & ANSWERS

## Q1. Show every user along with their orders.

**What the interviewer tests:** Can you write a basic INNER JOIN? Do you understand that unmatched records are excluded?

```sql
-- Show name + product + amount for users who have orders
SELECT
    u.name,
    o.product,
    o.amount
FROM users u
INNER JOIN orders o
ON u.id = o.user_id;

-- Note: Users with no orders (Priya, Ankit) do NOT appear.
-- If you want all users: use LEFT JOIN instead.
```

---

## Q2. Find users who never placed an order.

**What the interviewer tests:** The anti-join pattern — LEFT JOIN + IS NULL. This is asked constantly.

```sql
-- Step 1: LEFT JOIN keeps all users (even those with no orders)
-- Step 2: Filter WHERE orders.order_id IS NULL → no match found
SELECT
    u.name
FROM users u
LEFT JOIN orders o
ON u.id = o.user_id
WHERE o.order_id IS NULL;

-- Result: Priya, Ankit
-- Why not INNER JOIN? INNER JOIN would return an empty result
-- because Priya and Ankit have no orders to match.
```

---

## Q3. Show employees and their managers.

**What the interviewer tests:** Can you write a self-join? Do you understand when a table can reference itself?

```sql
-- Same table is used twice with different aliases
-- e = the employee row
-- m = the manager row (also an employee in the same table)
SELECT
    e.employee_name AS employee,
    m.employee_name AS manager
FROM employees e
LEFT JOIN employees m
ON e.manager_id = m.emp_id;

-- LEFT JOIN is used so the CEO (no manager) still appears
-- INNER JOIN would exclude the CEO row (manager_id IS NULL)
```

---

## Q4. What is the difference between INNER JOIN and LEFT JOIN?

**What the interviewer tests:** Conceptual understanding. This is the most common JOIN interview question.

```
INNER JOIN:
  → Returns ONLY rows that have a match in BOTH tables
  → Unmatched rows from either table are excluded
  → Use when: you only care about records that have a relationship
  → Example: Show orders with customer names (only existing customers)

LEFT JOIN:
  → Returns ALL rows from the LEFT table
  → Adds matching data from the RIGHT table
  → If no match: right-side columns show NULL
  → Use when: you want to keep all records from the main (left) table
  → Example: Show all customers, whether they've ordered or not
```

---

## Q5. What is a Foreign Key?

**What the interviewer tests:** Understanding of relational database design.

```
A Foreign Key is a column that references the PRIMARY KEY of another table.
It creates a relationship between two tables.

Example:
  users table:
    id INTEGER PRIMARY KEY   ← Primary Key

  orders table:
    user_id INTEGER          ← Foreign Key (references users.id)

The Foreign Key constraint ensures referential integrity:
  → You cannot insert an order with a user_id that doesn't exist in users
  → You cannot delete a user that has existing orders (unless CASCADE is set)

JOIN uses these keys:
  ON users.id = orders.user_id
     ↑ PK          ↑ FK
```

---

## Q6. What does NULL mean in a JOIN result?

**What the interviewer tests:** Understanding of NULL semantics in SQL.

```
NULL in a JOIN result means: no matching row was found in the other table.

LEFT JOIN:
  → users.name = 'Priya', orders.product = NULL
  → Means: Priya exists in users but has no entry in orders

RIGHT JOIN:
  → users.name = NULL, orders.product = 'Monitor'
  → Means: This order exists but its user_id has no match in users

FULL OUTER JOIN:
  → NULL on the left = row only in right table (orphan order)
  → NULL on the right = row only in left table (user without order)

NULL ≠ 0, NULL ≠ '', NULL ≠ FALSE
NULL means: unknown, missing, or no corresponding record.
```

---

## Q7. When would you use RIGHT JOIN vs LEFT JOIN?

**What the interviewer tests:** Whether you understand that RIGHT JOIN is just LEFT JOIN with tables swapped.

```sql
-- These two queries produce IDENTICAL results:

-- RIGHT JOIN version:
SELECT u.name, o.product
FROM users u
RIGHT JOIN orders o
ON u.id = o.user_id;

-- LEFT JOIN version (same result — just swapped table order):
SELECT u.name, o.product
FROM orders o
LEFT JOIN users u
ON o.user_id = u.id;

-- In practice:
-- Most developers AVOID RIGHT JOIN.
-- They rewrite it as LEFT JOIN by swapping the table order.
-- LEFT JOIN is more readable and universally understood.
-- RIGHT JOIN exists for completeness, but LEFT JOIN covers all cases.
```

---

## Q8. What is FULL OUTER JOIN used for in real applications?

**What the interviewer tests:** Practical knowledge of when to use FULL OUTER JOIN.

```sql
-- FULL OUTER JOIN is used for data reconciliation:
-- "Find everything that doesn't have a perfect match on either side"

-- Use case 1: Data migration audit
-- Old database users vs new database users — find discrepancies
SELECT
    old_db.user_id AS old_id,
    new_db.user_id AS new_id,
    old_db.email,
    new_db.email
FROM old_users old_db
FULL OUTER JOIN new_users new_db
ON old_db.email = new_db.email
WHERE old_db.user_id IS NULL     -- In new but not old
   OR new_db.user_id IS NULL;    -- In old but not new

-- Use case 2: Find unmatched records on both sides
SELECT
    u.name AS user_without_order,
    o.product AS order_without_user
FROM users u
FULL OUTER JOIN orders o ON u.id = o.user_id
WHERE u.id IS NULL OR o.order_id IS NULL;
```

---

# SECTION 5 — BACKEND CONNECTION

## JOINs in FastAPI + PostgreSQL

```
Every meaningful backend API endpoint uses JOINs.

GET /users/42/profile
─────────────────────────────────────────────
  SELECT u.name, u.email, a.city, a.country
  FROM users u
  LEFT JOIN addresses a ON u.id = a.user_id
  WHERE u.id = 42;

GET /orders (admin dashboard)
─────────────────────────────────────────────
  SELECT o.order_id, u.name, p.product_name, o.amount, o.status
  FROM orders o
  INNER JOIN users u    ON o.user_id = o.user_id
  INNER JOIN products p ON o.product_id = p.id
  ORDER BY o.created_at DESC;

GET /users/inactive (marketing)
─────────────────────────────────────────────
  SELECT u.name, u.email
  FROM users u
  LEFT JOIN orders o ON u.id = o.user_id
  WHERE o.order_id IS NULL;   ← users who never ordered

GET /employees/hierarchy (HR portal)
─────────────────────────────────────────────
  SELECT e.name, m.name AS manager
  FROM employees e
  LEFT JOIN employees m ON e.manager_id = m.id;
```

---

# JOIN TYPE SUMMARY TABLE

```
JOIN Type      │ Rows Returned                              │ NULL Appears When
───────────────┼────────────────────────────────────────────┼────────────────────────────────
INNER JOIN     │ Only rows matching in BOTH tables          │ Never (no unmatched rows)
LEFT JOIN      │ All left rows + matching right rows        │ Right side when no match
RIGHT JOIN     │ All right rows + matching left rows        │ Left side when no match
FULL OUTER     │ All rows from both tables                  │ Either side when no match
SELF JOIN      │ Table joined with itself                   │ Depends on join type used
CROSS JOIN     │ Every left row × every right row           │ Never (but produces huge results)
```

---

# REVISION SHEET

```
JOIN CHEAT SHEET

Syntax:
  SELECT columns
  FROM table_A
  [INNER/LEFT/RIGHT/FULL OUTER] JOIN table_B
  ON table_A.key = table_B.foreign_key;

INNER JOIN:
  → Only matching rows from both tables
  → Unmatched rows excluded silently

LEFT JOIN:
  → All rows from LEFT table
  → NULL on right side if no match
  → Use to find "all X even without Y"

LEFT JOIN + IS NULL:
  → Find records that have NO match in right table
  → "Find users who never ordered"
  → WHERE right_table.id IS NULL

RIGHT JOIN:
  → All rows from RIGHT table
  → NULL on left side if no match
  → Same as LEFT JOIN with tables swapped

FULL OUTER JOIN:
  → Everything from both tables
  → NULL on either side when no match
  → Use for data reconciliation/audits

SELF JOIN:
  → Table joins itself
  → MUST use aliases (FROM employees e JOIN employees m)
  → Use for hierarchies (employee-manager)

NULL RULES:
  → NULL != 2 → UNKNOWN (not true, not false)
  → Always use IS NULL, never = NULL
  → Add OR IS NULL when filtering NULLable columns

FOREIGN KEY:
  → References PRIMARY KEY of another table
  → Drop child table before parent table
  → JOIN connects PK to FK: ON users.id = orders.user_id
```

---

## LeetCode Solved This Day

| Problem | Difficulty | Topic | Status | Runtime |
|---------|-----------|-------|--------|---------|
| #175 Combine Two Tables | Easy | LEFT JOIN | ✅ Accepted 8/8 | 268ms |
| #584 Find Customer Referee | Easy | WHERE + IS NULL | ✅ Accepted 19/19 | 266ms |
| #595 Big Countries | Easy | WHERE + OR | ✅ Accepted 7/7 | 303ms |

---

## 🎥 Recommended Resource

> **▶ sqlzoo.net Level 4 to 6 (JOINs section)** — interactive SQL practice directly in the browser, immediate feedback, perfect for practicing every JOIN type

---

*Day 30 Complete.* ✅