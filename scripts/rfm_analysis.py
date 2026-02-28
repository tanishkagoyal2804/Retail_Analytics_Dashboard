import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans


# 1. Load Cleaned Data

df = pd.read_csv("data/cleaned_retail_sales.csv")
df['Order Date'] = pd.to_datetime(df['Order Date'])

print("Data Loaded Successfully ✅")


# 2. Create Snapshot Date

snapshot_date = df['Order Date'].max() + dt.timedelta(days=1)


# 3. RFM Calculation

rfm = df.groupby('Customer ID').agg({
    'Order Date': lambda x: (snapshot_date - x.max()).days,
    'Order ID': 'count',
    'Sales': 'sum'
})

rfm.columns = ['Recency', 'Frequency', 'Monetary']

print("\nRFM Table Created ✅")
print(rfm.head())


# 4. Feature Scaling

scaler = StandardScaler()
rfm_scaled = scaler.fit_transform(rfm)


# 5. Elbow Method (Find Best Clusters)

inertia = []

for k in range(1, 10):
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(rfm_scaled)
    inertia.append(kmeans.inertia_)

plt.figure()
plt.plot(range(1, 10), inertia)
plt.xlabel("Number of Clusters")
plt.ylabel("Inertia")
plt.title("Elbow Method For Optimal Clusters")
plt.show()


# 6. Apply KMeans (Choose 4 based on elbow)

kmeans = KMeans(n_clusters=4, random_state=42)
rfm['Cluster'] = kmeans.fit_predict(rfm_scaled)

print("\nCluster Distribution:")
print(rfm['Cluster'].value_counts())


# 7. Cluster Summary (Business Insight)

cluster_summary = rfm.groupby('Cluster').mean()

print("\nCluster Summary (Average RFM Values):")
print(cluster_summary)


# 8. Assign Business Segment Labels

def label_cluster(cluster):
    if cluster == 0:
        return "High Value Customers"
    elif cluster == 1:
        return "Loyal Customers"
    elif cluster == 2:
        return "At Risk Customers"
    else:
        return "Low Value Customers"

rfm['Segment'] = rfm['Cluster'].apply(label_cluster)

print("\nSegment Distribution:")
print(rfm['Segment'].value_counts())


# 9. Save Final RFM Data

rfm.to_csv("data/rfm_with_clusters.csv")

print("\nRFM Analysis Completed Successfully ✅")
print("File Saved: data/rfm_with_clusters.csv")