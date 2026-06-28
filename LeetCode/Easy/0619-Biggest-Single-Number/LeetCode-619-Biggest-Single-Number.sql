
-- Table: MyNumbers
-- +-------------+------+
-- | Column Name | Type |
-- +-------------+------+
-- | num         | int  |
-- +-------------+------+
-- This table may contain duplicates (In other words, there is no primary key for this table in SQL).
-- Each row of this table contains an integer.

-- A single number is a number that appeared only once in the MyNumbers table.
-- Find the largest single number. If there is no single number, report null.
-- The result format is in the following example.

-- Example 1:
-- Input: 
-- MyNumbers table:
-- +-----+
-- | num |
-- +-----+
-- | 8   |
-- | 8   |
-- | 3   |
-- | 3   |
-- | 1   |
-- | 4   |
-- | 5   |
-- | 6   |
-- +-----+
-- Output: 
-- +-----+
-- | num |
-- +-----+
-- | 6   |
-- +-----+
-- Explanation: The single numbers are 1, 4, 5, and 6.
-- Since 6 is the largest single number, we return it.

-- Example 2:
-- Input: 
-- MyNumbers table:
-- +-----+
-- | num |
-- +-----+
-- | 8   |
-- | 8   |
-- | 7   |
-- | 7   |
-- | 3   |
-- | 3   |
-- | 3   |
-- +-----+
-- Output: 
-- +------+
-- | num  |
-- +------+
-- | null |
-- +------+
-- Explanation: There are no single numbers in the input table so we return null.



-- ═══════════════════════════════════════════════════════════════
-- LeetCode #619 — Biggest Single Number
-- Difficulty: Easy | Status: ✅ Accepted (18/18 test cases)
-- Runtime: 201 ms | Memory: 0.00 MB
-- Topic: GROUP BY + HAVING + MAX() + Subquery
-- ═══════════════════════════════════════════════════════════════

-- Problem:
-- Find the largest number that appears exactly once.
-- If no such number exists, return NULL.

-- Setup
DROP TABLE IF EXISTS MyNumbers;

CREATE TABLE MyNumbers (
    num INT
);

INSERT INTO MyNumbers VALUES
(8),
(8),
(3),
(3),
(1),
(4),
(5),
(6),
(6);

-- View table
SELECT * FROM MyNumbers;

-- SOLUTION
-- Step 1:
-- GROUP BY each number.
--
-- Step 2:
-- Keep only numbers appearing once.
--
-- Step 3:
-- Find the largest unique number.
--
-- MAX() automatically returns NULL
-- if no unique number exists.

SELECT
    MAX(num) AS num
FROM
(
    SELECT
        num
    FROM MyNumbers
    GROUP BY num
    HAVING COUNT(*) = 1
) AS unique_numbers;

-- Why GROUP BY?
-- To count how many times each number appears.

-- Why HAVING?
-- To keep only numbers with exactly one occurrence.

-- Why MAX()?
-- To return the largest unique number.
-- If there are no unique numbers,
-- MAX() returns NULL automatically.

-- Visualization
--
-- Original
--
-- 8
-- 8
-- 3
-- 3
-- 1
-- 4
-- 5
-- 6
-- 6
--
-- GROUP BY
--
-- Number | Count
-- -------+------
-- 1      | 1
-- 3      | 2
-- 4      | 1
-- 5      | 1
-- 6      | 2
-- 8      | 2
--
-- HAVING COUNT(*) = 1
--
-- 1
-- 4
-- 5
--
-- MAX()
--
-- 5

-- Special Case
--
-- 1
-- 1
-- 2
-- 2
--
-- HAVING
--
-- Empty
--
-- MAX()
--
-- NULL

-- Expected Output
--
-- num
-- ---
-- 5