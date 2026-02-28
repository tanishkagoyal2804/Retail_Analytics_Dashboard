import pandas as pd

# Load main cleaned dataset
df = pd.read_csv("data/cleaned_retail_sales.csv")

# Load RFM with clusters
rfm = pd.read_csv("data/rfm_with_clusters.csv")

# Merge on Customer ID
final_df = df.merge(rfm[['Customer ID', 'Cluster']], on='Customer ID', how='left')

# Save final dataset
final_df.to_csv("data/final_retail_data.csv", index=False)

print("Final Dataset with Clusters Created ✅")
print(final_df.head())