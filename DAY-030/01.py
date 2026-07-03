# 1. CONCEPTUAL SUMMARY


# Why Do We Need JOIN?
# Real databases don't store everything in one table.

# Instead of: Users
# -------------------------
# ID | Name | Order | Price

# Databases are normalized into separate tables:
# Users
# -----------
# ID | Name

# Orders
# ------------------
# ID | User_ID | Price

# JOIN combines data from multiple tables into one result.
# Backend applications use JOINs constantly—for dashboards, user profiles, orders, payments, products, and reports.



# What is an INNER JOIN?
# INNER JOIN returns only matching records from both tables.

# Think of it as the common part of two circles in a Venn diagram.
# If a user has no order, that user is not shown.
# If an order has no matching user, that order is not shown. 

# It is the most frequently used JOIN in SQL.
# Example: Users->
# 1 Adyaprana
# 2 Rahul
# 3 Priya

# Orders->
# 1 Laptop
# 2 Phone

# Result->
# Adyaprana Laptop
# Rahul Phone
# Priya is not shown because she has no order.



# What is LEFT JOIN?
# LEFT JOIN returns: Every row from the left table & the Matching rows from the right table
# If there is no match: NULL is returned.

# This is useful when you want to see all users—even those without orders.
# Example: Users->
# Adyaprana
# Rahul
# Priya

# Orders->
# Laptop
# Phone

# Result->
# Adyaprana Laptop
# Rahul Phone
# Priya NULL



# What is RIGHT JOIN?
# Opposite of LEFT JOIN.
# Returns: Every row from the right table & Matching rows from left

# Useful when the right table is more important.
# Example: Show every order—even if the user was deleted.



# What is FULL OUTER JOIN?
# Returns everything.
# Matching rows
# Left-only rows
# Right-only rows
# Missing values become NULL.
# Useful for finding unmatched records on both sides.



# What is a SELF JOIN?
# A table joins with itself.
# Common example:
# Employees
# ID
# Employee
# Manager_ID

# Manager is also an employee.
# So: Employee table joins itself.


# Backend Example
# Suppose Instagram:
# Users
# ID
# Username
# Followers
# Follower_ID
# Following_ID
# Backend joins: Users with Users

# (Self Join)
# to know: Rahul follows Adyaprana



# Why JOINs Matter
# Almost every backend application uses JOINs.
# Examples:
# User + Orders
# Product + Category
# Employee + Department
# Student + Course
# Customer + Payment
# Doctor + Hospital

# Without JOINs: Real applications cannot work.