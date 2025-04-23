import pandas as pd
import numpy as np
from mysql.connector import connect
connection= connect(
host='localhost',
port='3306',
user='root',
password='Mysql@7'
)
cursor=connection.cursor()
print(connection.is_connected())
df0=pd.read_csv('customer_journey.csv')
df1=pd.read_csv('customer_reviews.csv')
df2=pd.read_csv('customers.csv')
df3=pd.read_csv('engagement_data.csv')
df4=pd.read_csv('geography.csv')
df5=pd.read_csv('products.csv')

print(df0.isnull().sum())
print(df1.isnull().sum())
print(df2.isnull().sum())
print(df3.isnull().sum())
print(df4.isnull().sum())
print(df5.isnull().sum())

df0['Duration'].fillna(df0['Duration'].mean(),inplace=True)
#1
cursor.execute("CREATE DATABASE IF NOT EXISTS dummy1;")
print("MySQL database 'dummy1' created successfully!")

cursor.execute("USE dummy1;")  # Select database
cursor.execute("""
    CREATE TABLE IF NOT EXISTS customer_journey (
        JourneyID INT,
        CustomerID INT,
        ProductID INT,    
        VisitDate Date,
        Stage VARCHAR(100),
        Action VARCHAR(100),  
        Duration FLOAT
        
    );
""")
connection.commit()
print("Table 'customer_journey' created successfully in MySQL!")
#2

cursor.execute("""
    CREATE TABLE IF NOT EXISTS customer_reviews (
        ReviewID INT,
        CustomerID INT,
        ProductID INT,
        ReviewDate  Date,
        Rating INT,
        ReviewText VARCHAR(2000)
        
    );
""")
connection.commit()
print("Table 'customer_reviews' created successfully in MySQL!")

#3
cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        CustomerID INT,
        CustomerName VARCHAR(50),
        Email VARCHAR(50),
        Gender VARCHAR(50),
        Age INT,
        GeographyID INT
        
    );
""")
connection.commit()
print("Table 'customer' created successfully in MySQL!")

#4

cursor.execute("""
    CREATE TABLE IF NOT EXISTS engagement_data (
        EngagementID INT,
               ContentID INT,
               ContentType VARCHAR(50),
               Likes INT,
               EngagementDate Date,
               CampaignID INT ,
               ProductID  INT,
               ViewsClicksCombined VARCHAR(50)
        
    );
""")
connection.commit()
print("Table 'engagement_data' created successfully in MySQL!")

#5
cursor.execute("""
    CREATE TABLE IF NOT EXISTS geography (
      GEographyID INT,
      Country VARCHAR(50),
      City VARCHAR(50)
               
        
    );
""")
connection.commit()
print("Table 'geography' created successfully in MySQL!")
#6

cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        ProductID INT,
        ProductName VARCHAR(50),
        Category VARCHAR(50) ,
        Price INT
        
    );
""")
connection.commit()
print("Table 'products' created successfully in MySQL!")


#inserting 1
data_list = df0.values.tolist()
query = """
    INSERT INTO customer_journey (JourneyID,CustomerID,ProductID,VisitDate,Stage,Action,Duration)
    VALUES (%s, %s, %s, %s, %s, %s, %s);
"""
cursor.executemany(query, data_list)
connection.commit()
print("Data inserted using to_list()")


#inserting 2
data_list = df1.values.tolist()
query = """
    INSERT INTO customer_reviews (ReviewID,CustomerID,ProductID,ReviewDate,Rating,ReviewText)
    VALUES (%s, %s, %s, %s, %s, %s);
"""

cursor.executemany(query, data_list)
connection.commit()

print("Data inserted using to_list()")

#inserting 3
data_list = df2.values.tolist()
query = """
    INSERT INTO customers(CustomerID,CustomerName,Email,Gender,Age,GeographyID)
    VALUES ( %s, %s, %s, %s, %s, %s);
"""
cursor.executemany(query, data_list)
connection.commit()
print("Data inserted using to_list()")
#4
data_list = df3.values.tolist()
query = """
    INSERT INTO engagement_data(EngagementID,ContentID,ContentType,Likes,EngagementDate,CampaignID,ProductID,ViewsClicksCombined)
    VALUES (%s, %s, %s, %s, %s, %s, %s,%s);
"""
cursor.executemany(query, data_list)
connection.commit()
print("Data inserted using to_list()")



#5
data_list = df5.values.tolist()
query = """
    INSERT INTO products (ProductID,ProductName,Category,Price)
    VALUES (%s, %s, %s, %s);
"""
cursor.executemany(query, data_list)
connection.commit()
print("Data inserted using to_list()")
#6
data_list = df4.values.tolist()
query = """
    INSERT INTO geography (GeographyID, Country, City)
    VALUES (%s, %s, %s);
"""
cursor.executemany(query, data_list)
connection.commit()
print("Data inserted into 'geography' using to_list()")







