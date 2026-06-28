-- ═══════════════════════════════════════════════════════════════
-- LeetCode #596 — Classes With at Least 5 Students
-- Difficulty: Easy | Status: ✅ Accepted (11/11 test cases)
-- Runtime: 295ms | Memory: 0.00 MB | Beats memory: 100%
-- ═══════════════════════════════════════════════════════════════

-- Problem:
-- Find all classes that have at least five students enrolled.

-- Setup
DROP TABLE IF EXISTS Courses;

CREATE TABLE Courses (
    student VARCHAR(50),
    class VARCHAR(50)
);

INSERT INTO Courses (student, class) VALUES
('A','Math'),
('B','English'),
('C','Math'),
('D','Biology'),
('E','Math'),
('F','Computer'),
('G','Math'),
('H','Math'),
('I','Math');

-- View table
SELECT * FROM Courses;

-- SOLUTION:
-- GROUP BY creates one group for each class.
-- COUNT(student) counts how many students are in each class.
-- HAVING filters the grouped results.

SELECT
    class
FROM Courses
GROUP BY class
HAVING COUNT(student) >= 5;

-- Why GROUP BY?
-- We need to count students for EACH class.

-- Why HAVING?
-- HAVING filters grouped (aggregated) data.
-- WHERE filters individual rows before grouping.

-- GROUP BY Visualization
--
-- Math
-- ----
-- A
-- C
-- E
-- G
-- H
-- I
--
-- COUNT(student)
-- = 6
--
-- HAVING
-- 6 >= 5
--
-- Return:
-- Math

-- Expected Output:
--
-- class
-- -----
-- Math