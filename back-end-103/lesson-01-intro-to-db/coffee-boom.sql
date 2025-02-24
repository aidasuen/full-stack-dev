CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,  
    name VARCHAR(255) NOT NULL,         
    description TEXT,                   
    price DECIMAL(10, 2) NOT NULL,      
    category VARCHAR(100),              
    status ENUM('available', 'not_available') DEFAULT 'available',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE customers (
    id INT AUTO_INCREMENT PRIMARY KEY,      
    first_name VARCHAR(255) NOT NULL,        
    last_name VARCHAR(255) NOT NULL,         
    email VARCHAR(255) NOT NULL UNIQUE,      
    phone VARCHAR(20),                       
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  
    bonus_points INT DEFAULT 0             
);

CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT,
    total_amount DECIMAL(10, 2),  
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    order_status ENUM('pending', 'completed', 'cancelled', 'shipped') DEFAULT 'pending', 
    payment_method ENUM('credit card', 'cash', 'bank transfer') DEFAULT 'credit card',
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);

CREATE TABLE order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT,
    product_id INT,
    quantity INT,
    price DECIMAL(10, 2) NOT NULL,  
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);

INSERT INTO products (name, description, price, category, status)
VALUES 
    ('Coffee', 'Freshly brewed coffee', 2000.00, 'Beverage', 'available'),
    ('Cake', 'Delicious chocolate cake', 3000.00, 'Dessert', 'available'),
    ('Sandwich', 'Tasty ham and cheese sandwich', 1500.00, 'Snack', 'available'),
    ('Tea', 'Herbal tea', 1000.00, 'Beverage', 'available');


INSERT INTO customers (first_name, last_name, email, phone)
VALUES 
    ('Иван', 'Иванов', 'ivanov@example.com', '+7 123 456 7890'),
    ('Ирина', 'Иванов', 'ivanova@example.com', '+7 123 456 7899');

INSERT INTO orders (customer_id, total_amount, order_status, payment_method)
VALUES (1, 5000.00, 'completed', 'cash');

INSERT INTO order_items (order_id, product_id, quantity, price)
VALUES
    (1, 1, 1, 2000.00),  --Coffee
    (1, 2, 1, 3000.00);  --Cake

