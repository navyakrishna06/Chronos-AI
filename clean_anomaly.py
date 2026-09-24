import pandas as pd

input_file = "datasets/anomaly_label.csv"
output_file = "datasets/processed/anomaly_label_clean.csv"

print("Loading anomaly labels...")

df = pd.read_csv(input_file)

print("Original Shape:", df.shape)

# Rename column
df = df.rename(columns={
    "BlockId": "Block_ID"
})

# Remove duplicates
df = df.drop_duplicates()

# Missing value check
print("\nMissing Values:")
print(df.isnull().sum())

# Save cleaned file
df.to_csv(output_file, index=False)

print("\nAnomaly label cleaning completed!")
print("Final Shape:", df.shape)