
-- 570. Managers with at Least 5 Direct Reports

-- Table: Employee
-- +-------------+---------+
-- | Column Name | Type    |
-- +-------------+---------+
-- | id          | int     |
-- | name        | varchar |
-- | department  | varchar |
-- | managerId   | int     |
-- +-------------+---------+
-- id is the primary key (column with unique values) for this table.
-- Each row of this table indicates the name of an employee, their department, and the id of their manager.
-- If managerId is null, then the employee does not have a manager.
-- No employee will be the manager of themself.

-- Write a solution to find managers with at least five direct reports.
-- Return the result table in any order.
-- The result format is in the following example.

-- Example 1:
-- Input: 
-- Employee table:
-- +-----+-------+------------+-----------+
-- | id  | name  | department | managerId |
-- +-----+-------+------------+-----------+
-- | 101 | John  | A          | null      |
-- | 102 | Dan   | A          | 101       |
-- | 103 | James | A          | 101       |
-- | 104 | Amy   | A          | 101       |
-- | 105 | Anne  | A          | 101       |
-- | 106 | Ron   | B          | 101       |
-- +-----+-------+------------+-----------+
-- Output: 
-- +------+
-- | name |
-- +------+
-- | John |
-- +------+




-- ═══════════════════════════════════════════════════════════════
-- LeetCode #570 — Managers with at Least 5 Direct Reports
-- Difficulty: Medium | Status: ✅ Accepted
-- Topic: Self JOIN + GROUP BY + HAVING
-- ═══════════════════════════════════════════════════════════════

-- Problem:
-- Find managers who have at least 5 direct reports.

-- Setup
DROP TABLE IF EXISTS Employee;

CREATE TABLE Employee (
    id INT PRIMARY KEY,
    name VARCHAR(50),
    department VARCHAR(50),
    managerId INT
);

INSERT INTO Employee VALUES
(101,'John','A',NULL),
(102,'Dan','A',101),
(103,'James','A',101),
(104,'Amy','A',101),
(105,'Anne','A',101),
(106,'Ron','B',101),
(107,'Sam','B',102);

-- View table
SELECT * FROM Employee;

-- SOLUTION:
-- Self JOIN employees with managers.
-- GROUP BY manager.
-- COUNT direct reports.
-- Keep only managers with at least 5 reports.

SELECT
    m.name AS name
FROM Employee e
JOIN Employee m
ON m.id = e.managerId
GROUP BY
    m.id,
    m.name
HAVING COUNT(*) >= 5;

-- Why SELF JOIN?
-- Manager and employee data are stored in the same table.

-- Why GROUP BY?
-- We need one group for each manager.

-- Why HAVING?
-- HAVING filters grouped results after COUNT().

-- Visualization
--
-- John
-- ├── Dan
-- ├── James
-- ├── Amy
-- ├── Anne
-- └── Ron
--
-- COUNT(*) = 5
--
-- HAVING 5 >= 5
--
-- Return:
-- John

-- Expected Output:
--
-- name
-- ----
-- John