import pandas as pd

input_file = "datasets/Big_data_dataset.csv"
output_file = "datasets/processed/bigdata_clean.csv"

print("Loading Big Data dataset...")

df = pd.read_csv(input_file)

print("Original Shape:", df.shape)

# Check missing values
print("\nMissing Values:")
print(df.isnull().sum())

# Remove duplicates
df = df.drop_duplicates()

# Check target values
print("\nStatus Distribution:")
print(df["status"].value_counts())

# Save cleaned dataset
df.to_csv(output_file, index=False)

print("\nBig Data cleaning completed!")
print("Final Shape:", df.shape)