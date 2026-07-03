-- 181. Employees Earning More Than Their Managers

-- Table: Employee
-- +-------------+---------+
-- | Column Name | Type    |
-- +-------------+---------+
-- | id          | int     |
-- | name        | varchar |
-- | salary      | int     |
-- | managerId   | int     |
-- +-------------+---------+
-- id is the primary key (column with unique values) for this table.
-- Each row of this table indicates the ID of an employee, their name, salary, and the ID of their manager.

-- Write a solution to find the employees who earn more than their managers.
-- Return the result table in any order.
-- The result format is in the following example.

-- Example 1:
-- Input: 
-- Employee table:
-- +----+-------+--------+-----------+
-- | id | name  | salary | managerId |
-- +----+-------+--------+-----------+
-- | 1  | Joe   | 70000  | 3         |
-- | 2  | Henry | 80000  | 4         |
-- | 3  | Sam   | 60000  | Null      |
-- | 4  | Max   | 90000  | Null      |
-- +----+-------+--------+-----------+
-- Output: 
-- +----------+
-- | Employee |
-- +----------+
-- | Joe      |
-- +----------+
-- Explanation: Joe is the only employee who earns more than his manager.


-- Create Table
CREATE TABLE Employee (
    id INT PRIMARY KEY,
    name VARCHAR(255),
    salary INT,
    managerId INT
);

--  Insert Sample Data
INSERT INTO Employee (id, name, salary, managerId)
VALUES
(1,'Joe',70000,3),
(2,'Henry',80000,4),
(3,'Sam',60000,NULL),
(4,'Max',90000,NULL);

-- View Data
SELECT * FROM Employee;

--  My Solution
SELECT
    e2.name AS Employee
FROM Employee e1
JOIN Employee e2
ON e1.id = e2.managerId
WHERE e1.salary < e2.salary;