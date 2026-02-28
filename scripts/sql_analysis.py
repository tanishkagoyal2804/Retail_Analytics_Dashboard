import sqlite3
import pandas as pd

conn = sqlite3.connect("retail.db")

# Top 5 customers by sales
query1 = """
SELECT [Customer Name], SUM(Sales) as Total_Sales
FROM retail_sales
GROUP BY [Customer Name]
ORDER BY Total_Sales DESC
LIMIT 5
"""

result1 = pd.read_sql(query1, conn)
print("\nTop 5 Customers by Sales:")
print(result1)

# Sales by Region
query2 = """
SELECT Region, SUM(Sales) as Total_Sales
FROM retail_sales
GROUP BY Region
"""

result2 = pd.read_sql(query2, conn)
print("\nSales by Region:")
print(result2)