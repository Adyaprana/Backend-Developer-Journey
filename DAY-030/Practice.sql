
-- Practice Questions

-- Show all products purchased by Adyaprana.
SELECT
    users.name,
    orders.product
FROM users
INNER JOIN orders
ON users.id = orders.user_id
WHERE users.name = 'Adyaprana';


-- Find orders that don't belong to any user.
SELECT
orders.order_id,
orders.product
FROM users
RIGHT JOIN orders
ON users.id = orders.user_id
WHERE users.id IS NULL;


-- List every employee with their manager's name.
SELECT 
e.employee_name AS Employee,
m.employee_name AS Manager
FROM employees e
LEFT JOIN employees m
ON e.manager_id = m.emp_id;

-- Add a new user with no orders and verify they appear only in the LEFT JOIN.
INSERT INTO users VALUES
(7,'David','LA');
SELECT * FROM users;
SELECT
users.name,
orders.product
FROM users
LEFT JOIN orders
ON users.id = orders.user_id;


-- Add an order with a non-existent user_id and verify it appears in the RIGHT JOIN.
INSERT INTO orders VALUES
(109,9,'TV',40000);
SELECT * FROM orders;
SELECT
users.name,
orders.product
FROM users
RIGHT JOIN orders
ON users.id = orders.user_id;
