import pandas as pd
import matplotlib.pyplot as plt
from prophet import Prophet

# Load cleaned data
df = pd.read_csv("data/cleaned_retail_sales.csv")

# Convert date column
df['Order Date'] = pd.to_datetime(df['Order Date'])

# Aggregate daily sales
daily_sales = df.groupby('Order Date')['Sales'].sum().reset_index()

# Prophet requires column names: ds and y
daily_sales.columns = ['ds', 'y']

# Initialize model
model = Prophet()

# Train model
model.fit(daily_sales)

# Create future dataframe (predict next 90 days)
future = model.make_future_dataframe(periods=90)

# Forecast
forecast = model.predict(future)

# Plot forecast
model.plot(forecast)
plt.title("Sales Forecast (Next 90 Days)")
plt.show()
from sklearn.metrics import mean_absolute_error

# Merge actual and predicted values
forecast_df = forecast[['ds', 'yhat']].merge(daily_sales, on='ds', how='left')

# Remove rows where actual value is missing
forecast_df = forecast_df.dropna()

# Calculate MAE
mae = mean_absolute_error(forecast_df['y'], forecast_df['yhat'])

print("\nModel Evaluation:")
print("Mean Absolute Error (MAE):", round(mae, 2))