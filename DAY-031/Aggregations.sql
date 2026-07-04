
-- DAY 31 SQL PRACTICE
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS customers;

CREATE TABLE customers(
    customer_id SERIAL PRIMARY KEY,
    customer_name VARCHAR(100),
    city VARCHAR(50)
);
CREATE TABLE orders(
    order_id SERIAL PRIMARY KEY,
    customer_id INT REFERENCES customers(customer_id),
    order_date DATE,
    amount NUMERIC(10,2)
);

INSERT INTO customers(customer_name,city)
VALUES
('Adyaprana','Bangalore'),
('Rahul','Delhi'),
('Priya','Mumbai'),
('Amit','Kolkata'),
('Sneha','Chennai');
INSERT INTO orders(customer_id,order_date,amount)
VALUES
(1,'2026-01-02',500),
(1,'2026-01-08',700),
(1,'2026-02-01',1800),
(2,'2026-01-05',900),
(2,'2026-03-01',1200),
(3,'2026-02-11',300),
(3,'2026-02-25',450),
(4,'2026-03-04',600),
(4,'2026-03-10',400),
(5,'2026-01-12',1000);


-- View Customers
SELECT * FROM customers;


-- View Orders
SELECT * FROM orders;



-- COUNT
SELECT COUNT(*) AS total_orders
FROM orders;


-- SUM
SELECT SUM(amount) AS revenue
FROM orders;


-- AVG
SELECT AVG(amount) AS average_order
FROM orders;


-- MAX
SELECT MAX(amount)
FROM orders;


-- MIN
SELECT MIN(amount)
FROM orders;


-- GROUP BY
SELECT
customer_id,
COUNT(*) AS total_orders
FROM orders
GROUP BY customer_id;


-- HAVING
SELECT
customer_id,
COUNT(*) AS total_orders
FROM orders
GROUP BY customer_id
HAVING COUNT(*) >=2;


-- ORDER BY
SELECT *
FROM orders
ORDER BY amount DESC;


-- LIMIT
SELECT *
FROM orders
ORDER BY amount DESC
LIMIT 5;


-- OFFSET
SELECT *
FROM orders
ORDER BY amount DESC
LIMIT 3
OFFSET 2;


-- TOP 5 CUSTOMERS
SELECT
customer_id,
SUM(amount) AS total_sales
FROM orders
GROUP BY customer_id
ORDER BY total_sales DESC
LIMIT 5;


-- MONTHLY REVENUE
SELECT
DATE_TRUNC('month',order_date) AS month,
SUM(amount) AS revenue
FROM orders
GROUP BY month
ORDER BY month;


-- SUBQUERY
SELECT *
FROM orders
WHERE amount >
(
SELECT AVG(amount)
FROM orders
);