import pandas as pd

df = pd.read_csv("data/final_retail_data.csv")

print("\nTop 5 Customers by Sales:")
print(df.groupby('Customer Name')['Sales'].sum().sort_values(ascending=False).head())

print("\nMost Profitable Category:")
print(df.groupby('Category')['Profit'].sum().sort_values(ascending=False))

print("\nSegment Revenue Contribution:")
print(df.groupby('Segment')['Sales'].sum().sort_values(ascending=False))