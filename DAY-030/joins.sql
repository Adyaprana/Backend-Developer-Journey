
-- DAY 30 : SQL JOINS
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS employees;
DROP TABLE IF EXISTS users;


-- USERS TABLE
CREATE TABLE users(
    id INTEGER PRIMARY KEY,
    name VARCHAR(100),
    city VARCHAR(100)
);


-- ORDERS TABLE
CREATE TABLE orders(
    order_id INTEGER PRIMARY KEY,
    user_id INTEGER,
    product VARCHAR(100),
    amount INTEGER
);


-- EMPLOYEES TABLE
CREATE TABLE employees(
    emp_id INTEGER PRIMARY KEY,
    employee_name VARCHAR(100),
    manager_id INTEGER
);


-- INSERT USERS
INSERT INTO users VALUES
(1,'Adyaprana','Bangalore'),
(2,'Rahul','Delhi'),
(3,'Priya','Mumbai'),
(4,'Ankit','Pune');


-- INSERT ORDERS
INSERT INTO orders VALUES
(101,1,'Laptop',80000),
(102,1,'Mouse',1200),
(103,2,'Keyboard',2500),
(104,5,'Monitor',15000);


-- INSERT EMPLOYEES
INSERT INTO employees VALUES
(1,'CEO',NULL),
(2,'Manager',1),
(3,'Developer A',2),
(4,'Developer B',2);


-- VIEW TABLES
SELECT * FROM users;
SELECT * FROM orders;
SELECT * FROM employees;


-- INNER JOIN
SELECT
users.id,
users.name,
orders.product,
orders.amount
FROM users
INNER JOIN orders
ON users.id = orders.user_id;


-- LEFT JOIN
SELECT
users.name,
orders.product
FROM users
LEFT JOIN orders
ON users.id = orders.user_id;


-- RIGHT JOIN
SELECT
users.name,
orders.product
FROM users
RIGHT JOIN orders
ON users.id = orders.user_id;


-- FULL OUTER JOIN
SELECT
users.name,
orders.product
FROM users
FULL OUTER JOIN orders
ON users.id = orders.user_id;


-- SELF JOIN
SELECT
e.employee_name AS Employee,
m.employee_name AS Manager
FROM employees e
LEFT JOIN employees m
ON e.manager_id = m.emp_id;


-- USERS WHO HAVE ORDERS
SELECT
users.name,
orders.product
FROM users
INNER JOIN orders
ON users.id = orders.user_id;


-- USERS WITHOUT ORDERS
SELECT
users.name
FROM users
LEFT JOIN orders
ON users.id = orders.user_id
WHERE orders.order_id IS NULL;


-- ORDERS WITHOUT USERS
SELECT
orders.order_id,
orders.product
FROM users
RIGHT JOIN orders
ON users.id = orders.user_id
WHERE users.id IS NULL;



