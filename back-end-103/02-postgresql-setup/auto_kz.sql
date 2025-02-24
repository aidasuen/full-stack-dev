CREATE TABLE cars (
    id SERIAL PRIMARY KEY,
    brand VARCHAR(100),
    model VARCHAR(100),
    year INT,
    price DECIMAL(10, 2),
    status VARCHAR(50)
);

INSERT INTO cars (brand, model, year, price, status)
VALUES
    ('Toyota', 'Camry', 2022, 15000000.00, 'Available'),
    ('BMW', 'X5', 2021, 3000000.00, 'Sold'),
    ('Audi', 'A4', 2020, 2000000.00, 'Sold'),
    ('Hyundai', 'Tucson', 2023, 12000000.00, 'Available');

CREATE TABLE clients (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    iin VARCHAR(12) UNIQUE,
    phone VARCHAR(15),
    email VARCHAR(100)
);

INSERT INTO clients (first_name, last_name, iin, phone, email)
VALUES
    ('Ivan', 'Petrov', '900000000000', '123-456-7890', 'ivan.petrov@email.com'),
    ('Olga', 'Ivanova', '900000000001', '987-654-3210', 'olga.ivanova@email.com'),
    ('Alexey', 'Sidorov', '900000000002', '456-789-1234', 'alexey.sidorov@email.com'),
    ('Aigerim', 'Ni', '900000000003', '777-123-4567', 'aigerim.n@email.com');

CREATE TABLE sales (
    id SERIAL PRIMARY KEY,
    car_id INT REFERENCES cars(id),
    client_id INT REFERENCES clients(id),
    sale_date DATE,
    amount DECIMAL(10, 2)
);

INSERT INTO sales (car_id, client_id, sale_date, amount)
VALUES
    (2, 1, '2025-02-01', 3000000.00),
    (3, 2, '2025-02-10', 2000000.00),
    (1, 4, '2025-02-20', 15000000.00);

CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    position VARCHAR(100),
    hire_date DATE
);

INSERT INTO employees (first_name, last_name, position, hire_date)
VALUES
    ('Anna', 'Kuzmina', 'Sales Manager', '2022-06-15'),
    ('Dmitry', 'Morozov', 'Sales Agent', '2023-01-10'),
    ('Gulmira', 'Tolegenova', 'Sales Manager', '2024-01-15');