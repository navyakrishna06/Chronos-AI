import pandas as pd

# Load dataset
df = pd.read_csv("datasets/ai4i2020.csv")

# Show original columns
print("Original Columns:")
print(df.columns)

# Remove unwanted columns
df = df.drop(columns=["UDI", "Product ID"])

# Remove duplicate rows
df = df.drop_duplicates()

# Check missing values
print("\nMissing Values:")
print(df.isnull().sum())

# Save cleaned dataset
df.to_csv("datasets/processed/ai4i_clean.csv", index=False)

print("\n✅ AI4I dataset cleaned successfully!")
print("Shape:", df.shape)