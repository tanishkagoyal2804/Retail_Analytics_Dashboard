import pandas as pd

df = pd.read_csv("data/cleaned_retail_sales.csv")

total_sales = df['Sales'].sum()
total_profit = df['Profit'].sum()
total_orders = df['Order ID'].nunique()
total_customers = df['Customer ID'].nunique()

print("📊 BUSINESS KPIs")
print("----------------------------")
print("Total Sales: ", round(total_sales, 2))
print("Total Profit:", round(total_profit, 2))
print("Total Orders:", total_orders)
print("Total Customers:", total_customers)