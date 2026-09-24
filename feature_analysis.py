import pandas as pd

df = pd.read_csv("datasets/processed/ai4i_clean.csv")

print("Dataset Shape:")
print(df.shape)

print("\nColumns:")
print(df.columns)

print("\nDataset Information:")
df.info()

print("\nStatistical Summary:")
print(df.describe())

print("\nMachine Failure Count:")
print(df["Machine failure"].value_counts())