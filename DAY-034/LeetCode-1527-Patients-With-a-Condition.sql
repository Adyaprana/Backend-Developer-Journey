
-- LeetCode 1527 Patients With a Condition

-- Table: Patients
-- +--------------+---------+
-- | Column Name  | Type    |
-- +--------------+---------+
-- | patient_id   | int     |
-- | patient_name | varchar |
-- | conditions   | varchar |
-- +--------------+---------+
-- patient_id is the primary key (column with unique values) for this table.
-- 'conditions' contains 0 or more code separated by spaces. 
-- This table contains information of the patients in the hospital.

-- Write a solution to find the patient_id, patient_name, and conditions of the patients who have Type I Diabetes. Type I Diabetes always starts with DIAB1 prefix.
-- Return the result table in any order.
-- The result format is in the following example.


-- Example 1:
-- Input: 
-- Patients table:
-- +------------+--------------+--------------+
-- | patient_id | patient_name | conditions   |
-- +------------+--------------+--------------+
-- | 1          | Daniel       | YFEV COUGH   |
-- | 2          | Alice        |              |
-- | 3          | Bob          | DIAB100 MYOP |
-- | 4          | George       | ACNE DIAB100 |
-- | 5          | Alain        | DIAB201      |
-- +------------+--------------+--------------+
-- Output: 
-- +------------+--------------+--------------+
-- | patient_id | patient_name | conditions   |
-- +------------+--------------+--------------+
-- | 3          | Bob          | DIAB100 MYOP |
-- | 4          | George       | ACNE DIAB100 | 
-- +------------+--------------+--------------+
-- Explanation: Bob and George both have a condition that starts with DIAB1.


-- ═══════════════════════════════════════════════════════════════
-- LeetCode #1527 — Patients With a Condition
-- Difficulty: Easy | Status: ✅ Accepted (17/17 test cases)
-- Runtime: 216 ms | Memory: 0.00 MB
-- Topic: LIKE + Wildcards (%)
-- ═══════════════════════════════════════════════════════════════

-- Problem:
-- Find all patients whose conditions include
-- the Type I Diabetes code (DIAB1).

-- Setup
DROP TABLE IF EXISTS Patients;

CREATE TABLE Patients (
    patient_id INT PRIMARY KEY,
    patient_name VARCHAR(100),
    conditions VARCHAR(255)
);

INSERT INTO Patients VALUES
(1,'Daniel','YFEV COUGH'),
(2,'Alice','DIAB100 MYOP'),
(3,'Bob','ACNE DIAB100'),
(4,'George','DIAB201'),
(5,'Tom','FEVER');

-- View table
SELECT * FROM Patients;

-- SOLUTION
-- LIKE searches text patterns.
-- We check two cases:
-- 1. DIAB1 appears at the beginning.
-- 2. DIAB1 appears after a space.

SELECT
    patient_id,
    patient_name,
    conditions
FROM Patients
WHERE conditions LIKE 'DIAB1%'
   OR conditions LIKE '% DIAB1%';

-- Why two LIKE conditions?
--
-- DIAB100 MYOP
-- ↑ starts with DIAB1
--
-- ACNE DIAB100
--        ↑ appears after a space

-- Why not use:
--
-- LIKE '%DIAB1%'
--
-- Because it could match invalid strings
-- such as XXDIAB100.

-- Visualization
--
-- DIAB100 MYOP
-- ✔ LIKE 'DIAB1%'
--
-- ACNE DIAB100
-- ✔ LIKE '% DIAB1%'
--
-- DIAB201
-- ✘ Not matched
--
-- FEVER
-- ✘ Not matched

-- Expected Output
--
-- patient_id | patient_name | conditions
-- -----------+--------------+----------------
-- 2          | Alice        | DIAB100 MYOP
-- 3          | Bob          | ACNE DIAB100