CREATE DATABASE DDMA;
USE DDMA;

CREATE TABLE customers (
  id VARCHAR(36) NOT NULL PRIMARY KEY,
  first_name VARCHAR(100) NOT NULL,
  last_name VARCHAR(100) NOT NULL,
  email VARCHAR(160) UNIQUE,
  phone VARCHAR(32),
  address VARCHAR(255),
  city VARCHAR(120),
  state VARCHAR(120),
  postal_code VARCHAR(32),
  country VARCHAR(120),
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE products (
  id VARCHAR(36) NOT NULL PRIMARY KEY,
  name VARCHAR(200) NOT NULL,
  description TEXT,
  category VARCHAR(120),
  price DECIMAL(12,2) NOT NULL CHECK (price >= 0),
  sku VARCHAR(64) UNIQUE,
  stock_quantity INT NOT NULL DEFAULT 0 CHECK (stock_quantity >= 0),
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE sales (
  id VARCHAR(36) NOT NULL PRIMARY KEY,
  customer_id VARCHAR(36) NOT NULL,
  product_id VARCHAR(36) NOT NULL,
  sale_date DATETIME NOT NULL,
  quantity INT NOT NULL CHECK (quantity > 0),
  unit_price DECIMAL(12,2) NOT NULL CHECK (unit_price >= 0),
  total_amount DECIMAL(12,2) AS (quantity * unit_price) STORED,
  payment_method VARCHAR(32),
  sales_channel VARCHAR(32),
  CONSTRAINT fk_sales_customer FOREIGN KEY (customer_id) REFERENCES customers(id),
  CONSTRAINT fk_sales_product FOREIGN KEY (product_id) REFERENCES products(id),
  INDEX idx_sales_date (sale_date),
  INDEX idx_sales_customer (customer_id),
  INDEX idx_sales_product (product_id)
);
-- Insert sample customers
INSERT INTO customers (id, first_name, last_name, email, phone, address, city, state, postal_code, country) VALUES
('c1', 'John', 'Doe', 'john.doe@example.com', '1234567890', '123 Apple St', 'New York', 'NY', '10001', 'USA'),
('c2', 'Jane', 'Smith', 'jane.smith@example.com', '0987654321', '456 Orange Ave', 'Los Angeles', 'CA', '90001', 'USA'),
('c3', 'Michael', 'Brown', 'michael.brown@example.com', '2345678901', '789 Banana Blvd', 'Chicago', 'IL', '60601', 'USA'),
('c4', 'Sarah', 'Johnson', 'sarah.johnson@example.com', '3456789012', '101 Grape Rd', 'Houston', 'TX', '77001', 'USA');

-- Insert sample products
INSERT INTO products (id, name, description, category, price, sku, stock_quantity) VALUES
('p1', 'Wireless Mouse', 'Ergonomic wireless mouse', 'Accessories', 25.99, 'WM123', 120),
('p2', 'USB-C Cable', '1m USB-C charging cable', 'Cables', 9.99, 'USB456', 300),
('p3', 'Bluetooth Keyboard', 'Compact keyboard with Bluetooth', 'Accessories', 45.00, 'BK789', 150),
('p4', '27-inch Monitor', 'Full HD LED monitor', 'Electronics', 159.99, 'MTR345', 50);


-- Insert sample sales
INSERT INTO sales (id, customer_id, product_id, sale_date, quantity, unit_price, payment_method, sales_channel) VALUES
('s1', 'c1', 'p1', '2025-09-01 10:15:00', 2, 25.99, 'Credit Card', 'Online'),
('s2', 'c2', 'p2', '2025-09-02 14:30:00', 3, 9.99, 'PayPal', 'Retail Store'),
('s3', 'c3', 'p3', '2025-09-03 16:45:00', 1, 45.00, 'Debit Card', 'Online'),
('s4', 'c4', 'p4', '2025-09-04 13:10:00', 1, 159.99, 'Credit Card', 'Retail Store'),
('s5', 'c1', 'p2', '2025-09-05 11:30:00', 2, 9.99, 'Credit Card', 'Online'),
('s6', 'c2', 'p3', '2025-09-06 12:00:00', 1, 45.00, 'PayPal', 'Retail Store'),
('s7', 'c3', 'p1', '2025-09-07 15:00:00', 4, 25.99, 'Debit Card', 'Online'),
('s8', 'c4', 'p2', '2025-09-08 16:00:00', 5, 9.99, 'Credit Card', 'Retail Store');


SELECT COUNT(*) AS customers FROM customers;
SELECT COUNT(*) AS products FROM products;
SELECT COUNT(*) AS sales FROM sales;

SELECT
  DATE_FORMAT(sale_date, '%Y-%m') AS sale_month,
  SUM(quantity * unit_price) AS monthly_revenue
FROM sales
GROUP BY sale_month
ORDER BY sale_month;

SELECT
  DATE_FORMAT(sale_date, '%Y-%m') AS sale_month,
  AVG(quantity * unit_price) AS average_order_value
FROM sales
GROUP BY sale_month
ORDER BY sale_month;



SELECT s.id, c.first_name, p.name, s.quantity, s.unit_price, s.total_amount, s.sale_date
FROM sales s
JOIN customers c ON c.id = s.customer_id
JOIN products p ON p.id = s.product_id
ORDER BY s.sale_date DESC
LIMIT 10;



