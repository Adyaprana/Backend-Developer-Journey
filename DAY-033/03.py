# THEORY 6 — Why Transactions Matter

# Companies like:
# Amazon
# Razorpay
# PhonePe
# Google Pay
# UPI
# Banks
# use transactions every second.

# Examples: 
# Money transfer
# Ticket booking
# Product purchase
# Wallet recharge
# Inventory updates

# Without transactions--> companies would lose millions.



# THEORY 7 — Transaction Flow
# Customer buys laptop.
# BEGIN -> Reduce Stock -> Create Order -> Payment Success -> COMMIT

# If payment fails
# BEGIN -> Reduce Stock -> Payment Failed -> ROLLBACK
# Stock returns.



# THEORY 8 — N+1 Query Problem
#  Suppose: 100 users, Each user has orders, 

# Bad Code
# Query 1
# SELECT * FROM users;

# Then
# For each user
# SELECT * FROM orders
# WHERE user_id = ?

# Total: 1 + 100 = 101 Queries
# This is called -> N+1 Problem.

# Why is it bad?
# Because Instead of 1 Query we execute 101 Queries
# Much slower.


# Better Solution
# Use JOIN.
# Instead

# SELECT
# users.name,
# orders.id
# FROM users
# JOIN orders
# ON users.id = orders.user_id;

# One query.
# Huge performance improvement.


# ORM Solution: 

# Later in FastAPI you'll use SQLAlchemy.
# Instead of lazy loading, use eager loading.

# Example
# joinedload(User.orders)
# ORMs also solve the N+1 problem.





# THEORY 9 — Why Performance Matters

# Suppose: 1000 users Each has 50 orders N+1 1001 Queries
# JOIN 1 Query
# Difference is enormous.






# THEORY 10 — FastAPI + Transactions
# Frontend -> FastAPI -> SQLAlchemy Session -> BEGIN -> Queries -> COMMIT -> Response

# If any error occurs
# ROLLBACK
# This is how real production applications work.

# Working SQL Example
# BEGIN;
# INSERT INTO orders (user_id, status)
# VALUES (1, 'Pending');
# UPDATE products
# SET stock = stock - 1
# WHERE id = 5;
# COMMIT;
# If product stock update fails
# ROLLBACK;
# Nothing is inserted.





# SAVEPOINT

# Sometimes you don't want to rollback the entire transaction.
# You can rollback partially.

# BEGIN;
# SAVEPOINT step1;
# UPDATE accounts
# SET balance = balance - 500
# WHERE id = 1;
# ROLLBACK TO step1;
# COMMIT;






# INTERVIEW QUESTIONS:

# Q1. What is a transaction?
# Answer: A transaction is a sequence of SQL operations executed as one unit of work where all operations either succeed together or fail together.

# Q2. Why do we use transactions?
# Answer: To maintain data integrity and prevent partial updates.

# Q3. Difference between COMMIT and ROLLBACK?
# Answer:   COMMIT permanently saves changes.
#           ROLLBACK cancels changes since BEGIN.

# Q4. What does BEGIN do?
# Answer: Starts a transaction.

# Q5. Explain Atomicity.
# Answer: All operations in a transaction succeed together or none of them succeed.

# Q6. Explain Consistency.
# Answer: The database moves from one valid state to another valid state while respecting constraints.

# Q7. Explain Isolation.
# Answer: Concurrent transactions should not interfere with each other.

# Q8. Explain Durability.
# Answer: Once committed, data remains permanently stored even after crashes.

# Q9. What is the N+1 Query Problem?
# Answer: Fetching one main query followed by one additional query for each returned row, leading to excessive database queries.

# Q10. How do you solve the N+1 problem?
# Answer: se JOINs
# Use eager loading in ORMs
# Fetch related data in a single query whenever possible


# Q11. Why are JOINs faster than N+1 queries?
# Answer: JOINs reduce multiple database round trips into a single optimized query.

# Q12. Where are transactions commonly used?
# Answer: anking
# Payments
# E-commerce orders
# Ticket booking
# Inventory management


# Q13. Can a transaction contain multiple SQL statements?
# Answer: Yes. A transaction can include multiple INSERT, UPDATE, DELETE, and SELECT statements before COMMIT or ROLLBACK.

# Q14. What happens if the database crashes after COMMIT?
# Answer: Because of Durability, committed data is preserved and recovered after restart.

# Q15. What happens if a transaction fails halfway?
# Answer: The transaction should be rolled back so the database returns to its previous consistent state.