import pandas as pd

# Load cleaned dataset
df = pd.read_csv("datasets/processed/ai4i_clean.csv")

# Select input features
X = df[
    [
        "Type",
        "Air temperature [K]",
        "Process temperature [K]",
        "Rotational speed [rpm]",
        "Torque [Nm]",
        "Tool wear [min]",
    ]
]

# Select target variable
Y = df["Machine failure"]

print("Selected Features:")
print(X.head())

print("\nTarget Variable:")
print(Y.head())