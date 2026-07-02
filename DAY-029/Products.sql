
-- Step 1: Drop Existing Table
DROP TABLE IF EXISTS products;


-- Step 2:Create Product Table
CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    brand VARCHAR(50),
    category VARCHAR(50),
    price INTEGER,
    stock INTEGER,
    is_available BOOLEAN,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- Step 3: Insert Products
INSERT INTO products 
(product_id, product_name, brand, category, price, stock, is_available, description)
VALUES
(1,'iPhone 16','Apple','Mobile',89999,15,TRUE,'Apple flagship smartphone'),
(2,'Galaxy S25','Samsung','Mobile',79999,20,TRUE,'Samsung flagship smartphone'),
(3,'MacBook Air M4','Apple','Laptop',124999,8,TRUE,'Lightweight laptop'),
(4,'Dell XPS 15','Dell','Laptop',145000,5,TRUE,'Premium Windows laptop'),
(5,'Sennheiser Momentum 4','Sennheiser','Headphones',26989,5,TRUE,'Premium over-ear headphones'),
(6,'Sony WH-1000XM5','Sony','Headphones',29999,12,TRUE,'Noise cancelling headphones'),
(7,'Logitech MX Master 3S','Logitech','Mouse',9999,18,TRUE,'Wireless productivity mouse'),
(8,'HP Pavilion','HP','Laptop',65000,0,FALSE,'Out of stock laptop');


-- Step 4: View All Products
SELECT * FROM products;


-- Step 5: Select Only Product Name & Price
SELECT product_name, price
FROM products;


-- Step 6: Products Above ₹50,000
SELECT * from products
WHERE price > 50000;


-- Step 7: Available Products
SELECT * FROM products
WHERE is_available = TRUE;


-- Step 8: Apple Products
SELECT * FROM products
WHERE brand = 'Apple';


-- Step 9: Out Of Stock Products
SELECT * FROM products
WHERE is_available = FALSE;


-- Step 10: Headphones Only
SELECT * FROM products
WHERE category = 'Headphones';


-- Step 11: Update Price
UPDATE products
SET price = 34990
WHERE product_id = 5;

SELECT * FROM products
WHERE product_id = 5;


-- Step 12: Update Stock
UPDATE products
SET stock  = 21
WHERE product_id = 3;

SELECT * FROM products
WHERE product_id = 3;


-- Step 13: Mark Product Out Of Stock
UPDATE products
SET is_available = FALSE, stock = 0
WHERE product_id = 2;

SELECT * FROM products
WHERE product_id = 2;


-- Step 14: Delete One Product
DELETE FROM products
WHERE product_id = 8;

SELECT * FROM products;


-- Step 16: ALTER TABLE (Add Rating)
ALTER TABLE products
ADD COLUMN rating INTEGER;

-- Step 17: Update Rating
UPDATE products
SET rating = 5
WHERE product_id = 1;

UPDATE products
SET rating = 4
WHERE product_id = 2;

UPDATE products
SET rating = 5
WHERE product_id = 3;


-- Step 18: View Final Table
SELECT *
FROM products;


-- Practice Challenges:
-- Challenge 1 -> Insert some product. (Example: OnePlus 13)
INSERT INTO products 
(product_id, product_name, brand, category, price, stock, is_available, description)
VALUES
(9, 'OnePlus 13', 'OnePlus', 'Mobile', 57989, 23, TRUE, '5.5G flagship phone'),
(10,'Boat Rockerz 550','Boat','Headphones',1999,50,TRUE,'Wireless headphones');

SELECT * from products;


-- Challenge 2 -> Show only laptops
select * FROM products
WHERE category = 'Laptop';


-- Challenge 3 -> Show products cheaper than ₹30,000
SELECT * FROM products
WHERE price < 30000;


-- Challenge 4 -> Show products where stock is greater than 10
SELECT * FROM products
WHERE stock > 10;


-- Challenge 5 -> Update the stock of iPhone to 30
UPDATE products
SET stock = 30
WHERE  product_id = 1;
SELECT * FROM products
WHERE product_id = 1;


-- Challenge 6 -> Delete Boat headphones.
DELETE FROM products
WHERE product_id = 10;
SELECT * FROM products;


-- Challenge 7 -> Add a new column (discount INTEGER)
ALTER TABLE products
ADD COLUMN discount INTEGER;


-- Challenge 8 -> Give every Apple product a discount of 10
UPDATE products
SET discount = 10
WHERE brand = 'Apple';
select * from products;


-- Challenge 9 -> Find all unavailable products.
select * from products
where is_available = FALSE;


-- Challenge 10 -> Display only: Product Name, Brand, Price
select product_name, brand, price from products;


-- Challenge 11 -> Increase the price of every Apple product by ₹5,000
UPDATE products
SET price = price + 5000
where brand = 'Apple';
select * FROM products;


--Challenge 12 -> Reduce stock of all laptops by 2
UPDATE products
SET stock = stock - 2
where category = 'Laptop';
select * FROM products;


--Challenge 13 -> Delete all unavailable products
DELETE FROM products
where is_available = FALSE;
select * FROM products;


-- Challenge 14 -> Find products between ₹20,000 and ₹80,000
SELECT * FROM products
WHERE  price > 20000 and price < 80000;


-- Challenge 15 -> Find all products whose brand is NOT Apple
SELECT * FROM products
WHERE  brand != 'Apple';


-- Challenge 16 -> Show only: Product Name, Price where Stock > 10
SELECT product_name, price FROM products
where stock > 10;


-- Challenge 17 -> Insert three gaming laptops
INSERT INTO products 
(product_id, product_name, brand, category, price, stock, is_available, description)
VALUES
(11, 'ASUS ROG Zephyrus G14', 'ASUS', 'Laptop', 145000, 10, TRUE, 'High-end AMD Ryzen 9 gaming laptop'),
(12, 'Lenovo Legion Pro 5', 'Lenovo', 'Laptop', 125000, 15, TRUE, 'Intel i7 with RTX 4060 graphics'),
(13, 'Acer Predator Helios 16', 'Acer', 'Laptop', 115000, 8, TRUE, '165Hz display competitive gaming laptop');
SELECT * FROM products 
WHERE product_id IN (11, 12, 13);


-- Challenge 18 -> Increase discount of every product by 5
UPDATE products
SET discount = COALESCE(discount, 0) + 5;
select * FROM products;


-- Challenge 19 -> Update sony headphones stock to 100 cz boat is not avl
UPDATE products
set  stock = 100
where product_id = 6;
select * FROM products;


-- Challenge 20 -> Find all products containing the word: Laptop
SELECT * FROM products
WHERE category LIKE '%Laptop%' 
   OR description LIKE '%Laptop%';

