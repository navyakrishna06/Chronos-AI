import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# Load cleaned dataset
df = pd.read_csv("datasets/processed/ai4i_clean.csv")

# Features
X = df[[
    "Type",
    "Air temperature [K]",
    "Process temperature [K]",
    "Rotational speed [rpm]",
    "Torque [Nm]",
    "Tool wear [min]"
]]

# Convert Type column into numbers
X = pd.get_dummies(X)

# Target
y = df["Machine failure"]

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Create Random Forest Model
model = RandomForestClassifier(random_state=42)

print("Model Created Successfully")
print("Training Data Shape:", X_train.shape)
print("Testing Data Shape:", X_test.shape)