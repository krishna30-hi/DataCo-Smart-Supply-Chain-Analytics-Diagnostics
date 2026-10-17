-- Set the database
USE dataco_db;

-- ==========================================
-- 1. SALES ANALYSIS
-- ==========================================

-- Monthly Sales Trend[cite: 6]
SELECT `Order Month Name`, ROUND(SUM(Sales), 2) AS Total_Sales
FROM supply_chain_analytics
GROUP BY `Order Month Name`
ORDER BY FIELD(`Order Month Name`, 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December');

-- Year-wise Sales Trend[cite: 6]
SELECT `Order Year`, ROUND(SUM(Sales), 2) AS Total_Sales
FROM supply_chain_analytics
GROUP BY `Order Year`
ORDER BY `Order Year` ASC;

-- ==========================================
-- 2. PRODUCT ANALYSIS
-- ==========================================

-- Top 10 Product Categories by Sales[cite: 6]
SELECT `Category Name`, ROUND(SUM(Sales), 2) AS Total_Sales
FROM supply_chain_analytics
GROUP BY `Category Name`
ORDER BY Total_Sales DESC
LIMIT 10;

-- Top 10 Products by Sales[cite: 6]
SELECT `Product Name`, ROUND(SUM(Sales), 2) AS Total_Sales
FROM supply_chain_analytics
GROUP BY `Product Name`
ORDER BY Total_Sales DESC
LIMIT 10;

-- Sales by Department[cite: 6]
SELECT `Department Name`, ROUND(SUM(Sales), 2) AS Total_Sales
FROM supply_chain_analytics
GROUP BY `Department Name`
ORDER BY Total_Sales DESC;

-- ==========================================
-- 3. GEOGRAPHIC ANALYSIS
-- ==========================================

-- Sales by Market[cite: 6]
SELECT Market, ROUND(SUM(Sales), 2) AS Total_Sales
FROM supply_chain_analytics
GROUP BY Market
ORDER BY Total_Sales DESC;

-- Top 10 Order Regions by Sales[cite: 6]
SELECT `Order Region`, ROUND(SUM(Sales), 2) AS Total_Sales
FROM supply_chain_analytics
GROUP BY `Order Region`
ORDER BY Total_Sales DESC
LIMIT 10;

-- Top 10 Countries by Sales[cite: 6]
SELECT `Order Country`, ROUND(SUM(Sales), 2) AS Total_Sales
FROM supply_chain_analytics
GROUP BY `Order Country`
ORDER BY Total_Sales DESC
LIMIT 10;

-- ==========================================
-- 4. CUSTOMER ANALYSIS
-- ==========================================

-- Sales by Customer Segment[cite: 6]
SELECT `Customer Segment`, ROUND(SUM(Sales), 2) AS Total_Sales
FROM supply_chain_analytics
GROUP BY `Customer Segment`
ORDER BY Total_Sales DESC;

-- Top 10 Customers by Sales[cite: 6]
SELECT `Customer Id`, ROUND(SUM(Sales), 2) AS Total_Sales
FROM supply_chain_analytics
GROUP BY `Customer Id`
ORDER BY Total_Sales DESC
LIMIT 10;

-- ==========================================
-- 5. LOGISTICS & FRAUD ANALYSIS
-- ==========================================

-- Orders by Shipping Mode[cite: 6]
SELECT `Shipping Mode`, COUNT(*) AS Number_of_Orders
FROM supply_chain_analytics
GROUP BY `Shipping Mode`
ORDER BY Number_of_Orders DESC;

-- Delivery Status Distribution[cite: 6]
SELECT `Delivery Status`, COUNT(*) AS Number_of_Orders
FROM supply_chain_analytics
GROUP BY `Delivery Status`
ORDER BY Number_of_Orders DESC;

-- Suspected Fraud Orders by Market[cite: 6]
SELECT Market, COUNT(*) AS Number_of_Fraud_Orders
FROM supply_chain_analytics
WHERE `Order Status` = 'SUSPECTED_FRAUD'
GROUP BY Market
ORDER BY Number_of_Fraud_Orders DESC;

-- Fraud Orders by Shipping Mode[cite: 6]
SELECT `Shipping Mode`, COUNT(*) AS Number_of_Fraud_Orders
FROM supply_chain_analytics
WHERE `Order Status` = 'SUSPECTED_FRAUD'
GROUP BY `Shipping Mode`
ORDER BY Number_of_Fraud_Orders DESC;

-- Fraud Orders by Customer Segment[cite: 6]
SELECT `Customer Segment`, COUNT(*) AS Number_of_Fraud_Orders
FROM supply_chain_analytics
WHERE `Order Status` = 'SUSPECTED_FRAUD'
GROUP BY `Customer Segment`
ORDER BY Number_of_Fraud_Orders DESC;