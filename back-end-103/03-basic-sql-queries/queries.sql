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

CREATE TABLE sales (
    id SERIAL PRIMARY KEY,
    car_id INT REFERENCES cars(id),
    client_id INT REFERENCES clients(id),
    sale_date DATE,
    amount DECIMAL(10, 2)
);

CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    position VARCHAR(100),
    hire_date DATE
);

INSERT INTO cars (brand, model, year, price, status) VALUES
  ('Toyota', 'Camry', 2024, 18500000, 'Available'),
  ('Hyundai', 'Accent', 2023, 9800000, 'Available'),
  ('BMW', 'X5', 2024, 45000000, 'On Order'),
  ('Kia', 'K5', 2023, 15500000, 'Available'),
  ('Mercedes', 'E-Class', 2024, 42000000, 'Available'),
  ('Toyota', 'Land Cruiser', 2024, 52000000, 'On Order'),
  ('Hyundai', 'Santa Fe', 2023, 22500000, 'Available');

INSERT INTO clients (first_name, last_name, iin, phone, email) VALUES
  ('Азамат', 'Сериков', '940825300123', '+77071234567', 'azamat@mail.kz'),
  ('Динара', 'Алиева', '880915400789', '+77082345678', 'dinara@mail.kz'),
  ('Бауыржан', 'Нурланов', '910304500456', '+77093456789', 'baur@mail.kz');

INSERT INTO employees (first_name, last_name, position, hire_date) VALUES
  ('Ерлан', 'Касымов', 'Менеджер продаж', '2023-01-15'),
  ('Айгуль', 'Нурпеисова', 'Старший менеджер', '2022-05-20');

INSERT INTO sales (car_id, client_id, sale_date, amount) VALUES
  (1, 1, '2024-02-15', 18500000),
  (4, 2, '2024-02-20', 15500000);
