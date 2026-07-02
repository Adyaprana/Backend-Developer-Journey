# 3. Important Things to Know

# 1. Never Forget WHERE in UPDATE
# Wrong:
# UPDATE students
# SET age = 30;
# Result: Every student's age becomes 30.

# Correct: 
# UPDATE students
# SET age = 30
# WHERE id = 1;




# 2. Never Forget WHERE in DELETE
# Wrong:
# DELETE FROM students;
# Everything is deleted.

# Correct:
# DELETE FROM students
# WHERE id = 2;




# 3. VARCHAR vs TEXT
# VARCHAR
# VARCHAR(100)
# Best for: Names, Emails, Phone Numbers

# TEXT -> # Unlimited length.
# Best for: Articles, Product Description, User Bio





# 4. PRIMARY KEY Must Be Unique
# Bad: 
# ID 1, 1
# Not allowed.
# Good: 1, 2, 3,




# 5. SELECT * Is Fine for Learning
# In production:
# Instead of:
# SELECT *
# Prefer:
# SELECT
# name,
# age
# This improves readability and can reduce unnecessary data transfer.





# SQL Execution Order
# Although you write queries in this order:
# SELECT
# FROM
# WHERE
# SQL logically processes them as:
# FROM
# WHERE
# SELECT
# Understanding this helps when queries become more complex.