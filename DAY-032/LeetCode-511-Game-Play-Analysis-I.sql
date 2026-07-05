
-- 511. Game Play Analysis I
-- Table: Activity

-- +--------------+---------+
-- | Column Name  | Type    |
-- +--------------+---------+
-- | player_id    | int     |
-- | device_id    | int     |
-- | event_date   | date    |
-- | games_played | int     |
-- +--------------+---------+
-- (player_id, event_date) is the primary key (combination of columns with unique values) of this table.
-- This table shows the activity of players of some games.
-- Each row is a record of a player who logged in and played a number of games (possibly 0) before logging out on someday using some device.

-- Write a solution to find the first login date for each player.
-- Return the result table in any order.
-- The result format is in the following example.

-- Example 1:
-- Input: 
-- Activity table:
-- +-----------+-----------+------------+--------------+
-- | player_id | device_id | event_date | games_played |
-- +-----------+-----------+------------+--------------+
-- | 1         | 2         | 2016-03-01 | 5            |
-- | 1         | 2         | 2016-05-02 | 6            |
-- | 2         | 3         | 2017-06-25 | 1            |
-- | 3         | 1         | 2016-03-02 | 0            |
-- | 3         | 4         | 2018-07-03 | 5            |
-- +-----------+-----------+------------+--------------+
-- Output: 
-- +-----------+-------------+
-- | player_id | first_login |
-- +-----------+-------------+
-- | 1         | 2016-03-01  |
-- | 2         | 2017-06-25  |
-- | 3         | 2016-03-02  |
-- +-----------+-------------+






-- ═══════════════════════════════════════════════════════════════
-- LeetCode #511 — Game Play Analysis I
-- Difficulty: Easy | Status: ✅ Accepted (12/12 test cases)
-- Runtime: 2457ms | Memory: 0.00 MB
-- Topic: GROUP BY + MIN()
-- ═══════════════════════════════════════════════════════════════

-- Problem:
-- Find the first login date for every player.

-- Setup
DROP TABLE IF EXISTS Activity;

CREATE TABLE Activity (
    player_id INT,
    device_id INT,
    event_date DATE,
    games_played INT,
    PRIMARY KEY (player_id, event_date)
);

INSERT INTO Activity VALUES
(1,2,'2016-03-01',5),
(1,2,'2016-05-02',6),
(2,3,'2017-06-25',1),
(3,1,'2016-03-02',0),
(3,4,'2018-07-03',5);

-- View table
SELECT * FROM Activity;

-- SOLUTION
-- GROUP BY creates one group per player.
-- MIN() finds the earliest login date.

SELECT
    player_id,
    MIN(event_date) AS first_login
FROM Activity
GROUP BY player_id;

-- Why GROUP BY?
-- One result is required for each player.

-- Why MIN()?
-- It returns the earliest login date.

-- Visualization
--
-- Player 1
-- 2016-03-01
-- 2016-05-02
--
-- MIN()
-- 2016-03-01
--
-- Player 2
-- 2017-06-25
--
-- MIN()
-- 2017-06-25
--
-- Player 3
-- 2016-03-02
-- 2018-07-03
--
-- MIN()
-- 2016-03-02

-- Expected Output
--
-- player_id | first_login
-- ----------+------------
--     1     | 2016-03-01
--     2     | 2017-06-25
--     3     | 2016-03-02