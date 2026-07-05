
# Interview Questions:

# Q1. What is a Primary Key?
# Answer: A Primary Key uniquely identifies every row in a table. It cannot be NULL or duplicated.

# Q2. Difference between Primary Key and Unique?
# Answer: 
# Primary Key: Only one per table, Cannot be NULL
# Unique: Multiple allowed, Usually allows NULL depending on the database

# Q3. What is a Foreign Key?
# Answer: A Foreign Key creates a relationship between two tables and enforces referential integrity.

# Q4. What is Referential Integrity?
# Answer: It ensures that foreign key values always reference existing rows in the parent table.

# Q5. What is NOT NULL?
# Answer: A constraint that prevents NULL values from being inserted.

# Q6. What is UNIQUE?
# Answer: A constraint that prevents duplicate values in a column.

# Q7. What is an Index?
# Answer: A database structure that speeds up data retrieval by avoiding full table scans.

# Q8. Do indexes make everything faster?
# Answer: No. They speed up reads (SELECT) but add overhead to writes (INSERT, UPDATE, DELETE).

# Q9. What is a One-to-Many relationship?
# Answer: One row in the parent table can relate to many rows in the child table (e.g., one user can have many orders).

# Q10. What is a Many-to-Many relationship?
# Answer: Many rows in one table relate to many rows in another. It is implemented using a junction table.

# Q11. What is a Schema?
# Answer: The logical structure of a database, including tables, columns, relationships, keys, and constraints.

# Q12. Why is database design important?
# Answer: Good database design reduces duplication, improves performance, ensures data integrity, and makes applications easier to maintain.