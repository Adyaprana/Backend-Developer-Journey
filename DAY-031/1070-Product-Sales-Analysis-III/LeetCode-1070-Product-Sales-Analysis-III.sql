
-- 1070. Product Sales Analysis III

-- Table: Sales
-- +-------------+-------+
-- | Column Name | Type  |
-- +-------------+-------+
-- | sale_id     | int   |
-- | product_id  | int   |
-- | year        | int   |
-- | quantity    | int   |
-- | price       | int   |
-- +-------------+-------+
-- (sale_id, year) is the primary key (combination of columns with unique values) of this table.
-- Each row records a sale of a product in a given year.
-- A product may have multiple sales entries in the same year.
-- Note that the per-unit price.

-- Write a solution to find all sales that occurred in the first year each product was sold.
-- For each product_id, identify the earliest year it appears in the Sales table.
-- Return all sales entries for that product in that year.
-- Return a table with the following columns: product_id, first_year, quantity, and price.
-- Return the result in any order.

-- Example 1:
-- Input: 
-- Sales table:
-- +---------+------------+------+----------+-------+
-- | sale_id | product_id | year | quantity | price |
-- +---------+------------+------+----------+-------+
-- | 1       | 100        | 2008 | 10       | 5000  |
-- | 2       | 100        | 2009 | 12       | 5000  |
-- | 7       | 200        | 2011 | 15       | 9000  |
-- +---------+------------+------+----------+-------+
-- Output: 
-- +------------+------------+----------+-------+
-- | product_id | first_year | quantity | price |
-- +------------+------------+----------+-------+
-- | 100        | 2008       | 10       | 5000  |
-- | 200        | 2011       | 15       | 9000  |
-- +------------+------------+----------+-------+





-- ═══════════════════════════════════════════════════════════════
-- LeetCode #1070 — Product Sales Analysis III
-- Difficulty: Easy | Status: ✅ Accepted (10/10 test cases)
-- Runtime: 944ms | Memory: 0.00 MB
-- Topic: Subquery + GROUP BY + JOIN
-- ═══════════════════════════════════════════════════════════════

-- Problem:
-- Find each product's first sale year,
-- along with its quantity and price.

-- Setup
DROP TABLE IF EXISTS Sales;

CREATE TABLE Sales (
    sale_id INT PRIMARY KEY,
    product_id INT,
    year INT,
    quantity INT,
    price INT
);

INSERT INTO Sales VALUES
(1,100,2008,10,5000),
(2,100,2009,12,5000),
(7,200,2011,15,9000);

-- View table
SELECT * FROM Sales;

-- SOLUTION
-- Step 1:
-- Find the first sale year for each product.
--
-- Step 2:
-- Join that result back with the Sales table
-- to get quantity and price.

SELECT
    s.product_id,
    f.first_year,
    s.quantity,
    s.price
FROM Sales s
JOIN
(
    SELECT
        product_id,
        MIN(year) AS first_year
    FROM Sales
    GROUP BY product_id
) AS f
ON s.product_id = f.product_id
AND s.year = f.first_year;

-- Why Subquery?
-- It finds the earliest sale year for every product.

-- Why JOIN?
-- The subquery only knows the first year.
-- Quantity and price are stored in the original table.

-- Visualization
--
-- Sales
--
-- Product | Year
-- 100     | 2008
-- 100     | 2009
-- 200     | 2011
--
-- Subquery
--
-- Product | First Year
-- 100     | 2008
-- 200     | 2011
--
-- Join Result
--
-- Product | Year | Qty | Price
-- 100     |2008  |10   |5000
-- 200     |2011  |15   |9000

-- Expected Output
--
-- product_id | first_year | quantity | price
-- -----------+------------+----------+------
-- 100        | 2008       | 10       | 5000
-- 200        | 2011       | 15       | 9000




