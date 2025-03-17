CREATE INDEX idx_cars_brand_model ON cars (brand, model) ;
CREATE INDEX idx_cars_year ON cars (year);
CREATE INDEX idx_sales_client_id ON sales (client_id) ;
CREATE INDEX idx_cars_price ON cars (price);

CREATE INDEX idx_cars_year_price ON cars (year, price);
CREATE INDEX idx_orders_car_id ON orders (car_id);

EXPLAIN SELECT c.brand, c.model, c.year, c.price, o.order_date 
FROM cars c
JOIN orders o 
ON c.id = o.car_id 
WHERE c.year > 2020
AND c.price < 10000000;