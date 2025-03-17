CREATE TABLE extra_equipment (
    id SERIAL PRIMARY KEY,
    car_id INT REFERENCES cars(id),
    name VARCHAR(100),
    cost DECIMAL(10, 2)
);

INSERT INTO extra_equipment (car_id, name, cost) VALUES
    (1, 'Кожаный салон', 500000.00), 
    (1, 'Зимняя резина', 300000.00),
    (2, 'Навигация', 200000.00),     
    (3, 'Аудиосистема', 700000.00); 


CREATE OR REPLACE FUNCTION get_car_total_price(car_id_input INT)
RETURNS DECIMAL AS $$
DECLARE
    base_price DECIMAL;
    extra_cost DECIMAL;
    total_price DECIMAL;
BEGIN
    
    SELECT price INTO base_price
    FROM cars
    WHERE id = car_id_input;

    SELECT COALESCE(SUM(cost), 0) INTO extra_cost
    FROM extra_equipment
    WHERE car_id = car_id_input;

    total_price := base_price + extra_cost;

    RETURN total_price;
END;
$$ LANGUAGE plpgsql;

SELECT get_car_total_price(1);  


CREATE OR REPLACE FUNCTION find_available_cars(min_year INT, min_price DECIMAL, max_price DECIMAL)
RETURNS TABLE (
    brand VARCHAR,
    model VARCHAR,
    year INT,
    price DECIMAL
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        c.brand,
        c.model,
        c.year,
        c.price
    FROM cars c
    WHERE c.status = 'Available'
    AND c.year >= min_year
    AND c.price BETWEEN min_price AND max_price
    ORDER BY c.price ASC;
END;
$$ LANGUAGE plpgsql;

SELECT * FROM find_available_cars(2023, 5000000, 20000000);


CREATE OR REPLACE FUNCTION analyze_sales(start_date DATE, end_date DATE)
RETURNS TABLE (
    sale_month DATE,
    total_sales BIGINT,
    total_revenue DECIMAL,
    avg_sale_amount DECIMAL
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        DATE_TRUNC('month', s.sale_date) AS sale_month,
        COUNT(s.id) AS total_sales,
        SUM(s.amount) AS total_revenue,
        AVG(s.amount) AS avg_sale_amount
    FROM sales s
    WHERE s.sale_date BETWEEN start_date AND end_date
    GROUP BY DATE_TRUNC('month', s.sale_date)
    ORDER BY sale_month ASC;
END;
$$ LANGUAGE plpgsql;

SELECT * FROM analyze_sales('2024-01-01', '2024-12-31');


CREATE OR REPLACE FUNCTION calculate_manager_commission(sale_id_input INT, commission_rate DECIMAL)
RETURNS DECIMAL AS $$
DECLARE
    sale_amount DECIMAL;
    commission DECIMAL;
BEGIN
    
    SELECT amount INTO sale_amount
    FROM sales
    WHERE id = sale_id_input;

    commission := sale_amount * commission_rate;

    RETURN commission;
END;
$$ LANGUAGE plpgsql;

SELECT calculate_manager_commission(1, 0.05);  