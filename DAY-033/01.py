# THEORY 1 — What is a Transaction?

# Definition: A Transaction is a group of one or more SQL operations that execute as one logical unit of work.
# Either: ✅ Everything succeeds OR ❌ Everything fails
# There is no partial success.

# Real Life Example:  Imagine transferring ₹500 from your account to your friend's account.
# Step 1: Deduct ₹500 from your account
# Step 2: Add ₹500 to friend's account
# If Step 1 succeeds but Step 2 fails,
# then ₹500 disappears forever.
# That is unacceptable.
# A transaction ensures: Both happen OR Neither happens.

# Interview Definition: A transaction is a sequence of SQL operations executed as one unit where either all operations succeed or all are rolled back.






# THEORY 2 — BEGIN

# Every transaction starts with BEGIN;
# Example:
# BEGIN;
# UPDATE accounts
# SET balance = balance - 500
# WHERE id = 1;
# Nothing is permanent yet.

# THEORY 3 — COMMIT
# COMMIT permanently saves all changes.
# Example:
# BEGIN;
# UPDATE accounts
# SET balance = balance - 500
# WHERE id = 1;
# UPDATE accounts
# SET balance = balance + 500
# WHERE id = 2;
# COMMIT;

# Result: Both balances are permanently updated.

# THEORY 4 — ROLLBACK
# Rollback cancels all changes since BEGIN.
# Example: 
# BEGIN;
# UPDATE accounts
# SET balance = balance - 500
# WHERE id = 1;
# ROLLBACK;

# Result: Balance returns to its original value. Nothing changed.


# Full Working Example:
# Imagine this table.
# | id | name  | balance |
# | -- | ----- | ------- |
# | 1  | Adya  | 1000    |
# | 2  | Rahul | 500     |


# Transfer ₹300: --> 

# BEGIN;
# UPDATE accounts
# SET balance = balance - 300
# WHERE id = 1;

# UPDATE accounts
# SET balance = balance + 300
# WHERE id = 2;

# COMMIT;

# Final:
# | id | balance |
# | -- | ------- |
# | 1  | 700     |
# | 2  | 800     |


# Now imagine server crashes after first UPDATE.
# Instead:

# BEGIN;
# UPDATE accounts
# SET balance = balance - 300
# WHERE id = 1;
# ROLLBACK;

# Final:
# | id | balance |
# | -- | ------- |
# | 1  | 1000    |
# | 2  | 500     |

# No money lost.






