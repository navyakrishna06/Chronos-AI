import pandas as pd

hdfs_file = "datasets/processed/hdfs_clean.csv"
label_file = "datasets/processed/anomaly_label_clean.csv"
output_file = "datasets/processed/hdfs_final.csv"

print("Loading datasets...")

hdfs = pd.read_csv(hdfs_file)
labels = pd.read_csv(label_file)

print("HDFS Shape:", hdfs.shape)
print("Labels Shape:", labels.shape)

# Merge using Block ID
merged = hdfs.merge(
    labels,
    on="Block_ID",
    how="left"
)

# Check missing labels
print("\nMissing Labels:")
print(merged["Label"].isnull().sum())

# Save final dataset
merged.to_csv(output_file, index=False)

print("\nMerge completed!")
print("Final Shape:", merged.shape)