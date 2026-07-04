
-- Count total customers.
select count(*) as total_customer
FROM customers;

-- Count total orders.
select count(*) as total_order
from orders;

-- Find highest order amount.
select MAX(amount) 
from orders;

-- Find lowest order amount.
select MIN(amount)
from orders;

-- Find average order amount.
select avg(amount)
from orders;

-- Sort customers alphabetically.
select * from customers
ORDER BY customer_name ASC;

-- Display top 3 highest orders.
select * from orders
order by amount DESC LIMIT 3;

-- Display last 2 orders using OFFSET.
select * from orders
limit 2 offset 8;

-- Find total revenue.
select sum(amount) as revenue
from orders;

-- Count orders placed in January.
select count(*) as january_order
from orders
WHERE EXTRACT(MONTH FROM order_date) = 1;

-- Find customer with maximum total purchase.
SELECT 
    customer_id, 
    SUM(amount) AS total_spent
FROM orders
GROUP BY customer_id
ORDER BY total_spent DESC
LIMIT 1;

-- Find customer with minimum total purchase.
SELECT 
    customer_id, 
    SUM(amount) AS total_spent
FROM orders
GROUP BY customer_id
ORDER BY total_spent asc
LIMIT 1 ;

-- Show customers having more than one order.
SELECT 
    customer_id, 
    COUNT(order_id) AS total_order
FROM orders
GROUP BY customer_id
HAVING COUNT(order_id) > 1
ORDER BY total_order DESC;

-- Show monthly revenue.
select 
date_trunc('month',order_date) as month,
sum(amount) as revenue
from orders
group by month
order by month;

-- Find customers whose purchase is above average.
select * from orders
where amount > (select avg(amount) from orders);

-- Find customers with total sales between ₹1000 and ₹2000.
SELECT 
    customer_id, 
    SUM(amount) AS total_spent
FROM orders
GROUP BY customer_id
HAVING SUM(amount) BETWEEN 1000 AND 2000
ORDER BY total_spent DESC;

-- Show top 3 customers by revenue.
SELECT 
    customer_id, 
    SUM(amount) AS total_spent
FROM orders
GROUP BY customer_id
order by total_spent desc
limit 3;

-- Show bottom 2 customers by revenue.
SELECT 
    customer_id, 
    SUM(amount) AS total_spent
FROM orders
GROUP BY customer_id
order by total_spent asc
limit 2;

-- Find the month with highest revenue.
SELECT
DATE_TRUNC('month',order_date) AS month,
SUM(amount) AS revenue
FROM orders
GROUP BY month
order by revenue desc
limit 1;

-- Find average purchase per customer.
SELECT 
    customer_id, 
    avg(amount) AS average_spent
FROM orders
GROUP BY customer_id
order by average_spent desc
