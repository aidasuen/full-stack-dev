CREATE TABLE cars (
    id SERIAL PRIMARY KEY,
    brand VARCHAR(100),
    model VARCHAR(100),
    year INT,
    price DECIMAL(10, 2),
    status VARCHAR(50)
);

CREATE TABLE clients (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    iin VARCHAR(12) UNIQUE,
    phone VARCHAR(15),
    email VARCHAR(100)
);

CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    position VARCHAR(100),
    hire_date DATE
);

CREATE TABLE sales (
    id SERIAL PRIMARY KEY,
    car_id INT REFERENCES cars(id),
    client_id INT REFERENCES clients(id),
    sale_date DATE,
    amount DECIMAL(10, 2),
    employee_id INT REFERENCES employees(id)
);

INSERT INTO cars (brand, model, year, price, status) VALUES
    ('Toyota', 'Camry', 2024, 18500000.00, 'Sold'),
    ('Hyundai', 'Accent', 2023, 9800000.00, 'Available'),
    ('BMW', 'X5', 2024, 45000000.00, 'On Order'),
    ('Kia', 'K5', 2023, 15500000.00, 'Sold'),
    ('Mercedes', 'E-Class', 2024, 42000000.00, 'Available');

INSERT INTO clients (first_name, last_name, iin, phone, email) VALUES
    ('Азамат', 'Сериков', '940825300123', '+77000000001', 'azamat@mail.kz'),
    ('Динара', 'Алиева', '880915400789', '+77002345678', 'dinara@mail.kz'),
    ('Бауыржан', 'Нурланов', '910304500456', '+77001234567', 'baur@mail.kz');

INSERT INTO employees (first_name, last_name, position, hire_date) VALUES
    ('Ерлан', 'Касымов', 'Менеджер продаж', '2023-01-15'),
    ('Айгуль', 'Нурпеисова', 'Старший менеджер', '2022-05-20');

INSERT INTO sales (car_id, client_id, sale_date, amount, employee_id) VALUES
    (1, 1, '2024-02-15', 18500000.00, 1),
    (4, 2, '2024-02-20', 15500000.00, 2);