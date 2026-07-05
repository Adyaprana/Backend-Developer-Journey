# DAY 32 — DATABASE DESIGN: SCHEMAS, KEYS, RELATIONS & INDEXES

> **Goal:** Understand how professional databases are designed — primary keys, foreign keys, constraints, relationships, indexes, and how to build a complete e-commerce schema from scratch.
>
> **Week:** W5 — SQL + PostgreSQL (Days 29–42)
>
> **Status:** ✅

---

# 🎯 Learning Roadmap

```
Database Design — Schemas, Keys, Relations

  ✅ Primary key, foreign key, unique constraint, NOT NULL
  ✅ One-to-many, many-to-many relationships
  ✅ Indexes: what they are, when to add them, why they speed up queries
  ✅ Design: e-commerce DB schema (users, products, orders, order_items)
  ✅ Draw this on paper — interviewers ask you to design schemas

  ▶ Lucidchart DB Design Tutorial (English — 30 min)
```

## Day 32 Checklist

- [ ] Define Primary Key, Foreign Key, UNIQUE, NOT NULL from memory
- [ ] Explain the difference between PK and UNIQUE constraint
- [ ] Draw the e-commerce schema on paper (4 tables + relationships)
- [ ] Explain One-to-Many vs Many-to-Many with real examples
- [ ] Explain what an index is and when NOT to create one
- [ ] Write the complete e-commerce schema SQL from scratch
- [ ] Explain referential integrity and what happens without foreign keys
- [ ] Solve LeetCode 511 — Game Play Analysis I ✅

---

# SECTION 1 — WHY DATABASE DESIGN MATTERS

## The Consequence of Bad Design

Imagine you are building Amazon.

You need to store millions of users, millions of products, millions of orders, reviews, payments, and addresses.

**Poor design:**

```
One giant table:
┌────┬──────────┬──────────┬───────────┬────────┬───────┬───────────┐
│ id │ username │ email    │ prod_name │ price  │ qty   │ order_dt  │
├────┼──────────┼──────────┼───────────┼────────┼───────┼───────────┤
│  1 │ Adya     │ a@x.com  │ Laptop    │ 80000  │  1    │ 2026-01   │
│  2 │ Adya     │ a@x.com  │ Mouse     │  1200  │  2    │ 2026-01   │
│  3 │ Rahul    │ r@x.com  │ Keyboard  │  2500  │  1    │ 2026-02   │
└────┴──────────┴──────────┴───────────┴────────┴───────┴───────────┘
Problems:
  → Adya's email is stored twice. If it changes, two rows must be updated.
  → Product price is in the order row. If price changes, old orders show wrong price.
  → No way to add a user without an order.
  → 1 million orders = 1 million copies of each user's name and email.
```

**Good design (normalized):**

```
users table:        products table:      orders table:
id | name | email   id | name | price    id | user_id | date
1  | Adya | a@x.com 1  | Laptop| 80000   1  |    1    | 2026-01
                    2  | Mouse |  1200   2  |    1    | 2026-01
                                         3  |    2    | 2026-02

order_items table:
id | order_id | product_id | qty | price
1  |    1     |     1      |  1  | 80000
2  |    1     |     2      |  2  |  1200
3  |    3     |     2      |  1  |  2500

Benefits:
  → Each user's email stored once. One update fixes everything.
  → Price at time of order preserved in order_items.
  → Tables are small, focused, and fast.
  → Queries are predictable.
```

---

# SECTION 2 — DATABASE SCHEMA

## Definition

A **database schema** is the blueprint of your database. It defines:

```
→ Which tables exist
→ What columns each table has
→ What data type each column stores
→ What constraints apply (NOT NULL, UNIQUE, etc.)
→ How tables relate to each other (foreign keys)
→ What indexes exist for performance
```

**Analogy:** A schema is like the architectural blueprint of a building. The blueprint doesn't contain furniture (data) — it just defines the rooms (tables), what each room can contain (columns), and how rooms connect (relationships).

```
Schema (Blueprint)
├── Table: users
│   ├── id         SERIAL        PRIMARY KEY
│   ├── name       VARCHAR(100)  NOT NULL
│   ├── email      VARCHAR(255)  UNIQUE NOT NULL
│   └── created_at TIMESTAMP     DEFAULT NOW()
│
├── Table: products
│   ├── id         SERIAL        PRIMARY KEY
│   ├── name       VARCHAR(150)  NOT NULL
│   ├── price      DECIMAL(10,2) NOT NULL
│   └── stock      INTEGER       DEFAULT 0
│
├── Table: orders
│   ├── id         SERIAL        PRIMARY KEY
│   ├── user_id    INTEGER       REFERENCES users(id)  ← FOREIGN KEY
│   ├── order_date TIMESTAMP     DEFAULT NOW()
│   └── status     VARCHAR(20)   DEFAULT 'pending'
│
└── Table: order_items
    ├── id         SERIAL        PRIMARY KEY
    ├── order_id   INTEGER       REFERENCES orders(id)  ← FOREIGN KEY
    ├── product_id INTEGER       REFERENCES products(id) ← FOREIGN KEY
    ├── quantity   INTEGER       NOT NULL
    └── price      DECIMAL(10,2) NOT NULL
```

---

# SECTION 3 — PRIMARY KEY

## Definition

A **Primary Key (PK)** uniquely identifies every single row in a table.

## Rules

```
Rule 1: Every value must be UNIQUE — no two rows can have the same PK
Rule 2: Cannot be NULL — every row must have a PK value
Rule 3: Only ONE primary key per table
Rule 4: PK values should never change (immutable)
```

## Why Not Use Name as a Primary Key?

```
users table:
id | name
1  | Adyaprana
2  | Rahul
3  | Adyaprana   ← DUPLICATE! Two users named Adyaprana

If you use name as PK: two Adyapranas cannot exist.
But two people can have the same name.
→ Always use id as PK.
```

## SERIAL vs INTEGER PRIMARY KEY

```sql
-- SERIAL: auto-generates unique values 1, 2, 3, 4...
-- You never need to provide the id manually
id SERIAL PRIMARY KEY

-- INTEGER: you must provide the id manually
id INTEGER PRIMARY KEY
```

**Always use `SERIAL PRIMARY KEY` for new tables.** It prevents you from accidentally inserting duplicate IDs.

## SQL Examples

```sql
-- Simple primary key
CREATE TABLE users (
    id   SERIAL       PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

-- Composite primary key (two columns together form the unique identifier)
CREATE TABLE activity (
    player_id  INT,
    event_date DATE,
    PRIMARY KEY (player_id, event_date)
    -- Same player can login on different dates ✅
    -- Same player cannot login twice on the same date ❌
);

-- Verify primary key constraint
INSERT INTO users (name) VALUES ('Adyaprana');   -- id = 1 auto-assigned
INSERT INTO users (name) VALUES ('Rahul');        -- id = 2 auto-assigned
INSERT INTO users (id, name) VALUES (1, 'Amit');  -- ERROR: duplicate key value
```

---

# SECTION 4 — FOREIGN KEY

## Definition

A **Foreign Key (FK)** is a column in one table that references the Primary Key of another table. It creates and enforces the relationship between tables.

## Visual Explanation

```
users table:               orders table:
┌────┬──────────────┐      ┌──────────┬─────────┬────────┐
│ id │ name         │      │ order_id │ user_id │ amount │
├────┼──────────────┤      ├──────────┼─────────┼────────┤
│  1 │ Adyaprana    │◄─────│    101   │    1    │  500   │
│  2 │ Rahul        │◄─────│    102   │    1    │  700   │
│  3 │ Priya        │◄─────│    103   │    2    │  900   │
└────┴──────────────┘      └──────────┴─────────┴────────┘
                                            ↑
                                         FOREIGN KEY
                                     references users.id
```

## What Foreign Keys Enforce (Referential Integrity)

```
Without foreign key:
  INSERT INTO orders (user_id, amount) VALUES (999, 500);
  → Succeeds even though user 999 doesn't exist!
  → Orphan record — order belongs to nobody.

With foreign key:
  INSERT INTO orders (user_id, amount) VALUES (999, 500);
  → ERROR: insert or update on table "orders" violates
    foreign key constraint "orders_user_id_fkey"
  → DETAIL: Key (user_id)=(999) is not present in table "users".
  → Data integrity is preserved.
```

## SQL Examples

```sql
-- Basic foreign key
CREATE TABLE orders (
    order_id SERIAL  PRIMARY KEY,
    user_id  INTEGER REFERENCES users(id),   -- Shorthand syntax
    amount   NUMERIC(10, 2)
);

-- Explicit foreign key syntax (more readable, preferred in production)
CREATE TABLE orders (
    order_id SERIAL       PRIMARY KEY,
    user_id  INTEGER      NOT NULL,
    amount   NUMERIC(10, 2),
    CONSTRAINT fk_orders_user FOREIGN KEY (user_id) REFERENCES users(id)
);

-- ON DELETE behavior
CREATE TABLE orders (
    order_id SERIAL  PRIMARY KEY,
    user_id  INTEGER REFERENCES users(id) ON DELETE CASCADE,
    -- If a user is deleted, all their orders are also deleted automatically
    amount   NUMERIC(10, 2)
);

CREATE TABLE orders (
    order_id SERIAL  PRIMARY KEY,
    user_id  INTEGER REFERENCES users(id) ON DELETE SET NULL,
    -- If user deleted, user_id becomes NULL (order remains, user gone)
    amount   NUMERIC(10, 2)
);

CREATE TABLE orders (
    order_id SERIAL  PRIMARY KEY,
    user_id  INTEGER REFERENCES users(id) ON DELETE RESTRICT,
    -- Default behavior: prevents deleting a user who has orders
    amount   NUMERIC(10, 2)
);
```

## Drop Order with Foreign Keys

```sql
-- ❌ WRONG — cannot drop users if orders references it
DROP TABLE users;  -- ERROR: cannot drop because other objects depend on it

-- ✅ CORRECT — drop child tables first, then parent
DROP TABLE IF EXISTS order_items;   -- references orders and products
DROP TABLE IF EXISTS orders;        -- references users
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS users;         -- parent table, dropped last
```

---

# SECTION 5 — CONSTRAINTS

## UNIQUE

Prevents duplicate values in a column. Unlike PRIMARY KEY, a table can have multiple UNIQUE constraints.

```sql
-- Single column unique
email VARCHAR(255) UNIQUE

-- Explicitly named constraint (better for error messages)
CONSTRAINT uq_users_email UNIQUE (email)

-- Composite unique (combination must be unique)
CONSTRAINT uq_student_course UNIQUE (student_id, course_id)
-- Same student cannot enroll in the same course twice
-- But same student CAN enroll in different courses ✅
```

**PRIMARY KEY vs UNIQUE:**

```
PRIMARY KEY:
  → Only ONE per table
  → Cannot be NULL
  → Automatically creates an index

UNIQUE:
  → Multiple allowed per table
  → CAN be NULL in most databases (NULL ≠ NULL, so two NULLs are allowed)
  → Also creates an index
```

---

## NOT NULL

Forces every row to have a value for that column. NULL means "no value" — it is not zero, not empty string, it is the absence of any value.

```sql
-- Without NOT NULL: name can be NULL (missing)
name VARCHAR(100)

-- With NOT NULL: name is required
name VARCHAR(100) NOT NULL

-- Good candidates for NOT NULL:
CREATE TABLE users (
    id         SERIAL        PRIMARY KEY,
    name       VARCHAR(100)  NOT NULL,         -- User must have a name
    email      VARCHAR(255)  UNIQUE NOT NULL,  -- Email is required and unique
    password   VARCHAR(255)  NOT NULL,         -- Password is required
    bio        TEXT,                           -- Bio is optional (can be NULL)
    created_at TIMESTAMP     DEFAULT NOW()     -- Has default, still NOT NULL
);
```

---

## DEFAULT

Provides an automatic value when none is specified.

```sql
is_active  BOOLEAN   DEFAULT TRUE,
created_at TIMESTAMP DEFAULT NOW(),
status     VARCHAR   DEFAULT 'pending',
stock      INTEGER   DEFAULT 0,
rating     NUMERIC   DEFAULT 0.0
```

---

## CHECK

Validates that values meet a specific condition.

```sql
-- Age must be positive
age   INTEGER CHECK (age > 0),

-- Rating must be between 1 and 5
rating INTEGER CHECK (rating BETWEEN 1 AND 5),

-- Status must be one of specific values
status VARCHAR(20) CHECK (status IN ('pending', 'shipped', 'delivered', 'cancelled'))
```

---

# SECTION 6 — RELATIONSHIPS

## One-to-One

One row in table A corresponds to exactly one row in table B.

```
users ──────────── profiles
  1   →    1

Real examples:
  User → Passport (one person, one passport)
  User → Profile (one account, one profile page)
  Employee → SalaryRecord

SQL:
  CREATE TABLE profiles (
      id      SERIAL  PRIMARY KEY,
      user_id INTEGER UNIQUE REFERENCES users(id),  -- UNIQUE enforces one-to-one
      bio     TEXT,
      website VARCHAR(255)
  );
```

---

## One-to-Many (Most Common)

One row in table A can correspond to MANY rows in table B.

```
users ──────────── orders
  1   →   many

Real examples:
  User → Orders (one user, many orders)
  Author → Books (one author, many books)
  Department → Employees (one department, many employees)
  Customer → Reviews (one customer, many reviews)

Visual:
  User: Adyaprana
  ├── Order #101 (Laptop)
  ├── Order #102 (Mouse)
  └── Order #103 (Keyboard)

SQL:
  CREATE TABLE orders (
      id      SERIAL  PRIMARY KEY,
      user_id INTEGER REFERENCES users(id),  -- Foreign key (no UNIQUE = one-to-many)
      amount  NUMERIC(10,2)
  );
```

---

## Many-to-Many

Many rows in table A can correspond to many rows in table B.

```
students ──────────── courses
  many  ←→   many

Real examples:
  Students ↔ Courses (a student takes many courses, a course has many students)
  Products ↔ Orders  (an order has many products, a product appears in many orders)
  Actors ↔ Movies    (an actor appears in many movies, a movie has many actors)
  Users ↔ Tags       (a user has many tags, a tag applies to many users)

Implementation: ALWAYS requires a JUNCTION TABLE (also called bridge table)

students table:     courses table:      enrollments (junction):
id | name           id | course_name    student_id | course_id
1  | Adya           1  | Python         1          | 1
2  | Rahul          2  | SQL            1          | 2
                    3  | FastAPI        2          | 1
                                        2          | 3

Adya takes Python and SQL.
Rahul takes Python and FastAPI.

SQL:
  CREATE TABLE enrollments (
      id         SERIAL  PRIMARY KEY,
      student_id INTEGER REFERENCES students(id),
      course_id  INTEGER REFERENCES courses(id),
      enrolled_at TIMESTAMP DEFAULT NOW(),
      UNIQUE (student_id, course_id)  -- Can't enroll in same course twice
  );
```

---

## Relationship Summary Table

```
Type            │ FK Location        │ UNIQUE on FK? │ Example
────────────────┼────────────────────┼───────────────┼──────────────────
One-to-One      │ Either table       │ YES           │ User → Profile
One-to-Many     │ "Many" side table  │ NO            │ User → Orders
Many-to-Many    │ Junction table     │ Composite     │ Students ↔ Courses
```

---

# SECTION 7 — INDEXES

## What is an Index?

An **index** is a separate data structure that PostgreSQL maintains to speed up data retrieval.

**The book analogy:**

```
Without index:
  You want to find "PostgreSQL" in a 1000-page book.
  You read every single page until you find it.
  → Slow. O(n) search.

With index (the book's index at the back):
  You go to the index, find "PostgreSQL → page 542"
  You open page 542 directly.
  → Fast. O(log n) search.

Database works exactly the same way.
```

## How PostgreSQL Stores Indexes

PostgreSQL uses a **B-tree (Balanced Tree)** structure for most indexes.

```
B-tree index on users.email:

                    [m@x.com]
                   /         \
          [d@x.com]           [r@x.com]
         /         \         /         \
    [a@x] [b@x]  [e@x] [f@x] [p@x] [q@x] [z@x]

Finding 'p@x.com':
  Step 1: Compare with root 'm@x.com' → p > m → go right
  Step 2: Compare with 'r@x.com'      → p < r → go left
  Step 3: Found 'p@x.com' in 3 steps

Without index: scan all 7 emails = 7 steps
With index:    3 steps (log₂ of 7)

For 1 million records:
  Without index: up to 1,000,000 comparisons
  With index:    about 20 comparisons (log₂ of 1,000,000)
```

## When Indexes Are Created Automatically

```
PostgreSQL creates an index automatically for:
  → PRIMARY KEY columns
  → UNIQUE constraint columns

You create indexes manually for:
  → Foreign key columns (PostgreSQL does NOT auto-create these)
  → Columns used frequently in WHERE clauses
  → Columns used in ORDER BY for large tables
  → Columns used in JOIN conditions
```

## When to Create an Index

```sql
-- ✅ GOOD index candidates:
CREATE INDEX idx_orders_user_id ON orders(user_id);         -- FK column
CREATE INDEX idx_users_email    ON users(email);            -- Frequent WHERE filter
CREATE INDEX idx_orders_date    ON orders(order_date);      -- Frequent date filter
CREATE INDEX idx_products_name  ON products(name);          -- Search by name

-- Examples of queries that BENEFIT from these indexes:
SELECT * FROM orders WHERE user_id = 42;         -- uses idx_orders_user_id
SELECT * FROM users  WHERE email = 'a@x.com';    -- uses idx_users_email
SELECT * FROM orders WHERE order_date > '2026-01-01';  -- uses idx_orders_date
```

## When NOT to Create an Index

```
❌ Columns that are rarely searched
❌ Very small tables (< 1000 rows) — full scan is faster than index lookup
❌ Columns with very few unique values (e.g., is_active BOOLEAN — only TRUE/FALSE)
❌ Every single column — indexes have costs!

Index costs:
  → Slows INSERT, UPDATE, DELETE operations
    (Index must be updated every time data changes)
  → Uses extra disk space
  → Requires maintenance (VACUUM, ANALYZE)
```

## Index SQL Commands

```sql
-- Create index
CREATE INDEX idx_orders_user_id
ON orders(user_id);

-- Create unique index (same as UNIQUE constraint)
CREATE UNIQUE INDEX idx_users_email
ON users(email);

-- Composite index (searches that filter on BOTH columns benefit)
CREATE INDEX idx_orders_user_date
ON orders(user_id, order_date);

-- Partial index (only index active users — saves space)
CREATE INDEX idx_active_users
ON users(email)
WHERE is_active = TRUE;

-- View all indexes on a table
SELECT indexname, indexdef
FROM pg_indexes
WHERE tablename = 'orders';

-- Drop an index
DROP INDEX idx_orders_user_id;

-- Check if a query uses an index (EXPLAIN)
EXPLAIN SELECT * FROM orders WHERE user_id = 1;
-- If you see "Index Scan" → index is being used
-- If you see "Seq Scan"   → full table scan (no index used)
```

---

# SECTION 8 — E-COMMERCE SCHEMA (COMPLETE PROJECT)

## Schema Diagram

```
┌───────────────────────────┐
│         USERS             │
│ PK  id          SERIAL    │
│     name        VARCHAR   │
│     email       VARCHAR   │◄─────────────────────────────┐
│     password    VARCHAR   │                               │
│     phone       VARCHAR   │                               │
│     created_at  TIMESTAMP │                               │
└───────────────┬───────────┘                               │
                │ 1                                         │
                │ (one user has many orders)                │
                │ many                                      │
┌───────────────▼───────────┐     ┌────────────────────────┴──┐
│         ORDERS            │     │        PRODUCTS            │
│ PK  id          SERIAL    │     │ PK  id          SERIAL     │
│ FK  user_id     INTEGER   │     │     name        VARCHAR    │
│     order_date  TIMESTAMP │     │     description TEXT       │
│     status      VARCHAR   │     │     price       DECIMAL    │
│     total_price DECIMAL   │     │     stock       INTEGER    │
└───────────────┬───────────┘     │     category    VARCHAR    │
                │ 1               └────────────────┬──────────┘
                │ (one order has many items)        │
                │ many                              │ many
┌───────────────▼───────────────────────────────────┘
│        ORDER_ITEMS                                 │
│ PK  id          SERIAL                             │
│ FK  order_id    INTEGER  REFERENCES orders(id)     │
│ FK  product_id  INTEGER  REFERENCES products(id)   │
│     quantity    INTEGER                            │
│     price       DECIMAL  (price at time of order)  │
└────────────────────────────────────────────────────┘
```

## Complete SQL Script

```sql
-- ═══════════════════════════════════════════════════════════════
-- DAY 32 — E-COMMERCE DATABASE SCHEMA
-- Complete production-ready schema
-- Copy and run in pgAdmin.
-- ═══════════════════════════════════════════════════════════════


-- ─────────────────────────────────────────────────────────────────
-- STEP 1: CLEANUP (correct order — child tables first)
-- ─────────────────────────────────────────────────────────────────

DROP TABLE IF EXISTS order_items  CASCADE;
DROP TABLE IF EXISTS orders       CASCADE;
DROP TABLE IF EXISTS products     CASCADE;
DROP TABLE IF EXISTS users        CASCADE;


-- ─────────────────────────────────────────────────────────────────
-- STEP 2: USERS TABLE
-- ─────────────────────────────────────────────────────────────────

CREATE TABLE users (
    id          SERIAL        PRIMARY KEY,
    name        VARCHAR(100)  NOT NULL,
    email       VARCHAR(255)  UNIQUE NOT NULL,
    password    VARCHAR(255)  NOT NULL,         -- store hashed password only!
    phone       VARCHAR(15),                    -- optional
    is_active   BOOLEAN       DEFAULT TRUE,
    created_at  TIMESTAMP     DEFAULT NOW(),
    updated_at  TIMESTAMP     DEFAULT NOW()
);

-- Index on email (most common search field for login)
CREATE INDEX idx_users_email ON users(email);


-- ─────────────────────────────────────────────────────────────────
-- STEP 3: PRODUCTS TABLE
-- ─────────────────────────────────────────────────────────────────

CREATE TABLE products (
    id          SERIAL         PRIMARY KEY,
    name        VARCHAR(150)   NOT NULL,
    description TEXT,
    price       DECIMAL(10, 2) NOT NULL CHECK (price >= 0),
    stock       INTEGER        NOT NULL DEFAULT 0 CHECK (stock >= 0),
    category    VARCHAR(50),
    is_active   BOOLEAN        DEFAULT TRUE,
    created_at  TIMESTAMP      DEFAULT NOW()
);

-- Index on category (frequent filter)
CREATE INDEX idx_products_category ON products(category);


-- ─────────────────────────────────────────────────────────────────
-- STEP 4: ORDERS TABLE
-- ─────────────────────────────────────────────────────────────────

CREATE TABLE orders (
    id          SERIAL         PRIMARY KEY,
    user_id     INTEGER        NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    order_date  TIMESTAMP      DEFAULT NOW(),
    status      VARCHAR(20)    DEFAULT 'pending'
                               CHECK (status IN ('pending','confirmed','shipped','delivered','cancelled')),
    total_price DECIMAL(10, 2) DEFAULT 0
);

-- Index on user_id (frequent JOIN and WHERE filter)
CREATE INDEX idx_orders_user_id   ON orders(user_id);
-- Index on order_date (frequent date range queries)
CREATE INDEX idx_orders_date      ON orders(order_date);
-- Index on status (frequent filter)
CREATE INDEX idx_orders_status    ON orders(status);


-- ─────────────────────────────────────────────────────────────────
-- STEP 5: ORDER_ITEMS TABLE (Junction table — Orders ↔ Products)
-- ─────────────────────────────────────────────────────────────────

CREATE TABLE order_items (
    id          SERIAL         PRIMARY KEY,
    order_id    INTEGER        NOT NULL REFERENCES orders(id)   ON DELETE CASCADE,
    product_id  INTEGER        NOT NULL REFERENCES products(id) ON DELETE RESTRICT,
    quantity    INTEGER        NOT NULL CHECK (quantity > 0),
    price       DECIMAL(10, 2) NOT NULL  -- price at time of purchase (not current price)
);

-- Indexes on foreign keys
CREATE INDEX idx_order_items_order_id   ON order_items(order_id);
CREATE INDEX idx_order_items_product_id ON order_items(product_id);


-- ─────────────────────────────────────────────────────────────────
-- STEP 6: INSERT SAMPLE DATA
-- ─────────────────────────────────────────────────────────────────

-- Insert users
INSERT INTO users (name, email, password, phone) VALUES
('Adyaprana', 'adya@example.com',  'hashed_pw_1', '9876543210'),
('Rahul',     'rahul@example.com', 'hashed_pw_2', '9876543211'),
('Priya',     'priya@example.com', 'hashed_pw_3', NULL),
('Amit',      'amit@example.com',  'hashed_pw_4', '9876543213');

-- Insert products
INSERT INTO products (name, description, price, stock, category) VALUES
('iPhone 16',           'Apple flagship smartphone',        89999.00, 15, 'Mobile'),
('MacBook Air M4',      'Lightweight laptop',              124999.00,  8, 'Laptop'),
('Sony WH-1000XM5',    'Noise cancelling headphones',      29999.00, 12, 'Audio'),
('Logitech MX Master', 'Wireless productivity mouse',       9999.00, 18, 'Accessories'),
('Dell XPS 15',        'Premium Windows laptop',          145000.00,  5, 'Laptop'),
('Samsung Galaxy S25', 'Android flagship',                 79999.00, 20, 'Mobile');

-- Insert orders
INSERT INTO orders (user_id, status) VALUES
(1, 'delivered'),   -- Adyaprana's order 1
(1, 'pending'),     -- Adyaprana's order 2
(2, 'shipped'),     -- Rahul's order
(3, 'confirmed');   -- Priya's order

-- Insert order items
INSERT INTO order_items (order_id, product_id, quantity, price) VALUES
(1, 1, 1, 89999.00),   -- Order 1: iPhone 16
(1, 4, 2, 9999.00),    -- Order 1: 2× Logitech Mouse
(2, 2, 1, 124999.00),  -- Order 2: MacBook Air
(3, 3, 1, 29999.00),   -- Order 3: Sony Headphones
(3, 4, 1, 9999.00),    -- Order 3: Logitech Mouse
(4, 6, 1, 79999.00),   -- Order 4: Samsung Galaxy

-- Update total_price in orders
UPDATE orders SET total_price = 109997.00 WHERE id = 1;  -- 89999 + 2×9999
UPDATE orders SET total_price = 124999.00 WHERE id = 2;
UPDATE orders SET total_price =  39998.00 WHERE id = 3;  -- 29999 + 9999
UPDATE orders SET total_price =  79999.00 WHERE id = 4;


-- ─────────────────────────────────────────────────────────────────
-- STEP 7: VERIFY DATA
-- ─────────────────────────────────────────────────────────────────

SELECT * FROM users;
SELECT * FROM products;
SELECT * FROM orders;
SELECT * FROM order_items;


-- ─────────────────────────────────────────────────────────────────
-- STEP 8: REAL QUERIES (What your FastAPI backend will run)
-- ─────────────────────────────────────────────────────────────────

-- GET /users/1/orders — Show all orders for a user
SELECT
    o.id          AS order_id,
    o.order_date,
    o.status,
    o.total_price
FROM orders o
WHERE o.user_id = 1
ORDER BY o.order_date DESC;


-- GET /orders/1 — Full order detail with all items and product names
SELECT
    o.id                  AS order_id,
    u.name                AS customer,
    o.status,
    o.order_date,
    p.name                AS product,
    oi.quantity,
    oi.price              AS unit_price,
    oi.quantity * oi.price AS line_total
FROM orders o
INNER JOIN users       u  ON u.id  = o.user_id
INNER JOIN order_items oi ON oi.order_id   = o.id
INNER JOIN products    p  ON p.id  = oi.product_id
WHERE o.id = 1
ORDER BY p.name;


-- Analytics: Top 3 customers by total spending
SELECT
    u.name,
    COUNT(DISTINCT o.id)        AS total_orders,
    SUM(oi.quantity * oi.price) AS total_spent
FROM users u
INNER JOIN orders      o  ON o.user_id    = u.id
INNER JOIN order_items oi ON oi.order_id  = o.id
GROUP BY u.id, u.name
ORDER BY total_spent DESC
LIMIT 3;


-- Analytics: Best-selling products
SELECT
    p.name,
    p.category,
    SUM(oi.quantity)            AS total_units_sold,
    SUM(oi.quantity * oi.price) AS total_revenue
FROM products p
INNER JOIN order_items oi ON oi.product_id = p.id
GROUP BY p.id, p.name, p.category
ORDER BY total_revenue DESC;


-- Analytics: Low stock alert (products with stock < 10)
SELECT id, name, category, stock
FROM products
WHERE stock < 10
ORDER BY stock ASC;


-- Analytics: Orders by status
SELECT status, COUNT(*) AS count
FROM orders
GROUP BY status
ORDER BY count DESC;
```

---

# SECTION 9 — LeetCode 511 — Game Play Analysis I

```sql
-- ═══════════════════════════════════════════════════════════════
-- LeetCode #511 — Game Play Analysis I
-- Difficulty: Easy | Status: ✅ Accepted (12/12 test cases)
-- Runtime: 2457ms | Memory: 0.00 MB | Beats memory: 100%
-- Topic: GROUP BY + MIN()
-- ═══════════════════════════════════════════════════════════════

DROP TABLE IF EXISTS Activity;

CREATE TABLE Activity (
    player_id    INT,
    device_id    INT,
    event_date   DATE,
    games_played INT,
    PRIMARY KEY (player_id, event_date)
);

INSERT INTO Activity VALUES
(1, 2, '2016-03-01', 5),
(1, 2, '2016-05-02', 6),
(2, 3, '2017-06-25', 1),
(3, 1, '2016-03-02', 0),
(3, 4, '2018-07-03', 5);

SELECT * FROM Activity;

-- SOLUTION: Find the first login date for each player
SELECT
    player_id,
    MIN(event_date) AS first_login
FROM Activity
GROUP BY player_id;

-- Why GROUP BY?
-- Multiple rows per player. Need one result per player.

-- Why MIN()?
-- Find the earliest (smallest) date in each player's group.

-- Expected output:
-- player_id | first_login
--         1 | 2016-03-01
--         2 | 2017-06-25
--         3 | 2016-03-02

-- This exact pattern (GROUP BY + MIN/MAX) is used in e-commerce:
-- First purchase date per customer
-- Latest login per user
-- Earliest order per product
```

---

# SECTION 10 — DEEP THEORY

## Normalization — Why We Split Tables

**Normalization** is the process of organizing a database to reduce redundancy and improve data integrity.

**First Normal Form (1NF):**

```
Rule: Each column must contain atomic (single) values.

❌ Violates 1NF:
  user_id | products_ordered
  1       | Laptop, Mouse, Keyboard     ← multiple values in one cell

✅ Satisfies 1NF:
  user_id | product
  1       | Laptop
  1       | Mouse
  1       | Keyboard
```

**Second Normal Form (2NF):**

```
Rule: No partial dependency on a composite primary key.
Every non-key column must depend on the ENTIRE primary key.

❌ Violates 2NF (composite PK: order_id + product_id):
  order_id | product_id | product_name | quantity
  1        | 101        | Laptop       | 1
  ↑ product_name depends only on product_id, not on the full composite key

✅ Solution: Move product_name to products table
```

**Third Normal Form (3NF):**

```
Rule: No transitive dependency.
Non-key columns should not depend on other non-key columns.

❌ Violates 3NF:
  order_id | customer_id | customer_city
  ↑ customer_city depends on customer_id, not directly on order_id

✅ Solution: Move customer_city to users table
```

---

## What is Referential Integrity?

Referential integrity means the database guarantees that every foreign key value points to an existing row in the referenced table.

```
Without referential integrity:
  orders.user_id = 500  but  users table has no row with id=500
  → Orphan record: an order that belongs to nobody
  → Queries joining users+orders will produce wrong results
  → Difficult to diagnose

With referential integrity (foreign key constraint):
  INSERT INTO orders (user_id) VALUES (500);
  → ERROR: Foreign key violation: user 500 doesn't exist
  → Problem caught immediately at insert time
  → Data is always consistent
```

---

# SECTION 11 — IMPORTANT THINGS TO KNOW

```
 1. PRIMARY KEY = UNIQUE + NOT NULL + only one per table.

 2. SERIAL is the easiest way to create auto-incrementing IDs.
    BIGSERIAL for very large tables (> 2 billion rows).

 3. Foreign keys enforce referential integrity.
    Without FK: orphan records can exist silently.

 4. Drop child tables before parent tables (foreign key order).
    Use CASCADE to drop dependencies automatically.

 5. UNIQUE allows multiple NULL values (NULL ≠ NULL in SQL).
    PRIMARY KEY allows zero NULLs.

 6. Indexes are created automatically for PRIMARY KEY and UNIQUE.
    You must manually create indexes for foreign key columns.

 7. FK columns without indexes cause slow JOIN queries.
    Always index your foreign key columns.

 8. B-tree index: default type in PostgreSQL. Good for equality and range queries.

 9. EXPLAIN shows whether a query uses an index.
    "Index Scan" = fast. "Seq Scan" = slow (full table scan).

10. CHECK constraint validates data at INSERT/UPDATE time.
    Use for: price >= 0, status IN (...), age BETWEEN 0 AND 150.

11. ON DELETE CASCADE: deleting parent also deletes children.
    ON DELETE RESTRICT: prevents deleting parent if children exist (default).
    ON DELETE SET NULL: sets FK to NULL when parent is deleted.

12. Many-to-many requires a junction table.
    NEVER use arrays of IDs in one column for relationships.

13. Composite primary key = two+ columns together form the PK.
    (player_id, event_date) means same player can appear multiple days.

14. DECIMAL(10,2) for money: 10 total digits, 2 after decimal.
    Never use FLOAT for monetary values (floating point rounding errors).

15. DEFAULT NOW() automatically sets timestamp to current time.

16. Naming conventions: use lowercase snake_case for all names.
    Good: user_id, order_date, product_name
    Bad:  UserID, OrderDate, ProductName

17. Schema design affects performance more than any query optimization.
    A well-designed schema with proper indexes is always faster.

18. Indexes slow down writes (INSERT, UPDATE, DELETE).
    Only create indexes that are actually used by queries.

19. Password must NEVER be stored as plain text.
    Store only bcrypt/argon2 hash. Never the original.

20. Interviewers frequently ask: "Design a schema for [Twitter/Uber/Instagram]"
    Practice drawing the tables, PKs, FKs, and relationships on paper.
```

---

# SECTION 12 — INTERVIEW QUESTIONS

## Q1. What is a Primary Key?

A Primary Key uniquely identifies every row in a table. It must be unique (no duplicates), cannot be NULL, and there can only be one per table. In PostgreSQL, `SERIAL PRIMARY KEY` auto-generates incrementing integer IDs.

---

## Q2. What is the difference between PRIMARY KEY and UNIQUE?

```
PRIMARY KEY:
  → Only ONE allowed per table
  → Cannot be NULL
  → Creates a clustered index (main index)
  → Used to identify rows

UNIQUE:
  → Multiple allowed per table
  → Can be NULL (in most databases)
  → Creates a non-clustered index
  → Used to prevent duplicate values in specific columns

Example:
  CREATE TABLE users (
      id    SERIAL  PRIMARY KEY,  -- One PK
      email VARCHAR UNIQUE,        -- Multiple UNIQUE constraints allowed
      phone VARCHAR UNIQUE         -- Another UNIQUE constraint
  );
```

---

## Q3. What is a Foreign Key and what does it prevent?

A Foreign Key is a column in one table that references the Primary Key of another table. It enforces **referential integrity** — it prevents inserting a child record that references a non-existent parent.

Without FK: `INSERT INTO orders (user_id) VALUES (9999)` would succeed even if user 9999 doesn't exist, creating an orphan record.

With FK: PostgreSQL raises an error, preserving data integrity.

---

## Q4. Explain One-to-Many and Many-to-Many relationships.

**One-to-Many:** One row in table A corresponds to many rows in table B. Implemented with a foreign key in the "many" table. Example: One user can have many orders.

**Many-to-Many:** Many rows in table A correspond to many rows in table B. Cannot be directly implemented — requires a **junction/bridge table** that has two foreign keys. Example: Students and courses (one student takes many courses, one course has many students). The `enrollments` table is the junction.

---

## Q5. What is an index? When should you NOT create one?

An index is a data structure (B-tree by default in PostgreSQL) that speeds up data retrieval by avoiding full table scans. PostgreSQL automatically creates indexes for PRIMARY KEY and UNIQUE constraints.

**Do NOT create indexes on:**
- Very small tables (< 1000 rows) — full scan is faster
- Columns with few unique values (like a boolean `is_active`)
- Columns that are rarely used in WHERE, JOIN, or ORDER BY
- Every column — excess indexes slow down INSERT, UPDATE, DELETE

---

## Q6. What is referential integrity?

Referential integrity guarantees that every foreign key value in a child table corresponds to an existing row in the parent table. It ensures no "orphan" records exist — orders without users, order_items without orders, etc.

Enforced by the FOREIGN KEY constraint in SQL. When violated, PostgreSQL raises an error rather than allowing inconsistent data.

---

## Q7. What is ON DELETE CASCADE?

`ON DELETE CASCADE` means: when a parent row is deleted, all child rows referencing it are automatically deleted too.

```sql
CREATE TABLE order_items (
    order_id INTEGER REFERENCES orders(id) ON DELETE CASCADE
);
-- If order #101 is deleted, all order_items for order #101 are also deleted.
```

Use when: child records have no meaning without the parent (order items without an order are meaningless).

Don't use when: you need to preserve historical data or audit trails.

---

## Q8. What does SERIAL do in PostgreSQL?

`SERIAL` is a shorthand for creating an auto-incrementing integer column.

```sql
id SERIAL PRIMARY KEY
-- Equivalent to:
-- CREATE SEQUENCE users_id_seq;
-- id INTEGER DEFAULT nextval('users_id_seq') NOT NULL
```

`SERIAL` automatically generates 1, 2, 3, 4... for each new row. You never need to specify the id value when inserting.

Use `BIGSERIAL` for tables expected to exceed 2 billion rows.

---

## Q9. Design a simple schema for a blog application.

```
Tables: users, posts, comments, tags, post_tags

users:
  id SERIAL PK, name, email (UNIQUE), password, created_at

posts:
  id SERIAL PK, user_id (FK → users.id), title, content,
  is_published BOOLEAN, published_at TIMESTAMP, created_at

comments:
  id SERIAL PK, post_id (FK → posts.id ON DELETE CASCADE),
  user_id (FK → users.id), content, created_at

tags:
  id SERIAL PK, name VARCHAR UNIQUE

post_tags: (junction for posts ↔ tags many-to-many)
  post_id (FK → posts.id), tag_id (FK → tags.id),
  PRIMARY KEY (post_id, tag_id)

Relationships:
  users → posts (one-to-many)
  posts → comments (one-to-many)
  posts ↔ tags (many-to-many via post_tags)
```

---

## Q10. Why must you store hashed passwords, never plain text?

If the database is compromised (SQL injection, breach), plain text passwords expose every user's password instantly — including passwords they reuse on other sites.

A proper password hash (bcrypt, argon2) is one-way: you can verify `bcrypt.check("password", hash)` but cannot reverse the hash to get the original password.

```python
# FastAPI example with bcrypt
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"])

# At registration: hash before storing
hashed = pwd_context.hash("user_password")

# At login: verify
pwd_context.verify("user_password", stored_hash)
```

---

# SECTION 13 — BACKEND CONNECTION

## How This Schema Powers FastAPI

```python
# Every FastAPI endpoint maps to SQL operations on this schema

# POST /register  → INSERT into users
# POST /login     → SELECT from users WHERE email = ?
# GET /products   → SELECT from products WHERE is_active = TRUE
# POST /orders    → INSERT into orders + INSERT into order_items
# GET /orders/1   → SELECT orders JOIN order_items JOIN products
# GET /analytics  → SELECT with GROUP BY + aggregates

# SQLAlchemy models (what you'll write in Week 7+):
from sqlalchemy import Column, Integer, String, ForeignKey, Decimal
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id       = Column(Integer, primary_key=True)
    name     = Column(String(100), nullable=False)
    email    = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)

class Order(Base):
    __tablename__ = "orders"
    id      = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status  = Column(String(20), default="pending")
```

---

# REVISION SHEET

```
═══════════════════════════════════════════════════════════
DATABASE DESIGN — ONE-PAGE REVISION
═══════════════════════════════════════════════════════════

SCHEMA = blueprint of the database
  Tables + Columns + Types + Constraints + Relationships

PRIMARY KEY:
  → Unique identifier for every row
  → NOT NULL + UNIQUE + one per table
  → Use SERIAL PRIMARY KEY for auto-increment

FOREIGN KEY:
  → References another table's PK
  → Enforces referential integrity (no orphan records)
  → Drop child table before parent table

CONSTRAINTS:
  UNIQUE     → No duplicate values (NULLs allowed)
  NOT NULL   → Value is required
  DEFAULT    → Use this if no value provided
  CHECK      → Validate data: CHECK (price >= 0)

RELATIONSHIPS:
  One-to-One:  FK column has UNIQUE constraint
  One-to-Many: FK in the "many" table (most common)
  Many-to-Many: Requires a junction/bridge table

INDEXES:
  Auto-created for: PRIMARY KEY, UNIQUE
  Manually create for: FK columns, frequent WHERE/JOIN cols
  Avoid for: boolean columns, tiny tables, every column
  Check usage: EXPLAIN SELECT ...

E-COMMERCE SCHEMA:
  users → orders (one-to-many)
  orders → order_items (one-to-many)
  products → order_items (one-to-many)
  orders ↔ products via order_items (many-to-many)

KEY RULES:
  ❌ Never store plain text passwords
  ❌ Never use FLOAT for money (use DECIMAL)
  ❌ Never use arrays instead of junction tables
  ✅ Always index foreign key columns
  ✅ Always use ON DELETE behavior on FK
  ✅ Store price in order_items (price at purchase time)
```

---

## LeetCode Solved This Day

| Problem | Difficulty | Topic | Status | Runtime |
|---------|-----------|-------|--------|---------|
| #511 Game Play Analysis I | Easy | GROUP BY + MIN() | ✅ Accepted 12/12 | 2457ms |

---

## 🎥 Recommended Resource

> **▶ Lucidchart DB Design Tutorial (English — 30 min)**
>
> Best visual introduction to database design. Shows how to draw ER diagrams (Entity-Relationship diagrams) which is exactly what interviewers ask you to do on a whiteboard.
>
> After watching, draw the e-commerce schema from this file on paper — this is the single best preparation for database design interview questions.

---

*Day 32 Complete.* ✅
