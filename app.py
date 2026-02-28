import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from sklearn.linear_model import LinearRegression
import numpy as np

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="Retail Analytics Dashboard", layout="wide")

st.title("📊 Retail Sales & Customer Analytics Dashboard")
st.markdown("Executive Business Intelligence Dashboard")

st.divider()

# -----------------------------
# DATABASE CONNECTION
# -----------------------------
conn = sqlite3.connect("retail.db")

df = pd.read_sql("SELECT * FROM retail_sales", conn)

# -----------------------------
# DATA PREPROCESSING
# -----------------------------
df['Order Date'] = pd.to_datetime(df['Order Date'])
df['Year'] = df['Order Date'].dt.year
df['Month'] = df['Order Date'].dt.to_period("M")

# -----------------------------
# SIDEBAR FILTERS
# -----------------------------
st.sidebar.header("Filters")

selected_year = st.sidebar.selectbox("Select Year", sorted(df['Year'].unique()))
selected_segment = st.sidebar.multiselect(
    "Select Segment",
    df['Segment'].unique(),
    default=df['Segment'].unique()
)

filtered_df = df[
    (df['Year'] == selected_year) &
    (df['Segment'].isin(selected_segment))
]

# -----------------------------
# KPIs
# -----------------------------
total_sales = filtered_df['Sales'].sum()
total_profit = filtered_df['Profit'].sum()
total_orders = filtered_df['Order ID'].nunique()

profit_margin = (total_profit / total_sales) * 100 if total_sales != 0 else 0
avg_order_value = total_sales / total_orders if total_orders != 0 else 0

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Total Sales", f"{total_sales:,.0f}")
col2.metric("Total Profit", f"{total_profit:,.0f}")
col3.metric("Total Orders", total_orders)
col4.metric("Profit Margin %", f"{profit_margin:.2f}%")
col5.metric("Avg Order Value", f"{avg_order_value:.2f}")

st.divider()

# -----------------------------
# SALES BY CATEGORY
# -----------------------------
st.subheader("📈 Sales by Category")

category_sales = filtered_df.groupby("Category")["Sales"].sum().reset_index()

fig1 = px.bar(category_sales, x="Category", y="Sales", text_auto=True)
st.plotly_chart(fig1, use_container_width=True)

# -----------------------------
# SALES BY SEGMENT
# -----------------------------
st.subheader("👥 Sales by Segment")

segment_sales = filtered_df.groupby("Segment")["Sales"].sum().reset_index()

fig2 = px.pie(segment_sales, names="Segment", values="Sales")
st.plotly_chart(fig2, use_container_width=True)

st.divider()

# -----------------------------
# MONTHLY SALES TREND
# -----------------------------
st.subheader("📅 Monthly Sales Trend")

monthly_sales = filtered_df.groupby("Month")["Sales"].sum().reset_index()
monthly_sales["Month"] = monthly_sales["Month"].astype(str)

fig3 = px.line(monthly_sales, x="Month", y="Sales", markers=True)
st.plotly_chart(fig3, use_container_width=True)

# -----------------------------
# MONTHLY GROWTH KPI
# -----------------------------
growth_rate = monthly_sales['Sales'].pct_change().mean() * 100
st.metric("📊 Avg Monthly Growth %", f"{growth_rate:.2f}%")

st.divider()

# -----------------------------
# TOP 10 PRODUCTS
# -----------------------------
st.subheader("🏆 Top 10 Products by Sales")

top_products = (
    filtered_df.groupby("Product Name")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

st.dataframe(top_products)

st.divider()

# -----------------------------
# RFM CLUSTER VISUALIZATION
# -----------------------------
st.subheader("👤 Customer Segmentation (RFM Clusters)")

try:
    rfm = pd.read_csv("data/rfm_clustered.csv")

    fig4 = px.scatter(
        rfm,
        x="Recency",
        y="Monetary",
        color="Cluster",
        title="RFM Customer Segmentation"
    )

    st.plotly_chart(fig4, use_container_width=True)

except:
    st.warning("RFM cluster file not found. Please generate rfm_clustered.csv.")

st.divider()

# -----------------------------
# SALES FORECASTING
# -----------------------------
st.subheader("🔮 Sales Forecast (Next 90 Days)")

monthly_sales['Month_Num'] = np.arange(len(monthly_sales))

X = monthly_sales[['Month_Num']]
y = monthly_sales['Sales']

model = LinearRegression()
model.fit(X, y)

future_months = np.arange(len(monthly_sales), len(monthly_sales) + 3).reshape(-1, 1)
forecast = model.predict(future_months)

forecast_df = pd.DataFrame({
    "Month_Num": future_months.flatten(),
    "Forecasted Sales": forecast
})

fig5 = px.line(monthly_sales, x="Month_Num", y="Sales", title="Historical vs Forecast")
fig5.add_scatter(x=forecast_df["Month_Num"], y=forecast_df["Forecasted Sales"], mode='lines', name="Forecast")

st.plotly_chart(fig5, use_container_width=True)

st.success("✅ Dashboard Successfully Upgraded to Executive Level!")