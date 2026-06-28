

-- 610. Triangle Judgement

-- Table: Triangle
-- +-------------+------+
-- | Column Name | Type |
-- +-------------+------+
-- | x           | int  |
-- | y           | int  |
-- | z           | int  |
-- +-------------+------+
-- In SQL, (x, y, z) is the primary key column for this table.
-- Each row of this table contains the lengths of three line segments.

-- Report for every three line segments whether they can form a triangle.
-- Return the result table in any order.
-- The result format is in the following example.

-- Example 1:
-- Input: 
-- Triangle table:
-- +----+----+----+
-- | x  | y  | z  |
-- +----+----+----+
-- | 13 | 15 | 30 |
-- | 10 | 20 | 15 |
-- +----+----+----+
-- Output: 
-- +----+----+----+----------+
-- | x  | y  | z  | triangle |
-- +----+----+----+----------+
-- | 13 | 15 | 30 | No       |
-- | 10 | 20 | 15 | Yes      |
-- +----+----+----+----------+
 
-- ═══════════════════════════════════════════════════════════════
-- LeetCode #610 — Triangle Judgement
-- Difficulty: Easy | Status: ✅ Accepted (11/11 test cases)
-- Topic: CASE WHEN
-- ═══════════════════════════════════════════════════════════════

-- Problem:
-- Determine whether three side lengths can form a triangle.

-- Setup
DROP TABLE IF EXISTS Triangle;

CREATE TABLE Triangle (
    x INT,
    y INT,
    z INT
);

INSERT INTO Triangle VALUES
(13,15,30),
(10,20,15),
(7,8,10),
(5,6,12);

-- View table
SELECT * FROM Triangle;

-- SOLUTION
-- CASE works like an if-else statement.
-- Check all three triangle inequality conditions.

SELECT
    x,
    y,
    z,
    CASE
        WHEN x + y > z
         AND y + z > x
         AND x + z > y
        THEN 'Yes'
        ELSE 'No'
    END AS triangle
FROM Triangle;

-- Why CASE?
-- We don't want to remove rows.
-- We only classify each row as
-- "Yes" or "No".

-- Triangle Rule
--
-- x + y > z
-- y + z > x
-- x + z > y
--
-- All three conditions must be TRUE.

-- Visualization
--
-- (10,20,15)
--
-- 10+20 >15 ✔
-- 20+15 >10 ✔
-- 10+15 >20 ✔
--
-- Result
-- Yes
--
-- (13,15,30)
--
-- 13+15 >30 ✘
--
-- Result
-- No

-- Expected Output
--
-- x | y | z | triangle
-- --+---+---+----------
--13 |15 |30 | No
--10 |20 |15 | Yes
-- 7 | 8 |10 | Yes
-- 5 | 6 |12 | No