# DAY 29 — SQL BASICS: PostgreSQL, CRUD Operations & Interview Prep

> **Goal:** Write SQL confidently — create tables, insert data, query it, update it, and delete it. Every backend role needs this.
>
> **Week:** W5 — SQL + PostgreSQL (Days 29–42)
>
> **Status:** ✅

---

# 🎯 Learning Roadmap

```
SQL Basics — SELECT, INSERT, UPDATE, DELETE

  ✅ Install PostgreSQL + pgAdmin (free GUI tool)
  ✅ CREATE TABLE, DROP TABLE, ALTER TABLE
  ✅ Data types: VARCHAR, INTEGER, BOOLEAN, TIMESTAMP, TEXT
  ✅ INSERT INTO, SELECT * FROM, WHERE clause
  ✅ UPDATE, DELETE with WHERE

  ▶ freeCodeCamp SQL Full Course (English) — start here
  ▶ sqlzoo.net — Level 1 to 3
```

## Day 29 Checklist

- [ ] Explain what PostgreSQL is and why backend devs use it
- [ ] Create a table with correct data types from memory
- [ ] Insert at least 4 rows into a table
- [ ] Use WHERE to filter results
- [ ] UPDATE a specific row without breaking others
- [ ] DELETE a specific row safely
- [ ] Use ALTER TABLE to add a column
- [ ] Explain the difference between DELETE, DROP, and TRUNCATE

---

# SECTION 1 — CONCEPTUAL SUMMARY

## What is PostgreSQL?

PostgreSQL is one of the world's most powerful open-source relational database management systems (RDBMS). It stores application data permanently in structured tables — like super-powered Excel sheets — and supports millions of records, complex queries, transactions, and JSON.

**Why backend developers use it:**

```
Without a database:
  Data lives in Python lists/dicts → disappears when program stops
  Cannot handle concurrent users
  Cannot search efficiently

With PostgreSQL:
  Data lives permanently on disk
  Handles thousands of simultaneous users
  Searches are fast with indexing
  Used by Instagram, Reddit, Spotify, Uber, and thousands of startups
```

**The backend connection:**

```
User signs up on your website
           ↓
Browser sends form data to FastAPI
           ↓
FastAPI runs: INSERT INTO users (...)
           ↓
PostgreSQL stores it permanently
           ↓
200 OK → User is registered
```

---

## What is pgAdmin?

pgAdmin is the free graphical interface (GUI) for PostgreSQL. Instead of typing commands in a terminal, you get a visual dashboard where you can:

```
✅ Create databases visually
✅ Browse tables and their data
✅ Write and run SQL queries in a query editor
✅ See results in a clean table format
✅ Manage users and permissions
```

Think of pgAdmin as VS Code for your database — the same way VS Code makes writing Python easier, pgAdmin makes writing SQL easier.

---

## What is a Database Schema?

A schema is the **blueprint** of your database. It defines the structure — which tables exist, what columns they have, what data types each column accepts, and what rules (constraints) apply.

```
Schema (Blueprint)
├── Table: users
│   ├── id        INTEGER  PRIMARY KEY
│   ├── name      VARCHAR(100)  NOT NULL
│   ├── email     VARCHAR(150)  UNIQUE
│   └── created_at TIMESTAMP   DEFAULT NOW()
│
├── Table: products
│   ├── product_id INTEGER  PRIMARY KEY
│   ├── name      VARCHAR(100)
│   └── price     INTEGER
│
└── Table: orders
    ├── order_id  INTEGER  PRIMARY KEY
    ├── user_id   INTEGER  (references users)
    └── product_id INTEGER (references products)
```

**Analogy:** A schema is like the blueprint of a building. The building itself (actual data) doesn't exist yet — the blueprint just describes what rooms (tables) exist, what they contain (columns), and what rules apply.

---

## What is a Table?

A table stores data in rows and columns — exactly like an Excel sheet, but more powerful.

```
TABLE: students
┌────┬─────────────┬─────┬───────────┬───────────────────────┬──────────────────────┐
│ id │ name        │ age │ is_active │ created_at            │ description          │
├────┼─────────────┼─────┼───────────┼───────────────────────┼──────────────────────┤
│  1 │ Adyaprana   │  23 │ TRUE      │ 2026-06-21 10:00:00   │ Backend Developer    │
│  2 │ Rahul       │  24 │ TRUE      │ 2026-06-21 10:00:00   │ Python Developer     │
│  3 │ Priya       │  22 │ FALSE     │ 2026-06-21 10:00:00   │ Frontend Developer   │
│  4 │ Ankit       │  25 │ TRUE      │ 2026-06-21 10:00:00   │ DevOps Engineer      │
└────┴─────────────┴─────┴───────────┴───────────────────────┴──────────────────────┘

Each row   = one record (one student)
Each column = one attribute (one property)
```

---

## Data Types — The Complete Guide

Every column in a table has a **data type** that defines what kind of data it can store.

```
DATA TYPE    │ WHAT IT STORES              │ EXAMPLE                   │ WHEN TO USE
─────────────┼─────────────────────────────┼───────────────────────────┼──────────────────────────
VARCHAR(n)   │ Text up to n characters     │ 'Adyaprana', 'adya@x.com' │ Names, emails, cities
INTEGER      │ Whole numbers               │ 23, 5432, 89999           │ Age, price, quantity, ID
BOOLEAN      │ TRUE or FALSE only          │ TRUE, FALSE               │ is_active, is_verified
TIMESTAMP    │ Date + time                 │ 2026-06-21 10:45:30       │ created_at, updated_at
TEXT         │ Unlimited-length text       │ Long blog post, bio       │ Descriptions, articles
SERIAL       │ Auto-incrementing integer   │ 1, 2, 3, 4 (auto)        │ Auto-generated IDs
NUMERIC(p,s) │ Precise decimal numbers     │ 9999.99                   │ Money, prices (precise)
DATE         │ Date only (no time)         │ 2026-06-21                │ Birthdays, deadlines
```

**VARCHAR vs TEXT — the exact difference:**

```
VARCHAR(100):
  → Maximum 100 characters
  → PostgreSQL enforces this limit
  → Use for: Names, emails, phone numbers, short codes
  → Fast for short values

TEXT:
  → No practical length limit
  → Use for: Product descriptions, blog posts, bios, logs
  → PostgreSQL stores them the same way internally
  → In PostgreSQL, TEXT and VARCHAR are essentially equal in performance
```

**Tip:** In PostgreSQL, there is no performance difference between `VARCHAR(n)` and `TEXT`. The only difference is the length constraint. Use `VARCHAR` when you want to enforce a maximum length; use `TEXT` when you don't care about the length.

---

## SQL Command Categories

Before learning individual commands, understand the categories:

```
DDL (Data Definition Language) — Define structure
  CREATE TABLE    → Build a new table
  DROP TABLE      → Delete a table entirely
  ALTER TABLE     → Modify an existing table

DML (Data Manipulation Language) — Work with data
  INSERT INTO     → Add new rows
  SELECT          → Read/retrieve rows
  UPDATE          → Modify existing rows
  DELETE          → Remove rows

DCL (Data Control Language) — Permissions
  GRANT           → Give access
  REVOKE          → Remove access

TCL (Transaction Control Language) — Transactions
  BEGIN           → Start a transaction
  COMMIT          → Save changes permanently
  ROLLBACK        → Undo changes
```

---

# SECTION 2 — FULL WORKING CODE TEMPLATE

## Students Table — Complete Script

```sql
-- ═══════════════════════════════════════════════════════════════
-- DAY 29 — SQL BASICS: COMPLETE WORKING SCRIPT
-- Copy this entire script into pgAdmin Query Editor and run it.
-- ═══════════════════════════════════════════════════════════════


-- ─────────────────────────────────────────────────────────────────
-- STEP 1: SAFETY CLEANUP
-- Drop the table if it already exists so we can start fresh.
-- IF EXISTS prevents an error if the table doesn't exist yet.
-- ─────────────────────────────────────────────────────────────────

DROP TABLE IF EXISTS students;


-- ─────────────────────────────────────────────────────────────────
-- STEP 2: CREATE TABLE
-- Define the structure of the students table.
-- Each column has a name, a data type, and optional constraints.
-- ─────────────────────────────────────────────────────────────────

CREATE TABLE students (
    id          INTEGER     PRIMARY KEY,      -- Unique identifier for each student
    name        VARCHAR(100) NOT NULL,        -- Student name, max 100 chars, required
    age         INTEGER,                      -- Age as a whole number
    is_active   BOOLEAN     DEFAULT TRUE,     -- Is the student currently active?
    created_at  TIMESTAMP   DEFAULT NOW(),    -- When was this record created?
    description TEXT                          -- Free-form notes about the student
);

-- Verify the table was created
SELECT column_name, data_type, character_maximum_length
FROM information_schema.columns
WHERE table_name = 'students';


-- ─────────────────────────────────────────────────────────────────
-- STEP 3: INSERT DATA
-- Add records to the table.
-- Values must match the column order and data types.
-- ─────────────────────────────────────────────────────────────────

INSERT INTO students (id, name, age, is_active, created_at, description)
VALUES
    (1, 'Adyaprana', 23, TRUE,  NOW(), 'Backend Developer'),
    (2, 'Rahul',     24, TRUE,  NOW(), 'Python Developer'),
    (3, 'Priya',     22, FALSE, NOW(), 'Frontend Developer'),
    (4, 'Ankit',     25, TRUE,  NOW(), 'DevOps Engineer'),
    (5, 'Sneha',     21, TRUE,  NOW(), 'Data Scientist');


-- ─────────────────────────────────────────────────────────────────
-- STEP 4: SELECT — Read all data
-- SELECT * means "give me all columns"
-- FROM students means "from the students table"
-- ─────────────────────────────────────────────────────────────────

SELECT * FROM students;


-- ─────────────────────────────────────────────────────────────────
-- STEP 5: SELECT specific columns
-- Instead of *, list only the columns you need.
-- Better practice in production — avoids fetching unnecessary data.
-- ─────────────────────────────────────────────────────────────────

SELECT name, age, description
FROM students;


-- ─────────────────────────────────────────────────────────────────
-- STEP 6: WHERE — Filter rows
-- Only return rows that match the condition.
-- ─────────────────────────────────────────────────────────────────

-- Students older than 22
SELECT * FROM students
WHERE age > 22;

-- Active students only
SELECT * FROM students
WHERE is_active = TRUE;

-- Find a specific student by name
SELECT * FROM students
WHERE name = 'Rahul';

-- Multiple conditions with AND
SELECT * FROM students
WHERE age > 22 AND is_active = TRUE;

-- Multiple conditions with OR
SELECT * FROM students
WHERE age < 22 OR description = 'DevOps Engineer';


-- ─────────────────────────────────────────────────────────────────
-- STEP 7: UPDATE — Modify existing data
-- ALWAYS use WHERE — without it, ALL rows are updated!
-- ─────────────────────────────────────────────────────────────────

-- Update Ankit's age
UPDATE students
SET age = 26
WHERE id = 4;

-- Verify the change
SELECT * FROM students WHERE id = 4;

-- Update multiple columns at once
UPDATE students
SET age = 24, description = 'Senior Python Developer'
WHERE id = 2;

-- Verify
SELECT * FROM students WHERE id = 2;


-- ─────────────────────────────────────────────────────────────────
-- STEP 8: DELETE — Remove a row
-- ALWAYS use WHERE — without it, ALL rows are deleted!
-- ─────────────────────────────────────────────────────────────────

-- Delete Priya (id = 3)
DELETE FROM students
WHERE id = 3;

-- Verify Priya is gone
SELECT * FROM students;


-- ─────────────────────────────────────────────────────────────────
-- STEP 9: ALTER TABLE — Modify the table structure
-- This changes the table itself, not just the data inside.
-- ─────────────────────────────────────────────────────────────────

-- Add a new column: email
ALTER TABLE students
ADD COLUMN email VARCHAR(150);

-- Add another column: score
ALTER TABLE students
ADD COLUMN score INTEGER DEFAULT 0;

-- See the updated table structure
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'students'
ORDER BY ordinal_position;


-- ─────────────────────────────────────────────────────────────────
-- STEP 10: Update newly added columns
-- ─────────────────────────────────────────────────────────────────

UPDATE students SET email = 'adya@example.com',    score = 95 WHERE id = 1;
UPDATE students SET email = 'rahul@example.com',   score = 87 WHERE id = 2;
UPDATE students SET email = 'ankit@example.com',   score = 91 WHERE id = 4;
UPDATE students SET email = 'sneha@example.com',   score = 98 WHERE id = 5;


-- ─────────────────────────────────────────────────────────────────
-- STEP 11: FINAL VIEW — See the complete updated table
-- ─────────────────────────────────────────────────────────────────

SELECT * FROM students;
```

---

## Products Table — Complete Script

```sql
-- ═══════════════════════════════════════════════════════════════
-- PRODUCTS TABLE — Full CRUD operations with real-world data
-- ═══════════════════════════════════════════════════════════════


-- STEP 1: Cleanup
DROP TABLE IF EXISTS products;


-- STEP 2: Create Table
CREATE TABLE products (
    product_id   INTEGER      PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    brand        VARCHAR(50),
    category     VARCHAR(50),
    price        INTEGER,
    stock        INTEGER,
    is_available BOOLEAN      DEFAULT TRUE,
    description  TEXT,
    rating       INTEGER,
    created_at   TIMESTAMP    DEFAULT CURRENT_TIMESTAMP
);


-- STEP 3: Insert Products
INSERT INTO products
(product_id, product_name, brand, category, price, stock, is_available, description)
VALUES
(1, 'iPhone 16',             'Apple',    'Mobile',     89999, 15, TRUE,  'Apple flagship smartphone'),
(2, 'Galaxy S25',            'Samsung',  'Mobile',     79999, 20, TRUE,  'Samsung flagship smartphone'),
(3, 'MacBook Air M4',        'Apple',    'Laptop',    124999,  8, TRUE,  'Lightweight laptop'),
(4, 'Dell XPS 15',           'Dell',     'Laptop',    145000,  5, TRUE,  'Premium Windows laptop'),
(5, 'Sennheiser Momentum 4', 'Sennheiser','Headphones', 26989, 5, TRUE,  'Premium over-ear headphones'),
(6, 'Sony WH-1000XM5',       'Sony',     'Headphones', 29999, 12, TRUE,  'Noise cancelling headphones'),
(7, 'Logitech MX Master 3S', 'Logitech', 'Mouse',       9999, 18, TRUE,  'Wireless productivity mouse'),
(8, 'HP Pavilion',           'HP',       'Laptop',     65000,  0, FALSE, 'Out of stock laptop');


-- STEP 4: View all
SELECT * FROM products;


-- STEP 5: Filter — expensive items above ₹50,000
SELECT product_name, brand, price
FROM products
WHERE price > 50000;


-- STEP 6: Filter — available products
SELECT * FROM products
WHERE is_available = TRUE;


-- STEP 7: Filter — specific brand
SELECT * FROM products
WHERE brand = 'Apple';


-- STEP 8: Update price
UPDATE products
SET price = 34990
WHERE product_id = 5;

SELECT * FROM products WHERE product_id = 5;


-- STEP 9: Mark product out of stock
UPDATE products
SET is_available = FALSE, stock = 0
WHERE product_id = 2;

SELECT * FROM products WHERE product_id = 2;


-- STEP 10: Delete out-of-stock HP Pavilion
DELETE FROM products
WHERE product_id = 8;

SELECT * FROM products;


-- STEP 11: Add rating column
ALTER TABLE products
ADD COLUMN IF NOT EXISTS rating INTEGER;


-- STEP 12: Update ratings
UPDATE products SET rating = 5 WHERE product_id = 1;
UPDATE products SET rating = 4 WHERE product_id = 2;
UPDATE products SET rating = 5 WHERE product_id = 3;
UPDATE products SET rating = 4 WHERE product_id = 4;
UPDATE products SET rating = 4 WHERE product_id = 5;
UPDATE products SET rating = 5 WHERE product_id = 6;
UPDATE products SET rating = 4 WHERE product_id = 7;


-- STEP 13: Final view
SELECT * FROM products;
```

---

## Connect Python to PostgreSQL

```python
# connect-sql.py
# Connects Python to your local PostgreSQL database
# Install: pip install psycopg

import psycopg

# Connection details — must match your PostgreSQL setup
conn = psycopg.connect(
    host="localhost",       # PostgreSQL server location
    dbname="backend_journey",  # Your database name
    user="postgres",        # Your PostgreSQL username
    password="postgres123", # Your PostgreSQL password
    port=5432               # Default PostgreSQL port
)

print("✅ Connected Successfully!")

# Create a cursor to run SQL queries
cursor = conn.cursor()

# Run a query
cursor.execute("SELECT * FROM students;")
rows = cursor.fetchall()

for row in rows:
    print(row)

# Always close the connection
cursor.close()
conn.close()
print("✅ Connection closed.")
```

---

# SECTION 3 — IMPORTANT THINGS TO KNOW

## 1. NEVER Forget WHERE in UPDATE

This is the most dangerous SQL mistake a developer can make.

```sql
-- ❌ DANGEROUS — updates EVERY row in the table
UPDATE students
SET age = 30;
-- Result: Every single student now has age = 30. Cannot easily undo.

-- ✅ CORRECT — only updates the specific row
UPDATE students
SET age = 30
WHERE id = 1;
```

**In production systems, this has caused major outages.**

Best practice: Before running any UPDATE, run a SELECT with the same WHERE clause first to confirm you're targeting the right rows.

```sql
-- Step 1: Verify the target first
SELECT * FROM students WHERE id = 1;

-- Step 2: Only then update
UPDATE students SET age = 30 WHERE id = 1;
```

---

## 2. NEVER Forget WHERE in DELETE

```sql
-- ❌ CATASTROPHIC — deletes ALL data in the table
DELETE FROM students;
-- The table still exists but is now completely empty.

-- ✅ CORRECT
DELETE FROM students
WHERE id = 3;
```

**The difference between DELETE, TRUNCATE, and DROP:**

```
DELETE FROM table WHERE condition;
  → Removes specific rows
  → Can use WHERE to filter
  → Can be rolled back inside a transaction
  → Slower (logs each deletion)

TRUNCATE TABLE students;
  → Removes ALL rows instantly
  → Cannot use WHERE
  → Much faster than DELETE for clearing a table
  → Keeps table structure intact

DROP TABLE students;
  → Destroys the ENTIRE TABLE including its structure
  → All data, columns, indexes are permanently gone
  → Use only when you want to delete the table itself
```

---

## 3. VARCHAR vs TEXT in PostgreSQL

```sql
-- VARCHAR(100): enforces maximum length
-- PostgreSQL will reject values longer than 100 characters
name VARCHAR(100)   -- Good for names, emails, short codes

-- TEXT: no length limit at all
-- PostgreSQL won't reject based on length
bio TEXT            -- Good for descriptions, articles, logs
```

In PostgreSQL specifically:

```
Performance: VARCHAR and TEXT have IDENTICAL performance internally.
Storage:     Both stored the same way on disk.
Difference:  Only the length constraint differs.

Rule of thumb:
  Use VARCHAR(n) when you want to ENFORCE a length limit (e.g., username max 50 chars)
  Use TEXT when length doesn't need to be restricted
```

---

## 4. PRIMARY KEY Must Be Unique

```sql
-- ❌ WILL FAIL — duplicate ID
INSERT INTO students (id, name) VALUES (1, 'Adya');
INSERT INTO students (id, name) VALUES (1, 'Rahul');
-- ERROR: duplicate key value violates unique constraint "students_pkey"

-- ✅ CORRECT — unique IDs
INSERT INTO students (id, name) VALUES (1, 'Adya');
INSERT INTO students (id, name) VALUES (2, 'Rahul');
```

**Better practice: use SERIAL for auto-incrementing IDs:**

```sql
CREATE TABLE students (
    id   SERIAL PRIMARY KEY,  -- Auto generates 1, 2, 3, 4...
    name VARCHAR(100)
);

-- Now you don't need to specify id in INSERT
INSERT INTO students (name) VALUES ('Adya');    -- Gets id = 1
INSERT INTO students (name) VALUES ('Rahul');   -- Gets id = 2
```

---

## 5. SQL Execution Order vs. Writing Order

You write SQL in this order:

```sql
SELECT name, age
FROM students
WHERE age > 22;
```

But SQL processes it in this order:

```
1. FROM students        → Load the table
2. WHERE age > 22       → Filter rows
3. SELECT name, age     → Pick columns to show
```

**Why this matters:**

```sql
-- You CANNOT use a SELECT alias in a WHERE clause
-- Because WHERE is processed BEFORE SELECT

SELECT age * 2 AS double_age
FROM students
WHERE double_age > 40;   -- ❌ ERROR! double_age doesn't exist yet at WHERE stage

-- Fix: use the original expression
SELECT age * 2 AS double_age
FROM students
WHERE age * 2 > 40;      -- ✅ Correct
```

---

## 6. NOT NULL Constraint

```sql
-- NOT NULL means the column MUST have a value — it cannot be empty
name VARCHAR(100) NOT NULL

-- ❌ This will fail
INSERT INTO students (id, age) VALUES (5, 23);
-- ERROR: null value in column "name" violates not-null constraint

-- ✅ This works
INSERT INTO students (id, name, age) VALUES (5, 'Adya', 23);
```

---

## 7. DEFAULT Values

```sql
-- DEFAULT means: if you don't provide a value, use this one
is_active  BOOLEAN   DEFAULT TRUE,
created_at TIMESTAMP DEFAULT NOW()

-- When you don't specify is_active:
INSERT INTO students (id, name, age) VALUES (1, 'Adya', 23);
-- is_active automatically becomes TRUE
-- created_at automatically becomes the current date and time
```

---

# SECTION 4 — TOP INTERVIEW QUESTIONS & ANSWERS

## Q1. Retrieve all active students older than 22

**What the interviewer is testing:** Can you combine multiple conditions using AND in a WHERE clause?

```sql
-- Question: Find all students who are both active AND older than 22

SELECT *
FROM students
WHERE age > 22
AND is_active = TRUE;

-- Expected result:
-- Rows where age > 22 AND is_active = TRUE both hold
-- If student is 25 but is_active = FALSE, they are excluded
-- If student is 20 but is_active = TRUE, they are excluded

-- More specific: only show name and age
SELECT name, age
FROM students
WHERE age > 22
AND is_active = TRUE
ORDER BY age DESC;
```

---

## Q2. A student's email changed. Update only that student.

**What the interviewer is testing:** Can you UPDATE a specific row using WHERE? Will you cause unintended updates to other rows?

```sql
-- Question: Student with id = 1 changed their email to newemail@example.com

-- First: Verify which row you're about to update (best practice)
SELECT * FROM students WHERE id = 1;

-- Then: Perform the update
UPDATE students
SET email = 'newemail@example.com'
WHERE id = 1;

-- Verify it changed
SELECT * FROM students WHERE id = 1;

-- WRONG approach (without WHERE):
UPDATE students
SET email = 'newemail@example.com';
-- This changes EVERY student's email to the same value!
```

---

## Q3. Remove the student named Rahul from the database

**What the interviewer is testing:** Can you DELETE a specific row? Do you know to use WHERE?

```sql
-- Question: The student Rahul (id = 2) has left. Remove their record.

-- First: Verify you're targeting the right row
SELECT * FROM students WHERE name = 'Rahul';

-- Then: Delete
DELETE FROM students
WHERE name = 'Rahul';

-- Better: use id instead of name (names can have duplicates)
DELETE FROM students
WHERE id = 2;

-- Verify deletion
SELECT * FROM students;
-- Rahul should no longer appear
```

---

## Q4. What is the difference between DELETE, DROP, and TRUNCATE?

**What the interviewer is testing:** Understanding of DDL vs DML and when to use each.

```
DELETE:
  → DML command
  → Removes specific rows based on WHERE condition
  → Table structure remains intact
  → Can be rolled back if inside a transaction
  → Slower for large deletions (logs each row)
  → Use: DELETE FROM students WHERE id = 2;

TRUNCATE:
  → DDL command (in most databases)
  → Removes ALL rows in the table instantly
  → Table structure remains intact
  → Cannot use WHERE clause
  → Much faster than DELETE for clearing entire table
  → Use: TRUNCATE TABLE students;

DROP:
  → DDL command
  → Destroys the ENTIRE TABLE — structure and all data
  → Cannot be recovered without a backup
  → Use: DROP TABLE students;
  → Use only when you want to eliminate the table completely
```

---

## Q5. What is a Primary Key?

**What the interviewer is testing:** Do you understand database fundamentals?

```
A Primary Key is a column (or combination of columns) that uniquely identifies
each row in a table.

Rules:
  1. Must be UNIQUE — no two rows can have the same primary key value
  2. Cannot be NULL — every row must have a primary key
  3. There can only be ONE primary key per table

Example:
  id INTEGER PRIMARY KEY

Why it's important:
  → Used to find a specific row quickly (with an index)
  → Used to link tables together (foreign keys reference primary keys)
  → FastAPI uses IDs in URLs: GET /users/42 → finds user with id = 42

SQL:
  CREATE TABLE users (
      id   SERIAL PRIMARY KEY,
      name VARCHAR(100) NOT NULL
  );
```

---

## Q6. What is the difference between WHERE and HAVING?

**What the interviewer is testing:** Do you understand SQL execution order and aggregation?

```sql
-- WHERE: filters rows BEFORE any grouping
-- Use with: SELECT, UPDATE, DELETE

SELECT * FROM students
WHERE age > 22;   -- Filters individual rows


-- HAVING: filters groups AFTER GROUP BY
-- Use only with GROUP BY aggregations

SELECT department, COUNT(*) AS student_count
FROM students
GROUP BY department
HAVING COUNT(*) > 5;   -- Only show departments with more than 5 students

-- Cannot use WHERE here:
-- WHERE COUNT(*) > 5   -- ❌ ERROR — WHERE cannot use aggregate functions
```

---

## Q7. How would you find all products in a specific category with a price below a threshold?

**What the interviewer is testing:** Practical SQL query writing with multiple conditions.

```sql
-- Find all Laptops under ₹1,00,000

SELECT product_name, brand, price
FROM products
WHERE category = 'Laptop'
AND price < 100000
ORDER BY price ASC;

-- Find all available products under ₹30,000
SELECT product_name, brand, category, price
FROM products
WHERE is_available = TRUE
AND price < 30000
ORDER BY price ASC;
```

---

## Q8. Write a query to increase the price of all Apple products by ₹5,000

**What the interviewer is testing:** Can you UPDATE using arithmetic? Can you use WHERE with a text condition?

```sql
-- First: see what you're about to change
SELECT product_name, price
FROM products
WHERE brand = 'Apple';

-- Then: update with arithmetic
UPDATE products
SET price = price + 5000    -- Add 5000 to the existing price
WHERE brand = 'Apple';

-- Verify
SELECT product_name, brand, price
FROM products
WHERE brand = 'Apple';
```

---

## Q9. What happens if you run SELECT * FROM a table with 10 million rows?

**What the interviewer is testing:** Production awareness and best practices.

```
In production, SELECT * FROM large_table is dangerous because:
  1. It transfers all 10 million rows across the network → very slow
  2. It loads everything into memory → high memory usage
  3. It returns more data than the client needs

Best practices:
  1. Always add a LIMIT clause: SELECT * FROM users LIMIT 100;
  2. Select only needed columns: SELECT name, email FROM users LIMIT 100;
  3. Use WHERE to filter: SELECT * FROM users WHERE created_at > NOW() - INTERVAL '7 days';
  4. Use pagination: LIMIT 20 OFFSET 40 (page 3 of 20-per-page results)

FastAPI pagination example:
  GET /users?page=2&limit=20
  → SELECT * FROM users LIMIT 20 OFFSET 20;
```

---

## Q10. What is the difference between NULL and an empty string?

**What the interviewer is testing:** Precision in understanding SQL data.

```sql
-- NULL = no value at all (the field was never filled in)
-- ''   = empty string (the field was filled with nothing)

-- Check for NULL:
SELECT * FROM students WHERE email IS NULL;       -- ✅ correct
SELECT * FROM students WHERE email = NULL;        -- ❌ wrong! Always use IS NULL

-- Check for empty string:
SELECT * FROM students WHERE email = '';          -- ✅ correct

-- Both are different:
INSERT INTO students (id, name, email) VALUES (10, 'Test', NULL);   -- email is absent
INSERT INTO students (id, name, email) VALUES (11, 'Test', '');     -- email is present but empty
```

---

# SECTION 5 — BACKEND CONNECTION

## How SQL Powers Every Backend Feature

```
USER REGISTRATION → INSERT
───────────────────────────────────────────────────────────────
POST /register
{
  "name": "Adyaprana",
  "email": "adya@example.com",
  "password": "hashed_password"
}
    ↓ FastAPI processes request
    ↓
INSERT INTO users (name, email, password_hash, created_at)
VALUES ('Adyaprana', 'adya@example.com', 'hash123', NOW());
    ↓
201 Created → User registered


USER LOGIN → SELECT + WHERE
───────────────────────────────────────────────────────────────
POST /login
{
  "email": "adya@example.com",
  "password": "mypassword"
}
    ↓
SELECT id, name, password_hash
FROM users
WHERE email = 'adya@example.com';
    ↓
Verify password hash → Generate JWT token → 200 OK


UPDATE PROFILE → UPDATE + WHERE
───────────────────────────────────────────────────────────────
PATCH /users/1
{
  "name": "Adya Pradhan"
}
    ↓
UPDATE users
SET name = 'Adya Pradhan', updated_at = NOW()
WHERE id = 1;
    ↓
200 OK → Profile updated


DELETE ACCOUNT → DELETE + WHERE
───────────────────────────────────────────────────────────────
DELETE /users/1
    ↓
DELETE FROM users
WHERE id = 1;
    ↓
204 No Content → Account deleted
```

---

## Python + psycopg Integration Pattern

```python
# How FastAPI + PostgreSQL work together (preview of what's coming)
import psycopg
from fastapi import FastAPI, HTTPException

app = FastAPI()

def get_connection():
    return psycopg.connect(
        host="localhost",
        dbname="backend_journey",
        user="postgres",
        password="postgres123"
    )

@app.get("/students")
def get_all_students():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, age, description FROM students;")
    students = cursor.fetchall()
    cursor.close()
    conn.close()
    return [{"id": s[0], "name": s[1], "age": s[2], "description": s[3]} for s in students]

@app.get("/students/{student_id}")
def get_student(student_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE id = %s;", (student_id,))
    # Note: Use %s placeholders — NEVER use f-strings with SQL (SQL injection risk!)
    student = cursor.fetchone()
    cursor.close()
    conn.close()
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"id": student[0], "name": student[1], "age": student[2]}

@app.post("/students")
def create_student(name: str, age: int, description: str = None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO students (name, age, description, created_at) VALUES (%s, %s, %s, NOW()) RETURNING id;",
        (name, age, description)
    )
    new_id = cursor.fetchone()[0]
    conn.commit()   # IMPORTANT: commit to save the INSERT
    cursor.close()
    conn.close()
    return {"id": new_id, "name": name, "age": age}
```

---

# SECTION 6 — 20 PRACTICE SQL CHALLENGES

## Easy Level

```sql
-- Challenge 1: Insert a new student
INSERT INTO students (id, name, age, is_active, created_at, description)
VALUES (6, 'Vikram', 26, TRUE, NOW(), 'Cloud Engineer');

-- Challenge 2: Show only name and age of all students
SELECT name, age FROM students;

-- Challenge 3: Find all students younger than 24
SELECT * FROM students WHERE age < 24;

-- Challenge 4: Find all inactive students
SELECT * FROM students WHERE is_active = FALSE;

-- Challenge 5: Update Vikram's age to 27
UPDATE students SET age = 27 WHERE id = 6;
SELECT * FROM students WHERE id = 6;

-- Challenge 6: Delete the student with id = 5
DELETE FROM students WHERE id = 5;
SELECT * FROM students;

-- Challenge 7: Add a phone_number column
ALTER TABLE students ADD COLUMN phone_number VARCHAR(15);

-- Challenge 8: Find the student named 'Adyaprana'
SELECT * FROM students WHERE name = 'Adyaprana';

-- Challenge 9: Show all students ordered by age (youngest first)
SELECT * FROM students ORDER BY age ASC;

-- Challenge 10: Show all students ordered by name alphabetically
SELECT * FROM students ORDER BY name ASC;
```

## Medium Level

```sql
-- Challenge 11: Find students aged between 22 and 25 (inclusive)
SELECT * FROM students
WHERE age >= 22 AND age <= 25;
-- Alternative: WHERE age BETWEEN 22 AND 25;

-- Challenge 12: Find students whose description contains 'Developer'
SELECT * FROM students
WHERE description LIKE '%Developer%';

-- Challenge 13: Update all inactive students to active
UPDATE students SET is_active = TRUE WHERE is_active = FALSE;

-- Challenge 14: Find students who have no email set yet
SELECT * FROM students WHERE email IS NULL;

-- Challenge 15: Count how many active students exist
SELECT COUNT(*) AS active_count
FROM students
WHERE is_active = TRUE;

-- Challenge 16: Update all student scores by adding 5 bonus points
UPDATE students SET score = score + 5;
SELECT * FROM students;

-- Challenge 17: Show only the top 3 highest-scoring students
SELECT name, score
FROM students
ORDER BY score DESC
LIMIT 3;

-- Challenge 18: Find students whose name starts with 'A'
SELECT * FROM students
WHERE name LIKE 'A%';

-- Challenge 19: Show the count of students per age group
SELECT age, COUNT(*) AS student_count
FROM students
GROUP BY age
ORDER BY age ASC;

-- Challenge 20: Rename the description column to bio
ALTER TABLE students RENAME COLUMN description TO bio;
SELECT * FROM students;
```

---

# SECTION 7 — COMMON INTERVIEW MISTAKES TO AVOID

```
1.  Missing WHERE in UPDATE          → Updates every row in the table
2.  Missing WHERE in DELETE          → Deletes all data
3.  Using = NULL instead of IS NULL  → Always use IS NULL / IS NOT NULL
4.  Forgetting to COMMIT             → Inserts/Updates don't save in transactions
5.  Using f-strings for SQL          → SQL injection vulnerability
6.  SELECT * in production           → Performance issue on large tables
7.  Dropping wrong table             → Use IF EXISTS as safety net
8.  Confusing DELETE and DROP        → DELETE removes rows; DROP removes the table
9.  Not adding NOT NULL              → Allows blank critical fields like email, name
10. Not checking SQL execution order → Confused about why WHERE alias fails
11. Using reserved words as names    → Don't name a column 'select' or 'from'
12. Forgetting semicolons            → Statements run together or fail
13. Case sensitivity in strings      → 'Rahul' ≠ 'rahul' (use LOWER() for safe search)
14. Confusing VARCHAR and CHAR       → CHAR pads with spaces; VARCHAR doesn't
15. No indexes on searched columns   → Slow queries on large tables
```

---

# REVISION SHEET

```
SQL COMMANDS AT A GLANCE

DDL (Structure):
  CREATE TABLE tablename (col datatype constraints, ...);
  DROP TABLE IF EXISTS tablename;
  ALTER TABLE tablename ADD COLUMN colname datatype;
  ALTER TABLE tablename RENAME COLUMN old TO new;
  ALTER TABLE tablename DROP COLUMN colname;

DML (Data):
  INSERT INTO tablename (col1, col2) VALUES (val1, val2);
  SELECT col1, col2 FROM tablename WHERE condition;
  UPDATE tablename SET col = val WHERE condition;
  DELETE FROM tablename WHERE condition;

DATA TYPES:
  VARCHAR(n)  → Short text with length limit (name, email)
  INTEGER     → Whole numbers (age, price, id)
  BOOLEAN     → TRUE or FALSE
  TIMESTAMP   → Date + time (created_at)
  TEXT        → Long text (description, bio)
  SERIAL      → Auto-incrementing integer (best for IDs)

KEY RULES:
  PRIMARY KEY → Unique + NOT NULL
  NOT NULL    → Field is required
  DEFAULT     → Use this if value not provided
  IS NULL     → Check for empty (not = NULL)

SAFETY RULES:
  ALWAYS use WHERE in UPDATE and DELETE
  Run SELECT first to verify target before UPDATE/DELETE
  Use LIMIT in SELECT queries on large tables
  Never use f-strings in SQL — use parameterized queries (%s)
```

---

## 🎥 Recommended Resources

> **▶ freeCodeCamp SQL Full Course (English)** — the single best free SQL course, covers everything from basics to advanced joins
>
> **▶ sqlzoo.net Level 1 to 3** — interactive SQL practice directly in the browser, no installation needed

---

*Day 29 Complete.* ✅