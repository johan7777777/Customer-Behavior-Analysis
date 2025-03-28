import pandas as pd
import mysql.connector
from datetime import datetime, timedelta

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

# Fill missing numeric values with column means
for name, df in dfs.items():
    dfs[name] = df.fillna(df.mean(numeric_only=True))

# MySQL connection
conn_mysql = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Mysql@7"
)
cursor_mysql = conn_mysql.cursor()
print("MySQL connection established!")

# Create database
cursor_mysql.execute("CREATE DATABASE IF NOT EXISTS customer_db;")
cursor_mysql.execute("USE customer_db;")
print("Database 'customer_db' selected!")

# Create tables
table_queries = {
    "products": """
        CREATE TABLE IF NOT EXISTS products (
            ProductID INT PRIMARY KEY,
            ProductName VARCHAR(100),
            Category VARCHAR(50),
            Price DECIMAL(10,2)
        );
    """,
    "geography": """
        CREATE TABLE IF NOT EXISTS geography (
            GeographyID INT PRIMARY KEY,
            Country VARCHAR(50),
            City VARCHAR(50)
        );
    """,
    "customers": """
        CREATE TABLE IF NOT EXISTS customers (
            CustomerID INT PRIMARY KEY,
            CustomerName VARCHAR(100),
            Email VARCHAR(100),
            Gender VARCHAR(10),
            Age INT,
            GeographyID INT,
            FOREIGN KEY (GeographyID) REFERENCES geography(GeographyID)
        );
    """,
    "customer_reviews": """
        CREATE TABLE IF NOT EXISTS customer_reviews (
            ReviewID INT PRIMARY KEY,
            CustomerID INT,
            ProductID INT,
            Rating INT,
            ReviewDate DATE,
            ReviewText TEXT,
            FOREIGN KEY (CustomerID) REFERENCES customers(CustomerID),
            FOREIGN KEY (ProductID) REFERENCES products(ProductID)
        );
    """,
    "customer_journey": """
        CREATE TABLE IF NOT EXISTS customer_journey (
            JourneyID INT PRIMARY KEY,
            CustomerID INT,
            ProductID INT,
            VisitDate DATE,
            Stage VARCHAR(50),
            Action VARCHAR(50),
            Duration FLOAT,
            FOREIGN KEY (CustomerID) REFERENCES customers(CustomerID),
            FOREIGN KEY (ProductID) REFERENCES products(ProductID)
        );
    """,
    "engagement_data": """
        CREATE TABLE IF NOT EXISTS engagement_data (
            EngagementID INT PRIMARY KEY,
            ContentID INT,
            ContentType VARCHAR(50),
            Likes INT,
            EngagementDate DATE,
            CampaignID INT,
            ProductID INT,
            ViewsClicksCombined VARCHAR(50)
        );
    """
}

for table, query in table_queries.items():
    cursor_mysql.execute(query)
    print(f"Table '{table}' created successfully!")

conn_mysql.commit()

# Insert data into tables
def insert_data(table, query, data):
    try:
        for _, row in data.iterrows():
            cursor_mysql.execute(query, tuple(row))
        conn_mysql.commit()
        print(f"Successfully inserted into '{table}' table.")
    except Exception as e:
        print(f"Error inserting into '{table}': {e}")

# Insert into products
insert_data("products", """
    INSERT INTO products (ProductID, ProductName, Category, Price)
    VALUES (%s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE ProductName=VALUES(ProductName), Category=VALUES(Category), Price=VALUES(Price);
""", dfs["products"])

# Insert into geography
insert_data("geography", """
    INSERT INTO geography (GeographyID, Country, City)
    VALUES (%s, %s, %s)
    ON DUPLICATE KEY UPDATE Country=VALUES(Country), City=VALUES(City);
""", dfs["geography"])

# Insert into customers
insert_data("customers", """
    INSERT INTO customers (CustomerID, CustomerName, Email, Gender, Age, GeographyID)
    VALUES (%s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE CustomerName=VALUES(CustomerName), Email=VALUES(Email), Gender=VALUES(Gender), Age=VALUES(Age), GeographyID=VALUES(GeographyID);
""", dfs["customers"])

# Insert into customer_reviews
insert_data("customer_reviews", """
    INSERT INTO customer_reviews (ReviewID, CustomerID, ProductID, Rating, ReviewDate, ReviewText)
    VALUES (%s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE Rating=VALUES(Rating), ReviewDate=VALUES(ReviewDate), ReviewText=VALUES(ReviewText);
""", dfs["customer_reviews"])

# Insert into customer_journey
insert_data("customer_journey", """
    INSERT INTO customer_journey (JourneyID, CustomerID, ProductID, VisitDate, Stage, Action, Duration)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE VisitDate=VALUES(VisitDate), Stage=VALUES(Stage), Action=VALUES(Action), Duration=VALUES(Duration);
""", dfs["customer_journey"])

# Insert into engagement_data
insert_data("engagement_data", """
    INSERT INTO engagement_data (EngagementID, ContentID, ContentType, Likes, EngagementDate, CampaignID, ProductID, ViewsClicksCombined)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE ContentType=VALUES(ContentType), Likes=VALUES(Likes), EngagementDate=VALUES(EngagementDate), CampaignID=VALUES(CampaignID), ProductID=VALUES(ProductID), ViewsClicksCombined=VALUES(ViewsClicksCombined);
""", dfs["engagement_data"])

# Close connection
cursor_mysql.close()
conn_mysql.close()
print("All data inserted successfully!")
