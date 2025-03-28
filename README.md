# Customer Trends & Marketing Insights

## Overview

This project analyzes customer behavior trends, product performance, and marketing effectiveness using Python and SQL. The goal is to improve customer experience and optimize business strategies.

## Technologies Used

- **Python**: Pandas, SQLAlchemy, MySQL-Connector
- **SQL**: MySQL for querying and analysis
- **Jupyter Notebook**: Data visualization and reporting

## Data Processing Workflow

### 1. Download & Load Data

#### Steps:
1. Download customer-related CSV files.
2. Convert CSV data into structured SQL tables.
3. Use Python to automate data insertion into MySQL.

#### Code Example (Python):
```python
import pandas as pd
import mysql.connector

# Read CSV files
file_paths = {
    "customer_journey": "customer_journey.csv",
    "customer_reviews": "customer_reviews.csv",
    "customers": "customers.csv",
    "engagement_data": "engagement_data.csv",
    "geography": "geography.csv",
    "products": "products.csv"
}
dfs = {name: pd.read_csv(path) for name, path in file_paths.items()}

# Fill missing values
for name, df in dfs.items():
    dfs[name] = df.fillna(df.mean(numeric_only=True))
```

#### SQL Table Creation Example:
```sql
CREATE TABLE IF NOT EXISTS products (
    ProductID INT PRIMARY KEY,
    ProductName VARCHAR(100),
    Category VARCHAR(50),
    Price DECIMAL(10,2)
);
```

### 2. Data Extraction & Transformation

#### Steps:
1. Write SQL queries to extract relevant data.
2. Perform joins, window functions, CTEs, and subqueries for deeper insights.

#### SQL Query Example:
```sql
SELECT cj.JourneyID, c.CustomerName, p.ProductName, cj.VisitDate, 
       cj.Stage, cj.Action, cj.Duration
FROM customer_journey cj
JOIN customers c ON cj.CustomerID = c.CustomerID
JOIN products p ON cj.ProductID = p.ProductID;
```

### 3. Customer Journey & Engagement Analysis

#### Steps:
1. Identify drop-off points in the customer journey.
2. Analyze actions leading to successful conversions.
3. Calculate average time spent per stage.

#### SQL Query Example (Drop-off Analysis):
```sql
SELECT Stage, COUNT(*) AS DropOffCount
FROM customer_journey
WHERE Action = 'Drop-off'
GROUP BY Stage
ORDER BY DropOffCount DESC;
```

### 4. Customer Reviews Analysis

#### Steps:
1. Identify highest and lowest-rated products using SQL.
2. Perform sentiment analysis on customer reviews using Python.
3. Correlate review trends with product performance.

#### SQL Query Example (Top & Lowest Rated Products):
```sql
SELECT p.ProductName, ROUND(AVG(cr.Rating), 2) AS AvgRating, COUNT(*) AS TotalReviews
FROM customer_reviews cr
JOIN products p ON cr.ProductID = p.ProductID
GROUP BY p.ProductName
ORDER BY AvgRating DESC;
```

### 5. Marketing Effectiveness Analysis

#### Steps:
1. Calculate customer retention rate.
2. Compare repeat vs. first-time buyers.
3. Identify best-performing products per region.

#### SQL Query Example (Customer Retention Rate):
```sql
SELECT 
    (COUNT(DISTINCT CASE WHEN VisitDate >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR) THEN CustomerID END) 
     / COUNT(DISTINCT CustomerID)) * 100 AS RetentionRate
FROM customer_journey;
```

## Key Findings

- **High Checkout Drop-Off**: 70% of customers abandon checkout due to complexity and additional costs.
- **Conversion Insights**: Only 30% of users complete purchases.
- **Top-Rated Products**: Football Helmet (5.0 stars), Lowest: Basketball (2.67 stars).
- **Best Performing Regions**: Austria (Running Shoes), Spain (Football Helmet).

## Recommendations

✅ Simplify checkout process, display shipping costs upfront, and use cart reminders.  
✅ Improve product pages with better images, descriptions, and customer reviews.  
✅ Boost customer retention through loyalty programs and personalized recommendations.  
✅ Target top-performing regions with country-specific marketing campaigns.  

## How to Run the Project

1. Install dependencies:
   ```sh
   pip install pandas mysql-connector-python sqlalchemy
   ```
2. Run `script.py` to load data into MySQL.
3. Execute `queries.sql` for analysis.
4. View insights and recommendations in the final report.

## Conclusion

By optimizing checkout, improving product pages, and targeting marketing efforts, businesses can increase conversions and customer loyalty. 🚀


