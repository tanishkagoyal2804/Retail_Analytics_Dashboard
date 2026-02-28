import sqlite3
import pandas as pd

# Load cleaned data
df = pd.read_csv("data/cleaned_retail_sales.csv")

# Create database
conn = sqlite3.connect("retail.db")

# Store data into SQL
df.to_sql("retail_sales", conn, if_exists="replace", index=False)

print("Database Created Successfully ✅")