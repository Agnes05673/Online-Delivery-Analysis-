CREATE DATABASE food_db;
USE food_db;
CREATE TABLE food_orders (
    order_id INT,
    customer_id INT,
    age INT,
    city VARCHAR(100),
    restaurant VARCHAR(150),
    cuisine VARCHAR(100),
    order_value FLOAT
);
SELECT * FROM food_orders LIMIT 10;
SELECT COUNT(*) FROM food_orders;
SELECT SUM(order_value) FROM food_orders;
SELECT Customer_ID,
       SUM(Order_Value) AS Total_Spent
FROM food_orders
GROUP BY Customer_ID
ORDER BY Total_Spent DESC
LIMIT 10;
SELECT DISTINCT Customer_Age_Group FROM food_orders;
SELECT 
    CASE 
        WHEN Customer_Age <= 25 THEN '18-25'
        WHEN Customer_Age <= 35 THEN '26-35'
        WHEN Customer_Age <= 50 THEN '36-50'
        ELSE '50+'
    END AS Age_Group,
    AVG(Order_Value) AS Avg_Order_Value
FROM food_orders
GROUP BY Age_Group;
SELECT 
    CASE 
        WHEN Order_Day IN ('Saturday', 'Sunday') THEN 'Weekend'
        ELSE 'Weekday'
    END AS Day_Type,
    COUNT(*) AS Total_Orders,
    AVG(Order_Value) AS Avg_Order_Value
FROM food_orders
GROUP BY Day_Type;
SELECT 
    DATE_FORMAT(Order_Date, '%Y-%m') AS Month,
    SUM(Order_Value) AS Total_Revenue
FROM food_orders
GROUP BY Month
ORDER BY Month;
SELECT Order_Date 
FROM food_orders 
LIMIT 10;
SELECT 
    DATE_FORMAT(STR_TO_DATE(Order_Date, '%m/%d/%Y'), '%Y-%m') AS Month,
    SUM(Order_Value) AS Total_Revenue
FROM food_orders
GROUP BY Month
ORDER BY Month;
SELECT 
    City,
    AVG(Delivery_Time_Min) AS Avg_Delivery_Time
FROM food_orders
GROUP BY City
ORDER BY Avg_Delivery_Time;
SELECT 
    CASE 
        WHEN Distance_km <= 5 THEN '0-5 km'
        WHEN Distance_km <= 10 THEN '5-10 km'
        WHEN Distance_km <= 20 THEN '10-20 km'
        ELSE '20+ km'
    END AS Distance_Group,
    AVG(Delivery_Time_Min) AS Avg_Delivery_Time
FROM food_orders
GROUP BY Distance_Group;
SELECT 
    Delivery_Rating,
    AVG(Delivery_Time_Min) AS Avg_Delivery_Time
FROM food_orders
WHERE Delivery_Rating IS NOT NULL
GROUP BY Delivery_Rating
ORDER BY Delivery_Rating DESC;
SELECT 
    Restaurant_Name,
    AVG(Restaurant_Rating) AS Avg_Rating
FROM food_orders
GROUP BY Restaurant_Name
ORDER BY Avg_Rating DESC
LIMIT 10;
SELECT 
    Restaurant_Name,
    COUNT(*) AS Total_Orders,
    SUM(CASE WHEN Order_Status = 'Cancelled' THEN 1 ELSE 0 END) AS Cancelled_Orders,
    (SUM(CASE WHEN Order_Status = 'Cancelled' THEN 1 ELSE 0 END) / COUNT(*)) * 100 AS Cancellation_Rate
FROM food_orders
GROUP BY Restaurant_Name
ORDER BY Cancellation_Rate DESC;
SELECT 
    Cuisine_Type,
    COUNT(*) AS Total_Orders,
    AVG(Restaurant_Rating) AS Avg_Rating,
    SUM(Order_Value) AS Total_Revenue
FROM food_orders
GROUP BY Cuisine_Type
ORDER BY Total_Revenue DESC;
SELECT 
    Peak_Hour,
    COUNT(*) AS Total_Orders,
    AVG(Order_Value) AS Avg_Order_Value
FROM food_orders
GROUP BY Peak_Hour;
SELECT COUNT(*) 
FROM food_orders 
WHERE Cuisine_Type IS NULL;
SELECT 
    Peak_Hour,
    COUNT(*) AS Total_Orders,
    AVG(Order_Value) AS Avg_Order_Value
FROM food_orders
GROUP BY Peak_Hour;
SELECT 
    Payment_Mode,
    COUNT(*) AS Total_Orders
FROM food_orders
GROUP BY Payment_Mode
ORDER BY Total_Orders DESC;
SELECT 
    Cancellation_Reason,
    COUNT(*) AS Total_Cancellations
FROM food_orders
WHERE Order_Status = 'Cancelled'
GROUP BY Cancellation_Reason
ORDER BY Total_Cancellations DESC;