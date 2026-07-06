# THEORY 5 — ACID Properties

# A — Atomicity
# Definition: A transaction is all or nothing.

# Example: 
# Bank Transfer
# Deduct Money -> Server Crash -> Rollback
# No partial updates.

# Example: 
# Bad
# Deduct ₹500
# Friend doesn't receive money
# Impossible: Atomicity prevents this.

# Interview Definition: Atomicity ensures either every operation succeeds or every operation is rolled back.



# C — Consistency
# Definition: A transaction must leave the database in a valid state.

# Example:
# Before transfer
# Account A = 1000
# Account B = 500
# Total = 1500

# After transfer
# Account A = 700
# Account B = 800
# Total = 1500
# Database remains consistent.

# Consistency prevents
# Invalid data
# Broken relationships
# Constraint violations



# I — Isolation
# Definition: Multiple transactions should not interfere with each other.
# Imagine: Two people buying the last laptop. Without isolation Both users buy it. Inventory becomes -1 Wrong.
# Isolation prevents this.



# D — Durability
# Definition: Once COMMIT happens, data is permanently saved.
# Even if
# Server crashes
# Electricity goes
# Restart happens
# Data stays.

# Interview Definition: Durability guarantees committed data survives failures.


# Easy Way to Remember ACID: 
# | Letter | Meaning                      |
# | ------ | ---------------------------- |
# | A      | All or Nothing               |
# | C      | Database Always Valid        |
# | I      | Transactions Don't Interfere |
# | D      | Committed Data Never Lost    |

