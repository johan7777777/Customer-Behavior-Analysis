# Extract and Join Customer Journey Data
 SELECT 
    cj.JourneyID, c.CustomerName, p.ProductName, cj.VisitDate, 
    cj.Stage, cj.Action, cj.Duration
FROM CustomerJourney cj
JOIN Customers c ON cj.CustomerID = c.CustomerID
JOIN Products p ON cj.ProductID = p.ProductID 

#Drop-off & Conversion Insights
select Stage, COUNT(*) AS DropOffCount
FROM CustomerJourney
WHERE Action = 'Drop-off'
GROUP BY Stage
ORDER BY DropOffCount DESC;

SELECT Stage, Action, COUNT(*) AS ActionCount, 
       ROUND((COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY Stage)), 2) AS ActionPercentage
FROM CustomerJourney
GROUP BY Stage, Action
ORDER BY Stage, ActionCount DESC;

#conversion_df = run_query(query_conversion)
SELECT Stage, ROUND(AVG(Duration), 2) AS AvgDuration
FROM CustomerJourney
GROUP BY Stage
ORDER BY AvgDuration DESC;

#Customer Reviews Analysis** (Highest & Lowest-Rated Products)
SELECT p.ProductName, 
       ROUND(AVG(cr.Rating), 2) AS AvgRating, 
       COUNT(*) AS TotalReviews
FROM CustomerReviews cr
JOIN Products p ON cr.ProductID = p.ProductID
GROUP BY p.ProductName
ORDER BY AvgRating DESC;


SELECT p.ProductID, p.ProductName, 
       ROUND(AVG(cr.Rating), 2) AS AvgRating
FROM CustomerReviews cr  
JOIN Products p ON cr.ProductID = p.ProductID
GROUP BY p.ProductID, p.ProductName
ORDER BY AvgRating DESC;

# Marketing Effectiveness Analysis
#customer retension rate

SELECT 
    (COUNT(DISTINCT CASE WHEN VisitDate >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR) THEN CustomerID END) 
     / COUNT(DISTINCT CustomerID)) * 100 AS RetentionRate
FROM CustomerJourney;
#  repet vs first buyer 
SELECT BuyerType, COUNT(*) AS BuyerCount
FROM (
    SELECT 
        CustomerID, 
        CASE 
            WHEN COUNT(*) > 1 THEN 'Repeat Buyer' 
            ELSE 'First-Time Buyer' 
        END AS BuyerType
    FROM CustomerJourney
    WHERE Stage = 'Checkout'
    GROUP BY CustomerID
) AS BuyerData
GROUP BY BuyerType;
     
     #Best Performing Products per Country

SELECT g.Country, p.ProductName, COUNT(*) AS SalesCount
FROM CustomerJourney cj
JOIN Customers c ON cj.CustomerID = c.CustomerID
JOIN Geography g ON c.GeographyID = g.GeographyID
JOIN Products p ON cj.ProductID = p.ProductID
GROUP BY g.Country, p.ProductName
ORDER BY SalesCount DESC
