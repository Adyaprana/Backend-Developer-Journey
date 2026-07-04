# 1. Conceptual Summary

# GROUP BY: 
# GROUP BY combines rows that have the same value in one or more columns into a single group. 
# Instead of looking at individual records, SQL performs calculations on each group. 
# It is commonly used to generate reports like total sales per customer or number of employees in each department.
# Example:
# SELECT department,
# COUNT(*)
# FROM employees
# GROUP BY department;



# HAVING: 
# HAVING filters grouped data after GROUP BY has finished. 
# While WHERE filters individual rows before grouping, HAVING filters the groups themselves.
# Example:
# SELECT department,
# COUNT(*)
# FROM employees
# GROUP BY department
# HAVING COUNT(*) > 5;




# ORDER BY: 
# ORDER BY sorts query results.
# Ascending: ORDER BY salary ASC;
# Descending: ORDER BY salary DESC;
# Usually placed at the end of the query.




# LIMIT: LIMIT restricts how many rows SQL returns.
# Example:
# SELECT *
# FROM employees
# LIMIT 5;
# Useful for Top-N reports and pagination.




# OFFSET: OFFSET skips a specified number of rows.
# Example:
# SELECT *
# FROM employees
# LIMIT 5 OFFSET 10;
# Meaning: Skip first 10 rows and return next 5.




# COUNT(): Returns how many rows exist.
# Example:
# SELECT COUNT(*)
# FROM employees;




# SUM(): Returns total of numeric values.
# Example:
# SELECT SUM(salary)
# FROM employees;




# AVG(): Returns average.
# Example:
# SELECT AVG(salary)
# FROM employees;




# MAX(): Returns largest value.
# Example:
# SELECT MAX(salary)
# FROM employees;




# MIN(): Returns smallest value.
# Example:
# SELECT MIN(salary)
# FROM employees;




# Subqueries: A subquery is simply a query written inside another query.
# Example:
# SELECT *
# FROM employees
# WHERE salary >
# (
# SELECT AVG(salary)
# FROM employees
# );
# Read it like: "Find employees earning more than the average salary."




