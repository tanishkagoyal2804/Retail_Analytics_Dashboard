import pandas as pd
import datetime as dt

df = pd.read_csv("data/cleaned_retail_sales.csv")

snapshot_date = df['Order Date'].max() + dt.timedelta(days=1)

rfm = df.groupby('Customer ID').agg({
    'Order Date': lambda x: (snapshot_date - x.max()).days,
    'Order ID': 'count',
    'Sales': 'sum'
})

rfm.columns = ['Recency', 'Frequency', 'Monetary']

print(rfm.head())