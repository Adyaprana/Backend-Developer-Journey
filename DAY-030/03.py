# Interview Questions & Answers:

# Question 1: Show every user along with their orders.
# Concept: Use INNER JOIN to display only users who actually placed orders.

# SELECT
# users.name,
# orders.product
# FROM users
# INNER JOIN orders
# ON users.id = orders.user_id;


# Question 2: Find users who never placed an order.
# Concept: Use LEFT JOIN and filter where the right table is NULL.

# SELECT
# users.name
# FROM users
# LEFT JOIN orders
# ON users.id = orders.user_id
# WHERE orders.order_id IS NULL;


# Question 3: Show employees and their managers.
# Concept: Join the employees table with itself.

# SELECT
# e.employee_name,
# m.employee_name AS manager
# FROM employees e
# LEFT JOIN employees m
# ON e.manager_id = m.emp_id;


# Question 4: Difference between INNER JOIN and LEFT JOIN?
# Answer: 
# INNER JOIN → Returns only matching rows from both tables.
# LEFT JOIN → Returns all rows from the left table and matching rows from the right table. If no match exists, right-side columns contain NULL.


# Question 5: What is a Foreign Key?
# Answer: A Foreign Key is a column that references the Primary Key of another table, creating a relationship between the two.

# Example:
# Users
# ------
# id (Primary Key)

# Orders
# -------
# user_id (Foreign Key)

