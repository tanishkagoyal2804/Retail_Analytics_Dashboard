import pandas as pd

df = pd.read_csv("data/retail_sales.csv", encoding="latin1")

print("Dataset Loaded Successfully ✅")
print("\nFirst 5 Rows:\n")
print(df.head())

print("\nColumns:\n")
print(df.columns)