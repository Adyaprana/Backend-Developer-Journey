#JOIN VISUALIZATION:

# INNER JOIN -> (Only Matching)
# Users   Orders
   # ○────○


# LEFT JOIN -> (Everything from LEFT)
# Users   Orders
# █████────○


# RIGHT JOIN -> (Everything from RIGHT)
# Users   Orders
# ○────█████

# FULL OUTER JOIN -> (Everything)
# Users   Orders
# █████────█████



# 1. JOIN Always Needs a Condition
# Correct: ON users.id = orders.user_id
# Without ON, you'll get a Cartesian product (every row paired with every other row).


# 2. INNER JOIN Removes Unmatched Rows
# If no matching key exists: The row disappears.


# 3. LEFT JOIN Uses NULL
# If no matching row exists: NULL is returned for the right table's columns.


# 4. Self Join Requires Aliases
# Instead of: 
# FROM employees
# JOIN employees
# Use aliases:
# FROM employees e
# JOIN employees m
# Much cleaner.


# 5. Primary Key vs Foreign Key
# Users: id --> Primary Key
# Orders: user_id --> Foreign Key
# JOIN connects these keys.


