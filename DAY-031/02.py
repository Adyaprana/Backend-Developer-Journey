

# Important Things To Know

# WHERE vs HAVING ->
# WHERE: Filters rows.
# HAVING: Filters groups.


# GROUP BY Rule ->
# Every selected column must either:
# appear in GROUP BY
# or
# use an aggregate function.


# ORDER BY Position -> 
# Almost always the last clause.
# Typical order:
# SELECT
# FROM
# WHERE
# GROUP BY
# HAVING
# ORDER BY
# LIMIT
# OFFSET


# LIMIT before OFFSET -> 
# Example:
# LIMIT 5 OFFSET 10
# means: Skip first 10 rows.
# Return next 5.


# COUNT(*) -> 
# Counts every row.
# Even if values are NULL.




# Interview Questions

# Q1. Find total orders placed by each customer.
# Explanation: Groups orders using customer_id.
# SELECT
# customer_id,
# COUNT(*)
# FROM orders
# GROUP BY customer_id;

# Q2. Find customers placing at least two orders.
# Explanation: Uses HAVING because filtering happens after grouping.
# SELECT
# customer_id,
# COUNT(*)
# FROM orders
# GROUP BY customer_id
# HAVING COUNT(*)>=2;

# Q3. Find highest order amount.
# SELECT MAX(amount)
# FROM orders;

# Q4. Find customers whose total purchase exceeds ₹1000.
# SELECT
# customer_id,
# SUM(amount)
# FROM orders
# GROUP BY customer_id
# HAVING SUM(amount)>1000;

# Q5. Find all orders greater than average order amount.
# SELECT *
# FROM orders
# WHERE amount >
# (
# SELECT AVG(amount)
# FROM orders
# );
