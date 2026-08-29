-- Database initialization script for Shopzy services
-- Creates separate databases for each service

-- Product Service Database
CREATE DATABASE product_db OWNER shopzy;

-- Inventory Service Database
CREATE DATABASE inventory_db OWNER shopzy;

-- Customer Service Database
CREATE DATABASE customer_db OWNER shopzy;

-- Order Service Database
CREATE DATABASE order_db OWNER shopzy;

-- Payment Service Database
CREATE DATABASE payment_db OWNER shopzy;

-- Notification Service Database
CREATE DATABASE notification_db OWNER shopzy;

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE product_db TO shopzy;
GRANT ALL PRIVILEGES ON DATABASE inventory_db TO shopzy;
GRANT ALL PRIVILEGES ON DATABASE customer_db TO shopzy;
GRANT ALL PRIVILEGES ON DATABASE order_db TO shopzy;
GRANT ALL PRIVILEGES ON DATABASE payment_db TO shopzy;
GRANT ALL PRIVILEGES ON DATABASE notification_db TO shopzy;
