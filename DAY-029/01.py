# PostgreSQL + pgAdmin Installation (Brief Concept)

# PostgreSQL is one of the world's most popular open-source relational database management systems (RDBMS). 
# It stores application data in tables and supports advanced features like 
# transactions, indexing, JSON, stored procedures, and ACID compliance.

# pgAdmin is a graphical interface for PostgreSQL. 
# Instead of writing commands only in the terminal, 
# pgAdmin lets you create databases, tables, run SQL queries, 
# and manage your server visually.

# Why Backend Developers Use PostgreSQL: 
# Fast and reliable
# Free & open source
# Used by startups and enterprise companies
# Excellent with Python (FastAPI, Django, SQLAlchemy)
# Supports millions of records efficiently

# What is a Database?
# A database is an organized collection of data.
# Example: Instead of storing users in a Python list:
users = [
    {"name": "Adyaprana"},
    {"name": "Rahul"}
]
# A real application stores them permanently inside PostgreSQL.
# Without a database: Data disappears when the program stops.
# With PostgreSQL: Data stays permanently.



# What is a Table: (like an Excel sheet)
# | id | name      | age |
# | -- | --------- | --- |
# | 1  | Adyaprana | 23  |
# | 2  | Rahul     | 24  |
# A table stores similar types of information.
# Examples: Users, Orders, Products, Employees



# What is a Database Schema: 
# A schema is the structure or blueprint of your database. 
# It defines: Tables, Columns, Data types, Constraints, Relationships
# Think of it like the architectural blueprint of a building.




# CREATE TABLE:
# CREATE TABLE creates a new table.
# Example:
# CREATE TABLE students (
    # id INTEGER,
    # name VARCHAR(100)
# );
# Without CREATE TABLE, there is nowhere to store data.





# DROP TABLE
# Deletes an entire table permanently.
# DROP TABLE students;
# Everything inside the table is deleted.





# ALTER TABLE:
# Changes an existing table.
# Examples:
# Add column
# Remove column
# Rename column
# Change datatype
# Example:
# ALTER TABLE students
# ADD COLUMN email VARCHAR(100);





# VARCHAR: Stores short text.
# Examples: Name, City, Email, VARCHAR(100)
# Maximum 100 characters.





# INTEGER: Stores whole numbers.
# Examples: Age, Marks, Salary, Product Quantity, INTEGER





# BOOLEAN: 
# Stores only: TRUE or FALSE
# Examples:
# is_active
# is_verified
# is_admin





# TIMESTAMP: Stores date and time.
# Example: 2026-06-21 10:45:30
# Used for: Created Date, Login Time, Updated Time





# TEXT: Stores long text.
# Used for: Description, Blog Content, Comments, Product Details
# Unlike VARCHAR, there is no practical length limit.





# INSERT INTO: Adds new records.
# Example: INSERT INTO students
# VALUES (...);
# Every new user registration uses INSERT.





# SELECT: Retrieves data.
# SELECT * FROM students;
# This is the most commonly used SQL command.




# WHERE Clause: Filters records.
# Example:
# SELECT *
# FROM students
# WHERE age > 20;
# Without WHERE: All rows are returned.





# UPDATE: Changes existing data.
# UPDATE students
# SET age = 25
# WHERE id = 1;





# DELETE: Removes records.
# DELETE
# FROM students
# WHERE id = 1;
# Without WHERE: Everything gets deleted.




