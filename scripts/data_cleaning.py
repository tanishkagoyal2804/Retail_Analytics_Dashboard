import pandas as pd

# Load dataset
df = pd.read_csv("data/retail_sales.csv", encoding="latin1")

print("Original Shape:", df.shape)


# 1. Remove duplicates

df = df.drop_duplicates()

# 2. Handle missing values

print("\nMissing Values Before:\n", df.isnull().sum())

df = df.dropna()

print("\nMissing Values After:\n", df.isnull().sum())

# 3. Convert Date column
# -----------------------------
df['Order Date'] = pd.to_datetime(df['Order Date'])
df['Ship Date'] = pd.to_datetime(df['Ship Date'])


# 4. Create New Features

df['Year'] = df['Order Date'].dt.year
df['Month'] = df['Order Date'].dt.month
df['Month_Name'] = df['Order Date'].dt.month_name()

# Profit Margin
df['Profit_Margin'] = (df['Profit'] / df['Sales']) * 100


# 5. Save Cleaned Data

df.to_csv("data/cleaned_retail_sales.csv", index=False)

print("\nData Cleaning Completed ✅")
print("Cleaned Shape:", df.shape)