# 4. Top Interview Questions & Answers:

# Question 1. Retrieve all active students older than 22.
# Explanation: The interviewer wants to see if you know how to filter using multiple conditions.
# SQL
# SELECT *
# FROM students
# WHERE age > 22
# AND is_active = TRUE;


# Question 2. A student's email changed. Update only that student.
# Explanation: Tests whether you understand UPDATE with WHERE.
# SQL
# UPDATE students
# SET email = 'newemail@example.com'
# WHERE id = 1;
# Without WHERE, every student's email would be updated.


# Question 3. Remove the student named Rahul.
# Explanation: Tests DELETE with a filtering condition.
# SQL
# DELETE
# FROM students
# WHERE name = 'Rahul';


# Q4. Difference between DELETE, DROP, and TRUNCATE?
# Answer: 
# DELETE: Removes selected rows (can use WHERE; generally can be rolled back inside a transaction).
# TRUNCATE: Removes all rows quickly, keeps the table structure.
# DROP: Deletes the entire table including its structure.


# Q5. What is a Primary Key?
# Answer: A Primary Key uniquely identifies each row in a table. 
# It cannot contain duplicate or NULL values.
# Example: id INTEGER PRIMARY KEY


# Q6. What is the difference between WHERE and HAVING?
# Answer:
# WHERE filters rows before grouping.
# HAVING filters groups after GROUP BY.





# Backend Connection 
# Every backend application performs these operations constantly:
# User Registration → INSERT
# User Login → SELECT
# Update Profile → UPDATE
# Delete Account → DELETE
# For example, when someone signs up on your future FastAPI application:

# Frontend Form
#       │
#       ▼
# FastAPI Endpoint
#       │
#       ▼
# INSERT INTO users (...)
#       │
#       ▼
# PostgreSQL Database
#       │
#       ▼
# Success Response → Frontend