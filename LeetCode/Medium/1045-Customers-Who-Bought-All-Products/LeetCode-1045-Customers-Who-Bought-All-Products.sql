

-- 1045. Customers Who Bought All Products

-- Table: Customer
-- +-------------+---------+
-- | Column Name | Type    |
-- +-------------+---------+
-- | customer_id | int     |
-- | product_key | int     |
-- +-------------+---------+
-- This table may contain duplicates rows. 
-- customer_id is not NULL.
-- product_key is a foreign key (reference column) to Product table.

-- Table: Product
-- +-------------+---------+
-- | Column Name | Type    |
-- +-------------+---------+
-- | product_key | int     |
-- +-------------+---------+
-- product_key is the primary key (column with unique values) for this table.

-- Write a solution to report the customer ids from the Customer table that bought all the products in the Product table.
-- Return the result table in any order.
-- The result format is in the following example.

-- Example 1:
-- Input: 
-- Customer table:
-- +-------------+-------------+
-- | customer_id | product_key |
-- +-------------+-------------+
-- | 1           | 5           |
-- | 2           | 6           |
-- | 3           | 5           |
-- | 3           | 6           |
-- | 1           | 6           |
-- +-------------+-------------+
-- Product table:
-- +-------------+
-- | product_key |
-- +-------------+
-- | 5           |
-- | 6           |
-- +-------------+
-- Output: 
-- +-------------+
-- | customer_id |
-- +-------------+
-- | 1           |
-- | 3           |
-- +-------------+
-- Explanation: 
-- The customers who bought all the products (5 and 6) are customers with IDs 1 and 3.



-- ═══════════════════════════════════════════════════════════════
-- LeetCode #1045 — Customers Who Bought All Products
-- Difficulty: Medium | Status: ✅ Accepted (9/9 test cases)
-- Runtime: 473ms | Memory: 0.00 MB | Beats runtime: 97.91%
-- Topic: COUNT(DISTINCT) + GROUP BY + HAVING + Subquery
-- ═══════════════════════════════════════════════════════════════

-- Problem:
-- Find customers who purchased every product listed
-- in the Product table.

-- Setup
DROP TABLE IF EXISTS Customer;
DROP TABLE IF EXISTS Product;

CREATE TABLE Product (
    product_key INT PRIMARY KEY
);

CREATE TABLE Customer (
    customer_id INT,
    product_key INT
);

INSERT INTO Product VALUES
(5),
(6);

INSERT INTO Customer VALUES
(1,5),
(1,6),
(2,5),
(3,5),
(3,6);

-- View tables
SELECT * FROM Product;
SELECT * FROM Customer;
SELECT
    customer_id
FROM Customer
GROUP BY customer_id
HAVING COUNT(DISTINCT product_key) =
(
    SELECT COUNT(*)
    FROM Product
);

-- Why COUNT(DISTINCT)?
-- A customer may purchase the same product multiple times.
-- DISTINCT ensures each product is counted only once.

-- Why Subquery?
-- We need the total number of available products.

-- Visualization
--
-- Customer
--
-- 1 → 5,6
-- COUNT(DISTINCT)=2
--
-- 2 → 5
-- COUNT(DISTINCT)=1
--
-- 3 → 5,6
-- COUNT(DISTINCT)=2
--
-- Product
--
-- 5
-- 6
--
-- COUNT(*) = 2
--
-- Comparison
--
-- 2 = 2 ✅
-- 1 = 2 ❌
-- 2 = 2 ✅

-- Expected Output
--
-- customer_id
-- -----------
-- 1
-- 3