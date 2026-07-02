-- DAY 29 - PostgreSQL SQL Fundamentals

-- Drop table if it already exists
DROP TABLE IF EXISTS students;


-- Create table
CREATE TABLE students (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100),
    age INTEGER,
    is_active BOOLEAN,
    created_at TIMESTAMP,
    description TEXT
);


-- Insert records
INSERT INTO students
(id, name, age, is_active, created_at, description)
VALUES
(1,'Adyaprana',23,TRUE,NOW(),'Backend Developer'),
(2,'Rahul',24,TRUE,NOW(),'Python Developer'),
(3,'Priya',22,FALSE,NOW(),'Frontend Developer'),
(4,'Ankit',25,TRUE,NOW(),'DevOps Engineer');


-- SELECT ALL
SELECT *
FROM students;


-- - WHERE
SELECT *
FROM students
WHERE age > 22;


-- WHERE BOOLEAN
SELECT *
FROM students
WHERE is_active = TRUE;


-- WHERE VARCHAR
SELECT *
FROM students
WHERE name = 'Rahul';


-- UPDATE
UPDATE students
SET age = 26
WHERE id = 4;

-- VERIFY UPDATE
SELECT *
FROM students
WHERE id = 4;


-- DELETE
DELETE
FROM students
WHERE id = 3;

-- VERIFY DELETE
SELECT *
FROM students;


-- ALTER TABLE
ALTER TABLE students
ADD COLUMN email VARCHAR(150);


-- UPDATE NEW COLUMN
UPDATE students
SET email = 'adyaprana@example.com'
WHERE id = 1;

-- FINAL OUTPUT
SELECT *
FROM students;