# DAY 33 — TRANSACTIONS, ACID PROPERTIES & THE N+1 PROBLEM

> **Goal:** Understand how databases guarantee data integrity — transactions, ACID properties, and why the N+1 query problem silently kills backend performance.
>
> **Week:** W5 — SQL + PostgreSQL (Days 29–42)
>
> **Status:** ✅

---

# 🎯 Learning Roadmap

```
Transactions + ACID Properties

  ✅ BEGIN, COMMIT, ROLLBACK
  ✅ ACID: Atomicity, Consistency, Isolation, Durability — define each
  ✅ Why transactions matter in banking/payments (interview context)
  ✅ N+1 problem — what it is, why it kills performance, how to fix it

  ▶ InterviewBit SQL interview questions section
```

## Day 33 Checklist

- [ ] Explain a transaction in one sentence from memory
- [ ] Write BEGIN → UPDATE → COMMIT for a bank transfer
- [ ] Write BEGIN → UPDATE → ROLLBACK and explain what changes
- [ ] Define all 4 ACID properties without notes
- [ ] Give a real-world example for each ACID property
- [ ] Explain the N+1 problem with a concrete example
- [ ] Show how JOIN fixes N+1
- [ ] Explain SAVEPOINT and when to use it
- [ ] Solve LeetCode 1045 — Customers Who Bought All Products ✅

---

# SECTION 1 — WHAT IS A TRANSACTION?

## Definition

A **transaction** is a group of one or more SQL statements that execute as a single logical unit of work.

The critical rule: **Either everything succeeds, or everything fails.**

There is no partial success.

---

## The Bank Transfer Problem

This is the most important example in all of database theory.

```
Task: Transfer ₹500 from Adya's account to Rahul's account.

Without transactions:
  Step 1: Deduct ₹500 from Adya      → SUCCESS
  Step 2: Server crashes mid-way
  Step 3: Add ₹500 to Rahul          → NEVER HAPPENS

Result:
  ₹500 disappeared from Adya.
  Rahul never received it.
  ₹500 is gone forever.
  This is catastrophic for a bank.

With transactions:
  BEGIN
  Step 1: Deduct ₹500 from Adya      → Tentative (not saved yet)
  Step 2: Server crashes mid-way
  Step 3: Database automatically ROLLBACK
  
Result:
  Adya's balance returns to original.
  Rahul's balance unchanged.
  No money lost.
  The transaction protected the data.
```

---

## Mental Model

```
A transaction is like filling out a government form.

Without transaction:
  You fill in your name → server saves it
  You fill in your address → server crashes
  Result: Form is half-filled and saved.
  Incomplete and inconsistent.

With transaction:
  You fill in everything → review → sign → submit (COMMIT)
  OR
  You fill in everything → realize mistake → tear up (ROLLBACK)
  
Result: The form is either complete or doesn't exist. No half-measures.
```

---

# SECTION 2 — BEGIN, COMMIT, ROLLBACK

## BEGIN — Starting a Transaction

```sql
BEGIN;
-- OR (same thing in PostgreSQL)
START TRANSACTION;
```

`BEGIN` starts a transaction block. Everything after this point is **temporary** — it can be saved or cancelled.

No changes are visible to other users until COMMIT is called.

---

## COMMIT — Making Changes Permanent

```sql
COMMIT;
```

`COMMIT` permanently saves all changes made since `BEGIN`.

After COMMIT:
- Changes are written to disk
- Other users can see the changes
- The transaction is complete
- Cannot be undone (except by a new UPDATE/DELETE)

---

## ROLLBACK — Cancelling All Changes

```sql
ROLLBACK;
```

`ROLLBACK` cancels all changes made since `BEGIN`.

After ROLLBACK:
- Database returns to exactly the state it was before BEGIN
- No data was changed
- Other users never saw the temporary changes

---

## Complete Bank Transfer Example

```sql
-- ─────────────────────────────────────────────────────────────────
-- SETUP: Create accounts table
-- ─────────────────────────────────────────────────────────────────

DROP TABLE IF EXISTS accounts;

CREATE TABLE accounts (
    id      SERIAL        PRIMARY KEY,
    name    VARCHAR(100)  NOT NULL,
    balance DECIMAL(10, 2) NOT NULL CHECK (balance >= 0)
);

INSERT INTO accounts (name, balance) VALUES
('Adyaprana', 1000.00),
('Rahul',      500.00);

SELECT * FROM accounts;
-- id | name      | balance
--  1 | Adyaprana | 1000.00
--  2 | Rahul     |  500.00


-- ─────────────────────────────────────────────────────────────────
-- SCENARIO 1: SUCCESSFUL TRANSFER
-- Transfer ₹300 from Adyaprana to Rahul
-- ─────────────────────────────────────────────────────────────────

BEGIN;

UPDATE accounts
SET balance = balance - 300
WHERE id = 1;   -- Deduct from Adyaprana

UPDATE accounts
SET balance = balance + 300
WHERE id = 2;   -- Add to Rahul

-- Verify before committing (changes are visible within this transaction)
SELECT * FROM accounts;
-- id | name      | balance
--  1 | Adyaprana |  700.00   ← changed (but not permanent yet)
--  2 | Rahul     |  800.00   ← changed (but not permanent yet)

COMMIT;   -- Make permanent

-- Final state
SELECT * FROM accounts;
-- id | name      | balance
--  1 | Adyaprana |  700.00   ← permanently saved
--  2 | Rahul     |  800.00   ← permanently saved


-- ─────────────────────────────────────────────────────────────────
-- SCENARIO 2: FAILED TRANSFER (Simulate error → ROLLBACK)
-- ─────────────────────────────────────────────────────────────────

-- Reset data
UPDATE accounts SET balance = 1000 WHERE id = 1;
UPDATE accounts SET balance = 500  WHERE id = 2;

BEGIN;

UPDATE accounts
SET balance = balance - 500
WHERE id = 1;   -- Deduct ₹500 from Adyaprana

-- Suppose: an error occurs here (validation fails, server issue, etc.)
-- We ROLLBACK instead of committing

ROLLBACK;

-- Check: Nothing changed
SELECT * FROM accounts;
-- id | name      | balance
--  1 | Adyaprana | 1000.00   ← back to original
--  2 | Rahul     |  500.00   ← unchanged


-- ─────────────────────────────────────────────────────────────────
-- SCENARIO 3: OVERDRAFT PROTECTION
-- ─────────────────────────────────────────────────────────────────

BEGIN;

UPDATE accounts
SET balance = balance - 2000   -- More than Adyaprana has!
WHERE id = 1;
-- ERROR: new row for relation "accounts" violates check constraint
-- "accounts_balance_check"
-- The CHECK (balance >= 0) constraint prevents this

ROLLBACK;
-- Balance returns to original — CHECK constraint acted as safety net
```

---

## SAVEPOINT — Partial Rollback

```sql
-- SAVEPOINT lets you rollback to a specific point within a transaction
-- without cancelling the entire transaction

BEGIN;

INSERT INTO orders (user_id, status) VALUES (1, 'pending');

SAVEPOINT step_order_created;   -- Mark this point

UPDATE products SET stock = stock - 1 WHERE id = 5;

-- Suppose stock update fails (maybe product doesn't exist)
-- We can rollback only the stock update, keep the order

ROLLBACK TO SAVEPOINT step_order_created;

-- Now decide: try again or abort entirely
-- Option 1: Fix and continue
UPDATE products SET stock = stock - 1 WHERE id = 6;   -- different product
COMMIT;

-- Option 2: Cancel everything
ROLLBACK;   -- Cancels everything including the INSERT

-- SAVEPOINTs are useful for:
-- Complex multi-step operations
-- Retrying specific parts of a transaction
-- Financial systems where partial success is meaningful
```

---

## E-Commerce Order Transaction

```sql
-- Real production example: customer places an order

BEGIN;

-- Step 1: Create the order
INSERT INTO orders (user_id, status)
VALUES (1, 'pending')
RETURNING id;   -- Get the new order_id

-- Step 2: Add order items
INSERT INTO order_items (order_id, product_id, quantity, price)
VALUES (1, 5, 2, 29999.00);   -- 2× headphones

-- Step 3: Reduce stock
UPDATE products
SET stock = stock - 2
WHERE id = 5 AND stock >= 2;   -- Only if sufficient stock

-- Step 4: Verify stock was actually reduced (check rows affected)
-- If 0 rows were updated, stock was insufficient → ROLLBACK

COMMIT;   -- Everything succeeded

-- If anything fails:
-- ROLLBACK;   → Order not created, items not added, stock unchanged
```

---

# SECTION 3 — ACID PROPERTIES

## What is ACID?

ACID is a set of four properties that guarantee database transactions are processed reliably, even in the presence of errors, crashes, or concurrent access.

Every serious database (PostgreSQL, MySQL, Oracle, SQL Server) implements ACID.

```
A — Atomicity
C — Consistency
I — Isolation
D — Durability
```

---

## A — Atomicity: All or Nothing

**Definition:** A transaction is treated as a single unit. Either ALL operations within it succeed, or NONE of them are saved.

```
The ATM Example:
  You withdraw ₹2000 from an ATM.
  
  Operations:
  1. Deduct ₹2000 from your bank account
  2. Dispense ₹2000 from the ATM machine

  If step 2 fails (ATM jammed):
    Without Atomicity: Your account is debited but no cash dispensed.
    With Atomicity:    Step 1 is rolled back. Your balance unchanged.

Database guarantee: Both happen or neither happens.
```

```sql
-- Atomicity in action
BEGIN;
UPDATE accounts SET balance = balance - 2000 WHERE id = 1;
-- Machine jams here, error occurs
UPDATE atm_cash SET cash = cash - 2000 WHERE machine_id = 101;  -- FAILS
ROLLBACK;   -- Atomicity: first UPDATE is cancelled too
```

---

## C — Consistency: Database Always Valid

**Definition:** A transaction brings the database from one valid state to another valid state. All constraints, rules, and checks must be satisfied after the transaction.

```
The Total Money Example:
  Before transfer:
    Adya: ₹1000, Rahul: ₹500
    TOTAL: ₹1500

  After ₹300 transfer:
    Adya: ₹700, Rahul: ₹800
    TOTAL: ₹1500

  The total money in the system hasn't changed.
  The database is in a consistent, valid state.

Consistency prevents:
  → Negative balances (CHECK constraint)
  → Duplicate primary keys (PK constraint)
  → Orphan records (FK constraint)
  → Invalid data types (column constraints)
```

```sql
-- Consistency enforced by constraints
CREATE TABLE accounts (
    id      SERIAL PRIMARY KEY,
    balance DECIMAL CHECK (balance >= 0)   -- CONSISTENCY: balance can't go negative
);

-- This transaction FAILS because it would violate consistency
BEGIN;
UPDATE accounts SET balance = balance - 5000 WHERE id = 1;
-- ERROR: Check constraint violation — balance would be -4000
ROLLBACK;   -- Database remains consistent
```

---

## I — Isolation: Transactions Don't See Each Other

**Definition:** Concurrent transactions execute independently. One transaction's intermediate (uncommitted) changes are NOT visible to other transactions.

```
The Last Laptop Example:
  stock = 1 (only one left)
  
  User A (Transaction 1):        User B (Transaction 2):
  BEGIN                          BEGIN
  Read stock → 1                 Read stock → 1
  Decide to buy                  Decide to buy
  UPDATE stock = stock - 1       UPDATE stock = stock - 1
  COMMIT                         COMMIT
  
  Without Isolation:
    Both users see stock=1
    Both "buy" the laptop
    stock becomes -1
    CATASTROPHIC — can't sell something you don't have
  
  With Isolation:
    Transaction 1 commits first, stock becomes 0
    Transaction 2 is blocked until Transaction 1 commits
    Transaction 2 reads stock = 0, cannot buy
    Only one laptop sold
```

**Isolation levels in PostgreSQL:**

```sql
-- READ COMMITTED (default in PostgreSQL)
-- Each statement sees only committed data
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;

-- REPEATABLE READ
-- All reads within transaction see same snapshot
SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;

-- SERIALIZABLE
-- Strictest: transactions appear to run one at a time
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
```

---

## D — Durability: Committed Data Survives Everything

**Definition:** Once a transaction is committed, the data is permanently saved — even if the server crashes, loses power, or restarts.

```
The Power Outage Example:
  
  Transaction:
    INSERT INTO orders (user_id, amount) VALUES (42, 89999);
    COMMIT;     ← Power goes out 0.001 seconds later
  
  Without Durability:
    The INSERT is lost.
    User paid but order doesn't exist.
    Customer service nightmare.
  
  With Durability:
    PostgreSQL uses Write-Ahead Logging (WAL).
    Before COMMIT, the change is written to a log file on disk.
    After restart, PostgreSQL replays the log.
    The INSERT is recovered.
    Data is safe.
```

---

## ACID Summary Table

```
┌───────────┬──────────────────────────┬────────────────────────────────────────────┐
│ Property  │ Simple Definition        │ Real Example                               │
├───────────┼──────────────────────────┼────────────────────────────────────────────┤
│ Atomicity │ All or nothing           │ Bank transfer: both updates or neither      │
│ Consist.  │ Database stays valid     │ Balance can't go negative (CHECK)          │
│ Isolation │ Transactions independent │ Two users can't buy the same last item     │
│ Durability│ Committed = permanent    │ Data survives server crash after COMMIT     │
└───────────┴──────────────────────────┴────────────────────────────────────────────┘
```

**Memory trick:**

```
A = All or Nothing
C = Constraints Always Satisfied
I = Invisible to Others Until Done
D = Data Lasts Forever After Commit
```

---

## Where Companies Use ACID

```
Banking (HDFC, SBI, ICICI):
  Every money transfer is a transaction.
  ACID prevents double-spending and lost transfers.

Payment Gateways (Razorpay, PayU, Stripe):
  Payment processing + order status update + invoice creation.
  All three must succeed or all three rollback.

E-commerce (Amazon, Flipkart):
  Order creation + stock reduction + payment capture.
  Three operations, one transaction.

UPI (PhonePe, Google Pay, Paytm):
  Every UPI transfer processes millions of ACID transactions per second.

Ticket Booking (IRCTC, BookMyShow):
  Seat reservation + payment + booking confirmation.
  ACID prevents two users from booking the same seat.
```

---

# SECTION 4 — THE N+1 QUERY PROBLEM

## What is the N+1 Problem?

The N+1 problem is when your application makes **1 query to get N records**, and then makes **N additional queries** to get related data for each record.

Total queries: **1 + N**

For 100 users: **101 queries**
For 1000 users: **1001 queries**

This is one of the most common performance killers in backend applications.

---

## Concrete Example

```
Scenario: Display all users with their orders on an admin dashboard.

N+1 APPROACH (WRONG):

Query 1 (1 query):
  SELECT * FROM users;
  Returns: User 1, User 2, User 3, ... User 100

Then for EACH user (N queries):
  SELECT * FROM orders WHERE user_id = 1;    -- Query 2
  SELECT * FROM orders WHERE user_id = 2;    -- Query 3
  SELECT * FROM orders WHERE user_id = 3;    -- Query 4
  ... 
  SELECT * FROM orders WHERE user_id = 100;  -- Query 101

TOTAL: 1 + 100 = 101 queries to the database
```

```python
# N+1 Problem in Python code (BAD)

users = db.execute("SELECT * FROM users")   # 1 query

for user in users:                          # N iterations
    orders = db.execute(
        f"SELECT * FROM orders WHERE user_id = {user['id']}"  # 1 query per user
    )
    user['orders'] = orders

# Total database round-trips: 1 + N
# For 1000 users: 1001 queries
# Each query has network latency: 1001 × 5ms = 5 seconds!
```

---

## Why N+1 Kills Performance

```
With 1000 users and 5ms per query:

N+1 approach:
  1001 queries × 5ms = 5,005ms = 5 seconds

JOIN approach:
  1 query × 5ms = 5ms

Performance difference: 1000x slower!

In production at scale:
  Imagine 10,000 concurrent users, each causing N+1
  Database gets flooded with millions of tiny queries
  Response times go from 50ms to 30 seconds
  Users see timeouts and errors
  Server CPU spikes to 100%
  The entire application appears down
```

---

## The Fix: Use a JOIN

```sql
-- ❌ N+1: One query per user (101 queries total)
SELECT * FROM users;
-- Then for each user:
SELECT * FROM orders WHERE user_id = ?;

-- ✅ JOIN: One query for everything
SELECT
    u.id         AS user_id,
    u.name       AS user_name,
    u.email,
    o.id         AS order_id,
    o.amount,
    o.status,
    o.order_date
FROM users u
LEFT JOIN orders o ON o.user_id = u.id
ORDER BY u.id, o.order_date DESC;

-- ONE query. Same result. 1000x faster.
```

---

## Complete N+1 Demonstration

```sql
-- ─────────────────────────────────────────────────────────────────
-- Setup for N+1 demonstration
-- ─────────────────────────────────────────────────────────────────

DROP TABLE IF EXISTS orders CASCADE;
DROP TABLE IF EXISTS users  CASCADE;

CREATE TABLE users (
    id    SERIAL PRIMARY KEY,
    name  VARCHAR(100),
    email VARCHAR(255)
);

CREATE TABLE orders (
    id         SERIAL PRIMARY KEY,
    user_id    INTEGER REFERENCES users(id),
    amount     DECIMAL(10,2),
    status     VARCHAR(20),
    order_date TIMESTAMP DEFAULT NOW()
);

INSERT INTO users (name, email) VALUES
('Adyaprana', 'adya@example.com'),
('Rahul',     'rahul@example.com'),
('Priya',     'priya@example.com'),
('Amit',      'amit@example.com');

INSERT INTO orders (user_id, amount, status) VALUES
(1, 89999, 'delivered'),
(1,  1200, 'delivered'),
(2,  2500, 'pending'),
(2, 29999, 'shipped'),
(3,  9999, 'delivered'),
(4, 14999, 'cancelled');


-- ─────────────────────────────────────────────────────────────────
-- THE WRONG WAY (N+1 in SQL — simulated)
-- ─────────────────────────────────────────────────────────────────

-- Step 1 (the "1" query):
SELECT id, name FROM users;

-- Step 2 (the "N" queries — one per user):
SELECT * FROM orders WHERE user_id = 1;
SELECT * FROM orders WHERE user_id = 2;
SELECT * FROM orders WHERE user_id = 3;
SELECT * FROM orders WHERE user_id = 4;
-- Total: 1 + 4 = 5 queries for 4 users
-- For 1 million users: 1,000,001 queries


-- ─────────────────────────────────────────────────────────────────
-- THE RIGHT WAY (single JOIN query)
-- ─────────────────────────────────────────────────────────────────

SELECT
    u.id          AS user_id,
    u.name,
    u.email,
    COUNT(o.id)   AS order_count,
    SUM(o.amount) AS total_spent
FROM users u
LEFT JOIN orders o ON o.user_id = u.id
GROUP BY u.id, u.name, u.email
ORDER BY total_spent DESC NULLS LAST;

-- Total: 1 query for any number of users


-- ─────────────────────────────────────────────────────────────────
-- FULL ORDER DETAILS (one query instead of N+1)
-- ─────────────────────────────────────────────────────────────────

SELECT
    u.name,
    u.email,
    o.id         AS order_id,
    o.amount,
    o.status,
    o.order_date
FROM users u
LEFT JOIN orders o ON o.user_id = u.id
ORDER BY u.id, o.order_date DESC;
```

---

## N+1 in ORM Code (SQLAlchemy)

```python
# ❌ WRONG: N+1 in SQLAlchemy (lazy loading)
users = session.query(User).all()    # 1 query: SELECT * FROM users
for user in users:
    print(user.orders)               # N queries: SELECT * FROM orders WHERE user_id = ?
# Result: 1 + N queries


# ✅ CORRECT: Eager loading (JOIN under the hood)
from sqlalchemy.orm import joinedload

users = session.query(User).options(joinedload(User.orders)).all()
# 1 query with JOIN: SELECT users.*, orders.* FROM users LEFT JOIN orders ON ...
for user in users:
    print(user.orders)   # No extra queries — data already loaded
# Result: 1 query total


# ✅ ALSO CORRECT: Explicit JOIN query
users_with_orders = session.execute(
    select(User, Order)
    .join(Order, Order.user_id == User.id, isouter=True)
).all()
```

---

## Transaction + N+1 Fix in FastAPI

```python
# How transactions work in FastAPI with SQLAlchemy

from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

app = FastAPI()

# TRANSACTION EXAMPLE: Place order with ACID guarantee
@app.post("/orders")
async def place_order(order_data: dict, db: AsyncSession = Depends(get_db)):
    async with db.begin():   # This is the BEGIN; ... COMMIT; block
        try:
            # Step 1: Create order
            new_order = Order(user_id=order_data["user_id"], status="pending")
            db.add(new_order)
            await db.flush()   # Get the new ID without committing

            # Step 2: Add order items
            for item in order_data["items"]:
                order_item = OrderItem(
                    order_id=new_order.id,
                    product_id=item["product_id"],
                    quantity=item["quantity"],
                    price=item["price"]
                )
                db.add(order_item)

            # Step 3: Reduce stock
            await db.execute(
                update(Product)
                .where(Product.id == item["product_id"])
                .values(stock=Product.stock - item["quantity"])
            )

            # All steps succeeded → db.begin() auto-commits
            return {"order_id": new_order.id}

        except Exception as e:
            # Any exception → auto ROLLBACK (db.begin() handles this)
            raise HTTPException(status_code=500, detail=str(e))


# N+1 FIX EXAMPLE: Get users with orders efficiently
@app.get("/users/dashboard")
async def get_dashboard(db: AsyncSession = Depends(get_db)):
    # ❌ N+1 (DON'T DO THIS):
    # users = (await db.execute(select(User))).scalars().all()
    # for user in users:
    #     orders = user.orders  # triggers N separate queries

    # ✅ Eager loading (DO THIS):
    result = await db.execute(
        select(User)
        .options(selectinload(User.orders))   # JOIN in one query
        .order_by(User.name)
    )
    users = result.scalars().all()
    return users   # No N+1 queries
```

---

# SECTION 5 — LEET CODE 1045

## LeetCode 1045 — Customers Who Bought All Products

```sql
-- ═══════════════════════════════════════════════════════════════
-- LeetCode #1045 — Customers Who Bought All Products
-- Difficulty: Medium | Status: ✅ Accepted (9/9 test cases)
-- Runtime: 473ms | Memory: 0.00 MB | Beats runtime: 97.91%
-- Topic: COUNT(DISTINCT) + GROUP BY + HAVING + Scalar Subquery
-- ═══════════════════════════════════════════════════════════════

DROP TABLE IF EXISTS Customer;
DROP TABLE IF EXISTS Product;

CREATE TABLE Product (
    product_key INT PRIMARY KEY
);

CREATE TABLE Customer (
    customer_id INT,
    product_key INT
);

INSERT INTO Product VALUES (5), (6);

INSERT INTO Customer VALUES
(1,5),(1,6),(2,5),(3,5),(3,6);

-- View data
SELECT * FROM Product;
SELECT * FROM Customer;

-- SOLUTION
-- Logic:
-- A customer has bought ALL products if the count of
-- their DISTINCT purchased products equals the total number of products.

SELECT customer_id
FROM Customer
GROUP BY customer_id
HAVING COUNT(DISTINCT product_key) = (
    SELECT COUNT(*) FROM Product
);

-- Step by step:
-- 1. GROUP BY customer_id → one group per customer
-- 2. COUNT(DISTINCT product_key) → unique products per customer
-- 3. Subquery: (SELECT COUNT(*) FROM Product) → total products = 2
-- 4. HAVING: keep customers where unique bought = total available

-- Why COUNT(DISTINCT)?
-- Customer may buy same product twice. DISTINCT prevents double-counting.
-- COUNT(product_key) = 3 for customer who bought product 5 twice and product 6 once
-- COUNT(DISTINCT product_key) = 2 → correct

-- Alternative: verify against COUNT(DISTINCT product_key) FROM Customer
-- (same result, but referencing Customer table instead of Product table)
-- HAVING COUNT(DISTINCT product_key) = (SELECT COUNT(DISTINCT product_key) FROM Customer);

-- Expected output:
-- customer_id
-- 1
-- 3
```

---

# SECTION 6 — DEEP THEORY

## How PostgreSQL Implements Transactions (WAL)

PostgreSQL uses **Write-Ahead Logging (WAL)** to guarantee durability:

```
When you run a query inside a transaction:

1. PostgreSQL first writes the change to the WAL log file on disk
2. Then applies the change to the in-memory buffer
3. Periodically flushes the buffer to actual data files

On COMMIT:
  → WAL record is flushed and synced to disk (fsync)
  → Change is guaranteed to survive any crash

On ROLLBACK:
  → WAL records for this transaction are marked as void
  → In-memory changes are discarded
  → Data files are unchanged

After crash:
  → On restart, PostgreSQL reads WAL
  → Replays committed transactions
  → Discards uncommitted changes
  → Database is consistent
```

---

## Isolation Levels Explained

```
Problem 1: Dirty Read
  Transaction A reads data that Transaction B hasn't committed yet.
  If B rolls back, A read data that never officially existed.
  PostgreSQL prevents this by default.

Problem 2: Non-Repeatable Read
  Transaction A reads a row.
  Transaction B updates that row and commits.
  Transaction A reads the same row again → different value.
  Same transaction, same query, different results.

Problem 3: Phantom Read
  Transaction A queries "all products under ₹1000".
  Transaction B inserts a new product under ₹1000.
  Transaction A repeats the query → new row appears (phantom).

Isolation Level Protections:
  READ UNCOMMITTED → Prevents nothing (not available in PostgreSQL)
  READ COMMITTED   → Prevents Dirty Reads (PostgreSQL default)
  REPEATABLE READ  → Prevents Dirty + Non-Repeatable Reads
  SERIALIZABLE     → Prevents all three
```

---

## Deadlock — When Transactions Block Each Other

```
Transaction A:
  BEGIN;
  UPDATE accounts SET balance = balance - 100 WHERE id = 1;  -- Locks row 1
  UPDATE accounts SET balance = balance + 100 WHERE id = 2;  -- Waits for row 2

Transaction B (running simultaneously):
  BEGIN;
  UPDATE accounts SET balance = balance - 100 WHERE id = 2;  -- Locks row 2
  UPDATE accounts SET balance = balance + 100 WHERE id = 1;  -- Waits for row 1

DEADLOCK:
  A is waiting for row 2 (held by B)
  B is waiting for row 1 (held by A)
  Neither can proceed.
  They wait forever.

PostgreSQL detects this automatically:
  → Picks one transaction as the "victim"
  → Rolls it back
  → The other transaction can proceed

Prevention:
  → Always acquire locks in the same order
  → Keep transactions short
  → Use shorter isolation levels when possible
```

---

# SECTION 7 — IMPORTANT THINGS TO KNOW

```
 1. Every transaction starts with BEGIN and ends with COMMIT or ROLLBACK.

 2. In PostgreSQL, every single statement is automatically wrapped
    in a transaction if you don't use BEGIN explicitly.
    Single statements are auto-committed.

 3. COMMIT is permanent. After COMMIT, you cannot ROLLBACK.
    To undo, you must write a new correcting transaction.

 4. ROLLBACK undoes everything since the last BEGIN.

 5. SAVEPOINT lets you rollback to a specific point without
    cancelling the entire transaction.

 6. ACID is the gold standard for relational database guarantees.
    NoSQL databases (MongoDB, DynamoDB) often sacrifice some ACID properties for speed.

 7. Atomicity = All or Nothing.
    Consistency = Database always valid after transaction.
    Isolation = Transactions don't interfere.
    Durability = Committed data survives crashes.

 8. PostgreSQL is ACID-compliant by default. This is a major selling point.

 9. N+1 is almost always caused by ORM lazy loading.
    Solution: use eager loading (joinedload, selectinload) or explicit JOINs.

10. One JOIN is ALWAYS faster than N+1 separate queries for reasonable data sizes.

11. Transactions in FastAPI/SQLAlchemy: use async with db.begin():
    This automatically commits on success and rolls back on exception.

12. Never store money as FLOAT. Use DECIMAL(10,2) or INTEGER (cents).
    FLOAT has rounding errors: 0.1 + 0.2 ≠ 0.3 in floating point.

13. Deadlocks are detected automatically by PostgreSQL.
    Prevention: always lock tables/rows in the same order.

14. PostgreSQL uses MVCC (Multi-Version Concurrency Control) for isolation.
    Readers don't block writers, writers don't block readers.

15. TRUNCATE is NOT transactional in all databases.
    In PostgreSQL, TRUNCATE IS transactional (can be rolled back inside BEGIN).

16. The CHECK constraint on balance >= 0 enforces Consistency.
    It prevents the balance from going negative even within a transaction.

17. ON DELETE CASCADE is automatic deletion of children — essentially
    a mini-transaction handled by the database automatically.

18. EXPLAIN ANALYZE shows actual query execution time.
    Use it to verify that JOIN is faster than N+1 in your specific case.

19. Read-only transactions (only SELECT) don't need COMMIT or ROLLBACK.
    They are automatically clean.

20. In production FastAPI apps, the transaction is typically the entire
    HTTP request: BEGIN when request starts, COMMIT when response is sent,
    ROLLBACK on any exception.
```

---

# SECTION 8 — INTERVIEW QUESTIONS

## Q1. What is a database transaction?

A transaction is a sequence of one or more SQL operations that execute as a single logical unit of work. The fundamental rule is "all or nothing" — either every operation in the transaction succeeds and is committed, or if any operation fails, all changes are rolled back and the database returns to its state before the transaction began.

---

## Q2. Explain ACID properties with real-world examples.

**Atomicity:** A bank transfer deducts from one account and adds to another. If the second operation fails, the first is rolled back. You can't have money disappear from one account without appearing in the other.

**Consistency:** Before the transfer, total money in the system is ₹1500. After the transfer, total is still ₹1500. The database moves from one valid state to another, always respecting constraints like "balance cannot be negative."

**Isolation:** Two users simultaneously try to buy the last concert ticket. Isolation ensures only one of them succeeds. The other sees the updated count and is told the ticket is sold.

**Durability:** After a payment is committed, even if the server loses power immediately afterward, the payment record survives and is recovered when the server restarts.

---

## Q3. What is the difference between COMMIT and ROLLBACK?

`COMMIT` permanently saves all changes made within the transaction. The data is written to disk, becomes visible to all other users, and cannot be undone with ROLLBACK.

`ROLLBACK` cancels all changes made since `BEGIN`. The database returns to exactly the state it was in before the transaction started. It is used when an error occurs or when you explicitly want to discard changes.

---

## Q4. What is the N+1 query problem? How do you fix it?

The N+1 problem occurs when you execute 1 query to fetch N records (e.g., 100 users), then execute N additional queries to fetch related data for each record (e.g., orders for each user). Total: 101 queries instead of 1.

**Why it's bad:** Each query has network latency (~5ms). 101 queries = ~500ms. For 1000 users: 1001 queries = ~5 seconds. At scale, this floods the database.

**Fix 1 — SQL JOIN:**

```sql
SELECT u.name, o.amount
FROM users u
LEFT JOIN orders o ON o.user_id = u.id;
-- One query instead of N+1
```

**Fix 2 — ORM eager loading:**

```python
# SQLAlchemy: loads users and orders in one query
users = session.query(User).options(joinedload(User.orders)).all()
```

---

## Q5. When should you use transactions?

Use transactions whenever you have two or more related operations that must either all succeed or all fail together:

- Money transfers (debit + credit)
- Order placement (create order + reduce stock + charge payment)
- User registration (insert user + send welcome email log)
- Ticket booking (reserve seat + process payment + send confirmation)
- Any multi-table insert/update that must remain consistent

For simple single-statement operations (one INSERT, one UPDATE), PostgreSQL automatically wraps them in a transaction.

---

## Q6. What is Isolation and what problems does it prevent?

Isolation ensures that concurrent transactions execute as if they were running sequentially, preventing them from interfering with each other.

It prevents three problems:

**Dirty Read:** Reading uncommitted data from another transaction (which might get rolled back).

**Non-Repeatable Read:** Reading the same row twice within a transaction and getting different values because another transaction updated it.

**Phantom Read:** A query returns different rows when executed twice because another transaction inserted or deleted rows.

PostgreSQL's default isolation level (READ COMMITTED) prevents dirty reads. REPEATABLE READ also prevents non-repeatable reads. SERIALIZABLE prevents all three.

---

## Q7. What happens if a transaction fails halfway through?

If any error occurs within a transaction (constraint violation, network failure, server crash), PostgreSQL will ROLLBACK the entire transaction. Because of WAL (Write-Ahead Logging), uncommitted changes are never permanently applied to the data files.

If the server crashes mid-transaction:
- On restart, PostgreSQL reads the WAL
- Finds the unfinished transaction (no COMMIT record)
- Discards those changes
- Database is restored to the consistent state before the transaction

---

## Q8. What is a deadlock? How does PostgreSQL handle it?

A deadlock occurs when two transactions each hold a lock the other needs:

Transaction A holds lock on row 1, waiting for row 2.
Transaction B holds lock on row 2, waiting for row 1.
Neither can proceed.

PostgreSQL's deadlock detector identifies this automatically (typically within 1 second), picks one transaction as the "victim," rolls it back, and lets the other proceed. The rolled-back transaction receives an error and should be retried.

Prevention: always acquire locks in a consistent order across all transactions.

---

## Q9. How do transactions work in FastAPI with SQLAlchemy?

```python
# Method 1: Context manager (recommended)
async with db.begin():
    # All operations here are in one transaction
    db.add(new_order)
    await db.execute(update_stock_query)
    # Auto-commits on success, auto-rollbacks on exception

# Method 2: Manual
try:
    db.add(new_order)
    await db.flush()
    await db.commit()
except Exception:
    await db.rollback()
    raise
```

In FastAPI, the common pattern is one transaction per HTTP request. The request starts the transaction, the response commits it, and any unhandled exception triggers a rollback.

---

## Q10. What is MVCC and why does PostgreSQL use it?

MVCC (Multi-Version Concurrency Control) is PostgreSQL's concurrency mechanism. Instead of using exclusive locks that force readers and writers to wait for each other, PostgreSQL maintains multiple versions of each row.

A writer creates a new version of the row without overwriting the old one. A concurrent reader sees the old version, unchanged. When the writer commits, future readers see the new version.

Result:
- Readers never block writers
- Writers never block readers
- High concurrency without lock contention
- This is a major performance advantage over lock-based systems

---

# SECTION 9 — COMPLETE WORKING SQL SCRIPT

```sql
-- ═══════════════════════════════════════════════════════════════
-- DAY 33 — TRANSACTIONS: COMPLETE PRACTICE SCRIPT
-- Copy and run in pgAdmin.
-- ═══════════════════════════════════════════════════════════════

-- ─────────────────────────────────────────────────────────────────
-- SETUP
-- ─────────────────────────────────────────────────────────────────

DROP TABLE IF EXISTS transfers;
DROP TABLE IF EXISTS accounts;

CREATE TABLE accounts (
    id      SERIAL         PRIMARY KEY,
    name    VARCHAR(100)   NOT NULL,
    balance DECIMAL(10, 2) NOT NULL DEFAULT 0 CHECK (balance >= 0)
);

CREATE TABLE transfers (
    id           SERIAL         PRIMARY KEY,
    from_id      INTEGER        REFERENCES accounts(id),
    to_id        INTEGER        REFERENCES accounts(id),
    amount       DECIMAL(10, 2) NOT NULL CHECK (amount > 0),
    transferred_at TIMESTAMP    DEFAULT NOW(),
    status       VARCHAR(20)    DEFAULT 'completed'
);

INSERT INTO accounts (name, balance) VALUES
('Adyaprana', 1000.00),
('Rahul',      500.00),
('Priya',     2000.00);

SELECT * FROM accounts;


-- ─────────────────────────────────────────────────────────────────
-- EXAMPLE 1: Successful Transaction
-- ─────────────────────────────────────────────────────────────────

BEGIN;

-- Deduct from Adyaprana
UPDATE accounts
SET balance = balance - 300
WHERE id = 1;

-- Add to Rahul
UPDATE accounts
SET balance = balance + 300
WHERE id = 2;

-- Log the transfer
INSERT INTO transfers (from_id, to_id, amount, status)
VALUES (1, 2, 300.00, 'completed');

COMMIT;

SELECT * FROM accounts;
SELECT * FROM transfers;


-- ─────────────────────────────────────────────────────────────────
-- EXAMPLE 2: Rollback (simulate failed transfer)
-- ─────────────────────────────────────────────────────────────────

BEGIN;

UPDATE accounts
SET balance = balance - 100
WHERE id = 2;

-- Something goes wrong! Roll back.
ROLLBACK;

-- Rahul's balance unchanged
SELECT * FROM accounts WHERE id = 2;


-- ─────────────────────────────────────────────────────────────────
-- EXAMPLE 3: CHECK constraint enforces Consistency
-- ─────────────────────────────────────────────────────────────────

BEGIN;

-- Try to overdraft Rahul (he has 800, try to deduct 1000)
UPDATE accounts
SET balance = balance - 1000
WHERE id = 2;
-- ERROR: new row violates check constraint "accounts_balance_check"

ROLLBACK;

SELECT * FROM accounts WHERE id = 2;  -- Balance unchanged


-- ─────────────────────────────────────────────────────────────────
-- EXAMPLE 4: SAVEPOINT
-- ─────────────────────────────────────────────────────────────────

BEGIN;

SAVEPOINT before_priya_transfer;

UPDATE accounts
SET balance = balance - 500
WHERE id = 3;   -- Deduct from Priya

-- Decide to undo this specific step
ROLLBACK TO SAVEPOINT before_priya_transfer;

-- Now do a different operation instead
UPDATE accounts
SET balance = balance - 200
WHERE id = 3;

COMMIT;

SELECT * FROM accounts;


-- ─────────────────────────────────────────────────────────────────
-- N+1 FIX DEMONSTRATION
-- ─────────────────────────────────────────────────────────────────

DROP TABLE IF EXISTS orders;

CREATE TABLE orders (
    id      SERIAL  PRIMARY KEY,
    user_id INTEGER REFERENCES accounts(id),
    amount  DECIMAL(10,2)
);

INSERT INTO orders (user_id, amount) VALUES
(1, 89999), (1, 1200),
(2, 2500),  (2, 29999),
(3, 9999);

-- ❌ N+1 (don't do this):
-- SELECT * FROM accounts;
-- SELECT * FROM orders WHERE user_id = 1;
-- SELECT * FROM orders WHERE user_id = 2;
-- SELECT * FROM orders WHERE user_id = 3;
-- Total: 4 queries

-- ✅ JOIN (do this):
SELECT
    a.name,
    COUNT(o.id)   AS order_count,
    SUM(o.amount) AS total_spent
FROM accounts a
LEFT JOIN orders o ON o.user_id = a.id
GROUP BY a.id, a.name
ORDER BY total_spent DESC NULLS LAST;
-- Total: 1 query
```

---

# REVISION SHEET

```
═══════════════════════════════════════════════════════════
TRANSACTIONS + ACID — ONE-PAGE REVISION
═══════════════════════════════════════════════════════════

TRANSACTION COMMANDS:
  BEGIN;              → Start a transaction
  COMMIT;             → Save all changes permanently
  ROLLBACK;           → Cancel all changes since BEGIN
  SAVEPOINT name;     → Mark a partial rollback point
  ROLLBACK TO name;   → Rollback to a specific savepoint

ACID PROPERTIES:
  A = Atomicity    → All or nothing. Partial success impossible.
  C = Consistency  → Database always remains in valid state.
  I = Isolation    → Transactions are invisible to each other until committed.
  D = Durability   → Committed data survives crashes (WAL logging).

WHEN TO USE TRANSACTIONS:
  ✅ Bank transfers
  ✅ Order placement (order + items + stock update)
  ✅ Ticket booking
  ✅ Any multi-step operation that must stay consistent

N+1 PROBLEM:
  What: 1 query + N queries = N+1 total
  Why bad: Network overhead × N queries
  Fix: Use JOIN (1 query total)
  ORM Fix: joinedload() or selectinload()

ISOLATION LEVELS (low to high strictness):
  READ COMMITTED (default) → No dirty reads
  REPEATABLE READ          → No dirty + non-repeatable reads
  SERIALIZABLE             → No dirty + non-repeatable + phantom reads

KEY RULES:
  ❌ Single UPDATE without BEGIN = auto-committed (permanent!)
  ❌ FLOAT for money (use DECIMAL)
  ❌ N+1 queries (use JOIN)
  ✅ Always ROLLBACK on error in multi-step operations
  ✅ Keep transactions short and fast
  ✅ Use savepoints for complex workflows
```

---

## LeetCode Solved This Day

| Problem | Difficulty | Topic | Status | Runtime |
|---------|-----------|-------|--------|---------|
| #1045 Customers Who Bought All Products | Medium | COUNT(DISTINCT) + GROUP BY + HAVING + Subquery | ✅ Accepted 9/9 | 473ms |

---

## 🎥 Recommended Resource

> **▶ InterviewBit SQL Interview Questions Section**
>
> Covers the exact transaction and ACID questions asked at Amazon, Flipkart, Goldman Sachs, and other top companies. The N+1 problem is a common follow-up in backend system design interviews.

---

*Day 33 Complete.* ✅
